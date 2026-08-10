"""
Retrieval híbrido da fábrica: denso (Chroma) + BM25 + meta(projeto/tags)
→ RRF → affinity → rerank bge-reranker-v2-m3 (ligado por padrão).

Usado por indexar_obsidian_chroma.py (--server e --buscar).
MCP rag_buscar / buscar_historico / buscar_solucao consomem o mesmo HTTP :7332.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

RRF_K = 60
POOL_DENSE = 48
POOL_BM25 = 48
POOL_META = 32
RERANK_POOL = int(os.environ.get("RAG_RERANK_POOL", "24"))
RERANK_MODEL = os.environ.get("RAG_RERANK_MODEL", "BAAI/bge-reranker-v2-m3").strip()

# Hot path: rerank ON por padrão. Desligar: RAG_RERANK=0
RERANK_ENABLED = os.environ.get("RAG_RERANK", "1").strip().lower() not in (
    "0", "false", "no", "off",
)

DENSE_WEIGHT = 1.5
BM25_WEIGHT = 1.0
META_WEIGHT = 1.25

_ERROR_MARKERS = (
    "erro", "bug", "permission", "undefined", "failed", "132001", "131030",
    "fecha", "crash", "exception", "denied", "template não",
)
_PATTERN_MARKERS = (
    "deploy", "checklist", "como ", "padrao", "padrão", "schema", "modelar",
    "estrutur", " path", "regra", "fluxo", "export", "firestore", "multi-tenant",
    "cadastro", "login", "hosting", "functions", "members", "salão", "salao",
    "google sign", "gate ", "rag_", "mcp ", "7332", "chroma", "endpoint",
    "resource", "dto", "java ", "angular", "sinaflor", "tramitacao", "arquivar",
)

_NOISE_LOG_FILES = frozenset({"decisoes.md"})
_SOLUCAO_FILE = "erros-e-solucoes.md"

POST_RRF_POOL = 36

# Aliases query → projeto canônico (3ª recall + filtro)
_PROJECT_ALIASES: dict[str, tuple[str, ...]] = {
    "sinaflor": ("sinaflor", "ibama", "sinaflor2", "hu13", "tramitacao"),
    "lashmatch": ("lashmatch", "lash match"),
    "cortejo": ("cortejo",),
    "erp": ("erp", "flyway", "multi-tenant erp"),
    "setmatch": ("setmatch",),
    "zenpro": ("zenpro",),
    "whatsapp": ("whatsapp", "meta cloud"),
    "firebase": ("firebase", "firestore"),
    "mercadopago": ("mercadopago", "mercado pago"),
    "fabrica": ("fabrica", "rag_", "7332", "chroma", "mcp "),
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", (text or "").lower(), flags=re.UNICODE)


def infer_tipo_doc(arquivo: str, meta: dict | None = None) -> str:
    if meta and meta.get("tipo_doc"):
        return str(meta["tipo_doc"])
    nome = (arquivo or "").lower()
    if nome.startswith("report-") or "/eval/" in nome or nome.endswith("report-baseline.md"):
        return "eval"
    if nome.endswith("-prd.md") or nome.endswith("prd.md") or "-prd." in nome:
        return "spec"
    if nome == "erros-e-solucoes.md":
        return "solucao"
    return "padrao"


def infer_projeto_meta(arquivo: str, meta: dict | None = None) -> str:
    if meta and meta.get("projeto"):
        return str(meta["projeto"]).strip().lower()
    nome = (arquivo or "").lower()
    path = str((meta or {}).get("path", "")).lower()
    blob = f"{path} {nome}"
    for proj in _PROJECT_ALIASES:
        if proj in blob or nome.startswith(proj):
            return proj
    return "fabrica"


def should_demote_spec(query: str) -> bool:
    q = query.lower()
    if any(m in q for m in _ERROR_MARKERS):
        return False
    return any(m in q for m in _PATTERN_MARKERS)


def _is_excluded_doc(arquivo: str, meta: dict | None) -> bool:
    tipo = infer_tipo_doc(arquivo, meta)
    return tipo in ("spec", "eval")


def extract_projetos_from_query(query: str) -> list[str]:
    q = query.lower()
    found: list[str] = []
    for proj, aliases in _PROJECT_ALIASES.items():
        if any(a in q for a in aliases) or proj in q:
            found.append(proj)
    # unique preserve order
    seen: set[str] = set()
    out: list[str] = []
    for p in found:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


@dataclass
class ChunkHit:
    chunk_id: str
    document: str
    metadata: dict
    score: float = 0.0

    @property
    def arquivo(self) -> str:
        return self.metadata.get("arquivo", "")


def _arquivo_nome(arquivo: str) -> str:
    nome = (arquivo or "").replace("\\", "/")
    return nome.rsplit("/", 1)[-1].lower()


def _query_has_error_intent(query: str) -> bool:
    q = query.lower()
    return any(m in q for m in _ERROR_MARKERS)


def _trecho_citacao(doc: str, query: str, max_len: int = 320) -> str:
    """Trecho citável: preferir sentença que contenha termo da query."""
    text = (doc or "").strip().replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    if not text:
        return ""
    tokens = [t for t in _tokenize(query) if len(t) > 2][:8]
    best = ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        low = sent.lower()
        if tokens and any(t in low for t in tokens):
            if len(sent) > len(best):
                best = sent
    trecho = best or text
    if len(trecho) > max_len:
        trecho = trecho[: max_len - 1].rstrip() + "…"
    return trecho


def _affinity_multiplier(arquivo: str, query: str, meta: dict | None = None) -> float:
    """
    Ajuste leve pós-RRF por afinidade query↔nota.
    Não substitui retrieval — só reordena o pool híbrido.
    """
    q = query.lower()
    nome = _arquivo_nome(arquivo)
    mult = 1.0
    pattern_q = should_demote_spec(query)
    error_q = _query_has_error_intent(query)
    projeto = infer_projeto_meta(arquivo, meta)
    projetos_q = extract_projetos_from_query(query)

    if projetos_q:
        if projeto in projetos_q:
            mult *= 1.55
        elif projeto not in ("fabrica",) and not any(p == projeto for p in projetos_q):
            # Outro projeto competindo — demote leve
            if "fabrica" not in projetos_q:
                mult *= 0.72

    # Logs cronológicos vs notas canônicas
    if pattern_q and not error_q:
        if nome in _NOISE_LOG_FILES:
            mult *= 0.28
        if nome == _SOLUCAO_FILE:
            mult *= 0.35
    elif error_q and nome == _SOLUCAO_FILE:
        mult *= 1.45

    # Schema salão / Cortejo (gs-001)
    if any(k in q for k in ("members", "salão", "salao", "salons", "multi-tenant")) and (
        "firestore" in q or "modelar" in q or "schema" in q
    ):
        if nome == "cortejo-schemas.md":
            mult *= 2.4
        elif nome.endswith("-schemas.md") or "schema" in nome:
            mult *= 1.35
        if nome in (
            "capinhas-multitenant.md",
            "erp-postgres-schema.md",
            "lashmatch-mercadopago-assinatura.md",
            "excluir-conta-app-expo-padrao.md",
        ):
            mult *= 0.4

    # Path LashMatch artifacts (gs-002)
    if "artifacts" in q or ("appid" in q and "users" in q):
        if nome == "lashmatch-schemas.md":
            mult *= 2.2
        elif nome in ("firebase-setup-patterns.md", "padroes-fabrica.md"):
            mult *= 1.25

    # Expo web + Hosting (gs-015)
    if ("export" in q or "hosting" in q) and ("web" in q or "firebase" in q or "deploy" in q):
        if nome in ("firebase-setup-patterns.md", "lashmatch-web-plataforma.md"):
            mult *= 2.0
        elif "deploy" in nome or "hosting" in nome or "checklist" in nome:
            mult *= 1.3

    # Servidor Chroma / porta 7332 (gs-018 / gs-019)
    if any(k in q for k in ("7332", "chroma", "indexar_obsidian", "servidor rag", "rag porta")):
        if error_q or "fecha" in q or "crash" in q:
            if nome == _SOLUCAO_FILE:
                mult *= 2.4
            if nome in ("arquitetura-fabrica-ia.md", "guia-completo-usuario-fabrica.md"):
                mult *= 0.65
        else:
            if nome in ("arquitetura-fabrica-ia.md", "guia-completo-usuario-fabrica.md", "rag-retrieval-fabrica.md"):
                mult *= 2.1
            if nome in _NOISE_LOG_FILES:
                mult *= 0.25

    # Qual MCP (gs-020)
    if "mcp" in q:
        if nome == "mcps-cursor-padrao.md":
            mult *= 2.0

    # SINAFLOR vs ERP (map/regras)
    if "sinaflor" in q or "ibama" in q:
        if nome.startswith("erp-"):
            mult *= 0.35
        if nome in (
            "mapeamento-frontend-backend.md",
            "regras-gerais.md",
            "angular-frontend.md",
            "spring-backend.md",
            "testes-frontend.md",
            "testes-backend.md",
            "tramitacao-arquivar-desarquivar.md",
            "gestao-visibilidade-perfis.md",
        ):
            mult *= 1.55
        if nome.endswith("-prd.md") or nome == "sinaflor-prd.md":
            mult *= 0.55
        if pattern_q and not error_q and nome == _SOLUCAO_FILE:
            mult *= 0.3

    if "sinaflor" in q and any(k in q for k in ("endpoint", "resource", "dto", "mapeamento", "request", "response")):
        if nome == "mapeamento-frontend-backend.md":
            mult *= 2.2
        if nome in ("angular-frontend.md", "testes-frontend.md", "spring-backend.md"):
            mult *= 0.7

    if "sinaflor" in q and any(k in q for k in ("arquivar", "desarquivar", "tramitacao", "tramitação")):
        if nome == "tramitacao-arquivar-desarquivar.md":
            mult *= 2.3
        if nome == "gestao-visibilidade-perfis.md":
            mult *= 1.2

    if "sinaflor" in q and any(k in q for k in ("java 17", "records", "legado", "não fazer", "nao fazer", "modernizar")):
        if nome == "regras-gerais.md":
            mult *= 2.2

    if "java" in q and ("17" in q or "records" in q) and "sinaflor" in q:
        if nome == "regras-gerais.md":
            mult *= 1.5
        if nome in ("testes-backend.md", "spring-backend.md", "testes-frontend.md"):
            mult *= 0.55

    # Tags no metadata
    tags = str((meta or {}).get("tags", "")).lower()
    if tags:
        q_tokens = set(_tokenize(query))
        tag_tokens = set(_tokenize(tags.replace(",", " ")))
        overlap = q_tokens & tag_tokens
        if overlap:
            mult *= 1.0 + 0.12 * min(len(overlap), 4)

    return mult


def _preferred_note_names(query: str) -> list[str]:
    """Notas canônicas que devem entrar no pool mesmo se o RRF as deixou de fora."""
    q = query.lower()
    prefs: list[str] = []

    if any(k in q for k in ("members", "salão", "salao", "salons", "multi-tenant")) and (
        "firestore" in q or "modelar" in q or "schema" in q
    ):
        prefs.append("cortejo-schemas.md")

    if "artifacts" in q or ("appid" in q and "uid" in q):
        prefs.append("lashmatch-schemas.md")

    if "sinaflor" in q or "ibama" in q:
        if any(k in q for k in ("endpoint", "resource", "dto", "mapeamento", "request", "response")):
            prefs.append("mapeamento-frontend-backend.md")
        if any(k in q for k in ("java", "legado", "regra", "records", "modernizar", "não fazer", "nao fazer")):
            prefs.append("regras-gerais.md")
        if any(k in q for k in ("arquivar", "desarquivar", "tramitacao", "tramitação")):
            prefs.append("tramitacao-arquivar-desarquivar.md")

    if any(k in q for k in ("7332", "chroma", "servidor rag", "rerank", "retrieval")):
        if _query_has_error_intent(query):
            prefs.append(_SOLUCAO_FILE)
        else:
            prefs.append("rag-retrieval-fabrica.md")

    seen: set[str] = set()
    out: list[str] = []
    for p in prefs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _apply_query_affinity(hits: list[ChunkHit], query: str) -> list[ChunkHit]:
    if not hits:
        return hits
    scored: list[ChunkHit] = []
    for h in hits:
        m = _affinity_multiplier(h.arquivo, query, h.metadata)
        scored.append(
            ChunkHit(
                chunk_id=h.chunk_id,
                document=h.document,
                metadata=h.metadata,
                score=h.score * m,
            )
        )
    scored.sort(key=lambda x: x.score, reverse=True)
    return scored


class HybridRetriever:
    """Carrega corpus do Chroma uma vez; busca híbrida por query."""

    def __init__(self, collection, embed_model):
        self.collection = collection
        self.embed_model = embed_model
        self._bm25_default = None
        self._bm25_demote = None
        self._corpus_default: list[ChunkHit] = []
        self._corpus_demote: list[ChunkHit] = []
        self._corpus: list[ChunkHit] = []
        self._reranker = None
        self._ready = False

    def _ensure_corpus(self) -> None:
        if self._ready:
            return
        raw = self.collection.get(include=["documents", "metadatas"])
        ids = raw.get("ids") or []
        docs = raw.get("documents") or []
        metas = raw.get("metadatas") or []
        self._corpus = [
            ChunkHit(
                chunk_id=cid,
                document=doc or "",
                metadata=meta or {},
            )
            for cid, doc, meta in zip(ids, docs, metas)
        ]
        if self._corpus:
            from rank_bm25 import BM25Okapi

            self._corpus_demote = [
                c for c in self._corpus if not _is_excluded_doc(c.arquivo, c.metadata)
            ]
            self._corpus_default = [
                c
                for c in self._corpus
                if infer_tipo_doc(c.arquivo, c.metadata) != "eval"
            ]
            self._bm25_demote = BM25Okapi(
                [_tokenize(c.document) for c in self._corpus_demote]
            )
            self._bm25_default = BM25Okapi(
                [_tokenize(c.document) for c in self._corpus_default]
            )
        self._ready = True

    def _ensure_reranker(self):
        if self._reranker is not None:
            return self._reranker
        try:
            from sentence_transformers import CrossEncoder

            print(f"⏳  Carregando reranker `{RERANK_MODEL}`...")
            self._reranker = CrossEncoder(RERANK_MODEL, max_length=512)
            print("✅  Reranker pronto")
        except Exception as e:
            print(f"⚠️  Reranker indisponível: {e}")
            self._reranker = False
        return self._reranker

    def _filter_hits(self, hits: list[ChunkHit], query: str) -> list[ChunkHit]:
        if not should_demote_spec(query):
            return [
                h for h in hits
                if not _is_excluded_doc(h.arquivo, h.metadata)
                or infer_tipo_doc(h.arquivo, h.metadata) != "eval"
            ]
        return [h for h in hits if not _is_excluded_doc(h.arquivo, h.metadata)]

    def _dense_hits(self, query: str, n: int) -> list[ChunkHit]:
        cnt = self.collection.count()
        if cnt == 0:
            return []
        k = max(1, min(n * 3, cnt))
        emb = self.embed_model.encode(
            [query],
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0].tolist()
        res = self.collection.query(
            query_embeddings=[emb],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        hits: list[ChunkHit] = []
        for i, doc in enumerate(res["documents"][0]):
            meta = res["metadatas"][0][i]
            dist = res["distances"][0][i]
            hits.append(
                ChunkHit(
                    chunk_id=res["ids"][0][i],
                    document=doc,
                    metadata=meta,
                    score=1.0 - dist,
                )
            )
        filtered = self._filter_hits(hits, query)
        return filtered[:n]

    def _bm25_hits(self, query: str, n: int) -> list[ChunkHit]:
        if not self._corpus:
            return []
        tokens = _tokenize(query)
        if not tokens:
            return []

        if should_demote_spec(query):
            bm25, corpus = self._bm25_demote, self._corpus_demote
        else:
            bm25, corpus = self._bm25_default, self._corpus_default

        if not bm25 or not corpus:
            return []

        scores = bm25.get_scores(tokens)
        ranked = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:n]
        hits: list[ChunkHit] = []
        for i in ranked:
            if scores[i] <= 0:
                break
            c = corpus[i]
            hits.append(
                ChunkHit(
                    chunk_id=c.chunk_id,
                    document=c.document,
                    metadata=c.metadata,
                    score=float(scores[i]),
                )
            )
        return hits

    def _meta_hits(self, query: str, n: int, projeto_filter: str | None = None) -> list[ChunkHit]:
        """
        3ª recall: projeto/tags (metadata) + nome de arquivo.
        Só ativa quando a query (ou filtro) aponta projeto/tags.
        """
        if not self._corpus:
            return []
        projetos = extract_projetos_from_query(query)
        if projeto_filter:
            pf = projeto_filter.strip().lower()
            if pf and pf not in projetos:
                projetos = [pf] + projetos
        q_tokens = set(_tokenize(query))
        if not projetos and not q_tokens:
            return []

        scored: list[tuple[float, ChunkHit]] = []
        for c in self._corpus:
            if _is_excluded_doc(c.arquivo, c.metadata) and should_demote_spec(query):
                continue
            proj = infer_projeto_meta(c.arquivo, c.metadata)
            tags = str(c.metadata.get("tags", "")).lower()
            nome = _arquivo_nome(c.arquivo)
            score = 0.0
            if projetos and proj in projetos:
                score += 3.0
            if projetos and any(p in nome or p in str(c.metadata.get("path", "")).lower() for p in projetos):
                score += 1.5
            tag_tokens = set(_tokenize(tags.replace(",", " ")))
            overlap = q_tokens & tag_tokens
            if overlap:
                score += 0.8 * len(overlap)
            # token no nome do arquivo
            name_tokens = set(_tokenize(nome.replace("-", " ").replace("_", " ").replace(".md", "")))
            score += 0.35 * len(q_tokens & name_tokens)
            if score <= 0:
                continue
            scored.append(
                (
                    score,
                    ChunkHit(
                        chunk_id=c.chunk_id,
                        document=c.document,
                        metadata=c.metadata,
                        score=score,
                    ),
                )
            )

        scored.sort(key=lambda x: x[0], reverse=True)
        # Diversificar: no máx 3 chunks por arquivo
        out: list[ChunkHit] = []
        per_file: dict[str, int] = {}
        for _, hit in scored:
            nome = _arquivo_nome(hit.arquivo)
            if per_file.get(nome, 0) >= 3:
                continue
            per_file[nome] = per_file.get(nome, 0) + 1
            out.append(hit)
            if len(out) >= n:
                break
        return out

    @staticmethod
    def _rrf_fuse(
        dense: list[ChunkHit],
        bm25: list[ChunkHit],
        meta: list[ChunkHit] | None = None,
    ) -> list[ChunkHit]:
        by_id: dict[str, ChunkHit] = {}
        rrf_scores: dict[str, float] = {}

        def add_list(hits: list[ChunkHit], weight: float) -> None:
            for rank, hit in enumerate(hits):
                rrf_scores[hit.chunk_id] = rrf_scores.get(hit.chunk_id, 0.0) + weight / (
                    RRF_K + rank + 1
                )
                by_id.setdefault(hit.chunk_id, hit)

        add_list(dense, DENSE_WEIGHT)
        add_list(bm25, BM25_WEIGHT)
        if meta:
            add_list(meta, META_WEIGHT)

        ordered = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)
        return [
            ChunkHit(
                chunk_id=cid,
                document=by_id[cid].document,
                metadata=by_id[cid].metadata,
                score=rrf_scores[cid],
            )
            for cid in ordered
        ]

    def _demote_spec(self, hits: list[ChunkHit], query: str) -> list[ChunkHit]:
        return self._filter_hits(hits, query)

    def _rerank(self, query: str, hits: list[ChunkHit], n: int) -> list[ChunkHit]:
        pool = hits[:RERANK_POOL]
        if len(pool) <= 1:
            return pool[:n]
        head = pool[0]
        tail_in = pool[1:]
        if not tail_in:
            return [head][:n]
        reranker = self._ensure_reranker()
        if not reranker:
            return pool[:n]
        pairs = [[query, h.document] for h in tail_in]
        try:
            scores = reranker.predict(pairs, show_progress_bar=False)
        except Exception:
            return pool[:n]
        ranked = sorted(
            zip(tail_in, scores),
            key=lambda x: float(x[1]),
            reverse=True,
        )
        tail_out: list[ChunkHit] = []
        for h, s in ranked[: max(0, n - 1)]:
            tail_out.append(
                ChunkHit(
                    chunk_id=h.chunk_id,
                    document=h.document,
                    metadata=h.metadata,
                    score=float(s),
                )
            )
        return [head] + tail_out

    def _inject_preferred_notes(self, hits: list[ChunkHit], query: str) -> list[ChunkHit]:
        prefs = _preferred_note_names(query)
        if not prefs or not self._corpus:
            return hits
        existing_ids = {h.chunk_id for h in hits}
        existing_names = {_arquivo_nome(h.arquivo) for h in hits}
        missing = [p for p in prefs if p not in existing_names]
        if not missing:
            return hits
        per_file: dict[str, int] = {p: 0 for p in missing}
        injected: list[ChunkHit] = []
        for c in self._corpus:
            nome = _arquivo_nome(c.arquivo)
            if nome not in per_file or per_file[nome] >= 3:
                continue
            if c.chunk_id in existing_ids:
                continue
            per_file[nome] += 1
            injected.append(
                ChunkHit(
                    chunk_id=c.chunk_id,
                    document=c.document,
                    metadata=c.metadata,
                    score=0.08,
                )
            )
            existing_ids.add(c.chunk_id)
        if not injected:
            return hits
        return injected + hits

    def buscar(
        self,
        query: str,
        n: int = 5,
        projeto: str | None = None,
    ) -> list[dict[str, Any]]:
        self._ensure_corpus()
        if not query.strip():
            return []

        dense = self._dense_hits(query, POOL_DENSE)
        bm25 = self._bm25_hits(query, POOL_BM25)
        meta = self._meta_hits(query, POOL_META, projeto_filter=projeto)
        fused = self._rrf_fuse(dense, bm25, meta)
        filtered = self._demote_spec(fused, query)
        if projeto:
            pf = projeto.strip().lower()
            filtered = [
                h for h in filtered
                if infer_projeto_meta(h.arquivo, h.metadata) == pf
                or pf in _arquivo_nome(h.arquivo)
                or pf in str(h.metadata.get("path", "")).lower()
            ] or filtered  # se filtro zerar, mantém pool (fail-open)
        merged = self._inject_preferred_notes(filtered[:POST_RRF_POOL], query)
        ranked = _apply_query_affinity(merged, query)
        if RERANK_ENABLED:
            final = self._rerank(query, ranked, n)
        else:
            final = ranked[:n]

        saida = []
        for rank, h in enumerate(final, 1):
            sim = h.score
            if sim <= 1.0:
                sim_out = round(min(max(sim, 0.0), 1.0), 3)
            else:
                sim_out = round(sim, 4)
            saida.append(
                {
                    "conteudo": h.document,
                    "arquivo": h.arquivo,
                    "path": h.metadata.get("path", h.arquivo),
                    "projeto": infer_projeto_meta(h.arquivo, h.metadata),
                    "tags": h.metadata.get("tags", ""),
                    "chunk": h.metadata.get("chunk", 0),
                    "tipo_doc": infer_tipo_doc(h.arquivo, h.metadata),
                    "similaridade": sim_out,
                    "rank": rank,
                    "trecho": _trecho_citacao(h.document, query),
                    "citacao": f"{h.arquivo}#{h.metadata.get('chunk', 0)}",
                }
            )
        return saida


def buscar_hibrido(
    collection,
    embed_model,
    query: str,
    n: int = 5,
    projeto: str | None = None,
) -> list[dict]:
    retriever = getattr(buscar_hibrido, "_singleton", None)
    if retriever is None:
        retriever = HybridRetriever(collection, embed_model)
        buscar_hibrido._singleton = retriever  # type: ignore[attr-defined]
    return retriever.buscar(query, n, projeto=projeto)


def reset_singleton() -> None:
    if hasattr(buscar_hibrido, "_singleton"):
        del buscar_hibrido._singleton  # type: ignore[attr-defined]


def warmup_indices(collection, embed_model) -> None:
    """Pré-carrega corpus + BM25. Reranker fica lazy (1ª /buscar) — no App Runner
    carregar CrossEncoder no boot compete com MiniLM/Chroma e causa OOM."""
    reset_singleton()
    retriever = HybridRetriever(collection, embed_model)
    retriever._ensure_corpus()
    # Não chamar _ensure_reranker() aqui.
    buscar_hibrido._singleton = retriever  # type: ignore[attr-defined]
    if RERANK_ENABLED:
        print("ℹ️  Rerank ON — modelo carrega na 1ª busca (lazy, evita OOM no boot)")


def invalidate_indices() -> None:
    """Chamar após reindex do vault (novo conteúdo no Chroma)."""
    reset_singleton()


def buscar_denso(collection, embed_model, query: str, n: int = 5) -> list[dict]:
    """Fallback denso puro (sem BM25/rerank) — útil para debug."""
    cnt = collection.count()
    if cnt == 0:
        return []
    k = max(1, min(n, cnt))
    emb = embed_model.encode(
        [query],
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0].tolist()
    res = collection.query(
        query_embeddings=[emb],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    saida = []
    for i, doc in enumerate(res["documents"][0]):
        meta = res["metadatas"][0][i]
        saida.append(
            {
                "conteudo": doc,
                "arquivo": meta["arquivo"],
                "similaridade": round(1 - res["distances"][0][i], 3),
                "trecho": _trecho_citacao(doc, query),
                "citacao": f"{meta['arquivo']}#{meta.get('chunk', 0)}",
                "projeto": infer_projeto_meta(meta.get("arquivo", ""), meta),
            }
        )
    return saida
