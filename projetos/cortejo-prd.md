---
projeto: Cortejo
tipo: app-salao-beleza
stack: React Native (Expo) + Firebase
package: com.fabricaapps.cortejo
autor: Gustavo Jordao
atualizado_em: 2026-06-13
status: greenfield
---

# Cortejo — PROJECT.md

> Contexto único e definitivo para a IA (Cursor + fábrica-apps MCP) construir o app.
> **Local deste PRD:** `obsidian/projetos/cortejo-prd.md` (projetos por app).
> Padrões reutilizáveis cross-projeto: `obsidian/fabrica/`.
> Antes de codar qualquer feature: `rag_buscar` + `buscar_historico` na base Obsidian `fabrica/`.
> Reaproveitar TODOS os padrões já validados em LashMatch (auth, Firestore multi-tenant, Firebase upload, WhatsApp, Mercado Pago).

---

## 1. Visão do produto

**Cortejo** é um app de gestão para **salões de cabeleireiro** (e profissionais autônomos da beleza).
O nome brinca com "corte" + "cortejar/cuidar do cliente".

Resolve quatro dores em um único app:

1. **Agendamento** — agenda do profissional + página pública de auto-agendamento.
2. **Estoque** — controle de produtos, entradas, saídas, alerta de mínimo.
3. **Vendas / PDV** — venda de produtos e serviços, carrinho, recibo.
4. **Financeiro** — caixa diário, contas a pagar/receber, comissões, relatórios.

Tudo amarrado por um padrão visual consistente (design tokens abaixo).

### Público-alvo
- Donos de salão pequeno/médio (1 a 10 profissionais).
- Profissional autônomo (cadeira alugada, atendimento em casa).

### Modelo de negócio
- Freemium → assinatura mensal/anual via **Mercado Pago**.
- Free: 1 profissional, agenda + agendamento público.
- Pro: estoque + PDV + financeiro + multi-profissional + relatórios.

---

## 2. Design system (padrão de qualidade obrigatório)

A IA NUNCA usa cores hardcoded fora destes tokens. Centralizar em `theme/tokens.ts`.

### Paleta

| Token | Hex | Uso |
|-------|-----|-----|
| `primary` | `#6B4226` | Marrom café — marca, botões primários, headers |
| `primaryDark` | `#4A2D1A` | Pressed states, texto sobre claro |
| `accent` | `#D4A373` | Caramelo/dourado — destaques, CTA secundário |
| `accentSoft` | `#EFE3D3` | Fundos de card, chips |
| `bg` | `#FAF6F1` | Background geral (off-white quente) |
| `surface` | `#FFFFFF` | Cards, inputs, modais |
| `text` | `#2B2521` | Texto principal |
| `textMuted` | `#8A7E73` | Texto secundário, placeholders |
| `border` | `#E5DACE` | Bordas, divisores |
| `success` | `#5C8A5A` | Confirmado, pago, em estoque |
| `warning` | `#D98E04` | Estoque baixo, pendente |
| `danger` | `#B3463A` | Erro, cancelado, vencido |

### Tipografia
- Família: **Inter** (via `expo-font`), pesos 400/500/600/700.
- Escala: `display 28/700`, `h1 22/700`, `h2 18/600`, `body 15/400`, `caption 13/400`, `label 13/500`.

### Espaçamento & forma
- Grid base **4px**. Spacing: 4, 8, 12, 16, 24, 32.
- `radius`: sm 8, md 12, lg 20, pill 999.
- Sombra única `shadow.card` suave (elevation 2). Evitar sombras pesadas.
- Toda tela respeita `SafeAreaView` + padding horizontal 16.

### Componentes base (criar primeiro, em `components/ui/`)
`Button` (primary/secondary/ghost/danger), `Input`, `Card`, `Chip`, `Avatar`, `EmptyState`,
`Sheet` (bottom sheet), `Badge` (status), `ListItem`, `SectionHeader`, `Loader`, `Toast`.
Acessibilidade: alvo mínimo de toque 44px, `accessibilityLabel` em todo botão de ícone.

---

## 3. Stack técnica (igual à fábrica)

| Camada | Tecnologia |
|--------|-----------|
| App | React Native + **Expo 54**, Expo Router (file-based) |
| Linguagem | TypeScript estrito |
| Estado | Zustand (global) + React Query (dados Firestore/cache) |
| Auth | Firebase Auth — Google (`expo-auth-session`) + email/senha |
| DB | Cloud Firestore (multi-tenant) |
| Storage | Firebase Storage (logo, foto produto, avatar) |
| Backend | Cloud Functions (Node 20) |
| Pagamento | Mercado Pago (assinatura) |
| Notificação | WhatsApp Business API (Meta) via Cloud Function + `expo-notifications` (push) |
| Web pública | Firebase Hosting (página de agendamento) |
| Build | EAS Build / EAS Update |

### Padrões herdados do Obsidian (NÃO reinventar)
- `initializeAuth` com `getReactNativePersistence(AsyncStorage)`.
- Login Google sempre com `expo-auth-session`.
- Upload Storage: `ref → uploadBytes → getDownloadURL` na sequência validada.
- `utils/firebaseConfig.ts` único ponto de init.

---

## 4. Modelo de dados (Firestore multi-tenant)

Raiz padrão da fábrica: `artifacts/{appId}/...`. `appId = "cortejo"`.
Cada salão é um **tenant** (`salonId`).

```
artifacts/cortejo/
  salons/{salonId}
    - name, logoUrl, phone, address, timezone, ownerUid
    - plan: "free" | "pro"
    - subscription: { status, mpPreapprovalId, currentPeriodEnd }
    - businessHours: { mon:[{start,end}], ... }
    - createdAt, updatedAt

    members/{uid}
      - role: "owner" | "professional" | "receptionist"
      - displayName, photoUrl, commissionPct, active

    services/{serviceId}
      - name, durationMin, price, category, active

    clients/{clientId}
      - nome, sobrenome, name (desnormalizado nome + sobrenome)
      - celular (5511999999999), phone ((11) 99999-9999)
      - dataNascimento (YYYY-MM-DD), notes?
      - criadoEm, atualizadoEm
      - legado: email, birthday, tags[], totalSpent, lastVisitAt, photoUrl

    appointments/{appointmentId}
      - clientId, professionalUid, serviceIds[]
      - start (ts), end (ts), status: "scheduled"|"confirmed"|"done"|"canceled"|"no_show"
      - priceTotal, source: "app"|"public"|"walk_in"
      - reminderSentAt, notes, saleId?

    products/{productId}
      - name, sku, category, brand
      - costPrice, salePrice, unit
      - stockQty, stockMin, active, photoUrl

    stockMovements/{movId}
      - productId, type: "in"|"out"|"adjust"|"sale"
      - qty, reason, refSaleId?, byUid, createdAt

    sales/{saleId}
      - items[]: { kind:"service"|"product", refId, name, qty, unitPrice, total }
      - clientId, professionalUid
      - subtotal, discount, total
      - payment: { method:"cash"|"pix"|"credit"|"debit", installments }
      - status: "open"|"paid"|"canceled"
      - appointmentId?, createdAt, paidAt

    financeEntries/{entryId}
      - type: "income"|"expense"
      - category, description, amount
      - dueDate, paidAt, status:"pending"|"paid"|"overdue"
      - refSaleId?, recurring?, byUid

    cashSessions/{sessionId}
      - openedBy, openingAmount, closingAmount
      - openedAt, closedAt, status:"open"|"closed"
      - expectedTotal, difference
```

### Regras de segurança (resumo a implementar)
- Usuário só lê/escreve em `salons/{salonId}` se existir em `members/{uid}`.
- `role` define permissão: `professional` não edita `financeEntries` nem `members`.
- Página pública lê apenas `services`, `members` (nome/foto) e escreve `appointments` com `source:"public"` (status `scheduled`) via Cloud Function (não direto).

---

## 5. Navegação (Expo Router)

```
app/
  (auth)/
    login.tsx
    onboarding.tsx          ← criar salão (nome, logo, horários)
  (tabs)/
    index.tsx               ← Agenda (home)
    estoque.tsx
    vendas.tsx
    financeiro.tsx
    mais.tsx                ← config, equipe, plano, perfil
  agendamento/[id].tsx      ← detalhe/edição de agendamento
  cliente/[id].tsx
  produto/[id].tsx
  venda/nova.tsx            ← PDV
  venda/[id].tsx
  config/
    equipe.tsx
    servicos.tsx
    clientes.tsx          ← CRUD clientes (dono/equipe)
    horarios.tsx
    plano.tsx               ← assinatura Mercado Pago
  agendar/index.tsx         ← agendamento público (app); web = booking.html
```

Tab bar com 5 ícones (Agenda, Estoque, Vendas, Financeiro, Mais), cor ativa `primary`.

### Documentação técnica no repositório (`docs/`)

| Arquivo | Conteúdo |
|---------|----------|
| `docs/cadastro-clientes-salao.md` | CRUD clientes, schema, link público, checklist reutilizável |
| `docs/padroes-agendamento-web.md` | Hosting, booking.html, APIs públicas |
| `docs/notificacoes-push-inbox.md` | Inbox + Expo Push |
| `docs/whatsapp-business-api.md` | WhatsApp Meta |

**PRD Obsidian:** `obsidian/projetos/cortejo-prd.md` · padrões cross-projeto: `obsidian/fabrica/`

---

## 6. Fluxos detalhados

### 6.0 Cadastro de clientes (dono / equipe)

> Detalhe: [[../fabrica/cadastro-clientes-salao-expo]] · repo `docs/cadastro-clientes-salao.md`

1. **Mais → Clientes** (`app/config/clientes.tsx`).
2. Listar, buscar (nome/WhatsApp), cadastrar e editar.
3. Campos: nome, sobrenome, WhatsApp, data nascimento (DD/MM/AAAA na UI → ISO no Firestore), observações.
4. Serviço: `services/clients.ts` — payload único (`celular` normalizado + `phone` mascarado).
5. Mesmos campos usados no agendamento interno e no **link público** (lookup por celular ou nascimento).

---

### 6.1 Onboarding & Auth

1. Splash → checa sessão Firebase.
2. Sem sessão → `login` (Google ou email/senha).
3. Primeiro acesso → `onboarding`: nome do salão, logo (upload Storage), telefone, horário de funcionamento.
4. Cria `salons/{salonId}` + `members/{uid}` role `owner` + plano `free`.
5. Redireciona para Agenda.

### 6.2 Agendamento (núcleo)

> **Padrão reutilizável (Obsidian):** [[../fabrica/agenda-salao-expo-padrao]] — layout aba Agenda, slots 30 min, `businessHours`, cadastro salão LashMatch, checklist para outros projetos Expo.

**Criar (interno):**
1. Tap no "+" na Agenda ou em um slot livre.
2. Seleciona cliente (busca ou cadastra na hora) → serviço(s) → profissional → data/hora.
3. Sistema calcula `end` somando `durationMin`, valida conflito de horário do profissional.
4. Salva `appointment` status `scheduled`, `priceTotal` somado.
5. Agenda lembrete WhatsApp (Cloud Function scheduled).

**Agendamento público (web Hosting):**
1. Cliente abre link `https://cortejo-app.web.app/agendar?salon={salonId}`.
2. Identificação: WhatsApp → confirma identidade → ou data nascimento (ver `publicClientLookup`).
3. Se já tem agendamentos futuros: lista + botão **+ Novo agendamento** (`publicClientAppointments`).
4. Escolhe serviço → profissional → data/horário; aviso se novo horário &lt; 7 dias de outro agendamento (reagendar ou criar novo).
5. Produção web: `public/booking.html` → `dist/agendar/index.html` (ver `docs/padroes-agendamento-web.md`).
6. Function cria `appointment` `source:"public"`; dono recebe inbox + push; cliente WhatsApp confirmação.

**Estados:** scheduled → confirmed → done (gera venda opcional) | canceled | no_show.
Mudança de status muda cor do card (tokens de status).

**Lembrete WhatsApp:** Function diária roda 1x/h, busca appointments nas próximas 24h sem `reminderSentAt`, envia template Meta (UTILITY) e marca `reminderSentAt`.

### 6.3 Estoque
1. Cadastro de produto (nome, SKU, custo, venda, unidade, estoque inicial, mínimo, foto).
2. Entrada: registra `stockMovement type:"in"`, soma `stockQty`.
3. Saída manual / ajuste: movimento correspondente com motivo.
4. Venda de produto → movimento `type:"sale"` automático (debita estoque).
5. **Alerta:** quando `stockQty <= stockMin` → badge `warning` na lista + card na home.
6. Histórico de movimentos por produto.

### 6.4 Vendas / PDV
1. Nova venda → adiciona itens (serviço e/ou produto) ao carrinho.
2. Vincula cliente e profissional (para comissão).
3. Aplica desconto (valor ou %), calcula total.
4. Seleciona forma de pagamento (cash/pix/credit/debit, parcelas).
5. Finaliza → `sale` status `paid`, gera `financeEntry` income, debita estoque dos produtos, atualiza `totalSpent` do cliente.
6. Recibo na tela (compartilhável). Se vier de um appointment, marca este como `done`.

### 6.5 Financeiro
1. **Caixa diário:** abrir caixa (valor inicial) → registra vendas → fechar caixa (confere esperado x informado, calcula diferença).
2. **Contas a pagar/receber:** lançamentos manuais com vencimento; status vira `overdue` automático (Function diária).
3. **Comissões:** por profissional, calcula `% sobre serviços` no período.
4. **Relatórios:** faturamento por período, ticket médio, top serviços, top produtos, comparativo mês a mês. Gráficos com tokens da paleta.

### 6.6 Assinatura (Mercado Pago)
1. Tela `plano`: mostra Free vs Pro, preço mensal/anual.
2. Cria `preapproval` (assinatura recorrente) via Function MP.
3. Webhook MP → atualiza `salons.subscription.status` e `plan`.
4. Gating: features Pro (estoque/PDV/financeiro/multi-prof) bloqueadas no plano free com paywall.

---

## 7. Cloud Functions (functions/SRC/)

| Function | Trigger | Faz |
|----------|---------|-----|
| `publicBooking` | HTTPS | Cria agendamento público; suporta `clientId`, reagendamento (`rescheduleAppointmentId`) |
| `publicClientLookup` | HTTPS | Identifica cliente por celular ou data nascimento |
| `publicClientAppointments` | HTTPS | Lista agendamentos futuros da cliente (pós-identificação) |
| `availableSlots` | HTTPS | Meta do salão + slots livres por profissional/dia |
| `notificarDonoAgendamentoPublico` | Firestore onCreate appointment | Inbox + Expo Push ao dono |
| `enviarConfirmacaoAgendamento` | Firestore onCreate | WhatsApp confirmação (Meta) |
| `enviarLembretesAgendamento` | Scheduled | Lembrete WhatsApp 24h antes (Z-API ou Meta) |
| `onSalePaid` | Firestore onCreate sale paid | Gera financeEntry + debita estoque |
| `markOverdue` | Scheduled (daily) | Atualiza financeEntries vencidas |
| `mpWebhook` | HTTPS | Recebe eventos Mercado Pago, atualiza assinatura |
| `mpCreatePreapproval` | HTTPS callable | Inicia assinatura |
| `onAppointmentDone` | Firestore onUpdate | Atualiza lastVisitAt do cliente |

---

## 8. Pendências de credenciais (Gustavo fornece)
- Firebase project (Blaze) + `google-services` / `GoogleService-Info`.
- Meta WABA + token System User + template UTILITY aprovado.
- Mercado Pago access token + plano de assinatura.
- EAS project criado + slug `cortejo.app` (Hosting).

---

## 9. Ordem de construção (a IA segue esta sequência)
1. Setup projeto (Expo + TS + Expo Router + Firebase config + tokens + componentes UI base).
2. Auth + Onboarding (criar salão).
3. Cadastros base: serviços, equipe, **clientes** (`config/clientes` + `services/clients.ts`).
4. **Agenda** (criar/editar/estados) — entregar e validar no device.
5. Estoque (produtos + movimentos + alertas).
6. PDV (vendas + recibo).
7. Financeiro (caixa + lançamentos + relatórios).
8. Agendamento público (Hosting) + lembrete WhatsApp.
9. Assinatura Mercado Pago + gating de plano.
10. QA, regras Firestore, polish visual, EAS build.

Cada etapa: branch `feature/<nome>` → código → PR (`publicar_funcionalidade`) → revisão → `salvar_decisao` no Obsidian. Erros corrigidos → `registrar_erro_solucao`.

---

## 10. Critérios de qualidade (definição de pronto)
- Zero cores fora dos tokens; todos os textos usam a escala tipográfica.
- Estados vazios, loading e erro tratados em toda lista.
- Toda mutação otimista com rollback (React Query).
- Sem `any` solto; tipos das entidades em `types/`.
- Telas testadas no Expo Go (iOS + Android) antes do merge.
- Regras Firestore impedem acesso cross-tenant.

---

*Cortejo · React Native (Expo) + Firebase · Fábrica de Apps com IA · Autor: Gustavo*
