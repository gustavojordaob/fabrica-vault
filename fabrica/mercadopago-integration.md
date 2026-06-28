---
tags:
  - pagamentos
  - mercadopago
  - assinatura
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "Para Deep Links (retorno ao app após pagamento)"
  - "26.6 No app — iniciar pagamento"
  - "26.9 Ambiente de testes (Sandbox)"
  - "26.10 Checklist Mercado Pago"
  - "27. MERCADO PAGO — Assinatura (preapproval), planos e webhooks"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **mercadopago** — checkout, assinaturas, webhooks (Android)
> 2. MCP **revenuecat** + **appstore-connect** — IAP iOS (não usar MP no iPhone)
> 3. MCP **fabrica-apps** — `rag_buscar("mercadopago ...")` + `buscar_historico`
>
> Guia MCPs: [[mcps-cursor-padrao]] · Assinatura completa: [[mercadopago-assinatura-ota-padroes]] · [[cortejo-modulos-jun2026-padrao]]

---

# Para Deep Links (retorno ao app após pagamento)
npx expo install expo-linking
```

Nenhuma outra dependência de Mercado Pago no app — toda a lógica fica no backend.

---

### 26.6 No app — iniciar pagamento

```typescript
// utils/mercadoPago.ts
import { openBrowserAsync } from 'expo-web-browser';
import { auth } from './firebaseConfig';

const FUNCAO_URL = process.env.EXPO_PUBLIC_MP_FUNCTION_URL!;

export async function iniciarPagamento(dados: {
  titulo: string;
  valor: number;
  referencia?: string;
}): Promise<'cancelado' | 'pendente'> {

  const uid = auth.currentUser?.uid;
  if (!uid) throw new Error('Usuário não autenticado');

  const resp = await fetch(FUNCAO_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...dados, uid }),
  });

  if (!resp.ok) throw new Error('Falha ao criar preferência');

  const { sandboxInitPoint, initPoint } = await resp.json();
  const url = __DEV__ ? sandboxInitPoint : initPoint;

  const resultado = await openBrowserAsync(url);
  return resultado.type === 'cancel' ? 'cancelado' : 'pendente';
}
```

---

### 26.9 Ambiente de testes (Sandbox)

```
1. mercadopago.com.br/developers/panel/test-users → criar usuários de teste
2. Usar credenciais do usuário VENDEDOR no ACCESS_TOKEN
3. Usar credenciais do usuário COMPRADOR para simular pagamentos

Cartão de teste aprovado (Brasil):
  Número:   5031 4332 1540 6351
  CVV:      123
  Validade: 11/25
  Nome:     APRO
```

---

### 26.10 Checklist Mercado Pago

- [ ] `MP_ACCESS_TOKEN` salvo como secret Firebase — nunca no `.env` do app
- [ ] Cloud Function `criarPreferenciaPagamento` deployada
- [ ] Cloud Function `webhookMercadoPago` deployada com URL na preferência
- [ ] `expo-web-browser` instalado no app
- [ ] `scheme: "lashmatch"` no `app.json`
- [ ] `intentFilters` Android configurado para Deep Link
- [ ] `back_urls` apontando para `lashmatch://pagamento/...`
- [ ] `external_reference` com `uid` para conciliação no Firestore
- [ ] Schema `pagamentos` no Firestore
- [ ] `sandboxInitPoint` em `__DEV__`, `initPoint` em produção
- [ ] Webhook responde `200` imediatamente antes de processar

---

---

## 27. MERCADO PAGO — Assinatura (preapproval), planos e webhooks

---

## Regra da fábrica — Mercado Pago em Dev

As credenciais do Mercado Pago são as MESMAS
em desenvolvimento e produção.

Sempre copiar todas as variáveis EXPO_PUBLIC_MP_*
do .env para o .env.development ao criar ambiente dev.

Variáveis obrigatórias:
- EXPO_PUBLIC_MP_PUBLIC_KEY
- EXPO_PUBLIC_MP_ACCESS_TOKEN
- EXPO_PUBLIC_MP_TOKENIZE_URL
- (qualquer outra EXPO_PUBLIC_MP_*)

Também copiar do `.env` para `.env.development`:
- `EXPO_PUBLIC_INTERNAL_API` → `https://us-central1-lashmatch-627fd.cloudfunctions.net`
- `EXPO_PUBLIC_API_URL` (mesma base)

**Erro 404 HTML na tela de cartão:** o app estava chamando `criarAssinaturaMercadoPago` em `lashmatch-dev`, onde a função não existe. A URL correta é sempre produção (`lashmatch-627fd`). Utilitário: `utils/mercadoPagoEndpoints.ts`.

**Auth em dev híbrido:** login em `lashmatch-dev` + Functions em `lashmatch-627fd` → token com `aud` diferente. Mensagem `AUTH_WRONG_FIREBASE_PROJECT` ou testar com `.env` de produção.

---

## Assinatura com cartão tokenizado + paywall (Cortejo — jun/2026)

**Guia completo:** [[mercadopago-assinatura-ota-padroes]]

Resumo dos erros que **não** podem se repetir:

| Erro | Regra |
|------|--------|
| Cancelou no app, MP ainda cobra | Sempre `PUT cancelled` na API MP antes de `plan: free` |
| Várias assinaturas no MP | `cancelAllActivePreapprovalsForEmail` antes de `POST /preapproval` |
| Pagou e ficou na paywall | `mpSyncSubscription` busca por e-mail; botão "Atualizar acesso"; recarregar store após `mpCriarAssinatura` |
| `salonId doesn't exist` | Não remover variável do store se JSX ainda referencia |

Deploy obrigatório após mudar `functions/SRC/mercadoPagoAssinatura.ts` ou handlers em `index.ts`.