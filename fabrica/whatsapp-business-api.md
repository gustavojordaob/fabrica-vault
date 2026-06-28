---
tags:
  - integracao
  - whatsapp
  - meta
  - cloud-functions
  - lashmatch
fonte: LashMatch/docs/whatsapp-business-api.md
atualizado_em: 2026-06-20
projeto: LashMatch
links:
  - "[[../projetos/lashmatch-prd]]"
  - "[[lashmatch-schemas]]"
  - "[[whatsapp-salao-expo-padrao]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **whatsapp** (`user-whatsapp`) — Graph API, templates Meta, credenciais Business
> 2. MCP **fabrica-apps** — `rag_buscar("whatsapp meta")` + `buscar_historico("whatsapp")`
>
> **Multi-tenant / Embedded Signup / Coexistence:** ver **[[whatsapp-salao-expo-padrao]]** (Cortejo — padrão reutilizável).
>
> **Espelho no repo:** `LashMatch/docs/whatsapp-business-api.md` ou `cortejo/docs/whatsapp-business-api.md` — manter sincronizado após mudança em templates ou `functions/SRC/whatsapp.ts`.

---

# WhatsApp Business API (Meta) — LashMatch

> **Status:** Z-API removido (maio/2026). Envio automático via **Graph API** + templates aprovados pela Meta.  
> **Documentação oficial:** [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)

---

## Visão geral

| Canal | Onde | Como |
|-------|------|------|
| **Automático (servidor)** | Cloud Functions | Templates Meta (`agendamento_confirmado_v7`, `lembrete_agendamento_v2`) |
| **Manual (app)** | Telas de agendamento | `Linking` abre WhatsApp com texto pré-preenchido (sem API) |

O app **não** embute `WHATSAPP_TOKEN`. Toda chamada à Graph API roda nas **Cloud Functions**.

---

## Arquivos do projeto

| Arquivo | Função |
|---------|--------|
| `functions/SRC/whatsapp.ts` | Módulo central: formatação E.164, envio de templates, `DadosMensagemAgendamentoWhatsApp` |
| `functions/SRC/index.ts` | Schedulers e triggers que chamam `whatsapp.ts` |
| `functions/SRC/relatorioAnalisesJob.ts` | Relatório periódico via `enviarTextoWhatsApp` |
| `hooks/useLembretesEnviados.ts` | Notificação local à profissional após lembretes |
| `app/(tabs)/perfilUsuario.tsx` | Perfil + `telefoneSalao` + relatório WhatsApp |
| `app/cadastroUsuario.tsx` | Cadastro com **`telefoneSalao` obrigatório** |
| `docs/whatsapp-business-api.md` | Este guia (cópia no repositório) |

---

## Credenciais e variáveis

### `functions/.env` (params — não secretos)

```env
WHATSAPP_PHONE_ID=1190765630776115
WHATSAPP_BUSINESS_ID=937817869078549
WHATSAPP_VERIFY_TOKEN=lashmatch-webhook-2026
WHATSAPP_API_VERSION=v25.0
WHATSAPP_TEMPLATE_CONFIRMACAO=agendamento_confirmado_v7
WHATSAPP_TEMPLATE_LEMBRETE=lembrete_agendamento_v2
```

| Variável | Uso |
|----------|-----|
| `WHATSAPP_PHONE_ID` | ID do número remetente na Graph API (`defineString`) |
| `WHATSAPP_BUSINESS_ID` | Meta Business ID (referência / MCP) |
| `WHATSAPP_VERIFY_TOKEN` | Verificação do webhook Meta (GET `hub.verify_token`) |
| `WHATSAPP_APP_SECRET` | Opcional — valida `X-Hub-Signature-256` nos POST |
| `WHATSAPP_API_VERSION` | Default `v25.0` |
| `WHATSAPP_TEMPLATE_CONFIRMACAO` | Template de confirmação (`agendamento_confirmado_v7`, 9 variáveis) |
| `WHATSAPP_TEMPLATE_LEMBRETE` | Template de lembrete (`lembrete_agendamento_v2`, 9 variáveis) |

> **Erro comum:** `PHONE_ID` antigo `1139549772571990` causava **132001** (template não existe nesse número). Usar sempre o ID do número conectado no painel Meta.

### Secret Firebase (obrigatório para deploy)

```bash
firebase functions:secrets:set WHATSAPP_TOKEN
```

Emulador local: `functions/.secret.local` → `WHATSAPP_TOKEN=...`

### Números (referência)

| Ambiente | Número |
|----------|--------|
| Teste Meta | +1 555 644 6429 |
| Produção (pendente verificação) | +55 19 98963-1786 |

---

## Templates Meta (pt_BR)

Todos devem estar **APPROVED** no Business Manager antes do envio funcionar.

| Nome | Categoria | Variáveis | Uso |
|------|-----------|-----------|-----|
| `agendamento_confirmado_v7` | UTILITY | 9 vars (ver abaixo) | Confirmação ao criar agendamento |
| `lembrete_agendamento_v2` | UTILITY | 9 vars (mesma ordem) | Lembrete ~24h antes (scheduler 08:00) |
| `mensagem_utilidade` | UTILITY | `{{1}}` texto completo | Relatório de análises/financeiro |

**Ordem das 9 variáveis (confirmação e lembrete):**

| # | Campo | Origem |
|---|--------|--------|
| 1 | Nome da cliente | `clienteNome` |
| 2 | Nome do salão | `usuarios/{uid}.nomeSalao` |
| 3 | Endereço | perfil do salão |
| 4 | Data | `dataHoraInicio` (fuso BR) |
| 5 | Hora | idem |
| 6 | Serviço | `servicoNome` |
| 7 | Profissional | `funcionariaNome` |
| 8 | Telefone do salão | `usuarios/{uid}.telefoneSalao` |
| 9 | Assinatura | mesmo nome do salão |

> Cadastre **WhatsApp do salão** no cadastro (`cadastroUsuario.tsx`) ou em Perfil → Editar (`telefoneSalao`). Fallback: `relatorioAnalisesWhatsApp.telefone`.

---

## Cloud Functions

| Função | Trigger | Envio |
|--------|---------|-------|
| `enviarLembretesAgendamento` | Scheduler `0 8 * * *` America/Sao_Paulo | `enviarLembrete()` |
| `enviarConfirmacaoAgendamento` | `onDocumentCreated` em `agendamentos/{id}` | confirmação v7 |
| `enviarRelatorioAnalisesWhatsApp` | Scheduler horário | `enviarTextoWhatsApp()` |
| `testarLembrete` | HTTP POST | Teste template lembrete (`uid` opcional para dados do salão) |
| `testarConfirmacaoAgendamento` | HTTP POST | Teste template `agendamento_confirmado_v7` |
| `testarLembrete24h` | HTTP POST | Teste por `appId` + `uid` + `agendamentoId` |
| `webhookWhatsApp` | HTTP GET/POST | Webhook Meta |

**Webhook URL:** `https://us-central1-lashmatch-627fd.cloudfunctions.net/webhookWhatsApp`

### Fluxo lembrete (resumo)

1. Scheduler às **08:00** (BR).
2. `collectionGroup('agendamentos')` — janela `(agora, agora+30h]`, `lembreteEnviado != true`.
3. Template `lembrete_agendamento_v2` → atualiza `lembreteEnviado`, `lembreteEnviadoEm`.
4. Grava `resumoLembretes/ultimo` → app notifica a profissional.

### Teste manual

```bash
curl -X POST https://us-central1-lashmatch-627fd.cloudfunctions.net/testarConfirmacaoAgendamento \
  -H "Content-Type: application/json" \
  -d '{"telefone":"19989632897","nome":"Camila","uid":"SEU_UID"}'

curl -X POST https://us-central1-lashmatch-627fd.cloudfunctions.net/testarLembrete \
  -H "Content-Type: application/json" \
  -d '{"telefone":"19989632897","nome":"Camila","uid":"SEU_UID"}'
```

---

## Firestore — campos relevantes

```
artifacts/{appId}/users/{uid}/agendamentos/{id}
  - clienteNome, clienteTelefone  (desnormalizados, só dígitos no telefone)
  - dataHoraInicio, dataHoraFim
  - servicoNome, funcionariaNome
  - lembreteEnviado, lembreteEnviadoEm
  - confirmacaoEnviadaEm, confirmacaoErro

usuarios/{uid}
  - telefoneSalao: string (dígitos BR, obrigatório no cadastro novo)
  - nomeSalao, endereço (campos de perfil usados nas vars {{2}} {{3}} {{9}})
  - relatorioAnalisesWhatsApp: { ativo, telefone, frequencia, ... }
```

---

## Checklist operacional

- [ ] `WHATSAPP_TOKEN` no Firebase Secrets + redeploy
- [ ] Templates `agendamento_confirmado_v7`, `lembrete_agendamento_v2`, `mensagem_utilidade` **APPROVED**
- [ ] `WHATSAPP_PHONE_ID=1190765630776115` (ou ID correto após verificação Meta)
- [ ] `telefoneSalao` preenchido em `usuarios/{uid}` (cadastro ou perfil)
- [ ] Plano Firebase **Blaze**
- [ ] Testar `testarConfirmacaoAgendamento` e `testarLembrete` antes do scheduler

---

## Histórico

- **Até maio/2026:** Z-API — removido.
- **Maio/2026:** Meta Graph API com templates 3–5 vars (`lembrete_agendamento`, `confirmacao_agendamento`).
- **Jun/2026:** Templates 9 vars v7/v2 + `telefoneSalao` + `PHONE_ID` corrigido.

## LashMatch — Embedded Signup salão

*Atualizado em 25/06/2026*

- Flag: `artifacts/{appId}/system/platformConfig` campo `whatsappSalonEnabled: true`
- Schema: `usuarios/{uid}.whatsapp` (status, phoneNumberId, wabaId, effectiveSender)
- App: `/config/whatsapp` + hook `useWhatsappSalonFeature`
- CF: `startEmbeddedSignup`, `completeEmbeddedSignup`, `embeddedSignupPageConfig`, `cancelEmbeddedSignup`
- Env: `META_APP_ID`, `META_APP_SECRET`, `META_CONFIG_ID`, `EMBEDDED_SIGNUP_PUBLIC_BASE_URL`
- Envio automático: `resolveSender` em `whatsappSender.ts` — own vs shared LashMatch

---
