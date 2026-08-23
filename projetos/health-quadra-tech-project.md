---
projeto: Health Quadra Tech
produto: Trajeto
tipo: referencia-tecnica
stack: Expo (Expo Go) + Next.js (Vercel) + Supabase
**Supabase:** projeto `trajeto` · org shoutloud · ref `fzttsuuzfauqkagscrwc` · região `sa-east-1` (São Paulo) · URL `https://fzttsuuzfauqkagscrwc.supabase.co`  
(Arquivo Oregon `slaexnytybmgphknwbat` não é mais o backend do app.)  
**Vercel:** `shoutloud/health-quadra-tech` · `prj_iFLoaS9YVo87wCyXGZMLfS8QFONd`
vercel: shoutloud/health-quadra-tech
repo: C:/Users/gusta/projetosShout/health-quadra-tech
github: Shoutloud-web/health-quadra-tech
atualizado_em: 2026-08-20
links:
  - "[[health-quadra-tech-prd]]"
  - "[[../fabrica/health-quadra-tech-schemas]]"
---

# Trajeto — PROJECT (Health Quadra Tech)

> **Fonte de verdade:** esta nota + PRD **[[health-quadra-tech-prd]]**.  
> Clone: `C:/Users/gusta/projetosShout/health-quadra-tech`

## 1) Visão

**Trajeto** — plataforma de gestão para psicólogos e clínicas, com acompanhamento clínico e quiz de triagem. Empresa/repo: Health Quadra Tech.

### Stack

| Camada | Tecnologia | Pasta |
|--------|------------|-------|
| Web | Next.js App Router → Vercel | `apps/web` |
| App | Expo **SDK 54** + Expo Router ~6 (Expo Go da loja) | `apps/mobile` |
| Tokens/tipos | pacote compartilhado | `packages/shared` |
| Backend | Supabase | `supabase/` |
| Estilo | tokens sage/gold (mockups), **não** LashMatch |

**Não usar Firebase.**

## 2) Paleta (mockups Trajeto)

- Fundo: `#EEF1EC` · superfície: `#FFFFFF` · superfície quente: `#F6F2E9`
- Ink: `#1E332F` · ink soft: `#57685F` · ink faint: `#8A968E` · linha: `#DCE3DC`
- Gold: `#B8874B` · sage: `#6E8F73` · rust: `#B65B3F` · plum: `#7C6A8C`
- Display: Petrona · UI: Inter · números: IBM Plex Mono
- Ícones: SVGs do `docs/mockups` (stroke 1.6) em `apps/web/components/Icon.tsx` e `apps/mobile/components/Icon.tsx` — não FontAwesome/LashMatch

## 3) Telas e rotas

### Web (`apps/web`) — Auth Supabase + dados reais + **← Voltar** em todas as telas

| Rota | Papel | Dados |
|------|-------|--------|
| `/login` | todos | `signIn` / `signUp` — escolha **obrigatória** autônomo (`psicologo`) vs clínica (`gestor`); metadata `trajeto_role`; RPC `bootstrap_workspace` |
| `/auth/callback` | confirmação de e-mail | troca `code`/`token_hash` e chama `finishSignup` |
| `/clinica` | gestor | `professionals` + `professional_kpis` · **Exportar relatório** |
| `/clinica/agenda` | gestor | agenda consolidada de todos os profissionais (só horário) |
| `/clinica/profissionais` | gestor | lista à esquerda; card **Adicionar novo profissional** (nome, CRP, papel Psicólogo/Gestor) + convite (`invite_token` + `invite_role` → `/equipe/cadastro?token=`) |
| `/clinica/pacientes` | gestor | carteira da casa: após o convite aceito mostra CPF, convênio, nascimento, motivo · **Enviar quiz novamente** |
| `/clinica/pacientes/[id]` | gestor | cadastro operacional (sem SOAP) · **WhatsApp** (templates + quiz automático) |
| `/clinica/financeiro` | gestor | painel: saldo, entrada/saída (sage/ouro), filtros Dia–Ano + intervalo **valendo no extrato**, ranking por psicólogo |
| `/clinica/relatorio` | gestor | KPIs + equipe + totais de `invoices` (sem SOAP) · Imprimir/PDF |
| `/equipe/cadastro` | psicólogo ou gestor convidado | RPC `claim_professional_invite` — `profiles.role` vem de `invite_role` |
| `/psico` | psicólogo **ou gestor que atende** | `appointments` do dia + notas SOAP recentes (`sessions`) |
| `/psico/agenda` | clínico | **Desktop (≥1100px):** semana de trabalho (seg–sex) estilo Teams. **Celular/tablet:** Dia / Mês. Clique no horário → **Entrar na consulta** (Jitsi `call.jordaob.com.br`) se online |
| `/psico/pacientes` | clínico | convite + lista **da própria carteira** + gráfico GAD-7/PHQ-9 (filtro **Todos** ou um paciente) |
| `/psico/pacientes/[id]` | clínico | ficha (CPF, convênio), gráfico, quiz, histórico SOAP · **WhatsApp** · **Enviar quiz novamente** · **Exportar relatório** |
| `/psico/pacientes/[id]/relatorio` | clínico | relatório clínico (ficha + GAD/PHQ + quiz + SOAP) · Imprimir/PDF |
| `/psico/sessoes` | clínico | lista de notas SOAP |
| `/psico/sessoes/nova` | clínico | insert `sessions` + `scale_scores` |
| `/psico/financeiro` | psicólogo / gestor no chapéu clínico | painel próprio (entradas, retenção, gráfico, períodos) + CRUD `invoices` |
| `/p/cadastro` | paciente (link) | RPC `claim_patient_invite` — CPF obrigatório + possui convênio (nome opcional) |
| `/p/quiz` | paciente | `quiz_*` + `pre_charts` · **D3 em hold** até evidência qualitativa (notas polarizadas sem “por quê”) |
| `/p` | paciente | próximas sessões (lista) · **Confirmar / Remarcar** · **Entrar na chamada** (Jitsi no browser) se online |
| `/p/agendar` | paciente | insert `appointments` com modalidade online/presencial |

Middleware: `apps/web/middleware.ts` refresca sessão. Papel só em `profiles`. Após login: `router.replace` para `/clinica` \| `/psico` \| `/p`. Layout `(workspace)`: sidebar **fixa** na borda esquerda (`100dvh`); só o `main` rola à direita — o conteúdo não passa por baixo do menu.

### App (`apps/mobile`) — mesma conta Supabase (AsyncStorage)

Paridade com a web (2026-08-19). EAS Update preview: ainda o grupo SDK 54 em https://expo.dev/accounts/shoutloud/projects/health-quadra-tech/updates/2c51c045-c591-485b-ac6f-dc6e89124fdd — OTA novo bloqueado enquanto a CLI estiver em `gabrieljorda0` (precisa `eas login` na conta **shoutloud**).

- `/login` — entrar / criar conta (psicólogo ou clínica)
- `/cadastro?token=` — convite do paciente (CPF + convênio, igual à web)
- `/cadastro-equipe?token=` — convite da equipe (psicólogo ou gestor, conforme `invite_role`)
- `(clinica)/` — Painel · **Agenda Dia/Mês** · Equipe · Pacientes (cadastro completo após convite + **Enviar quiz novamente**) · Config. **Exportar relatório** no painel → `(clinica)/relatorio`. **Financeiro**. Switch **Clínica | Psicólogo**
- `(patient)/index` · `quiz` · `agendar` — painel com **lista das próximas sessões** (confirmar/remarcar + entrar Jitsi), triagem, calendário + slots com modalidade
- `(psico)/` — Painel · **Agenda Dia/Mês** (`react-native-calendars` + timeline 30 min, toque no slot vazio) · Pacientes · **Ficha & evolução** · **Registrar sessão**. Gestor também entra aqui para atender
- Ficha `paciente/[id]` e evolução: gráfico, quiz com flag, **WhatsApp**, **Exportar relatório** → `(psico)/relatorio?patientId=` (cards + `Share.share`)
- Texto do relatório em `packages/shared/report.ts` (web imprime; app compartilha)
- SOAP: validação lê o texto do campo (ref); após salvar vai para Sessões — não limpa o form deixando “Preencha o subjetivo”
- Toda tela tem **← Voltar** (`BackBar`); painéis têm **Sair**

## 3.1) Contas demo (senha `Trajeto123`)

Seed: `supabase/seed_demo_clientes.sql` (ficha, quiz, SOAP, GAD-7/PHQ-9, agenda de hoje, invoices).

| E-mail | Papel | Casa | O que mostrar |
|--------|-------|------|----------------|
| `marina.autonomo@trajeto.dev` | psicólogo autônomo | Consultório Marina | Carlos e Felipe — evolução caindo, financeiro |
| `clara.clinica@trajeto.dev` | gestor (dois chapéus) | Clínica Vértice | Painel da casa + Beatriz no chapéu Psicólogo |
| `pedro.equipe@trajeto.dev` | psicólogo da equipe | Clínica Vértice | Ana (melhora), João (alerta no quiz), Renata |
| `ana.paciente@trajeto.dev` | paciente da Ana Prado | Clínica Vértice | quiz / agendar |

Não resetar as contas pessoais Jordao.

## 4) Schema

Ver **[[../fabrica/health-quadra-tech-schemas]]**

## 5) Multi-tenant e sigilo

- Tenant = `clinics`.
- Papel em `profiles.role` (`gestor` \| `psicologo` \| `paciente`) — **nunca** `user_metadata` para RLS.
- Helpers `current_*` são SECURITY DEFINER (senão SELECT em `profiles` dá 500 e o login volta para a mesma tela).
- **Dois chapéus:** gestor tem linha em `professionals` (bootstrap + `ensure_gestor_professional`) e acessa `/psico` só da **própria** carteira. Autônomo não vê equipe.
- Psicólogo da clínica entra por convite (`professionals.invite_token` + `invite_role` + `claim_professional_invite`) — não cria clínica nova. Convite de **Gestor** cria `profiles.role = gestor`.
- Psicólogo: só pacientes vinculados a `current_professional_id()`.
- Gestor: KPIs, agenda consolidada e financeiro da clínica; **sem** SELECT em notas SOAP / respostas do quiz de outros.
- Paciente: só o próprio registro, agendamentos e scores (não notas clínicas).

## 6) Deploy

1. Web: Vercel root directory = `apps/web` + `sourceFilesOutsideRootDirectory` (projeto `shoutloud/health-quadra-tech`).
   - Produção: https://health-quadra-tech-shoutloud.vercel.app
   - Último `--prod` READY em 2026-08-20 (`dpl_4Zw7yroz3jFTuqrueXUpm3vc7AoD`) — Jitsi em `call.jordaob.com.br`. Alias: https://health-quadra-tech-shoutloud.vercel.app
   - `apps/web` usa **react/react-dom 19.1.0** (override do monorepo). Não deixar `apps/web/node_modules/react@19.2.8` no lockfile — dual React quebra prerender (`useContext` null em `/_not-found`). Não aliasar `react` no webpack (quebra RSC).
   - Env: `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_ANON_KEY` + `NEXT_PUBLIC_SITE_URL=https://health-quadra-tech-shoutloud.vercel.app`
2. Edge Functions: `trajeto-notify` (JWT) e `trajeto-cron` (Bearer `CRON_SECRET`). Teleconsulta **Jitsi próprio** (`https://call.jordaob.com.br`, VPS Vultr SP) no **browser** (Expo Go). `trajeto-notify` v5 (2026-08-20): padrão `VIDEO_PROVIDER=jitsi` + `JITSI_BASE_URL=https://call.jordaob.com.br`. Daily só se `VIDEO_PROVIDER=daily`. Secrets: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `SITE_URL`, `CRON_SECRET` (+ Daily se rollback). WhatsApp: portfólio **Gerenciador S** `3566050263560437` · WABA `1012313901775778` · PHONE_ID `1347928901727664` (`+55 19 95873-1436`). Templates UTILITY `pt_BR` criados em 2026-08-20 (PENDING): `trajeto_sessao_confirmada`, `trajeto_lembrete_sessao`, `trajeto_quiz_triagem`. O teste `lembrete_agendamento` **não** é usado pelo app. Fallback `wa.me` até APPROVED. `patients.phone` é **obrigatório** (WhatsApp com DDD).
3. Supabase Auth (dashboard, MCP não altera):
   - Site URL: `https://health-quadra-tech-shoutloud.vercel.app`
   - Redirect URLs: `https://health-quadra-tech-shoutloud.vercel.app/**`, `http://localhost:3000/**`, `https://*-shoutloud.vercel.app/**`
   - Nome **Supabase Auth** no remetente só muda com SMTP próprio (Resend).
4. App: `cd apps/mobile` → `.env` com `EXPO_PUBLIC_SUPABASE_*` → `npx expo start` → QR / link `exp://` do **Metro** no Expo Go da loja (igual Cortejo/LashMatch).
   - SDK **54** (`expo-router` **~6.x**, não ~54). Overrides no `package.json` da raiz travam `expo`/`react-native` no 54 para o monorepo não puxar 57.
   - `react-refresh` ^0.14.2 é dependência **explícita** de `@trajeto/mobile` (peer do `babel-preset-expo`). Sem hoist na raiz o Metro quebra: `Cannot find module 'react-refresh/babel'`.
   - App importa `@trajeto/shared/...` (igual à web). **Não** usar `../../../packages/shared` nas rotas do Expo Router — de `app/(patient)` isso aponta para `apps/packages/` e o Metro falha.
   - Preview EAS (igual Cortejo): `eas update --branch preview`. Último grupo SDK 54: https://expo.dev/accounts/shoutloud/projects/health-quadra-tech/updates/2c51c045-c591-485b-ac6f-dc6e89124fdd — abrir no Expo Go **logado na conta shoutloud**.
   - Link Metro (PC ligado): `npm run start:share` → `exp://…`. Não usar update antigo de SDK 57.

## RAG

Antes de codar: MCP `rag_buscar` + `buscar_historico`. Depois: esta nota + PRD + schemas + `indexar_rapido.py`.
