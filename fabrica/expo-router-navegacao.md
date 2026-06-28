---
tags:
  - expo
  - router
  - navegacao
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "2. EXPO E EXPO GO"
  - "2.1 O que é Expo"
  - "Escaneie o QR com Expo Go no celular"
  - "2.3 Expo Router — Navegação file-based"
  - "2.4 Expo Router — Tabs"
---

## 2. EXPO E EXPO GO

---

### 2.1 O que é Expo
- Framework open-source construído sobre React Native que simplifica setup, build e deploy.
- Fornece: file-based routing (Expo Router), SDK de módulos nativos, EAS Build e EAS Submit.
- **Expo Go**: app gratuito (iOS + Android) que roda seu projeto via QR Code sem precisar buildar — ideal para desenvolvimento.
- **Expo SDK 54** (versão atual, 2025): suporta nova arquitetura RN, `firebase@^12.0.0`.

---

# Escaneie o QR com Expo Go no celular
```

---

### 2.3 Expo Router — Navegação file-based
Inspirado no Next.js: estrutura de arquivos define as rotas.

```
app/
  _layout.tsx          ← Layout raiz (Stack, Tabs, Drawer)
  index.tsx            ← Rota "/" (tela inicial)
  (tabs)/
    _layout.tsx        ← Layout com Tabs
    home.tsx           ← Aba Home
    profile.tsx        ← Aba Perfil
  product/
    [id].tsx           ← Rota dinâmica /product/123
```

```typescript
// app/_layout.tsx — Stack Navigator
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Início' }} />
      <Stack.Screen name="product/[id]" options={{ title: 'Produto' }} />
    </Stack>
  );
}

// Navegar entre telas
import { router } from 'expo-router';
router.push('/product/123');
router.back();

// Ler parâmetros
import { useLocalSearchParams } from 'expo-router';
const { id } = useLocalSearchParams();
```

---

### 2.4 Expo Router — Tabs
```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="home"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <Ionicons name="home" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Perfil',
          tabBarIcon: ({ color }) => <Ionicons name="person" size={24} color={color} />,
        }}
      />
    </Tabs>
  );
}
```

---

## 3. FIREBASE COM EXPO — GUIA COMPLETO

---

# Expo SDK 53+ requer firebase@^12.0.0
npx expo install firebase
```

> ⚠️ Não use `npm install firebase` — use `npx expo install` para garantir compatibilidade de versão.

---

### 3.4 Variáveis de ambiente com Expo
```bash

---

# .env (na raiz — prefixo EXPO_PUBLIC_ obrigatório para ser exposto ao cliente)
EXPO_PUBLIC_FIREBASE_API_KEY=AIzaSy...
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=meuapp.firebaseapp.com
EXPO_PUBLIC_FIREBASE_PROJECT_ID=meuapp
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=meuapp.appspot.com
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
EXPO_PUBLIC_FIREBASE_APP_ID=1:123:android:abc
```

> Adicione `.env` ao `.gitignore`. Nunca comite chaves Firebase no Git.

---

---

### 4.3 Proteger rotas com Expo Router
```typescript
// app/_layout.tsx
import { useAuth } from '../hooks/useAuth';
import { Redirect } from 'expo-router';

export default function RootLayout() {
  const { user, loading } = useAuth();

  if (loading) return <LoadingScreen />;
  if (!user) return <Redirect href="/login" />;

  return <Stack />;
}
```

---

### 4.4 Persistência de Auth no Expo Go
Firebase JS SDK com Expo Go pode ter problemas de persistência. Use `getReactNativePersistence`:
```typescript
import { initializeAuth, getReactNativePersistence } from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(AsyncStorage),
});
```
Instalar: `npx expo install @react-native-async-storage/async-storage`

---

---

### 6.1 Upload de imagem (com Expo ImagePicker)
```typescript
import * as ImagePicker from 'expo-image-picker';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebaseConfig';

async function pickAndUploadImage(userId: string): Promise<string> {
  // 1. Pedir permissão e abrir galeria
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  });

  if (result.canceled) throw new Error('Cancelado');

  // 2. Converter URI para blob
  const response = await fetch(result.assets[0].uri);
  const blob = await response.blob();

  // 3. Fazer upload para Firebase Storage
  const storageRef = ref(storage, `avatars/${userId}.jpg`);
  await uploadBytes(storageRef, blob);

  // 4. Retornar URL pública
  const downloadURL = await getDownloadURL(storageRef);
  return downloadURL;
}
```

Instalar: `npx expo install expo-image-picker`

---

---

### 7.2 Setup com Expo
```bash
npx expo install expo-dev-client
npx expo install @react-native-firebase/app

---

# Rodar o projeto (exibe QR Code para Expo Go)
npx expo start
```

> Preferir **Expo Go no celular físico** ao invés de Android Studio — mais rápido, sem configuração de emulador.

---

# já vem no Expo SDK, mas caso precise instalar separado:
npm install react-native-vector-icons
```

---

## 14. NAVEGAÇÃO — Stack + Bottom Tab (Caio Eduardo — Vídeo 3)

> Conceito central: **Stack Navigation** engloba o projeto todo. **Bottom Tab Navigation** fica dentro do Stack, contendo as telas autenticadas.

---

# 1. Biblioteca principal de navegação
npm install @react-navigation/native

---

# 2. Dependências do Expo (gesture + screens)
npx expo install react-native-screens react-native-safe-area-context
npx expo install react-native-gesture-handler

---

### 14.10 Estrutura hierárquica de navegação
```
NavigationContainer              ← app.tsx
  └── Stack Navigator            ← src/routes/index.tsx
        ├── "login"              ← tela pública (index 0)
        └── "bottomRoutes"       ← Bottom Tab Navigator
              ├── "list"         ← aba 0
              └── "user"         ← aba 1
```

> Stack engloba o Bottom Tab. Login e telas autenticadas são separados.
> Isso garante que `navigation.reset()` funcione corretamente ao fazer login.

---

### 14.12 Checklist de navegação

- [ ] `import 'react-native-gesture-handler'` na **primeira linha** do `app.tsx`
- [ ] `<NavigationContainer>` envolve tudo no `app.tsx`
- [ ] Stack Navigator na raiz — engloba login + telas autenticadas
- [ ] Bottom Tab Navigator dentro do Stack — só telas autenticadas
- [ ] Após login usar `navigation.reset()` — nunca `navigation.navigate()`
- [ ] `screenOptions={{ headerShown: false }}` para remover header padrão
- [ ] Custom Tab Bar recebe `{ state, navigation }` via props do Bottom Tab
- [ ] Usar `state.index` para indicar aba ativa (opacidade, cor do ícone)
- [ ] Nomes de rotas em `navigation.navigate()` devem ser **idênticos** aos declarados no Navigator
- [ ] Botão central flutuante: `marginTop: -30` + `zIndex: 99`

---

---

---

# Reanimated já deve estar instalado pelo bottom-tabs

---

### 18.12 Navegação com parâmetros (padrão LashMatch)

```typescript
// Navegar passando múltiplos parâmetros
router.push({
  pathname: '/camera',
  params: {
    clientId:   selectedClientId,
    userId:     user.uid,
    modo:       'ia',          // 'ia' | 'manual'
    createdNow: 'true',        // strings porque params são sempre string
  },
});

// Receber parâmetros com tipagem
const { clientId, modo = 'ia', userId, createdNow } = useLocalSearchParams<{
  clientId:    string;
  modo?:       'ia' | 'manual';
  userId?:     string;
  createdNow?: string;         // 'true' | 'false'
}>();

// Converter string para boolean
const isNewClient = createdNow === 'true';

// Navegar para perfil de cliente (rota dinâmica)
router.push(`/clientes/${clientId}`);
```

---

---

### 19.1 `Cannot find module 'expo-router/internal/routing'`

| | |
|---|---|
| **Sintoma** | Ao rodar `npx expo start`, o Metro ou o `@expo/cli` falha com `Error: Cannot find module 'expo-router/internal/routing'` (ou equivalente ao carregar `@expo/router-server`). |
| **Causa** | **Incompatibilidade de versão do pacote `expo-router` com o SDK do Expo.** A partir do Expo SDK 55, o número de versão do **`expo-router` alinha-se ao SDK** (ex.: `~55.0.x`), não à série antiga `5.x`. O `@expo/cli` depende de `@expo/router-server`, que importa `expo-router/internal/routing`. Esses submódulos `internal/*` existem apenas no pacote **`expo-router` v55+** empacotado para o SDK 55. Se o `package.json` tiver `expo-router@~5.1.x` (legado) junto com `expo@~55`, o pacote instalado **não** contém `internal/routing.js` → resolução de módulo quebra. |
| **Solução** | 1. No projeto, alinhar o router ao SDK: ** `npx expo install expo-router` ** (usa `bundledNativeModules` / compatibilidade do SDK). 2. Confirmar no `package.json` algo como **`"expo-router": "~55.0.12"`** (ou a faixa que o Expo sugerir para o seu SDK). 3. **Não** fixar manualmente `expo-router@5.x` quando o `expo` for 55.x. 4. Ao criar projeto novo ou adicionar dependências, preferir sempre **`npx expo install <pacote>`** para módulos nativos/expo, em vez de `npm install` com versão copiada de outro major. |

---

### 19.2 Firebase Hosting + Expo Web (pasta `dist`, `rewrites`, PowerShell)

| | |
|---|---|
| **Contexto** | O LashMatch usa **Expo Router** com **`app.json` → `web.output`: `"static"`**. O comando **`npx expo export --platform web`** gera os arquivos em **`dist/`** na raiz do projeto (não use a pasta `public` antiga do Hosting para o bundle web). |
| **`firebase.json`** | Manter `firestore` / `functions` / `emulators` como já existem; em **`hosting`**: `"public": "dist"`, **`rewrites`**: `[{ "source": "**", "destination": "/index.html" }]` para rotas SPA que não gerarem HTML próprio. Sem isso, rotas como `/agendar` podem retornar 404 no servidor. |
| **Deploy** | Na raiz: `npx expo export --platform web` → `firebase deploy --only hosting`. Projeto de referência: **`lashmatch-627fd`** → URL **`https://lashmatch-627fd.web.app`** (e `https://lashmatch-627fd.firebaseapp.com`). |
| **`/agendar` na web** | A rota **`/agendar`** é servida pelo export estático (pasta `dist/agendar`). Sem **`?uid=`** a UI mostra *Link inválido* — comportamento esperado. Link público completo: `https://<projeto>.web.app/agendar?uid=<UID_FIREBASE_AUTH_DA_PROFISSIONAL>`. Definir **`EXPO_PUBLIC_AGENDAR_PUBLIC_BASE_URL=https://<projeto>.web.app`** no `.env` para o app mobile gerar o mesmo link ao copiar/compartilhar. |
| **PowerShell (Windows)** | Em versões onde **`&&`** não é aceito entre comandos, usar **`Set-Location caminho; npx expo export --platform web`** (ponto e vírgula) em vez de `cd ... && ...`. |
| **Hosting mostra site errado / vazio** | Confirmar que **`firebase.json` → `hosting.public`** aponta para **`dist`** após o export (não `public`). Rodar export de novo antes do deploy se mudou rotas ou env. |
| **Credenciais Firebase** | Se `firebase deploy` falhar com erro de login, rodar **`firebase login`** e garantir que **`.firebaserc`** aponta o **`default`** para o projeto correto. |

---

---

### 20.2 Instalação (padrão Expo)

```bash

---

# No projeto Expo, preferir expo install quando aplicável
npx expo install react-native-calendars
```

---

## 21. NOTIFICAÇÕES PUSH E LOCAIS — Expo Notifications

> Fonte: docs.expo.dev/push-notifications/overview · docs.expo.dev/versions/latest/sdk/notifications
> Caso de uso principal: alertas de agendamento em salão de beleza, lembretes de tarefas, notificações de novos itens.

---

# 1. Instalar expo-dev-client
npx expo install expo-dev-client

---

### 21.12 LashMatch — Expo Go e carregamento de `expo-notifications`

No **Expo Go** (a partir do SDK 53), notificações **push remotas** foram removidas; o próprio pacote `expo-notifications` pode disparar **warning/erro ao ser importado** (side effects como registro de token), mesmo que você só use notificações **locais**.

**Padrão implementado no LashMatch** (`hooks/useLembretesEnviados.ts`):

- Não importar `expo-notifications` estaticamente no topo do arquivo.
- No `useEffect`, se `Constants.appOwnership === 'expo'`, **retornar sem carregar** o módulo (nada de push/listener no Expo Go).
- Fora do Expo Go (dev build / APK): `await import('expo-notifications')` **dinâmico** dentro do efeito; em seguida `setNotificationHandler`, `requestPermissionsAsync`, `scheduleNotificationAsync`, etc.
- Assim o app continua abrindo no Expo Go sem poluir o console; em build de desenvolvimento o fluxo de notificação local ao receber `resumoLembretes/ultimo` funciona.

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · Curso React Native Expo Go — Caio Eduardo · Projeto LashMatch (referência principal) · [Utilizando react-native-calendars na prática](https://dev.to/marcoswillianr/utilizando-react-native-calendars-na-pratica-2egc) · docs.expo.dev/push-notifications/overview*

---

---

## 26. MERCADO PAGO — Checkout Pro com Expo + Firebase Functions

> Fonte: mercadopago.com.br/developers/pt/docs · docs.expo.dev
> Caso de uso: salão de beleza cobrando clientes pelo app (serviços, assinaturas de plano, etc.)

---

### 26.3 Instalação no app Expo

```bash