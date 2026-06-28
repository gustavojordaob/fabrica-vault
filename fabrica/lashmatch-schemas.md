---
tags:
  - firestore
  - schema
  - lashmatch
fonte: LashMatch repo (código + docs)
atualizado_em: 2026-06-09
projeto: LashMatch
links:
  - "[[../projetos/lashmatch-prd]]"
  - "[[whatsapp-business-api]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** — rules e índices
> 2. MCP **fabrica-apps** — `rag_buscar("lashmatch firestore schema")`

Path padrão de dados do app: `artifacts/{appId}/users/{uid}/...` com `appId = app.options.appId`.

---

## `usuarios/{uid}` (perfil da profissional)

| Campo | Tipo | Obrigatório | Uso |
|-------|------|-------------|-----|
| `nome`, `sobrenome`, `email` | string | sim (cadastro) | Auth + perfil |
| `nomeSalao` | string | sim | WhatsApp var `{{2}}` e `{{9}}` |
| `telefoneSalao` | string (dígitos) | **sim no cadastro** | WhatsApp var `{{8}}`; editável no perfil |
| `cep`, `logradouro`, `numero`, `complemento`, `bairro`, `cidade`, `estado` | string | parcial | Endereço WhatsApp var `{{3}}` |
| `relatorioAnalisesWhatsApp` | object | não | Fallback do `{{8}}` se `telefoneSalao` vazio |
| `plano` | object | não | Assinatura — MP (Android) ou Apple (iOS). Ver [[lashmatch-modulos-assinatura-jun2026]] |
| `pagamento` | object | não | `metodo`: `MERCADO_PAGO` \| `APPLE`; `status` |
| `hadIosTrial` | boolean | não | Trial intro Apple já usado |
| `subscription` | object | não | Mirror webhook RC (`provider`, `status`, `currentPeriodEnd`) |
| `trialFimEm` | string ISO | não | Trial cadastro / MP |

**Telas:** `app/cadastroUsuario.tsx` (criação), `app/(tabs)/perfilUsuario.tsx` (edição).

**Regra CEP:** ViaCEP preenche logradouro/bairro/cidade/UF — **não** preenche `complemento` automaticamente.

---

## `artifacts/.../agendamentos/{id}`

| Campo | Tipo | Uso |
|-------|------|-----|
| `clienteId` | string | ref `clientes/{id}` |
| `clienteNome`, `clienteTelefone` | string | desnormalizado para Cloud Functions |
| `funcionariaId`, `funcionariaNome` | string | agenda + WhatsApp `{{7}}` |
| `servicoId`, `servicoNome` | string | WhatsApp `{{6}}` |
| `duracaoMinutos`, `preco` | number | conflito de horário + financeiro |
| `dataHoraInicio`, `dataHoraFim` | Timestamp | disponibilidade + WhatsApp data/hora |
| `status` | `'confirmado' \| 'cancelado' \| 'concluido'` | queries ignoram cancelados |
| `origem` | `'app' \| 'link_publico'` | |
| `lembreteEnviado`, `lembreteEnviadoEm` | boolean / Timestamp | scheduler ~24h |
| `lembrete7dEnviado`, `lembrete7dEnviadoEm` | boolean / Timestamp | scheduler ~7 dias antes |
| `confirmacaoEnviadaEm`, `confirmacaoErro` | Timestamp / string | trigger onCreate |

---

## Subcoleções relacionadas

- `clientes/{id}` — dados da cliente
- `funcionarias/{id}` — equipe
- `servicos/{id}` — catálogo com duração/preço
- `estoque/{id}` — produtos + `custoUnitario`
- `vendas/{id}`, `despesas/{id}` — financeiro
- `resumoLembretes/ultimo` — notificação local no app após lembretes automáticos

---

## Sincronização documentação

Ao alterar schema neste arquivo, atualizar também:

1. `obsidian/projetos/lashmatch-prd.md` (seção Firestore)
2. `LashMatch/docs/whatsapp-business-api.md` (se afetar WhatsApp)
3. Rodar `python C:/Users/gusta/obsidian/indexar_rapido.py`

---

## Exclusão de conta (LGPD / App Store)

Fluxo documentado em **[[excluir-conta-app-expo-padrao]]**.

| Item | Detalhe |
|------|---------|
| UI | `(tabs)/perfilUsuario.tsx` — botão **Excluir minha conta** |
| App | `hooks/useDeleteAccount.ts`, `services/account.ts` |
| Function | `excluirConta` — cancela MP + apaga `usuarios/{uid}` + `artifacts/{appId}/users/{uid}/*` + Storage + Auth |
| Env | `EXPO_PUBLIC_EXCLUIR_CONTA_URL` |

Subcoleções removidas: `clientes` (com `historicoAnalises`), `agendamentos`, `servicos`, `funcionarias`, `estoque`, `vendas`, `despesas`, `pagamentos`, `resumoLembretes`.
