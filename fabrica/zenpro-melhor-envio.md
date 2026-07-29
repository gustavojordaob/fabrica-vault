# Zen Pro — Melhor Envio (cotação + etiqueta postagem)

> **Agente Cursor — use MCP antes de codar**
> - `rag_buscar("zenpro melhor envio frete etiqueta")`
> - `buscar_historico("melhor envio zenpro")`

**Repo:** `C:/Users/gusta/projetos/zenpro`  
**Docs:** `docs/nota-fiscal-rastreio-automatico.md`

## Modo operacional

- Cotação no checkout (`calcularFreteMelhorEnvio`) — só **SEDEX + Loggi**
- Após pagamento: `envios_outbox` → `processarEnvioOutbox`
- Fluxo ME: cart → checkout (saldo) → generate → print
- **Postagem em agência** (`modoPostagem: "agencia"`) — **nunca** solicitar coleta
- Dono da Zen Pro leva o pacote até a agência sugerida (`meAgencyName`)

## Secrets / params

```powershell
firebase functions:secrets:set MELHOR_ENVIO_TOKEN --project zenpro-capinhas
# Opcional (refresh OAuth futuro — app "Zen Pro" Client ID 27166):
# firebase functions:secrets:set MELHOR_ENVIO_CLIENT_ID
# firebase functions:secrets:set MELHOR_ENVIO_CLIENT_SECRET
# functions/.env
MELHOR_ENVIO_USER_AGENT=Zen Pro (contato@usezenpro.com.br)
MELHOR_ENVIO_SANDBOX=false
MELHOR_ENVIO_TELEFONE_REMETENTE=5511...
MELHOR_ENVIO_EMAIL_REMETENTE=contato@usezenpro.com.br
MELHOR_ENVIO_WEBHOOK_SECRET=   # opcional
# Remetente PJ (mesmo Focus):
FOCUS_NFE_CNPJ_EMITENTE=
FOCUS_NFE_NOME_EMITENTE=
FOCUS_NFE_IE_EMITENTE=ISENTO
```

Runtime usa **só** `MELHOR_ENVIO_TOKEN` (Bearer). Client ID/Secret não vão no Git.

Webhook: `https://us-central1-zenpro-capinhas.cloudfunctions.net/webhookMelhorEnvio`

## Functions

| Function | Papel |
|----------|--------|
| `calcularFreteMelhorEnvio` | Cotação |
| `processarEnvioOutbox` | Compra etiqueta |
| `webhookMelhorEnvio` | Atualiza tracking |
| `reprocessarEnvioMelhorEnvio` | Admin re-enfileira |

## Checklist

- [ ] Token + telefone remetente + CNPJ
- [ ] Saldo na carteira Melhor Envio
- [ ] Expedição Zen Pro com CEP
- [ ] Produtos com peso/dimensões
- [ ] Deploy functions de envio
- [ ] Teste: PIX → outbox → rastreio no pedido (sem coleta)
