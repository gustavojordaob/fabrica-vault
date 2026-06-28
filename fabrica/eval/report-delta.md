# RAG Eval — Delta (híbrido vs baseline v2)

Baseline: `report-baseline-v2.json` · Híbrido: `report-hotpath.json`

## Agregado

| Métrica | v2 | híbrido | Δ |
|---------|-----|---------|---|
| hit@1 | 48.0% | 52.0% | +4.0% |
| hit@3 | 72.0% | 92.0% | +20.0% |
| hit@5 | 76.0% | 92.0% | +16.0% |
| MRR | 0.5947 | 0.7067 | +11.2% |

## Por tipo

| tipo | v2 hit@1 | híbrido hit@1 | Δ hit@1 | v2 MRR | híbrido MRR | Δ MRR |
|------|----------|---------------|---------|--------|-------------|-------|
| fabrica | 66.7% | 50.0% | -16.7% | 0.6667 | 0.7500 | +8.3% |
| fluxo | 25.0% | 50.0% | +25.0% | 0.3750 | 0.6250 | +25.0% |
| integracao | 25.0% | 50.0% | +25.0% | 0.5500 | 0.7083 | +15.8% |
| padrao | 40.0% | 40.0% | +0.0% | 0.4667 | 0.6000 | +13.3% |
| solucao | 66.7% | 66.7% | +0.0% | 0.8056 | 0.8056 | +0.0% |

## Gate PR (B4)

- padrao hit@1 melhorou: **NÃO**
- integracao hit@1 melhorou: **sim**
- Merge recomendado: **não — revisar retrieval**