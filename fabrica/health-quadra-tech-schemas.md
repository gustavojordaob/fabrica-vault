---
projeto: Health Quadra Tech
produto: Trajeto
tipo: schema-supabase
stack: Supabase Postgres
repo: C:/Users/gusta/projetosShout/health-quadra-tech
atualizado_em: 2026-08-20
links:
  - "[[../projetos/health-quadra-tech-project]]"
  - "[[../projetos/health-quadra-tech-prd]]"
---

# Trajeto — Schemas (Supabase / Postgres)

> **Agente Cursor:** MCP `rag_buscar("trajeto schema supabase clinica psicologo")` + `buscar_historico`.  
> Papel **nunca** em `user_metadata` (editável pelo cliente). Usar `profiles` + `auth.jwt() -> app_metadata` só se sincronizado por trigger.

## Status

Projeto hospedado: `trajeto` (`fzttsuuzfauqkagscrwc`, `sa-east-1`). Migrations no repo, aplicadas neste projeto:

- `20260814120000_trajeto_core.sql`
- `20260814130000_profiles_insert.sql`
- `20260814140000_auth_bootstrap.sql`
- `20260814150000_fix_profile_rls_recursion.sql`
- `20260819180000_patient_cpf_convenio.sql`
- `20260819190000_patient_quiz_request.sql`
- `20260819210000_messaging_daily_quiz_schedule.sql`
- `20260819220000_patient_phone_required.sql`

## Multi-tenant

`clinic_id` em quase todas as tabelas. Helper `public.current_clinic_id()` / `public.current_role()` via `profiles`.

## Tabelas

| Tabela | Função |
|--------|--------|
| `clinics` | Tenant (consultório autônomo = clínica de 1 profissional) |
| `profiles` | 1:1 `auth.users` — `role`, `clinic_id`, nome |
| `professionals` | CRP, ativo, % repasse, `user_id` (login), `invite_token`, `invite_role` (`psicologo` \| `gestor`) |
| `patients` | Vínculo clínica + psicólogo responsável; `user_id` após cadastro; `invite_token`; **`phone` NOT NULL** (WhatsApp com DDD); CPF, `has_convenio`, `convenio_name`; `quiz_requested_at` (pedido de novo quiz) |
| `fee_schedules` | Convênio / tipo × valor |
| `appointments` | Agenda; `starts_at`/`ends_at`; status; `modality` (`online` \| `presencial`); `video_room_name` / `video_join_url` (Jitsi `https://call.jordaob.com.br/trajeto-<uuid>`); `whatsapp_confirmed_at` / `whatsapp_reminded_at` |
| `quiz_schedules` | Cadência de reenvio do quiz (MBC lite): `off` \| `weekly` \| `biweekly` \| `monthly`; 1 linha por paciente; RLS psicólogo da carteira / gestor |
| `sessions` | Nota SOAP; **RLS só psicólogo responsável** |
| `scale_scores` | GAD-7, PHQ-9 ao longo do tempo (D1) |
| `quiz_templates` / `quiz_questions` | Instrumento de triagem |
| `quiz_responses` / `quiz_answers` | Respostas do paciente |
| `pre_charts` | Pré-ficha gerada + flags |
| `invoices` | Recebimentos / inadimplência — painel financeiro agrega no client (`packages/shared/finance.ts`) por `paid_at`/`due_date` + `professionals.payout_percent` |
| `payouts` | Repasse persistido (schema/RLS prontos; o painel atual calcula o recorte na hora) |
| `attachments` | Metadados; arquivo no Storage |
| `audit_logs` | Quem leu/alterou dado clínico |

## RLS (resumo)

| Tabela | paciente | psicólogo | gestor |
|--------|----------|-----------|--------|
| patients | próprio | os seus | todos da clínica |
| appointments | os seus | os seus | todos da clínica |
| sessions / quiz_answers | **não** | os seus | **não** |
| scale_scores | os seus (leitura) | os seus | agregados via view `professional_kpis` |
| professional_kpis (view security_invoker) | não | próprio | todos da clínica |
| invoices / payouts | não | próprio (psico) | todos |
| quiz_schedules | **não** | os seus | todos da clínica |

DELETE (20260814160000): `invoices`, `patients`, `appointments`, `sessions`. `fee_schedules` e `professionals` já tinham `FOR ALL` para o papel certo. FK `invoices.professional_id` e `patients.professional_id` = `ON DELETE SET NULL`.

Datas na UI: sempre `dd/mm/aaaa` (locale `pt-BR`). Campos obrigatórios mostram erro visível no campo após tentar enviar (`noValidate` + `FieldError`), sem depender só do `required` nativo.

Views com `security_invoker = true`.

## Storage

Bucket `clinical-attachments` — path `{clinic_id}/{patient_id}/...` · INSERT/SELECT só psicólogo responsável.

## RPCs (auth bootstrap)

| Função | Quem | Faz |
|--------|------|-----|
| `bootstrap_workspace(p_full_name, p_clinic_name, p_role, p_crp)` | `authenticated` | Cria clínica + profile + `professionals` (gestor **e** psicólogo) + taxas padrão |
| `ensure_gestor_professional()` | `authenticated` | Backfill: dono sem linha em `professionals` passa a ter (para atender) |
| `claim_patient_invite(p_token, p_full_name, p_phone, p_birth_date, p_intake, p_cpf, p_has_convenio, p_convenio_name)` | `authenticated` | Liga `auth.uid()` ao `patients.invite_token`; grava CPF (dígitos) e convênio |
| `claim_professional_invite(p_token, p_full_name, p_crp)` | `authenticated` | Liga `auth.uid()` ao `professionals.invite_token`; `profiles.role` = `invite_role` (`psicologo` ou `gestor`) na clínica existente |

Colunas extras: `clinics.hours_note`, `professionals.display_name`, `professionals.invite_token`, `professionals.invite_role`.
View `professional_kpis` faz `LEFT JOIN` em `profiles` (profissional ainda sem login aparece).

Migrations: `20260814120000_trajeto_core.sql`, `20260814130000_profiles_insert.sql`, `20260814140000_auth_bootstrap.sql`, `20260814150000_fix_profile_rls_recursion.sql`, `20260814160000_record_deletes.sql`, `20260815180000_gestor_clinician_and_pro_invite.sql`, `20260815200000_professional_invite_role.sql`, `20260819180000_patient_cpf_convenio.sql`.

Helpers `current_clinic_id()`, `current_role()`, `current_professional_id()` são **SECURITY DEFINER** com `row_security = off`. Se forem INVOKER, a policy de `profiles` entra em recursão (HTTP 500) e o login devolve o usuário para `/login`.

## Auth — confirmação de e-mail

*Atualizado em 14/08/2026*

RLS continua usando só `profiles.role`. `user_metadata` no signup (é permitido) carrega `full_name`, `clinic_name`, `role` pretendido, `invite_token`, **CPF e convênio** para o RPC `bootstrap_workspace` / `claim_patient_invite` **depois** do confirm.

- Callback web: `/auth/callback` (`code` ou `token_hash`).
- `emailRedirectTo` deve estar na allow list do dashboard (Site URL = URL da Vercel, não localhost).
- Remetente "Supabase Auth" = mailer padrão; SMTP próprio para nome Trajeto.


---
