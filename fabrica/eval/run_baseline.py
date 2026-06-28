#!/usr/bin/env python3
"""
Harness de avaliação RAG — baseline contra golden-set.jsonl.

Chama o retrieval atual via HTTP Chroma (porta 7332) e mede hit@1/3/5 + MRR.
Não altera indexação nem retrieval.

Uso:
    python fabrica/eval/run_baseline.py
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


def rank_of(arquivos: list[str], esperado: str) -> int | None:
    for i, nome in enumerate(arquivos, 1):
        if nome == esperado:
            return i
    return None


def compute_metrics(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {"hit@1": 0.0, "hit@3": 0.0, "hit@5": 0.0, "mrr": 0.0, "n": 0}

    hit1 = sum(1 for r in results if r["rank"] == 1) / n
    hit3 = sum(1 for r in results if r["rank"] is not None and r["rank"] <= 3) / n
    hit5 = sum(1 for r in results if r["rank"] is not None and r["rank"] <= 5) / n
    mrr = sum(
        (1.0 / r["rank"]) if r["rank"] is not None else 0.0 for r in results
    ) / n

    return {
        "hit@1": round(hit1, 4),
        "hit@3": round(hit3, 4),
        "hit@5": round(hit5, 4),
        "mrr": round(mrr, 4),
        "n": n,
    }


def evaluate(pairs: list[dict], porta: int, top_k: int) -> tuple[list[dict], dict]:
    per_query: list[dict] = []
    by_tipo: defaultdict[str, list[dict]] = defaultdict(list)

    for par in pairs:
        hits = buscar_chroma(par["query"], porta, top_k)
        arquivos = [h.get("arquivo", "") for h in hits]
        rank = rank_of(arquivos, par["esperado_nota"])
        row = {
            "id": par["id"],
            "query": par["query"],
            "tipo": par["tipo"],
            "esperado_nota": par["esperado_nota"],
            "revisar": bool(par.get("revisar", False)),
            "rank": rank,
            "hit": rank is not None,
            "top_k_arquivos": arquivos,
            "top_k_similaridade": [h.get("similaridade") for h in hits],
        }
        per_query.append(row)
        by_tipo[par["tipo"]].append(row)

    aggregate = compute_metrics(per_query)
    por_tipo = {tipo: compute_metrics(rows) for tipo, rows in sorted(by_tipo.items())}

    summary = {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "porta_chroma": porta,
        "top_k": top_k,
        "total_pares": len(pairs),
        "aggregate": aggregate,
        "por_tipo": por_tipo,
    }
    return per_query, summary


def write_report_md(
    validation: dict,
    per_query: list[dict],
    summary: dict,
    path: Path,
) -> None:
    agg = summary["aggregate"]
    lines = [
        "# RAG Eval — Baseline",
        "",
        f"Gerado em: {summary['gerado_em']}",
        f"Servidor: `http://localhost:{summary['porta_chroma']}/buscar` · top-k={summary['top_k']}",
        "",
        "## Auto-checagem do golden set",
        "",
        f"- Pares: **{validation['total']}**",
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
        status = f"rank {row['rank']}" if row["rank"] else "MISS"
        rev = " ⚠️ revisar" if row["revisar"] else ""
        lines.append(f"### {row['id']} — {status}{rev}")
        lines.append("")
        lines.append(f"- **Query:** {row['query']}")
        lines.append(f"- **Esperado:** `{row['esperado_nota']}` ({row['tipo']})")
        lines.append(f"- **Top-{summary['top_k']}:** {', '.join(f'`{a}`' for a in row['top_k_arquivos'])}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="Avalia retrieval RAG contra golden set")
    parser.add_argument("--porta", type=int, default=DEFAULT_PORT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--golden", type=Path, default=GOLDEN_PATH)
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

    per_query, summary = evaluate(pairs, args.porta, args.top_k)
    summary["validacao"] = validation
    summary["detalhe"] = per_query

    REPORT_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report_md(validation, per_query, summary, REPORT_MD)

    agg = summary["aggregate"]
    print(
        f"\nResultado: hit@1={agg['hit@1']:.1%} hit@3={agg['hit@3']:.1%} "
        f"hit@5={agg['hit@5']:.1%} MRR={agg['mrr']:.4f}"
    )
    print(f"Relatórios: {REPORT_MD.name}, {REPORT_JSON.name}")


if __name__ == "__main__":
    main()
