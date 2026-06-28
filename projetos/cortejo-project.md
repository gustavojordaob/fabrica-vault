---
projeto: Cortejo
tipo: referencia-tecnica
stack: React Native (Expo) + Firebase
package: com.fabricaapps.cortejo
firebase: cortejo-app
repo: C:/Users/gusta/projetos/cortejo
atualizado_em: 2026-06-18
links:
  - "[[cortejo-prd]]"
  - "[[../fabrica/cortejo-schemas]]"
  - "[[../fabrica/agenda-salao-expo-padrao]]"
---

# Cortejo — PROJECT (referência técnica)

> **Fonte de verdade:** esta nota + PRD **[[cortejo-prd]]**.  
> Padrões cross-projeto: `obsidian/fabrica/`.  
> O arquivo `PROJECT.md` no repo Git é só um **atalho** para cá.

---

## Visão rápida

App de gestão para salões: agenda, estoque, PDV, financeiro, assinatura MP.

- **Stack:** Expo Router + Firebase JS SDK + `theme/tokens.ts`
- **Multi-tenant:** `artifacts/cortejo/salons/{salonId}/…`

---

## Design tokens

Ver PRD seção 2 ou `theme/tokens.ts` no repo.

| Token | Hex |
|-------|-----|
| primary | `#6B4226` |
| bg | `#FAF6F1` |
| surface | `#FFFFFF` |

---

## Telas principais

| Rota | Função |
|------|--------|
| `/(tabs)/index` | Agenda |
| `/agendamento/novo` | Novo agendamento |
| `/config/horarios` | Horário **por profissional** |
| `/config/bloqueios` | Bloqueios agenda |
| `/config/clientes` | CRUD clientes |
| `/agendar` | Link público (web) |

---

## Documentação (Obsidian)

| Nota | Conteúdo |
|------|----------|
| **[[cortejo-prd]]** | Produto, design system, escopo |
| **[[../fabrica/cortejo-schemas]]** | Firestore Cortejo |
| **[[../fabrica/agenda-salao-expo-padrao]]** | Agenda, slots, bloqueios, busca cliente |
| **[[../fabrica/cadastro-clientes-salao-expo]]** | Clientes + link público |
| **[[../fabrica/whatsapp-business-api]]** | WhatsApp Meta |
| **[[../fabrica/mercadopago-assinatura-ota-padroes]]** | Assinatura MP |
| **[[../fabrica/decisoes]]** | Decisões técnicas (filtrar Cortejo) |
| **[[../fabrica/erros-e-solucoes]]** | Erros resolvidos |

---

## RAG obrigatório

Antes de codar: `rag_buscar` + `buscar_historico`  
Após erro/decisão: `registrar_erro_solucao` / `salvar_decisao` + `indexar_rapido.py`
