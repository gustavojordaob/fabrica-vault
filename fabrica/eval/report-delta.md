# RAG Eval — Delta (híbrido vs baseline v2)

Baseline: `report-baseline-v2.json` · Híbrido: `report-baseline-v2.json`

## Agregado

| Métrica | v2 | híbrido | Δ |
|---------|-----|---------|---|
| hit@1 | 46.4% | 46.4% | +0.0% |
| hit@3 | 64.3% | 64.3% | +0.0% |
| hit@5 | 64.3% | 64.3% | +0.0% |
| MRR | 0.5387 | 0.5387 | +0.0% |

## Por tipo

| tipo | v2 hit@1 | híbrido hit@1 | Δ hit@1 | v2 MRR | híbrido MRR | Δ MRR |
|------|----------|---------------|---------|--------|-------------|-------|
| fabrica | 50.0% | 50.0% | +0.0% | 0.6389 | 0.6389 | +0.0% |
| fluxo | 50.0% | 50.0% | +0.0% | 0.6250 | 0.6250 | +0.0% |
| integracao | 75.0% | 75.0% | +0.0% | 0.8333 | 0.8333 | +0.0% |
| padrao | 36.4% | 36.4% | +0.0% | 0.4141 | 0.4141 | +0.0% |
| solucao | 66.7% | 66.7% | +0.0% | 0.7593 | 0.7593 | +0.0% |

## Gate PR (B4)

- padrao hit@1 melhorou: **NÃO**
- integracao hit@1 melhorou: **NÃO**
- Merge recomendado: **não — revisar retrieval**