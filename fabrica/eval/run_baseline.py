#!/usr/bin/env python3
"""
Harness de avaliação RAG — baseline contra golden-set.jsonl.

Chama o retrieval atual via HTTP Chroma (porta 7332) e mede hit@1/3/5 + MRR.
Suporta campo opcional `aceitaveis` no golden set (réguas v2+).

Uso:
    python fabrica/eval/run_baseline.py
    python fabrica/eval/run_baseline.py --regua v2
    python fabrica/eval/run_baseline.py --porta 7332 --top-k 5
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FABRICA = ROOT / "fabrica"
EVAL_DIR = FABRICA / "eval"
GOLDEN_PATH = EVAL_DIR / "golden-set.jsonl"
REPORT_MD = EVAL_DIR / "report-baseline.md"
REPORT_JSON = EVAL_DIR / "report-baseline.json"
REPORT_V2_MD = EVAL_DIR / "report-baseline-v2.md"
REPORT_V2_JSON = EVAL_DIR / "report-baseline-v2.json"
REPORT_HYBRID_MD = EVAL_DIR / "report-hybrid.md"
REPORT_HYBRID_JSON = EVAL_DIR / "report-hybrid.json"
REPORT_DELTA_MD = EVAL_DIR / "report-delta.md"
DEFAULT_PORT = 7332
DEFAULT_TOP_K = 5


def _configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load_golden(path: Path) -> list[dict]:
    pairs: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                pairs.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"JSON inválido em {path}:{lineno}: {exc}") from exc
    return pairs


def list_fabrica_notes() -> set[str]:
    return {p.name for p in FABRICA.rglob("*.md")}


def validate_golden(pairs: list[dict], notas: set[str]) -> dict:
    queries: set[str] = set()
    tipos: defaultdict[str, int] = defaultdict(int)
    issues: list[str] = []
    revisar: list[str] = []

    required = {"id", "query", "esperado_nota", "esperado_secao", "tipo"}
    valid_tipos = {"padrao", "integracao", "fluxo", "solucao", "fabrica"}

    for par in pairs:
        missing = required - set(par.keys())
        if missing:
            issues.append(f"{par.get('id', '?')}: campos faltando {sorted(missing)}")
            continue

        if par["query"] in queries:
            issues.append(f"{par['id']}: query duplicada")
        queries.add(par["query"])

        if par["tipo"] not in valid_tipos:
            issues.append(f"{par['id']}: tipo inválido '{par['tipo']}'")
        else:
            tipos[par["tipo"]] += 1

        if par["esperado_nota"] not in notas:
            issues.append(
                f"{par['id']}: esperado_nota '{par['esperado_nota']}' não existe em fabrica/"
            )

        for alt in par.get("aceitaveis") or []:
            if alt not in notas:
                issues.append(f"{par['id']}: aceitavel '{alt}' não existe em fabrica/")

        if par.get("revisar"):
            revisar.append(par["id"])

    min_por_tipo = min(tipos.values()) if tipos else 0
    if min_por_tipo < 3:
        issues.append(
            f"cobertura mínima por tipo < 3: {dict(tipos)}"
        )

    return {
        "total": len(pairs),
        "tipos": dict(tipos),
        "revisar_ids": revisar,
        "revisar_count": len(revisar),
        "issues": issues,
        "valido": len(issues) == 0,
    }


def buscar_chroma(query: str, porta: int, top_k: int) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "n": str(top_k)})
    url = f"http://localhost:{porta}/buscar?{params}"
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise SystemExit(
            f"Chroma indisponível em localhost:{porta} — "
            f"rode: python {ROOT / 'indexar_obsidian_chroma.py'} --server\n"
            f"Erro: {exc}"
        ) from exc

    if not isinstance(data, list):
        raise SystemExit(f"Resposta inesperada de {url}: {type(data)}")
    return data


def notas_alvo(par: dict) -> list[str]:
    """Notas que contam como hit (esperado + aceitaveis, sem duplicata)."""
    alvo = [par["esperado_nota"]]
    for nome in par.get("aceitaveis") or []:
        if nome not in alvo:
            alvo.append(nome)
    return alvo


def rank_of(arquivos: list[str], alvos: list[str]) -> int | None:
    """Melhor rank entre todas as notas alvo (1 = melhor)."""
    ranks = []
    for alvo in alvos:
        for i, nome in enumerate(arquivos, 1):
            if nome == alvo:
                ranks.append(i)
                break
    return min(ranks) if ranks else None


def rank_estrito(arquivos: list[str], esperado: str) -> int | None:
    for i, nome in enumerate(arquivos, 1):
        if nome == esperado:
            return i
    return None


def compute_metrics(results: list[dict], rank_key: str = "rank") -> dict:
    n = len(results)
    if n == 0:
        return {"hit@1": 0.0, "hit@3": 0.0, "hit@5": 0.0, "mrr": 0.0, "n": 0}

    hit1 = sum(1 for r in results if r.get(rank_key) == 1) / n
    hit3 = sum(
        1 for r in results if r.get(rank_key) is not None and r[rank_key] <= 3
    ) / n
    hit5 = sum(
        1 for r in results if r.get(rank_key) is not None and r[rank_key] <= 5
    ) / n
    mrr = sum(
        (1.0 / r[rank_key]) if r.get(rank_key) is not None else 0.0 for r in results
    ) / n

    return {
        "hit@1": round(hit1, 4),
        "hit@3": round(hit3, 4),
        "hit@5": round(hit5, 4),
        "mrr": round(mrr, 4),
        "n": n,
    }


def build_summary(
    pairs: list[dict],
    per_query: list[dict],
    porta: int,
    top_k: int,
    regua: str,
) -> dict:
    rank_key = "rank" if regua == "v2" else "rank_primario"
    aggregate = compute_metrics(per_query, rank_key)
    by_tipo: defaultdict[str, list[dict]] = defaultdict(list)
    for row in per_query:
        by_tipo[row["tipo"]].append(row)
    por_tipo = {
        tipo: compute_metrics(rows, rank_key) for tipo, rows in sorted(by_tipo.items())
    }
    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "porta_chroma": porta,
        "top_k": top_k,
        "total_pares": len(pairs),
        "regua": regua,
        "aggregate": aggregate,
        "por_tipo": por_tipo,
    }


def evaluate(pairs: list[dict], porta: int, top_k: int) -> list[dict]:
    per_query: list[dict] = []

    for par in pairs:
        hits = buscar_chroma(par["query"], porta, top_k)
        arquivos = [h.get("arquivo", "") for h in hits]
        alvos = notas_alvo(par)
        rank = rank_of(arquivos, alvos)
        rank_primario = rank_estrito(arquivos, par["esperado_nota"])
        row = {
            "id": par["id"],
            "query": par["query"],
            "tipo": par["tipo"],
            "esperado_nota": par["esperado_nota"],
            "aceitaveis": par.get("aceitaveis") or [],
            "notas_alvo": alvos,
            "revisar": bool(par.get("revisar", False)),
            "rank": rank,
            "rank_primario": rank_primario,
            "hit": rank is not None,
            "hit_primario": rank_primario is not None,
            "top_k_arquivos": arquivos,
            "top_k_similaridade": [h.get("similaridade") for h in hits],
        }
        per_query.append(row)

    return per_query


def write_report_md(
    validation: dict,
    per_query: list[dict],
    summary: dict,
    path: Path,
    titulo: str = "Baseline",
    regua: str = "v1",
) -> None:
    agg = summary["aggregate"]
    pares_aceitaveis = sum(1 for r in per_query if r.get("aceitaveis"))
    lines = [
        f"# RAG Eval — {titulo}",
        "",
        f"Gerado em: {summary['gerado_em']}",
        f"Servidor: `http://localhost:{summary['porta_chroma']}/buscar` · top-k={summary['top_k']}",
        f"Régua: **{regua}**"
        + (
            " (hit se `esperado_nota` ou qualquer `aceitaveis` no top-k; MRR = melhor rank entre alvos)"
            if regua == "v2"
            else " (hit estrito em `esperado_nota` apenas)"
        ),
        "",
        "## Auto-checagem do golden set",
        "",
        f"- Pares: **{validation['total']}**",
        f"- Com `aceitaveis`: **{pares_aceitaveis}**",
        f"- Com `revisar: true`: **{validation['revisar_count']}** — {', '.join(validation['revisar_ids']) or '—'}",
        f"- Cobertura por tipo: `{validation['tipos']}`",
        "",
    ]

    if validation["issues"]:
        lines.append("### Problemas encontrados")
        lines.append("")
        for issue in validation["issues"]:
            lines.append(f"- {issue}")
        lines.append("")
    else:
        lines.append("Validação: **OK** (todos os `esperado_nota` existem, sem queries duplicadas).")
        lines.append("")

    lines.extend([
        "## Métricas agregadas",
        "",
        "| Métrica | Valor |",
        "|---------|-------|",
        f"| hit@1 | {agg['hit@1']:.1%} |",
        f"| hit@3 | {agg['hit@3']:.1%} |",
        f"| hit@5 | {agg['hit@5']:.1%} |",
        f"| MRR | {agg['mrr']:.4f} |",
        "",
        "## Por tipo",
        "",
        "| tipo | n | hit@1 | hit@3 | hit@5 | MRR |",
        "|------|---|-------|-------|-------|-----|",
    ])

    for tipo, m in summary["por_tipo"].items():
        lines.append(
            f"| {tipo} | {m['n']} | {m['hit@1']:.1%} | {m['hit@3']:.1%} | "
            f"{m['hit@5']:.1%} | {m['mrr']:.4f} |"
        )

    lines.extend(["", "## Detalhe por query", ""])
    for row in per_query:
        rank_key = "rank" if regua == "v2" else "rank_primario"
        display_rank = row.get(rank_key)
        status = f"rank {display_rank}" if display_rank else "MISS"
        rev = " ⚠️ revisar" if row["revisar"] else ""
        aceit = ""
        if row.get("aceitaveis"):
            aceit = f"\n- **Aceitáveis:** {', '.join(f'`{a}`' for a in row['aceitaveis'])}"
            if row.get("rank_primario") and row["rank_primario"] != row["rank"]:
                aceit += f" (primário rank {row['rank_primario']})"
        lines.append(f"### {row['id']} — {status}{rev}")
        lines.append("")
        lines.append(f"- **Query:** {row['query']}")
        lines.append(f"- **Esperado:** `{row['esperado_nota']}` ({row['tipo']}){aceit}")
        lines.append(f"- **Top-{summary['top_k']}:** {', '.join(f'`{a}`' for a in row['top_k_arquivos'])}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_delta_report(baseline_path: Path, hybrid_path: Path, out_path: Path) -> None:
    if not baseline_path.is_file() or not hybrid_path.is_file():
        print(f"⚠️  Delta ignorado — falta {baseline_path.name} ou {hybrid_path.name}")
        return
    base = json.loads(baseline_path.read_text(encoding="utf-8"))
    hybrid = json.loads(hybrid_path.read_text(encoding="utf-8"))
    ba, ha = base["aggregate"], hybrid["aggregate"]
    tipos = sorted(set(base.get("por_tipo", {})) | set(hybrid.get("por_tipo", {})))

    def delta(a: float, b: float) -> str:
        d = b - a
        sign = "+" if d >= 0 else ""
        return f"{sign}{d:.1%}" if abs(d) < 1 else f"{sign}{d:.4f}"

    lines = [
        "# RAG Eval — Delta (híbrido vs baseline v2)",
        "",
        f"Baseline: `{baseline_path.name}` · Híbrido: `{hybrid_path.name}`",
        "",
        "## Agregado",
        "",
        "| Métrica | v2 | híbrido | Δ |",
        "|---------|-----|---------|---|",
        f"| hit@1 | {ba['hit@1']:.1%} | {ha['hit@1']:.1%} | {delta(ba['hit@1'], ha['hit@1'])} |",
        f"| hit@3 | {ba['hit@3']:.1%} | {ha['hit@3']:.1%} | {delta(ba['hit@3'], ha['hit@3'])} |",
        f"| hit@5 | {ba['hit@5']:.1%} | {ha['hit@5']:.1%} | {delta(ba['hit@5'], ha['hit@5'])} |",
        f"| MRR | {ba['mrr']:.4f} | {ha['mrr']:.4f} | {delta(ba['mrr'], ha['mrr'])} |",
        "",
        "## Por tipo",
        "",
        "| tipo | v2 hit@1 | híbrido hit@1 | Δ hit@1 | v2 MRR | híbrido MRR | Δ MRR |",
        "|------|----------|---------------|---------|--------|-------------|-------|",
    ]
    for tipo in tipos:
        bm = base.get("por_tipo", {}).get(tipo, {})
        hm = hybrid.get("por_tipo", {}).get(tipo, {})
        lines.append(
            f"| {tipo} | {bm.get('hit@1', 0):.1%} | {hm.get('hit@1', 0):.1%} | "
            f"{delta(bm.get('hit@1', 0), hm.get('hit@1', 0))} | "
            f"{bm.get('mrr', 0):.4f} | {hm.get('mrr', 0):.4f} | "
            f"{delta(bm.get('mrr', 0), hm.get('mrr', 0))} |"
        )

    padrao_up = (
        hybrid.get("por_tipo", {}).get("padrao", {}).get("hit@1", 0)
        > base.get("por_tipo", {}).get("padrao", {}).get("hit@1", 0)
    )
    integr_up = (
        hybrid.get("por_tipo", {}).get("integracao", {}).get("hit@1", 0)
        > base.get("por_tipo", {}).get("integracao", {}).get("hit@1", 0)
    )
    lines.extend([
        "",
        "## Gate PR (B4)",
        "",
        f"- padrao hit@1 melhorou: **{'sim' if padrao_up else 'NÃO'}**",
        f"- integracao hit@1 melhorou: **{'sim' if integr_up else 'NÃO'}**",
        f"- Merge recomendado: **{'sim' if padrao_up and integr_up else 'não — revisar retrieval'}**",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Delta: {out_path.name}")


def main() -> None:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Avalia retrieval RAG contra golden set")
    parser.add_argument("--porta", type=int, default=DEFAULT_PORT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--golden", type=Path, default=GOLDEN_PATH)
    parser.add_argument(
        "--regua",
        choices=("v1", "v2", "both"),
        default="v1",
        help="v1=estrito; v2=aceitaveis; both=gera report-baseline e report-baseline-v2",
    )
    parser.add_argument(
        "--tag",
        choices=("default", "hybrid"),
        default="default",
        help="hybrid=grava report-hybrid.* em vez de report-baseline-v2.*",
    )
    parser.add_argument(
        "--compare-to",
        type=Path,
        default=None,
        help="Gera report-delta.md comparando com JSON baseline (ex.: report-baseline-v2.json)",
    )
    args = parser.parse_args()

    if not args.golden.is_file():
        raise SystemExit(f"Golden set não encontrado: {args.golden}")

    pairs = load_golden(args.golden)
    notas = list_fabrica_notes()
    validation = validate_golden(pairs, notas)

    print(f"Golden set: {len(pairs)} pares · revisar={validation['revisar_count']}")
    if validation["issues"]:
        print("⚠️  Problemas de validação:")
        for issue in validation["issues"]:
            print(f"   - {issue}")

    per_query = evaluate(pairs, args.porta, args.top_k)

    reguas = []
    if args.regua in ("v1", "both"):
        reguas.append(("v1", REPORT_MD, REPORT_JSON, "Baseline (estrito)"))
    if args.regua in ("v2", "both"):
        if args.tag == "hybrid":
            reguas.append(("v2", REPORT_HYBRID_MD, REPORT_HYBRID_JSON, "Retrieval híbrido (v2)"))
        else:
            reguas.append(("v2", REPORT_V2_MD, REPORT_V2_JSON, "Baseline v2 (réguas justas)"))

    for regua_id, md_path, json_path, titulo in reguas:
        summary = build_summary(pairs, per_query, args.porta, args.top_k, regua_id)
        summary["validacao"] = validation
        summary["detalhe"] = per_query
        json_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_report_md(validation, per_query, summary, md_path, titulo, regua_id)

    last = build_summary(pairs, per_query, args.porta, args.top_k, reguas[-1][0])
    agg = last["aggregate"]
    print(
        f"\nResultado ({reguas[-1][0]}): hit@1={agg['hit@1']:.1%} hit@3={agg['hit@3']:.1%} "
        f"hit@5={agg['hit@5']:.1%} MRR={agg['mrr']:.4f}"
    )
    print("Relatórios:", ", ".join(p.name for _, p, _, _ in reguas))

    if args.compare_to:
        hybrid_json = REPORT_HYBRID_JSON if args.tag == "hybrid" else reguas[-1][2]
        write_delta_report(args.compare_to, hybrid_json, REPORT_DELTA_MD)


if __name__ == "__main__":
    main()
