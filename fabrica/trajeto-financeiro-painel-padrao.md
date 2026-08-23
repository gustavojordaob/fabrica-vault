---
tags:
  - trajeto
  - financeiro
  - expo
  - next
  - grafico
projeto: trajeto
atualizado_em: 2026-08-19
---

> **Agente Cursor — use MCP antes de codar**
>
> ```
> rag_buscar("trajeto financeiro painel gráfico ranking psicólogo")
> buscar_historico("financeiro clínica entradas saídas")
> ```
>
> Código: `packages/shared/finance.ts` · web `apps/web/components/finance/` · mobile `apps/mobile/components/FinanceDashboard.tsx`

# Painel financeiro Trajeto (período + gráfico + ranking)

Padrão de **gestão financeira clínica** (não banco/fintech rosa). Paleta sage/gold. Sem lib de chart.

## O que mostra

- **Saldo do período** (entradas − repasses na visão clínica; líquido do psicólogo na visão própria)
- **Passado / Futuro** — pago vs a receber
- Filtros: Dia, Semana, Mês, Trimestre, Semestre, Ano, **Intervalo** (de/até) + setas de período — **o extrato usa o mesmo recorte** (Passado = pagos, Futuro = a receber). Toque numa barra para filtrar aquele dia/mês.
- Gráfico SVG: barra sage = **entrada**, barra/linha ouro = **saída** (repasse ou retenção). **Mês** mostra os dias do mês, **Ano** os 12 meses. Nunca desenhar o ano quando o filtro é mês.
- **Gestor:** ranking de rentabilidade por psicólogo (o que fica na clínica após `payout_percent`)
- Extrato = CRUD de `invoices` abaixo

## Rotas

| Superfície | Gestor | Psicólogo |
|------------|--------|-----------|
| Web | `/clinica/financeiro` | `/psico/financeiro` |
| App | `(clinica)/financeiro` | `(psico)/financeiro` |

## Checklist no próximo app

- [ ] Períodos e ranking em pacote shared (não duplicar conta em web/app)
- [ ] Gráfico SVG (Expo Go) — não recharts
- [ ] Gestor vê clínica; psicólogo só a fatia RLS
- [ ] Tokens da marca, não copiar UI de banco
