---
projeto: Health Quadra Tech
produto: Trajeto
tipo: risco-produto
atualizado_em: 2026-08-19
links:
  - "[[../projetos/health-quadra-tech-prd]]"
  - "[[../projetos/health-quadra-tech-project]]"
---

# Trajeto — D3 quiz de triagem: risco de adoção (hold)

> **Agente Cursor:** MCP `rag_buscar("quiz triagem D3 Trajeto risco adoção")` + `buscar_historico`.  
> **Não é backlog.** Não implementar o HTML de exemplo nem estrela 1–5 no produto até a próxima rodada qualitativa.

## O que aconteceu

Teste informal do quiz (D3): **2 notas 5/5** e **2 notas 1/5 e 2/5**. n=4. O formulário **não pediu justificativa**. Sem o “por quê”, a polarização não é acionável — só diz que metade rejeitou o diferencial.

Instrumento correto para a *próxima* rodada (não para o app): `docs/research/quiz-triagem-psicologia.html` (origem: Downloads). Lá a nota 1–5 de facilidade só libera envio se nota ≤ 3 vier com texto. Hint do próprio HTML: *sem isso, uma nota baixa só diz "algo deu errado", não o quê.*

## O que o Trajeto faz hoje (código)

Slug `triagem-inicial`, 5 perguntas em `supabase/migrations/20260814120000_trajeto_core.sql`:

1. Texto aberto — “O que te trouxe até aqui?”
2. Histórico de terapia (3 opções)
3. 1 item estilo GAD-7 (Likert 4 pontos)
4. 1 item estilo PHQ-9 (Likert 4 pontos)
5. Flag PHQ-9 item 9 — “pensamentos de que seria melhor estar morto(a)…” Sim/Não

Fluxo: uma pergunta por tela (`/p/quiz` e `(patient)/quiz`). Flag `Sim` vira `pre_charts.attention_flags`. **Não** há: roteamento de segurança, contato imediato da clínica, matching de profissional, nem nota de facilidade.

O app promete **“cerca de 8 minutos”** para 5 perguntas (~2 min). A web não menciona tempo. Copy inconsistente e inflada.

GAD-7/PHQ-9 de verdade vivem nas sessões (D1). No quiz, `scale_code` em 1 item **não** é a escala — rótulo clínico sem instrumento.

## Job do HTML de exemplo ≠ job do D3 atual

| | Trajeto hoje | HTML anexo |
|--|--|--|
| Promessa | “Para o seu psicólogo te conhecer” (já vinculado pelo convite) | “Encontrar o profissional mais adequado” |
| Tamanho | 5 passos, 8 min no copy do app | 6 perguntas, ~2 min, tudo na mesma página |
| Segurança | Flag numérica na ficha | Alerta + priorizar atendimento, não só agenda |
| UX research | Nenhuma no produto | Estrela 1–5 + **por quê obrigatório se ≤ 3** |

Investir em matching de profissional seria **outro produto**, não polish do D3.

## Hipóteses para as notas baixas (não validadas)

Ordem de plausibilidade, para a próxima entrevista — não para implementar agora:

1. **Pergunta 5 (risco de vida)** sem contenção — linguagem de prontuário, sem o que acontece se a pessoa disser Sim.
2. **Itens GAD/PHQ** soam exame, não acolhimento (choca com D4).
3. **Tempo prometido vs real** (8 min no app).
4. **Uma tela por pergunta** vs visão do todo.
5. Expectativa de **matching** que o convite já resolveu.

As notas 5/5 cabem no mesmo n: quem não bateu na pergunta 5, ou já esperava triagem clínica, avalia o fluxo curto como fácil.

## O que *não* fazer agora

- Não redesenhar o instrumento.
- Não copiar o HTML para produção.
- Não adicionar estrela 1–5 no app “para ter dado”.
- Não tratar D3 como feature a expandir (matching, 6 perguntas, etc.).

## Próxima evidência (fora do código)

Rodada com **≥10 pessoas**, mesmo HTML/form, **justificativa obrigatória para ≤ 3**. Só então decidir: (a) manter o quiz atual e só corrigir contenção/copy; (b) separar intake clínico de escala; (c) despriorizar D3 frente a D1/agenda/financeiro.

Até lá: **hold** em investimento pesado no diferencial D3.
