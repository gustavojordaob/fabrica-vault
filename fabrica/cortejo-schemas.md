---
tags:
  - firestore
  - schema
  - cortejo
fonte: repo cortejo (types + services)
atualizado_em: 2026-06-23
firebase_project: cortejo-app
links:
  - "[[../projetos/cortejo-prd]]"
  - "[[../projetos/cortejo-project]]"
  - "[[agenda-salao-expo-padrao]]"
  - "[[cadastro-clientes-salao-expo]]"
  - "[[whatsapp-salao-expo-padrao]]"
  - "[[whatsapp-business-api]]"
  - "[[mercadopago-assinatura-ota-padroes]]"
  - "[[cortejo-modulos-jun2026-padrao]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** — rules, deploy `cortejo-app`
> 2. MCP **fabrica-apps** — `rag_buscar("cortejo firestore schema")`

Path raiz: `artifacts/cortejo/salons/{salonId}`

---

## Documento do salão `salons/{salonId}`

| Campo | Tipo | Uso |
|-------|------|-----|
| `name`, `phone`, endereço (`cep`, `logradouro`, …) | string | Perfil + WhatsApp |
| `ownerUid`, `plan` | string | Auth + freemium |
| `planTier` | `PlanTier` | Tier Pro (4 planos) |
| `planMsgLimit` | number | Limite WhatsApp/mês |
| `planPlatform` | `ios` \| `android` | Origem assinatura |
| `planExpiresAt` | string ISO | Fim período |
| `planRenewalDay` | number | Dia renovação (1–28) |
| `hadAndroidTrial` | boolean? | Trial MP consumido |
| `hadIosTrial` | boolean? | Intro offer Apple consumido |
| `msgUsage` | object | Uso WhatsApp por período — ver [[cortejo-modulos-jun2026-padrao]] §3 |
| `whatsapp` | object | Ver seção abaixo — conexão Meta / envio |
| `businessHours` | `BusinessHours` | **Fallback** de horário (legado / template) |
| `blockedPeriods` | `BlockedPeriod[]` | Bloqueios de agenda (salão ou por profissional) |
| `subscription` | object | Mercado Pago |

### `BlockedPeriod` (no doc do salão)

| Campo | Tipo | Uso |
|-------|------|-----|
| `id` | string | `block_${timestamp}` |
| `startDate`, `endDate` | string YYYY-MM-DD | Range inclusivo |
| `label` | string? | Motivo (férias, folga) |
| `professionalUid` | string? | Omitido = salão inteiro |
| `startTime`, `endTime` | string HH:mm? | Bloqueio parcial do dia (repetido em cada dia do range) |

**Serviço:** `services/blockedPeriods.ts` · **Lógica:** `utils/blockedPeriodsLogic.ts`

**Regra:** nunca `undefined` em `arrayUnion` — montar objeto omitindo campos vazios.

### `whatsapp` (objeto no doc do salão)

Ver **[[whatsapp-salao-expo-padrao]]** — schema completo, status e fluxos.

| Campo | Tipo | Uso |
|-------|------|-----|
| `mode` | `'own' \| 'shared'` | Intenção número próprio vs plataforma |
| `effectiveSender` | `'own' \| 'shared'` | Remetente efetivo (downgrade → `shared`) |
| `provider` | `'meta' \| 'gupshup' \| 'shared'` | Integração |
| `status` | string | `not_connected`, `pending`, `live`, `error`, `ineligible`, `disconnected` |
| `wabaId`, `phoneNumberId`, `displayPhone` | string? | IDs Meta após Embedded Signup |
| `coexistence` | boolean? | Coexistence (app + API) |
| `statusReason` | string? | Erro Meta / inelegível |

Rota auxiliar: `artifacts/cortejo/whatsappPhoneRoutes/{phoneNumberId}` → `tenantId`.

---

## `members/{uid}`

| Campo | Tipo | Uso |
|-------|------|-----|
| `uid`, `role`, `displayName` | string | Equipe |
| `active` | boolean | Filtro agenda / link público |
| `commissionPct` | number | Financeiro |
| `businessHours` | `BusinessHours` | **Horário de atendimento deste profissional** |
| `expoPushToken` | string? | Push dono/profissional |

**Resolver slots:** `resolveBusinessHours(member.businessHours, salon.businessHours)` em `utils/businessHours.ts`

**UI:** `app/config/horarios.tsx` salva em `members/{uid}`

---

## `clients/{id}`

| Campo | Tipo | Uso |
|-------|------|-----|
| `nome`, `sobrenome`, `name` | string | Nome completo |
| `celular`, `phone` | string | WhatsApp |
| `dataNascimento` | string YYYY-MM-DD | Link público + cadastro |

Ver **[[cadastro-clientes-salao-expo]]**

---

## `appointments/{id}`

| Campo | Tipo | Uso |
|-------|------|-----|
| `clientId`, `clientName`, `clientPhone` | string | Desnormalizado |
| `professionalUid`, `professionalName` | string | Agenda + slots |
| `serviceIds[]`, `serviceNames[]` | string[] | Serviço |
| `start`, `end` | Timestamp | Conflito + bloqueio |
| `status` | scheduled \| confirmed \| done \| canceled \| no_show | |
| `source` | app \| public \| walk_in | |

---

## Subcoleções

`services`, `products`, `stockMovements`, `sales`, `financeEntries`, `cashSessions`, `notifications`

---

## Cloud Functions (agenda)

| Function | Uso |
|----------|-----|
| `availableSlots` | Slots públicos — lê `members/{uid}.businessHours` + `blockedPeriods` |
| `publicBooking` | Cria agendamento — valida `slotOverlapsBlockedBrt` |

Deploy:

```powershell
Set-Location c:\Users\gusta\projetos\cortejo
npx firebase-tools deploy --only "functions:availableSlots,functions:publicBooking" --project cortejo-app
```

---

## Config global da plataforma — `artifacts/cortejo/system/platformConfig`

Documento **fora** de `salons/` — flags e toggles globais do app.

| Campo | Tipo | Default | Uso |
|-------|------|---------|-----|
| `whatsappSalonEnabled` | boolean | `false` (doc ausente) | Libera Embedded Signup / "WhatsApp do salão" para todos os usuários |

**Path completo:** `artifacts/cortejo/system/platformConfig`

**Regras:** read se autenticado; write `false` (somente Admin SDK / Console / MCP).

**Código:** `services/platformConfig.ts`, `hooks/useWhatsappSalonFeature.ts`, gate em `functions/SRC/embeddedSignup.ts` → `startEmbeddedSignup`.

**❌ Não usar:** `artifacts/system` (documento solto) — caminho errado documentado em [[whatsapp-salao-expo-padrao]] §14.

---

## Sincronização

Ao alterar schema aqui, atualizar:

1. `obsidian/projetos/cortejo-prd.md` (seção Firestore)
2. `types/index.ts` no repo
3. `python C:/Users/gusta/obsidian/indexar_rapido.py`
