---
projeto: Health Quadra Tech
produto: Trajeto
tipo: prd
stack: Expo SDK 54 (Expo Go) + Next.js (Vercel) + Supabase
repo: C:/Users/gusta/projetosShout/health-quadra-tech
github: Shoutloud-web/health-quadra-tech
atualizado_em: 2026-08-20
links:
  - "[[health-quadra-tech-project]]"
  - "[[../fabrica/health-quadra-tech-schemas]]"
---

# Trajeto — PRD (Health Quadra Tech)

> Produto: **Trajeto** — gestão & cuidado para psicólogos e clínicas.  
> Repo: `health-quadra-tech`. Fontes de UX: mockups + protótipo (Downloads, copiados em `docs/mockups/`).  
> O PRD original era web-only; **app nativo entra desde o dia 1** (pedido do stakeholder).

## Stack (fixa)

| Camada | Tecnologia | Superfície |
|--------|------------|------------|
| Web clínica/psicólogo | **Next.js** App Router → **Vercel** (`apps/web`) | Desktop (sidebar, tabelas, gráfico de evolução) |
| App nativo | **Expo SDK 54** + Expo Router ~6 → **Expo Go** da loja (`apps/mobile`) | Paciente (primário) + psicólogo em campo |
| Backend | **Supabase** (Postgres + Auth + Storage + Edge Functions) | Única fonte de dados |

Não usar Firebase.

## Problema

Gestão do consultório/clínica (agenda, financeiro, equipe) está fragmentada de sistemas tipo iClinic/PsicoManager; acompanhamento clínico e triagem inicial ficam em planilha, papel ou apps de bem-estar. O psicólogo chega na 1ª sessão sem ficha estruturada.

## Público

- **Psicólogo autônomo** — consultório próprio.
- **Gestor de clínica** — múltiplos profissionais, visão consolidada (sem ver prontuário alheio).
- **Paciente** — quiz, agendar, ver evolução simplificada — **no celular**.

## Módulos

| ID | Módulo | Web | App |
|----|--------|-----|-----|
| M1 | Agenda, financeiro, convênios, recibo/NFS-e | Primário | Agenda do dia + confirmação |
| M2 | Prontuário, sessões SOAP, anexos, linha do tempo | Primário | Registrar sessão rápida |
| M3 | Multi-psicólogo, permissões, KPIs de equipe | Só web | — |
| M4 | Painel de evolução (GAD-7 / PHQ-9) | Primário (assinatura) | Versão simplificada do paciente |
| M5 | Quiz de triagem → pré-ficha | Link web também | **Primário no app** |

## Diferenciais

- **D1** Evolução com gráfico real (não só texto).
- **D2** Indicadores de processo entre profissionais (adesão a reavaliação, ocupação) — sem expor conteúdo clínico.
- **D3** Quiz → pré-ficha automática com flags. **HOLD (2026-08-19):** reação polarizada (2× 5/5 e 2× 1–2/5) **sem justificativa**. Não expandir o instrumento até rodada qualitativa com “por quê” em nota ≤ 3. Ver [[../fabrica/trajeto-quiz-triagem-risco-adocao]].
- **D4** Identidade acolhedora (sage/gold/Petrona) — não “prontuário hospitalar”.

## Papéis

| Papel | Web | App nativo |
|-------|-----|------------|
| Paciente | Cadastro/quiz por link (fallback) | Cadastro, quiz, meu painel, agendar |
| Psicólogo | Agenda, pacientes, ficha, sessão, financeiro próprio, **exportar relatório clínico** | Hoje, **agenda Dia/Mês** (calendário + grade), pacientes/ficha, sessões SOAP, financeiro, **compartilhar relatório** |
| Gestor | Painel, agenda da clínica, profissionais + convite, pacientes da casa, config, financeiro, **exportar relatório operacional** (sem SOAP); chapéu Psicólogo para atender | Painel, **agenda Dia/Mês da equipe**, equipe + convite, pacientes, config, **compartilhar relatório**; switch Clínica/Psicólogo |

## Telas (mockups 01–16)

**Gestor:** Painel da clínica · **Financeiro** (saldo, gráfico, períodos, ranking por psicólogo) · **Exportar relatório** (KPIs + equipe + financeiro, sem SOAP) · Agenda da clínica · Profissionais (card **Adicionar novo profissional**: nome, CRP, papel Psicólogo/Gestor, enviar convite) · Pacientes da casa · Configurações · switch Clínica/Psicólogo  
**Psicólogo:** Painel · Agenda (**desktop:** semana de trabalho seg–sex, trilho + grade, inspirado no Teams, paleta Trajeto; **celular:** Dia + Mês) · Pacientes e evolução (gráfico GAD-7/PHQ-9, **Todos** ou um paciente) · Ficha · **Exportar relatório clínico** (ficha + escalas + quiz + SOAP) · **Sessões** (lista SOAP) · Registrar sessão · Financeiro  
**Acesso:** Login (autônomo vs clínica) — no celular o card ocupa a largura toda (não metade). Equipe convidada: `/equipe/cadastro?token=` (papel do convite: psicólogo ou gestor)  
**Paciente:** Cadastro · Quiz (intro / pergunta / conclusão) · Meu painel · Agendar sessão  

## Identidade

Marca **Trajeto** · “Gestão & cuidado”. Cores e tipografia dos mockups (`packages/shared/tokens.ts`). Não usar paleta LashMatch.

## Fora do MVP 1

NFS-e / Receita Saúde, biblioteca ampla de escalas (BDI/EAT), biblioteca de tarefas, contas de supervisão (M8–M11). Recibo PDF nativo entra no MVP 2.

**M7 parcial (2026-08-20):** WhatsApp Cloud API + templates (confirmação, lembrete, quiz) com fallback `wa.me`; teleconsulta **Jitsi** (`call.jordaob.com.br`) no browser (Expo Go); Daily só como rollback. Cadência de reenvio do quiz. Paciente logado vê **as próximas sessões** no painel (`/p` e `(patient)`), com **Entrar na chamada** quando for online. Cadastro, convite e ficha exigem **WhatsApp válido com DDD** (`patients.phone` NOT NULL).

Relatório do MVP: web Imprimir/PDF do navegador; app `Share.share` do texto (Expo Go). App do gestor (painel, equipe, pacientes, financeiro, config, relatório) entrou no mobile em 2026-08-15.

## Objetivos (MVP 1)

1. Auth + clínica + papéis (RLS). **Feito (2026-08-14):** login/cadastro web+app, RPC bootstrap/convite, telas lendo/gravando Postgres, botão Voltar em todas as telas. Confirmação de e-mail: `emailRedirectTo` → `/auth/callback`; Site URL no dashboard precisa ser a URL da Vercel (não localhost). Remetente “Supabase Auth” só muda com SMTP.
2. Paciente no app: convite → cadastro (WhatsApp obrigatório, CPF + se possui convênio) → quiz → pré-ficha no psicólogo. **Feito** (web `/p/*` e mobile `(patient)` / `/cadastro`). Ficha e relatório mostram os mesmos campos.
3. Psicólogo na web: agenda do dia, ficha com gráfico, nota SOAP, escalas, **exportar relatório clínico**. **Feito** (web + app: Hoje, Agenda, Pacientes, Sessões, Financeiro, Relatório). Datas em `dd/mm/aaaa`.
4. Gestor na web e no app: KPIs, profissionais, convênios, pacientes, financeiro e **relatório operacional** (sem SOAP). **Feito.** Dono também atende (chapéu Psicólogo). Convite de login para a equipe. Agenda consolidada da clínica.
5. Financeiro: saldo, entradas/saídas, gráfico, filtros (dia/semana/mês/trimestre/semestre/ano + intervalo) e ranking de rentabilidade por psicólogo (gestor). Sem NFS-e. Lógica em `packages/shared/finance.ts`.
