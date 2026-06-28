---
tags:
  - firebase
  - firestore
  - setup
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "3.2 Instalação Firebase JS SDK (recomendado)"
  - "3.3 Configuração inicial — `firebaseConfig.ts`"
  - "4. FIREBASE AUTH"
  - "5. FIRESTORE"
  - "6. FIREBASE STORAGE"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** (plugin Cursor) — deploy, Firestore rules/indexes, Auth, Functions, Hosting
> 2. MCP **fabrica-apps** — `rag_buscar("firebase ...")` + `buscar_historico("firebase")`
>
> Não altere regras, índices ou deploy só com este `.md`. Use o MCP **firebase** para publicar e validar no projeto correto.

---

### 3.2 Instalação Firebase JS SDK (recomendado)
```bash

---

### 3.3 Configuração inicial — `firebaseConfig.ts`
```typescript
// firebaseConfig.ts (na raiz do projeto ou em /config)
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID,
};

export const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getStorage(app);
```

---

## 4. FIREBASE AUTH

---

## 5. FIRESTORE

---

## 6. FIREBASE STORAGE

---

### 7.1 Quando migrar do JS SDK para RN Firebase
- Precisa de **Analytics**, **Crashlytics** ou **Dynamic Links**
- Precisa de performance nativa máxima
- Não usa Expo Go (usa EAS Build / Development Build)

---

# Seguir https://rnfirebase.io/#managed-workflow para configuração nativa
npx expo prebuild --clean   # aplica config plugins antes de build local
```

> ⚠️ React Native Firebase **não funciona no Expo Go**. Requer development build ou EAS Build.

---

---

## 8. PADRÕES DE TELA COM FIREBASE

---

### 8.2 Tela de lista com Firestore realtime
```typescript
import { View, FlatList, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { usePosts } from '../hooks/usePosts'; // hook com onSnapshot

export default function HomeScreen() {
  const { posts, loading } = usePosts();

  if (loading) return <ActivityIndicator style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <FlatList
        data={posts}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.sub}>{item.authorId}</Text>
          </View>
        )}
        contentContainerStyle={{ padding: 16, gap: 12 }}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16 },
  title: { fontSize: 16, fontWeight: '600' },
  sub: { color: '#888', marginTop: 4 },
});
```

---

---

# Deploy Firebase Functions e Hosting
firebase deploy

---

# Emuladores locais Firebase
firebase emulators:start

---

# Ver logs Firebase Functions
firebase functions:log
```

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · docs.expo.dev/tutorial*

---

---

### 14.6 Configurar NavigationContainer no app.tsx
```typescript
// app.tsx
import 'react-native-gesture-handler'; // ← PRIMEIRA linha sempre
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { Routes } from './src/routes';

export default function App() {
  return (
    <NavigationContainer>
      <Routes />
    </NavigationContainer>
  );
}
```

---

### 18.3 Configuração Firebase — padrão correto

```typescript
// utils/firebaseConfig.ts — ÚNICA fonte de verdade
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey:            process.env.EXPO_PUBLIC_FIREBASE_API_KEY,
  authDomain:        process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId:         process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket:     process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId:             process.env.EXPO_PUBLIC_FIREBASE_APP_ID,
  measurementId:     process.env.EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID,
};

export const app       = initializeApp(firebaseConfig);
export const auth      = getAuth(app);
export const firestore = getFirestore(app);
export const storage   = getStorage(app);
```

```typescript
// ✅ USO CORRETO — importar do config centralizado
import { auth, firestore, storage, app } from '../../utils/firebaseConfig';

// ❌ ERRADO — reinicializar dentro do componente
const auth = getAuth(app);       // NÃO FAZER
const db = getFirestore(app);    // NÃO FAZER
```

> **Regra crítica do LashMatch:** `getAuth(app)` e `getFirestore(app)` chamados dentro de componentes são um anti-padrão encontrado no projeto. Todo código novo deve importar `auth` e `firestore` diretamente do `firebaseConfig.ts`.

---

---

### 18.4 URLs das Cloud Functions — config centralizado

```typescript
// utils/config.ts
export const CLOUD_FUNCTIONS = {
  uploadClientPhoto:    process.env.EXPO_PUBLIC_UPLOAD_FOTO,
  analisarRosto:        process.env.EXPO_PUBLIC_ANALISE_URL,
  assistenteVisagismo:  process.env.EXPO_PUBLIC_CHAT_URL,
};

// Uso nas telas:
import { CLOUD_FUNCTIONS } from '../utils/config';
const response = await fetch(CLOUD_FUNCTIONS.analisarRosto!, { ... });
```

---

---

### 18.5 Estrutura Firestore do LashMatch

```
// Coleção de usuários (lash designers)
usuarios/{uid}
  - nome: string
  - sobrenome: string
  - email: string
  - (outros dados do cadastro)

// Clientes de cada lash designer (subcoleção isolada por usuário)
artifacts/{appId}/users/{uid}/clientes/{clienteId}
  - nome: string
  - nomeCompleto: string
  - nomePrimeiro: string
  - sobrenome: string
  - telefone: string           // formato: "(11) 99999-9999"
  - dataNascimento: string     // formato: "DD/MM/AAAA"
  - tomPele: TomPele
  - fotoUrl: string
  - dataCadastro: Timestamp    // serverTimestamp()
  - ultimaVisita: Timestamp    // serverTimestamp()
  - ultimaAnalise: object | null

// Histórico de análises de cada cliente
artifacts/{appId}/users/{uid}/clientes/{clienteId}/historico/{analiseId}
  - estilo: string
  - formatoRosto: string
  - eixo / profundidade / alinhamento / distanciamento
  - curvaturasRecomendadas: object
  - colorimetria: object
  - fotoUrl: string
  - data: Timestamp
  - modoAnalise: 'ia' | 'manual'
```

> **Padrão de path do LashMatch:** `artifacts/${app.options.appId}/users/${user.uid}/clientes`
> Sempre pegar o `appId` via `app.options.appId` — nunca hardcodar.

---

---

### 21.3 Configuração global — `app/_layout.tsx`

Sempre configurar o handler no topo do app, antes de qualquer tela:

```typescript
import * as Notifications from 'expo-notifications';

// Define o comportamento quando chega notificação com app aberto
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldPlaySound: true,
    shouldSetBadge: true,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});
```

---

### 21.6 Salvar notificationId no Firestore

Sempre salvar o `notificationId` junto com o agendamento para poder cancelar depois:

```typescript
import { addDoc, collection, serverTimestamp } from 'firebase/firestore';
import { app, firestore } from '../utils/firebaseConfig';

async function criarAgendamento(dados: {
  clienteNome: string;
  dataHora: Date;
  servico: string;
  uid: string;
}) {
  const appId = app.options.appId!;

  // 1. Agendar notificação
  const notificationId = await agendarLembrete(dados.clienteNome, dados.dataHora);

  // 2. Salvar agendamento com o notificationId
  await addDoc(
    collection(firestore, 'artifacts', appId, 'users', dados.uid, 'agendamentos'),
    {
      clienteNome: dados.clienteNome,
      dataHora: dados.dataHora,
      servico: dados.servico,
      notificationId,           // ← salvar para cancelar depois
      criadoEm: serverTimestamp(),
    }
  );
}
```

---

### 22.7 Schema Firestore para agendamentos

```
artifacts/{appId}/users/{uid}/agendamentos/{agendamentoId}
  - clienteId:        string       // ref para clientes/{id}
  - clienteNome:      string       // desnormalizado para exibição rápida
  - clienteTelefone:  string       // para abrir WhatsApp direto
  - servico:          string
  - dataHora:         Timestamp
  - lembreteEnviado:  boolean      // false por padrão
  - lembreteEnviadoEm: Timestamp | null
  - notificationId:   string | null // para cancelar lembrete local
  - criadoEm:         Timestamp
```

---

## 23. WHATSAPP AUTOMÁTICO — Z-API + Firebase Cloud Functions

> Fonte: developer.z-api.io · docs.expo.dev/push-notifications
> Caso de uso: salão de beleza enviando lembrete automático 1 dia antes do agendamento, sem a dona precisar fazer nada.

---

### 23.6 Schema Firestore para agendamentos

```
artifacts/{appId}/users/{uid}/agendamentos/{agendamentoId}
  - clienteId:          string       // ref para clientes/{id}
  - clienteNome:        string       // desnormalizado — evita join extra
  - clienteTelefone:    string       // formato: "(11) 99999-9999"
  - servico:            string
  - dataHora:           Timestamp    // data e hora do agendamento
  - lembreteEnviado:    boolean      // false por padrão
  - lembreteEnviadoEm:  Timestamp | null
  - criadoEm:           Timestamp    // serverTimestamp()
  - atualizadoEm:       Timestamp    // serverTimestamp() ao editar
```

> **Regra crítica:** sempre desnormalizar `clienteNome` e `clienteTelefone` no documento do agendamento. A Cloud Function não pode fazer joins — precisa dos dados disponíveis diretamente.

---

### 24.2 Schema Firestore — módulo financeiro

```
// Vendas (cada atendimento registrado)
artifacts/{appId}/users/{uid}/vendas/{vendaId}
  - clienteNome:      string          // desnormalizado
  - clienteId:        string | null   // ref para clientes/{id}
  - servico:          string          // ex: "Extensão volume russo"
  - valorVenda:       number          // R$ cobrado da cliente
  - produtosUsados:   ProdutoUsado[]  // lista de produtos do estoque
  - custoTotal:       number          // soma dos custos dos produtos
  - lucroBruto:       number          // valorVenda - custoTotal
  - formaPagamento:   'pix' | 'dinheiro' | 'cartao_credito' | 'cartao_debito'
  - dataVenda:        Timestamp       // serverTimestamp()
  - observacao:       string | null

// Tipo ProdutoUsado (dentro da venda)
interface ProdutoUsado {
  produtoId:    string   // id do produto no estoque
  produtoNome:  string   // desnormalizado
  quantidade:   number   // quantas unidades foram usadas
  custoUnitario: number  // custo por unidade no momento da venda
  custoTotal:   number   // quantidade * custoUnitario
}

// Despesas fixas e variáveis
artifacts/{appId}/users/{uid}/despesas/{despesaId}
  - descricao:    string
  - valor:        number
  - categoria:    'aluguel' | 'produto' | 'marketing' | 'equipamento' | 'outros'
  - tipo:         'fixa' | 'variavel'
  - data:         Timestamp
  - criadoEm:     Timestamp

// Produtos do estoque — já existente — adicionar campo custoUnitario
artifacts/{appId}/users/{uid}/estoque/{produtoId}
  - ...campos já existentes...
  - custoUnitario: number   // ← NOVO: custo de compra por unidade
```

---

### 24.9 Índices Firestore necessários

```
// Criar no Firebase Console → Firestore → Índices
vendas: dataVenda (ASC) + uid implícito no path ← automático
vendas: dataVenda + formaPagamento             ← criar se precisar filtrar
despesas: data (ASC)                           ← automático
```

---

### 25.2 Schema Firestore completo

```
// Funcionárias do salão
artifacts/{appId}/users/{uid}/funcionarias/{funcId}
  - nome:          string
  - especialidade: string         // ex: "Volume russo, Clássico"
  - ativa:         boolean
  - criadoEm:      Timestamp

// Serviços oferecidos
artifacts/{appId}/users/{uid}/servicos/{servicoId}
  - nome:           string        // ex: "Volume russo - 1ª vez"
  - duracaoMinutos: number        // ex: 180 (3h), 90 (1h30), 150 (2h30)
  - preco:          number        // ex: 150.00
  - ativo:          boolean
  - criadoEm:       Timestamp

// Agendamentos (dona + cliente pública)
artifacts/{appId}/users/{uid}/agendamentos/{agendId}
  - clienteNome:       string
  - clienteTelefone:   string     // formato: "5511999999999" (com 55)
  - clienteId?:        string     // se cliente cadastrada no app
  - funcionariaId:     string     // ref para funcionarias/{id}
  - funcionariaNome:   string     // desnormalizado
  - servicoId:         string     // ref para servicos/{id}
  - servicoNome:       string     // desnormalizado
  - duracaoMinutos:    number     // copiado do serviço no momento
  - preco:             number     // copiado do serviço no momento
  - dataHoraInicio:    Timestamp
  - dataHoraFim:       Timestamp  // dataHoraInicio + duracaoMinutos
  - origem:            'app' | 'link_publico'
  - status:            'confirmado' | 'cancelado' | 'concluido'
  - lembreteEnviado:   boolean
  - lembreteEnviadoEm: Timestamp | null
  - criadoEm:          Timestamp
```

> **Regra crítica:** sempre salvar `dataHoraFim = dataHoraInicio + duracaoMinutos`. Sem isso a verificação de conflito não funciona.

---

### 25.9 Regras Firestore para página pública

```javascript
// firestore.rules — adicionar para permitir agendamento sem login
match /artifacts/{appId}/users/{uid}/servicos/{id} {
  allow read: if true;  // público — cliente precisa ver os serviços
}
match /artifacts/{appId}/users/{uid}/funcionarias/{id} {
  allow read: if true;  // público — cliente precisa ver as funcionárias
}
match /artifacts/{appId}/users/{uid}/agendamentos/{id} {
  allow read:   if request.auth.uid == uid;
  allow create: if true;  // cliente cria sem autenticação
  allow update, delete: if request.auth.uid == uid;
}
```

---

# Salvar como secrets do Firebase (NUNCA no .env do app)
firebase functions:secrets:set MP_ACCESS_TOKEN
firebase functions:secrets:set MP_PUBLIC_KEY
```

Painel de desenvolvedores: mercadopago.com.br/developers/panel

> Usar credenciais de Sandbox para testes e Produção para cobranças reais.

---

### 26.7 Configurar Deep Link no app.json

```json
{
  "expo": {
    "scheme": "lashmatch",
    "android": {
      "intentFilters": [{
        "action": "VIEW",
        "data": [{ "scheme": "lashmatch", "host": "pagamento" }],
        "category": ["BROWSABLE", "DEFAULT"]
      }]
    }
  }
}
```

---

### 26.8 Schema Firestore para pagamentos

```
artifacts/{appId}/users/{uid}/pagamentos/{id}
  - preferenceId:       string     // ID da preferência no MP
  - paymentId:          string     // ID do pagamento (vem do webhook)
  - titulo:             string
  - valor:              number
  - status:             'pendente' | 'approved' | 'rejected' | 'cancelled'
  - external_reference: string     // uid do usuário
  - criadoEm:           Timestamp
  - atualizadoEm:       Timestamp
```

---

### 27.3 Firestore

- `usuarios/{uid}.plano` — ver `PROJECT.md` (inclui `mp_preapproval_plan_id`, `ultimaSincronizacaoWebhook` quando aplicável).
- `config/mercadopago_planos` — ids de plano MP por período (`mensal` / `anual`).

### 27.4 Feature flags globais (Firestore)

Padrão Cortejo jun/2026 — rollout gradual sem redeploy:

| Item | Valor |
|------|-------|
| Path | `artifacts/{appNamespace}/system/platformConfig` |
| Exemplo | `artifacts/cortejo/system/platformConfig` |
| Campo | `whatsappSalonEnabled: boolean` |
| Rules | `read: request.auth != null`; `write: false` |
| App | `onSnapshot` listener (tempo real) |
| Backend | Admin SDK read + gate HTTP 503 |

**Guia completo:** [[whatsapp-salao-expo-padrao]] §14 · schema [[cortejo-schemas]]

**Armadilha:** doc em `artifacts/system` (errado) vs `artifacts/cortejo/system/platformConfig` (certo). Build/OTA antigo pode ignorar flag.

## ⚠️ Firebase Auth no React Native — REGRA DA FÁBRICA

### ❌ NUNCA usar getAuth simples
```typescript
import { getAuth } from 'firebase/auth';
export const auth = getAuth(app); // sessão não persiste entre sessões
```

### ✅ SEMPRE usar initializeAuth com AsyncStorage
npx expo install @react-native-async-storage/async-storage

```typescript
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(AsyncStorage)
});
```