"""
Retrieval híbrido da fábrica: denso (Chroma) + BM25 → RRF → rerank bge-reranker-v2-m3.

Usado por indexar_obsidian_chroma.py (--server e --buscar).
MCP rag_buscar / buscar_historico / buscar_solucao consomem o mesmo HTTP :7332.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

RRF_K = 60
POOL_DENSE = 40
POOL_BM25 = 40
RERANK_POOL = 20
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"

_ERROR_MARKERS = (
    "erro", "bug", "permission", "undefined", "failed", "132001", "131030",
    "fecha", "crash", "exception", "denied", "template não",
)
_PATTERN_MARKERS = (
    "deploy", "checklist", "como ", "padrao", "padrão", "schema", "modelar",
    "estrutur", " path", "regra", "fluxo", "export", "firestore", "multi-tenant",
    "cadastro", "login", "hosting", "functions", "members", "salão", "salao",
    "google sign", "gate ", "rag_", "mcp ",
)


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


def should_demote_spec(query: str) -> bool:
    q = query.lower()
    if any(m in q for m in _ERROR_MARKERS):
        return False
    return any(m in q for m in _PATTERN_MARKERS)


def _is_excluded_doc(arquivo: str, meta: dict | None) -> bool:
    tipo = infer_tipo_doc(arquivo, meta)
    return tipo in ("spec", "eval")


@dataclass
class ChunkHit:
    chunk_id: str
    document: str
    metadata: dict
    score: float = 0.0

    @property
    def arquivo(self) -> str:
        return self.metadata.get("arquivo", "")


class HybridRetriever:
    """Carrega corpus do Chroma uma vez; busca híbrida por query."""

    def __init__(self, collection, embed_model):
        self.collection = collection
        self.embed_model = embed_model
        self._bm25 = None
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

            tokenized = [_tokenize(c.document) for c in self._corpus]
            self._bm25 = BM25Okapi(tokenized)
        self._ready = True

    def _ensure_reranker(self):
        if self._reranker is not None:
            return self._reranker
        try:
            from sentence_transformers import CrossEncoder

            self._reranker = CrossEncoder(RERANK_MODEL, max_length=512)
        except Exception:
            self._reranker = False
        return self._reranker

    def _filter_hits(self, hits: list[ChunkHit], query: str) -> list[ChunkHit]:
        if not should_demote_spec(query):
            return [h for h in hits if not _is_excluded_doc(h.arquivo, h.metadata) or infer_tipo_doc(h.arquivo, h.metadata) != "eval"]
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
        if not self._bm25 or not self._corpus:
            return []
        tokens = _tokenize(query)
        if not tokens:
            return []
        corpus = (
            [c for c in self._corpus if not _is_excluded_doc(c.arquivo, c.metadata)]
            if should_demote_spec(query)
            else [c for c in self._corpus if infer_tipo_doc(c.arquivo, c.metadata) != "eval"]
        )
        if not corpus:
            return []
        from rank_bm25 import BM25Okapi

        tokenized = [_tokenize(c.document) for c in corpus]
        bm25 = BM25Okapi(tokenized)
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

    @staticmethod
    def _rrf_fuse(dense: list[ChunkHit], bm25: list[ChunkHit]) -> list[ChunkHit]:
        by_id: dict[str, ChunkHit] = {}
        rrf_scores: dict[str, float] = {}
        DENSE_WEIGHT = 1.5

        for rank, hit in enumerate(dense):
            rrf_scores[hit.chunk_id] = rrf_scores.get(hit.chunk_id, 0.0) + DENSE_WEIGHT / (
                RRF_K + rank + 1
            )
            by_id[hit.chunk_id] = hit

        for rank, hit in enumerate(bm25):
            rrf_scores[hit.chunk_id] = rrf_scores.get(hit.chunk_id, 0.0) + 1.0 / (
                RRF_K + rank + 1
            )
            by_id.setdefault(hit.chunk_id, hit)

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

    def buscar(self, query: str, n: int = 5) -> list[dict[str, Any]]:
        self._ensure_corpus()
        if not query.strip():
            return []

        dense = self._dense_hits(query, POOL_DENSE)
        bm25 = self._bm25_hits(query, POOL_BM25)
        fused = self._rrf_fuse(dense, bm25)
        filtered = self._demote_spec(fused, query)
        final = self._rerank(query, filtered, n)

        saida = []
        for h in final:
            saida.append(
                {
                    "conteudo": h.document,
                    "arquivo": h.arquivo,
                    "similaridade": round(min(max(h.score, 0.0), 1.0), 3)
                    if h.score <= 1.0
                    else round(h.score, 4),
                    "tipo_doc": infer_tipo_doc(h.arquivo, h.metadata),
                }
            )
        return saida


def buscar_hibrido(collection, embed_model, query: str, n: int = 5) -> list[dict]:
    retriever = getattr(buscar_hibrido, "_singleton", None)
    if (
        retriever is None
        or retriever.collection is not collection
        or retriever.embed_model is not embed_model
    ):
        retriever = HybridRetriever(collection, embed_model)
        buscar_hibrido._singleton = retriever  # type: ignore[attr-defined]
    return retriever.buscar(query, n)


def reset_singleton() -> None:
    if hasattr(buscar_hibrido, "_singleton"):
        del buscar_hibrido._singleton  # type: ignore[attr-defined]


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
            }
        )
    return saida
