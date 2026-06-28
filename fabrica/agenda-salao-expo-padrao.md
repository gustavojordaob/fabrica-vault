---
tags:
  - agenda
  - agendamento
  - salao
  - expo
  - react-native-calendars
  - cortejo
  - lashmatch
fonte: implementação Cortejo (jun/2026)
referencia_repo: cortejo
atualizado_em: 2026-06-09
links:
  - "[[react-native-calendars]]"
  - "[[lashmatch-schemas]]"
  - "[[whatsapp-business-api]]"
  - "[[rag-protocolo-antes-de-codar]]"
  - "[[../projetos/cortejo-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("agenda salao expo timeSlots businessHours")`
> 2. MCP **fabrica-apps** — `buscar_historico("agenda calendario cortejo")`
> 3. Ler **[[react-native-calendars]]** (componente e tema)
> 4. Ler **[[rag-protocolo-antes-de-codar]]** (nunca implementar calendário às cegas)
>
> **Referência de código:** repo `cortejo` — branch main, pasta `components/agenda/`, `utils/timeSlots.ts`, `app/(tabs)/index.tsx`.

---

# Agenda de salão — padrão Expo (Cortejo / LashMatch)

Padrão reutilizável para apps de **salão de beleza** com:
- aba Agenda (calendário + dia + lista)
- fluxo **Novo agendamento** (cliente → serviço → profissional → data → horários)
- slots **30 em 30 min** respeitando duração do serviço, profissional e horário do salão
- cadastro/perfil do salão com campos LashMatch (telefone, endereço ViaCEP)

---

## Quando usar

| Cenário | Use este padrão |
|---------|-----------------|
| App de salão / clínica / barbearia com agenda | ✅ |
| Multi-profissional + serviços com duração | ✅ |
| Link público de agendamento | ✅ (mesma lógica de slots na Cloud Function) |
| App sem calendário (só lista) | ❌ — usar FlatList simples |

---

## 1. Layout da aba Agenda (UI)

### Estrutura visual (não usar faixa branca solta)

Um **único card** (`agendaBlock`) contém:
1. Calendário compacto (`AgendaCalendar` com `compact` + `embedded`)
2. Barra do dia (`dayBar`): data formatada pt-BR + chip **+ Novo** (primary)
3. Abaixo do card: lista `FlatList` com `flex: 1` (fundo `colors.bg`)

```tsx
<SafeAreaView style={{ flex: 1, backgroundColor: colors.bg }}>
  <View style={styles.agendaBlock}>
    <AgendaCalendar compact embedded ... />
    <View style={styles.dayBar}>
      <Text>{selectedLabel}</Text>
      <Pressable style={styles.addChip}>+ Novo</Pressable>
    </View>
  </View>
  <View style={{ flex: 1, minHeight: 0 }}>
    <FlatList style={{ flex: 1 }} ... />
  </View>
  <FAB + /> {/* opcional, duplicata do chip Novo */}
</SafeAreaView>
```

### Estilos do card (tokens do projeto)

```typescript
agendaBlock: {
  marginHorizontal: spacing.lg,
  backgroundColor: colors.surface,
  borderRadius: radius.lg,
  borderWidth: 1,
  borderColor: colors.border,
  overflow: 'hidden',
  ...shadow.card,
},
dayBar: {
  flexDirection: 'row',
  alignItems: 'center',
  paddingHorizontal: spacing.lg,
  paddingVertical: spacing.md,
  borderTopWidth: 1,
  borderTopColor: colors.border,
},
```

### Calendário compacto

| Prop | Valor recomendado |
|------|-------------------|
| `calendarHeight` | `218` (aba principal) |
| `hideExtraDays` | `true` |
| `firstDay` | `0` (domingo) ou `1` (segunda BR) |
| `markingType` | `multi-dot` (status por cor) |
| `embedded` | remove borda/sombra própria — card pai unifica |

Arquivos Cortejo: `components/agenda/AgendaCalendar.tsx`, `calendarLocale.ts` (pt-BR).

---

## 2. Lógica de horários (LashMatch)

### Regras

1. **Intervalo base:** 30 minutos (`SLOT_STEP_MIN = 30`)
2. **Duração:** cada slot só aparece se `início + durationMin ≤ fechamento`
3. **Profissional:** conflito só com agendamentos **dele** (`professionalUid`), status `scheduled` | `confirmed`
4. **Horário do salão:** `members/{uid}.businessHours` (por profissional); fallback `salon.businessHours` — `resolveBusinessHours()` · tela `config/horarios`
5. **Bloqueios:** `salon.blockedPeriods` — salão inteiro ou por `professionalUid`; dia inteiro ou `startTime`/`endTime` — ver §9
6. **Hoje:** horários no passado indisponíveis
7. **Antes de salvar:** `checkConflict()` no Firestore (mesma regra de overlap)

### Código app (client)

`utils/businessHours.ts` — `getOpenRangesOrDefault(day, businessHours)`

`utils/timeSlots.ts` — `generateTimeSlots({ ..., businessHours, blockedPeriods, professionalUid })` — usa `slotOverlapsBlocked`

`utils/blockedPeriodsLogic.ts` — bloqueio por profissional e intervalo horário

### Código servidor (link público)

`functions/SRC/slotLogic.ts` — `generateAvailableSlots()` (espelho sem dependências RN)

Cloud Function `availableSlots` — query params: `salonId`, `serviceId`, `professionalUid`, `date` (YYYY-MM-DD)

---

## 3. Fluxo Novo agendamento

Rota: `/agendamento/novo?date=YYYY-MM-DD` (Expo: `id=novo` + param `date`)

Ordem das seções:
1. **Cliente** — busca no topo (`filterClientsByQuery`), lista limitada (8 sem busca / 20 com busca), card “Cliente selecionada”, ou formulário nova cliente
2. Serviço (chip com duração e preço) + Profissional (membros `active`)
3. Calendário (`embedded`, `minDate=hoje`)
4. Grid de horários (`TimeSlotGrid` — só slots `available`)
5. Resumo + Confirmar

Ao mudar serviço/profissional/data → limpar horário selecionado.

Persistir: `start`, `end` (start + durationMin), `clientPhone` desnormalizado (WhatsApp).

### Link público (web — Firebase Hosting)

Rota: `/agendar?salon={salonId}` — `app/agendar/index.tsx` (Expo Router, export estático)

Fluxo em 3 passos:
1. Serviço → 2. Profissional → 3. **Calendário compacto** (`AgendaCalendar` + `embedded`) + `TimeSlotGrid` + nome/WhatsApp

- Slots via `availableSlots` (mesma CF do app) — recarrega ao mudar a data no calendário
- `meta=1` retorna também `salonName` e `blockedPeriods` para marcar dias bloqueados
- **Web:** conteúdo centralizado `maxWidth: 520`, `AgendaCalendar` com `width: '100%'` (`Platform.OS === 'web'`)
- Antes de deploy web: `npx expo export --platform web` + `firebase deploy --only hosting`

---

## 4. Cadastro / perfil do salão (paridade LashMatch)

Formulário reutilizável: `components/forms/SalonProfileForm.tsx`

| Campo | Firestore Cortejo |
|-------|-------------------|
| Nome / Sobrenome | `members/{uid}.firstName`, `lastName`, `displayName` |
| Nome do salão | `salons/{id}.name` |
| Telefone WhatsApp | `salons/{id}.phone` |
| CEP → ViaCEP | `cep`, `logradouro`, `bairro`, `cidade`, `estado` |
| Número / complemento | `numero`, `complemento` |
| Endereço linha única | `address` (derivado — templates WhatsApp var endereço) |

Utils: `utils/address.ts` (`formatCep`, `fetchAddressByCep`, `buildAddressLine`)

Telas: `app/(auth)/onboarding.tsx` (criação), `app/config/conta.tsx` (edição)

---

## 5. Schema Firestore (Cortejo)

```
artifacts/cortejo/salons/{salonId}
  - name, phone, address, cep, logradouro, numero, complemento, bairro, cidade, estado
  - businessHours: { mon: [{ start, end }], ... }  ← fallback legado
  - blockedPeriods: [{ id, startDate, endDate, label?, professionalUid?, startTime?, endTime? }]

  /members/{uid}
    - businessHours: { mon: [{ start, end }], ... }  ← horário por profissional (preferencial)
  /services/{id}  → durationMin, price, active
  /clients/{id}
  /appointments/{id}
    - clientId, clientName, clientPhone
    - professionalUid, professionalName
    - serviceIds[], serviceNames[]
    - start, end (Timestamp)
    - status: scheduled | confirmed | done | canceled | no_show
```

LashMatch usa `usuarios/{uid}` + subcoleções — ver **[[lashmatch-schemas]]** para mapear campos.

---

## 6. Arquivos de referência (Cortejo)

| Arquivo | Responsabilidade |
|---------|------------------|
| `app/(tabs)/index.tsx` | Aba Agenda (layout agendaBlock + lista) |
| `app/agendamento/[id].tsx` | Criar / ver agendamento |
| `components/agenda/AgendaCalendar.tsx` | Calendário temático |
| `components/agenda/AppointmentCard.tsx` | Card na lista do dia |
| `components/agenda/TimeSlotGrid.tsx` | Grid de horários |
| `utils/appointmentCalendar.ts` | `markedDates`, bloqueios |
| `utils/timeSlots.ts` | Geração de slots |
| `utils/businessHours.ts` | Faixas por dia da semana |
| `components/forms/SalonProfileForm.tsx` | Cadastro/perfil salão |
| `functions/SRC/slotLogic.ts` | Slots API pública |
| `app/config/clientes.tsx` | CRUD clientes (dono) |
| `services/clients.ts` | Payload normalizado clients |
| `app/config/horarios.tsx` | Horário **por profissional** |
| `app/config/bloqueios.tsx` | Bloqueios (salão / profissional / horário) |
| `services/blockedPeriods.ts` | CRUD blockedPeriods |
| `utils/client.ts` | `filterClientsByQuery`, `getClientPhoneDisplay` |
| `docs/` no repo | **Atalhos** → notas em `obsidian/fabrica/` |

Schema detalhado: **[[cortejo-schemas]]**

---

## 9. Bloqueios, horários por profissional e busca de clientes (jun/2026)

### Bloqueios (`app/config/bloqueios`)

- Salão inteiro ou `professionalUid` específico
- Dia inteiro ou intervalo `startTime`–`endTime` (HH:mm)
- **Erro comum:** `arrayUnion` com `undefined` — omitir campos opcionais vazios

### Horários (`app/config/horarios`)

- Salva em `members/{uid}.businessHours`
- Novo profissional herda `salon.businessHours` em `createSalonMember`

### Busca de cliente (`app/agendamento/[id].tsx`)

- Campo busca no topo da seção Cliente
- Preview 8 / busca até 20 resultados
- Utils: `filterClientsByQuery` em `utils/client.ts`

### Deploy após mudar slots/bloqueio

```powershell
npx firebase-tools deploy --only "functions:availableSlots,functions:publicBooking" --project cortejo-app
```

---

## 7. Checklist — agente ao implementar em projeto novo

- [ ] `npx expo install react-native-calendars`
- [ ] Consultar RAG: este doc + `react-native-calendars.md` + `[[cortejo-schemas]]`
- [ ] `LocaleConfig` pt-BR antes do calendário
- [ ] Card único calendário + dayBar (sem faixa full-width solta)
- [ ] Lista do dia com `flex: 1` + `minHeight: 0`
- [ ] `generateTimeSlots` com `businessHours` do **profissional** + `blockedPeriods`
- [ ] Cloud Function espelhando slots para booking público
- [ ] `clientPhone` no agendamento (WhatsApp)
- [ ] Deploy `functions:availableSlots` se alterou slotLogic
- [ ] Documentar em `obsidian/projetos/<nome>-project.md` e `obsidian/fabrica/`
- [ ] `salvar_decisao` + `indexar_rapido.py` ao concluir

---

## 8. Adaptar para outro visual

Trocar apenas `theme/tokens.ts` e `calendarTheme` em `calendarLocale.ts` — **não** copiar cores LashMatch (`#D63384` / fundo preto) em apps claros como Cortejo.

---

## 9. Bloqueios, horários por profissional e busca de clientes (jun/2026)

### Bloqueios (`app/config/bloqueios`)

- Salão inteiro ou `professionalUid` específico
- Dia inteiro ou intervalo `startTime`–`endTime` (HH:mm)
- **Erro comum:** `arrayUnion` com `undefined` — omitir campos opcionais vazios

### Horários (`app/config/horarios`)

- Salva em `members/{uid}.businessHours`
- Novo profissional herda `salon.businessHours` em `createSalonMember`

### Busca de cliente (`app/agendamento/[id].tsx`)

- Campo busca no topo da seção Cliente
- Preview 8 / busca até 20 resultados
- Utils: `filterClientsByQuery` em `utils/client.ts`

### Deploy após mudar slots/bloqueio

```powershell
npx firebase-tools deploy --only "functions:availableSlots,functions:publicBooking" --project cortejo-app
```

---

*Origem: sessão Cortejo jun/2026 — agenda, slots, bloqueios, horário por profissional, busca cliente.*
