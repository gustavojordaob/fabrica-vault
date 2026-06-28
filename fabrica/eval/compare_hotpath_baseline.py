#!/usr/bin/env python3
"""Compara eval atual com snapshot baseline (hits idênticos)."""
import json
import shutil
import sys
from pathlib import Path

EVAL = Path(__file__).parent
BASELINE = EVAL / "report-hotpath-baseline.json"
CURRENT = EVAL / "report-hotpath.json"


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        shutil.copy2(CURRENT, BASELINE)
        print(f"Snapshot salvo: {BASELINE.name}")
        return 0

    if not BASELINE.is_file():
        print(f"Sem baseline — copie report-hotpath.json para {BASELINE.name} antes da otimização")
        return 1

    old = json.loads(BASELINE.read_text(encoding="utf-8"))
    new = json.loads(CURRENT.read_text(encoding="utf-8"))
    diffs = []
    for o, n in zip(old["detalhe"], new["detalhe"]):
        if o["rank"] != n["rank"] or o["top_k_arquivos"] != n["top_k_arquivos"]:
            diffs.append(f"{o['id']}: rank {o['rank']}->{n['rank']}")
    if diffs:
        print("HITS DIFERENTES:", diffs)
        return 1
    print("OK: ranks e top-5 idênticos ao baseline hotpath")
    agg_o, agg_n = old["aggregate"], new["aggregate"]
    print(f"Agregado baseline: hit@1={agg_o['hit@1']:.0%} MRR={agg_o['mrr']:.4f}")
    print(f"Agregado atual:    hit@1={agg_n['hit@1']:.0%} MRR={agg_n['mrr']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
