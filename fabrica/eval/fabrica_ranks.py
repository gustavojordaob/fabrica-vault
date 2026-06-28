#!/usr/bin/env python3
"""Análise pares tipo=fabrica: hit@1 v2 vs hotpath."""
import json
from pathlib import Path

v2 = json.loads(Path("fabrica/eval/report-baseline-v2.json").read_text(encoding="utf-8"))
hp = json.loads(Path("fabrica/eval/report-hotpath.json").read_text(encoding="utf-8"))
by_v2 = {r["id"]: r for r in v2["detalhe"]}
by_hp = {r["id"]: r for r in hp["detalhe"]}

print("tipo=fabrica — v2 (denso) vs hotpath")
for pid in sorted(by_v2.keys(), key=lambda x: int(x.split("-")[1])):
    if by_v2[pid]["tipo"] != "fabrica":
        continue
    rv2, rhp = by_v2[pid]["rank"], by_hp[pid]["rank"]
    top3 = rhp is not None and rhp <= 3
    drop = rv2 == 1 and (rhp is None or rhp > 1)
    flag = " *** caiu hit@1" if drop else ""
    print(f"  {pid}: v2 rank={rv2} hotpath rank={rhp} top3={top3}{flag}")
