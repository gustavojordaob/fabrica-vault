# Cadastro de clientes — padrão Expo + Firestore (salão)

> Fonte canônica no repo: `cortejo/docs/cadastro-clientes-salao.md`  
> PRD do app: [[../projetos/cortejo-prd]]  
> Relacionado: [[agenda-salao-expo-padrao]], [[firebase-setup-patterns]]

## Resumo

Módulo para o **dono/equipe** cadastrar clientes no app, alinhado ao **agendamento público** (lookup por WhatsApp ou data de nascimento).

**Path Cortejo:** `artifacts/cortejo/salons/{salonId}/clients/{id}`

**Campos obrigatórios:** `nome`, `sobrenome`, `name`, `celular` (5511...), `phone` ((11)...), `dataNascimento` (YYYY-MM-DD)

## Stack

- `services/clients.ts` — list / create / update
- `app/config/clientes.tsx` — FlatList + FormModalSheet + busca
- `utils/client.ts` — normalizeCelularBR, birthDateBRToISO, getClientFullName
- Cloud Functions: `publicClientLookup`, `publicBooking`, `publicClientAppointments`

## Checklist agente

1. Schema + regras Firestore (`isMember` read/write clients)
2. Utils BR (celular + nascimento)
3. Tela config + link no menu Mais
4. Mesmo payload no agendamento interno e link público
5. Deploy rules se mudou; indexes se query appointments por clientId

## Anti-padrões

- Só `name` sem nome/sobrenome
- Só `phone` sem `celular` normalizado
- Nascimento DD/MM/AAAA no Firestore
- Lookup público direto no client (usar Functions)

Ver doc completo no repositório Cortejo.
