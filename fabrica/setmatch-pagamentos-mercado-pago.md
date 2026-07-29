---
tags:
  - fabrica
  - setmatch
  - pagamentos
  - mercadopago
atualizado_em: 2026-07-26
---

# Setmatch — Pagamentos Mercado Pago (aulas, ranking, torneio)

> **Agente Cursor — use MCP antes de codar**
> `rag_buscar("setmatch mercado pago pagamentos setmatchId")`
> `buscar_historico("setmatch pagamentos aulas ranking torneio")`
> MCP **mercadopago** para credenciais / homologação

Repo: `setmatch-app` · Firebase: `setmatch-app-fabrica`

## ID amigável

- Campo `usuarios.setmatchId` = `SM-XXXXXX` (gerado em `garantirSetmatchId`)
- Admin adiciona aluno / ranking com esse ID (`/clube/alunos`)
- Exibido em Perfil e Meus pagamentos

## Regras (dono cadastra)

| Produto | Onde | Campos |
|---------|------|--------|
| Aulas | `clubes/{id}.aulas` + `regrasGerais` | ativo, valorMensal, regras, PIX/cartão |
| Ranking | `rankings/{id}.pagamento` | ativo, valor, ciclo mensal\|unico, exigeParaEntrar, regras |
| Torneio | `torneios/{id}.pagamento` | ativo, valor, prazoPagamento, regras, PIX + cartão **1x** |

## Cobrança

- Coleção `pagamentos/{id}` — status: aguardando_pagamento → aprovado \| liberado_admin
- Coleção `matriculas/{id}` — alunos do clube
- Checkout Pro via Cloud Function `criarPreferenciaSetmatch`
- Webhook `webhookMercadoPagoSetmatch` sincroniza status e libera matrícula / inscrição / classificacao
- Recorrência MVP: ciclo `mensal` + `vigenteAte` (+1 mês no webhook); renovação = novo checkout (não preapproval ainda)

## Admin UI

- `/clube/aulas-regras` — regras e valor das aulas
- `/clube/alunos` — matricular por ID SM-
- `/clube/financeiro` — lista + liberar sem MP + msg
- `/clube/torneio-mensagens` — avisar inscritos
- Criar ranking/torneio já com regras de pagamento

## Jogador UI

- Solicitar ranking / Quero aulas / Inscrever torneio → cria `pagamentos` + abre checkout
- `/pagamentos` — Meus pagamentos + ID

## Config deploy

1. `functions/.env` → `MP_ACCESS_TOKEN=APP_USR-...` (ou TEST-)
2. `npm run build` em `functions/`
3. `firebase deploy --only functions:criarPreferenciaSetmatch,functions:webhookMercadoPagoSetmatch`
4. App: `EXPO_PUBLIC_MP_FUNCTION_URL` (já no eas.json)

## Checklist

- [x] setmatchId
- [x] Schema regras aulas/ranking/torneio
- [x] Functions Checkout Pro + webhook
- [x] Admin financeiro / alunos / regras
- [x] Jogador checkout
- [ ] Preencher `MP_ACCESS_TOKEN` real e testar PIX sandbox
- [ ] Assinatura MP preapproval (fase 2)
