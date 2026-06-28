---
tags:
  - firebase
  - functions
  - backend
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "Deploy apenas Functions"
  - "18.14 Cloud Functions com Gemini — padrão do backend"
  - "23.5 Cloud Function agendada — `functions/SRC/index.ts`"
  - "23.8 Deploy da Cloud Function"
  - "Deploy apenas da função de lembretes"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** (plugin) — deploy de Functions, secrets, logs, emuladores
> 2. MCP **fabrica-apps** — `rag_buscar("cloud functions")` + `buscar_historico("functions")`
>
> Deploy e secrets de Functions: sempre via MCP **firebase** ou CLI documentada pelo plugin — não só este `.md`.

---

# Deploy apenas Functions
firebase deploy --only functions

---

### 18.14 Cloud Functions com Gemini — padrão do backend

```typescript
// functions/SRC/index.ts — estrutura das Cloud Functions
import { GoogleGenAI } from '@google/genai';
import { defineSecret } from 'firebase-functions/params';
import { onRequest } from 'firebase-functions/v2/https';
import * as admin from 'firebase-admin';

if (!admin.apps.length) admin.initializeApp();

// Secrets seguros (nunca no código, sempre no Firebase)
const apiKey = defineSecret('GEMINI_API_KEY');

// Cloud Function de análise facial
export const analisarRosto = onRequest(
  { secrets: [apiKey], cors: true },
  async (req, res) => {
    const ai = new GoogleGenAI({ apiKey: apiKey.value() });
    // ... lógica de análise com Gemini
  }
);
```

---

---

### 23.5 Cloud Function agendada — `functions/SRC/index.ts`

Implementação real: `export const enviarLembretesAgendamento` — `onSchedule` com `schedule: '0 8 * * *'`, `timeZone: 'America/Sao_Paulo'`, `secrets: [zapiInstance, zapiToken, zapiClientToken]`.

**Diferença importante em relação a um pseudo-código “só `GCLOUD_PROJECT`”:** o scheduler atual percorre **todos** os documentos da coleção raiz `artifacts` (cada `id` = namespace, no app costuma ser `app.options.appId`) e, para cada usuária em `usuarios/{uid}`, consulta `artifacts/{namespace}/users/{uid}/agendamentos` com janela de **amanhã** e `lembreteEnviado == false`. Após envios com sucesso para um par `(namespace, uid)`, grava `resumoLembretes/ultimo` nesse mesmo path.

Trecho essencial (secrets + chamada Z-API + tratamento de erro):

```typescript
import { defineSecret } from 'firebase-functions/params';
import { onSchedule } from 'firebase-functions/v2/scheduler';
import * as admin from 'firebase-admin';

const zapiInstance = defineSecret('ZAPI_INSTANCE');
const zapiToken = defineSecret('ZAPI_TOKEN');
const zapiClientToken = defineSecret('ZAPI_CLIENT_TOKEN');

function zApiHeaders(): Record<string, string> {
  return {
    'Content-Type': 'application/json',
    'Client-Token': zapiClientToken.value(),
  };
}

// onSchedule({ secrets: [zapiInstance, zapiToken, zapiClientToken], ... }, async () => { ... })

const resposta = await fetch(
  `https://api.z-api.io/instances/${zapiInstance.value()}/token/${zapiToken.value()}/send-text`,
  {
    method: 'POST',
    headers: zApiHeaders(),
    body: JSON.stringify({ phone: telefoneComPais, message: mensagem }),
  }
);

if (!resposta.ok) {
  const detalhe = await resposta.text();
  throw new Error(`Z-API erro ${resposta.status}: ${detalhe}`);
}
```

---

### 23.8 Deploy da Cloud Function

```bash

---

# Deploy apenas da função de lembretes
firebase deploy --only functions:enviarLembretesAgendamento

---

# PowerShell (Windows): ao deployar várias functions, use aspas na lista
firebase deploy --only "functions:testarLembrete,functions:enviarLembretesAgendamento"

---

### 23.9 Testar manualmente antes do deploy

Função HTTP **`testarLembrete`** em `functions/SRC/index.ts`: body JSON `{ telefone, nome }`, mesmos secrets e `zApiHeaders()` do scheduler. **Valida** `resposta.ok` e devolve corpo da Z-API em sucesso ou erro (nunca `ok: true` cego).

```typescript
export const testarLembrete = onRequest(
  { secrets: [zapiInstance, zapiToken, zapiClientToken] },
  async (req, res) => {
    const { telefone, nome } = req.body || {};
    if (!telefone || !nome) {
      res.status(400).json({ ok: false, error: 'Informe telefone e nome no body.' });
      return;
    }
    const telefoneComPais = `55${String(telefone).replace(/\D/g, '')}`;
    const url = `https://api.z-api.io/instances/${zapiInstance.value()}/token/${zapiToken.value()}/send-text`;
    const resposta = await fetch(url, {
      method: 'POST',
      headers: zApiHeaders(),
      body: JSON.stringify({
        phone: telefoneComPais,
        message: `Teste de lembrete para ${nome} 💅`,
      }),
    });
    const respostaTexto = await resposta.text();
    if (!resposta.ok) {
      res.status(502).json({
        ok: false,
        status: resposta.status,
        error: 'Falha no envio via Z-API.',
        detalhe: respostaTexto,
      });
      return;
    }
    res.json({ ok: true, status: resposta.status, detalhe: respostaTexto });
  }
);
```

---

### 23.10 Checklist Z-API + Cloud Function

- [ ] Conta criada em **app.z-api.io** e instância conectada
- [ ] Três secrets: `ZAPI_INSTANCE`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN` — e **redeploy** após alterar qualquer um
- [ ] Header `Client-Token` em **todas** as chamadas `fetch` à Z-API (helper `zApiHeaders()`)
- [ ] Plano Firebase Blaze ativado (necessário para chamadas externas)
- [ ] `npm run build` em `functions/` antes do deploy se o código TypeScript compilar para `lib/`
- [ ] `lembreteEnviado: false` ao criar cada agendamento
- [ ] `clienteNome` e `clienteTelefone` desnormalizados no agendamento
- [ ] Telefone sempre com código `55` do Brasil antes de enviar
- [ ] Cloud Function com `timeZone: 'America/Sao_Paulo'`
- [ ] Tratamento de erro individual por agendamento — um erro não para os outros
- [ ] Hook `useLembretesEnviados` no app para notificar a dona (§21.12 — Expo Go sem import estático)
- [ ] `testarLembrete` validando `resposta.ok` + corpo antes de responder sucesso

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · Curso React Native Expo Go — Caio Eduardo · Projeto LashMatch (referência principal) · developer.z-api.io · docs.expo.dev/push-notifications/overview · https://brunolagoa.medium.com/enviar-mensagem-para-whatsapp-com-react-native-70239bb65495*

---

---

### 25.7 Cloud Function — confirmação automática ao criar agendamento

```typescript
// functions/SRC/index.ts — adicionar junto às funções existentes
import { onDocumentCreated } from 'firebase-functions/v2/firestore';

export const enviarConfirmacaoAgendamento = onDocumentCreated(
  {
    document: 'artifacts/{appId}/users/{uid}/agendamentos/{agendId}',
    secrets: [zapiInstance, zapiToken, zapiClientToken],
  },
  async (event) => {
    const ag = event.data?.data();
    if (!ag || !ag.clienteTelefone) return;

    const dataHora = ag.dataHoraInicio.toDate();
    const data = dataHora.toLocaleDateString('pt-BR');
    const hora = dataHora.toLocaleTimeString('pt-BR', {
      hour: '2-digit', minute: '2-digit'
    });

    const mensagem =
      `Olá ${ag.clienteNome}! 💅\n\n` +
      `Seu agendamento foi *confirmado*:\n` +
      `📅 Data: *${data}*\n` +
      `⏰ Hora: *${hora}*\n` +
      `✂️ Serviço: *${ag.servicoNome}*\n` +
      `👩 Profissional: *${ag.funcionariaNome}*\n\n` +
      `Te esperamos! 😊`;

    const telefone = ag.clienteTelefone.replace(/\D/g, '');
    const telefoneComPais = telefone.startsWith('55')
      ? telefone : `55${telefone}`;

    const resposta = await fetch(
      `https://api.z-api.io/instances/${zapiInstance.value()}/token/${zapiToken.value()}/send-text`,
      {
        method: 'POST',
        headers: zApiHeaders(),  // inclui Client-Token (ver Seção 23.4.1)
        body: JSON.stringify({ phone: telefoneComPais, message: mensagem }),
      }
    );

    if (!resposta.ok) {
      const detalhe = await resposta.text();
      throw new Error(`Z-API confirmação erro ${resposta.status}: ${detalhe}`);
    }

    await event.data?.ref.update({
      confirmacaoEnviadaEm: admin.firestore.FieldValue.serverTimestamp(),
    });
  }
);
```

---

### 26.4 Cloud Function — criar preferência de pagamento

```typescript
// functions/SRC/index.ts
import { onRequest } from 'firebase-functions/v2/https';
import { defineSecret } from 'firebase-functions/params';
import * as admin from 'firebase-admin';

const mpAccessToken = defineSecret('MP_ACCESS_TOKEN');

export const criarPreferenciaPagamento = onRequest(
  { secrets: [mpAccessToken], cors: true },
  async (req, res) => {
    if (req.method !== 'POST') {
      res.status(405).json({ error: 'Método não permitido' });
      return;
    }

    const { titulo, valor, quantidade = 1, uid, referencia } = req.body;

    if (!titulo || !valor || !uid) {
      res.status(400).json({ error: 'titulo, valor e uid são obrigatórios' });
      return;
    }

    try {
      const resposta = await fetch('https://api.mercadopago.com/checkout/preferences', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${mpAccessToken.value()}`,
        },
        body: JSON.stringify({
          items: [{
            title: titulo,
            quantity: quantidade,
            currency_id: 'BRL',
            unit_price: Number(valor),
          }],
          back_urls: {
            success: 'lashmatch://pagamento/sucesso',
            failure: 'lashmatch://pagamento/falha',
            pending: 'lashmatch://pagamento/pendente',
          },
          auto_return: 'approved',
          external_reference: referencia || uid,
          notification_url: 'https://SUA_REGION-SEU_PROJETO.cloudfunctions.net/webhookMercadoPago',
        }),
      });

      if (!resposta.ok) {
        const erro = await resposta.text();
        res.status(502).json({ error: 'Falha ao criar preferência', detalhe: erro });
        return;
      }

      const dados = await resposta.json();

      // Salvar no Firestore para rastreamento
      const appId = process.env.GCLOUD_PROJECT || '';
      await admin.firestore()
        .collection('artifacts').doc(appId)
        .collection('users').doc(uid)
        .collection('pagamentos').add({
          preferenceId: dados.id,
          titulo,
          valor: Number(valor),
          status: 'pendente',
          criadoEm: admin.firestore.FieldValue.serverTimestamp(),
          external_reference: referencia || uid,
        });

      res.json({
        preferenceId: dados.id,
        initPoint: dados.init_point,
        sandboxInitPoint: dados.sandbox_init_point,
      });

    } catch (erro) {
      console.error('Erro ao criar preferência:', erro);
      res.status(500).json({ error: 'Erro interno' });
    }
  }
);
```

---

### 26.5 Cloud Function — webhook de confirmação

```typescript
export const webhookMercadoPago = onRequest(
  { secrets: [mpAccessToken] },
  async (req, res) => {
    res.status(200).send('OK'); // Responder imediatamente

    const { type, data } = req.body;
    if (type !== 'payment') return;

    try {
      const pagamentoResp = await fetch(
        `https://api.mercadopago.com/v1/payments/${data.id}`,
        { headers: { 'Authorization': `Bearer ${mpAccessToken.value()}` } }
      );

      const pagamento = await pagamentoResp.json();
      const { status, external_reference } = pagamento;

      const appId = process.env.GCLOUD_PROJECT || '';
      const snap = await admin.firestore()
        .collection('artifacts').doc(appId)
        .collection('users').doc(external_reference)
        .collection('pagamentos')
        .where('external_reference', '==', external_reference)
        .orderBy('criadoEm', 'desc')
        .limit(1)
        .get();

      if (!snap.empty) {
        await snap.docs[0].ref.update({
          status,
          paymentId: data.id,
          atualizadoEm: admin.firestore.FieldValue.serverTimestamp(),
        });
      }
    } catch (erro) {
      console.error('Erro webhook:', erro);
    }
  }
);
```

---

### 27.1 Cloud Functions (LashMatch)

| Função | Descrição |
|--------|-----------|
| `criarAssinatura` | Mesmo fluxo de `criarAssinaturaMercadoPago`: Bearer Firebase + `card_token_id` + `plano`; cria preapproval no MP e atualiza `usuarios/{uid}.plano`. |
| `criarAssinaturaMercadoPago` | Handler compartilhado com `criarAssinatura` (código único). |
| `criarPlanoMP` | POST administrativo: cria `preapproval_plan` na API MP e grava `config/mercadopago_planos` (chaves `mensal` / `anual`). Body: `{ planoId, setupKey }` com `setupKey` igual a `process.env.MP_PLANO_SETUP_KEY` (ex.: `functions/.env` ou variável no runtime Cloud Functions). |
| `webhookAssinatura` | URL dedicada a notificações de assinatura; responde `200` e sincroniza `usuarios/{uid}.plano` via GET `/preapproval/{id}`. Ignora `topic=payment` (checkout usa `webhookMercadoPago`). |

Se existir `mp_plan_id` em `config/mercadopago_planos` para o plano escolhido, `criarAssinatura*` usa `preapproval_plan_id` em vez de `auto_recurring` inline. O preapproval envia `notification_url` para `webhookAssinatura` quando `GCLOUD_PROJECT` está definido.