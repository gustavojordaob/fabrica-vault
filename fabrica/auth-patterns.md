---
tags:
  - firebase
  - auth
  - seguranca
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "4.1 Login com Email e Senha"
  - "4.2 Observar estado de autenticação (hook)"
  - "8.1 Tela de Login completa"
  - "12.10 Função de login com loading e validação"
  - "12.15 Tela de Login completa — padrão do curso"
---

### 4.1 Login com Email e Senha
```typescript
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { auth } from '../firebaseConfig';

// Criar conta
async function register(email: string, password: string) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  return userCredential.user;
}

// Login
async function login(email: string, password: string) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
}

// Logout
async function logout() {
  await signOut(auth);
}
```

---

### 4.2 Observar estado de autenticação (hook)
```typescript
import { useState, useEffect } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from '../firebaseConfig';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return unsubscribe; // cleanup — SEMPRE fazer isso
  }, []);

  return { user, loading };
}
```

---

### 8.1 Tela de Login completa
```typescript
import { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  ActivityIndicator, KeyboardAvoidingView, Platform, StyleSheet
} from 'react-native';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebaseConfig';
import { router } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const insets = useSafeAreaInsets();

  async function handleLogin() {
    setError('');
    setLoading(true);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      router.replace('/(tabs)/home');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      style={[styles.container, { paddingTop: insets.top }]}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <Text style={styles.title}>Entrar</Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <TextInput
        style={styles.input}
        placeholder="E-mail"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Senha"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TouchableOpacity style={styles.button} onPress={handleLogin} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Entrar</Text>}
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', backgroundColor: '#fff' },
  title: { fontSize: 28, fontWeight: '700', marginBottom: 24 },
  input: { borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12, marginBottom: 12, fontSize: 16 },
  button: { backgroundColor: '#2563eb', borderRadius: 8, padding: 14, alignItems: 'center' },
  buttonText: { color: '#fff', fontWeight: '600', fontSize: 16 },
  error: { color: '#ef4444', marginBottom: 12 },
});
```

---

### 12.10 Função de login com loading e validação
```typescript
import { Alert, ActivityIndicator } from 'react-native';

async function handleLogin() {
  // 1. Validação básica — campos vazios
  if (!email || !password) {
    Alert.alert('Atenção', 'Informe os campos obrigatórios');
    return;
  }

  // 2. Ativar loading
  setLoading(true);

  try {
    // 3. Lógica de autenticação (Firebase ou mock)
    await signInWithEmailAndPassword(auth, email, password);
    // redirecionar após login bem-sucedido
    router.replace('/(tabs)/home');
  } catch (error: any) {
    Alert.alert('Erro', error.message);
  } finally {
    // 4. Desativar loading sempre — mesmo em erro
    setLoading(false);
  }
}
```

---

### 12.15 Tela de Login completa — padrão do curso
```typescript
// src/pages/login/index.tsx
import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  Image, Alert, ActivityIndicator,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { styles } from './styles';
import { themes } from '../../global/themes';
import logo from '../../../assets/images/logo.png';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!email || !password) {
      Alert.alert('Atenção', 'Informe os campos obrigatórios');
      return;
    }
    setLoading(true);
    try {
      // substituir por: await signInWithEmailAndPassword(auth, email, password)
      await new Promise(resolve => setTimeout(resolve, 2000)); // mock
      Alert.alert('Sucesso', 'Logado com sucesso!');
    } catch (error: any) {
      Alert.alert('Erro', error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      {/* Topo */}
      <View style={styles.boxTop}>
        <Image source={logo} style={styles.logo} resizeMode="contain" />
        <Text style={styles.title}>Bem-vindo de volta</Text>
      </View>

      {/* Meio — formulário */}
      <View style={styles.boxMid}>
        <Text style={styles.titleInput}>Endereço de e-mail</Text>
        <View style={styles.boxInput}>
          <TextInput
            style={styles.input}
            placeholder="seu@email.com"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <MaterialIcons name="email" size={20} color={themes.colors.grey} />
        </View>

        <Text style={styles.titleInput}>Senha</Text>
        <View style={styles.boxInput}>
          <TextInput
            style={styles.input}
            placeholder="••••••••"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
          <MaterialIcons name="lock" size={20} color={themes.colors.grey} />
        </View>
      </View>

      {/* Base — botão */}
      <View style={styles.boxBottom}>
        <TouchableOpacity
          style={styles.button}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading
            ? <ActivityIndicator color="#fff" size="small" />
            : <Text style={styles.buttonText}>Entrar</Text>
          }
        </TouchableOpacity>

        <Text style={styles.textBottom}>
          Não tem conta?{' '}
          <Text style={{ color: themes.colors.primary }}>Crie agora</Text>
        </Text>
      </View>
    </View>
  );
}
```

```typescript
// src/pages/login/styles.ts
import { StyleSheet, Dimensions } from 'react-native';
import { themes } from '../../global/themes';

const { width, height } = Dimensions.get('window');

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: themes.colors.white,
  },
  boxTop: {
    width,
    height: height * 0.4,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 80,
    height: 80,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 40,
  },
  boxMid: {
    width,
    height: height * 0.35,
    paddingHorizontal: 37,
  },
  titleInput: {
    marginTop: 20,
    marginLeft: 5,
    color: themes.colors.grey,
  },
  boxInput: {
    width: '90%',
    height: 40,
    borderWidth: 1,
    borderRadius: 40,
    borderColor: themes.colors.lightGrey,
    backgroundColor: themes.colors.lightGrey,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    marginTop: 10,
  },
  input: {
    width: '90%',
    paddingLeft: 5,
  },
  boxBottom: {
    width,
    height: height * 0.25,
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingTop: 20,
  },
  button: {
    width: 250,
    height: 50,
    backgroundColor: themes.colors.primary,
    borderRadius: 40,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 5,
  },
  buttonText: {
    fontSize: 16,
    color: '#fff',
    fontWeight: 'bold',
  },
  textBottom: {
    fontSize: 16,
    marginTop: 20,
    color: themes.colors.grey,
  },
});
```

---

---

### 13.4 Usando o componente Input na tela de login
```typescript
// src/pages/login/index.tsx
import { Input } from '../../components/Input';
import { MaterialIcons } from '@expo/vector-icons';
import { useState } from 'react';

export default function Login() {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  return (
    <View style={styles.container}>
      {/* ... boxTop com logo ... */}

      <View style={styles.boxMid}>
        {/* Input de e-mail com ícone à direita */}
        <Input
          title="Endereço de e-mail"
          iconRight={MaterialIcons}
          iconRightName="email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          placeholder="seu@email.com"
        />

        {/* Input de senha com ícone de olho clicável */}
        <Input
          title="Senha"
          iconRight={MaterialIcons}
          iconRightName={showPassword ? 'visibility' : 'visibility-off'}
          onIconRightPress={() => setShowPassword(prev => !prev)}
          value={password}
          onChangeText={setPassword}
          secureTextEntry={!showPassword}
          placeholder="••••••••"
        />
      </View>

      {/* ... boxBottom com botão ... */}
    </View>
  );
}
```

> Antes eram ~40 linhas de código repetido. Agora são **2 componentes `<Input />`** cada um com ~8 linhas.

---

### 13.6 Usando o componente Button na tela de login
```typescript
import { Button } from '../../components/Button';

// Antes — código repetido
<TouchableOpacity style={styles.button} onPress={handleLogin} disabled={loading}>
  {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Entrar</Text>}
</TouchableOpacity>

// Depois — componente reutilizável
<Button
  text="Entrar"
  loading={loading}
  onPress={handleLogin}
/>
```

---

### 14.7 navigate vs reset — qual usar após login
```typescript
import { useNavigation } from '@react-navigation/native';

export function Login() {
  const navigation = useNavigation<any>();

  async function handleLogin() {
    // lógica de auth...

    // ❌ navigate — empilha a tela, usuário consegue voltar ao login
    navigation.navigate('bottomRoutes');

    // ✅ reset — substitui a pilha INTEIRA, não permite voltar ao login
    navigation.reset({
      index: 0,
      routes: [{ name: 'bottomRoutes' }],
    });
  }
}
```

> **Regra do curso:** após login bem-sucedido usar sempre **`navigation.reset()`**.
> Com `navigate`, o botão "voltar" leva de volta ao login.
> Com `reset`, a pilha é destruída — comportamento correto para autenticação.

---

### 18.6 Pattern de autenticação — `app/index.tsx`

O `index.tsx` é a tela de splash que redireciona baseado no estado de auth:

```typescript
// app/index.tsx — padrão LashMatch
import { useRouter } from 'expo-router';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';
import { app } from '../utils/firebaseConfig';

export default function Index() {
  const router = useRouter();
  const [initializing, setInitializing] = useState(true);

  useEffect(() => {
    const auth = getAuth(app);
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        router.replace('/(tabs)');
      } else {
        router.replace('/Login');
      }
      setInitializing(false);
    });
    return () => unsubscribe();
  }, []);

  if (initializing) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' }}>
        <ActivityIndicator size="large" color="#D63384" />
      </View>
    );
  }

  return null;
}
```

---

---

### 18.9 Padrão de tela com FlatList + onAuthStateChanged + useFocusEffect

Padrão usado em `clientes.tsx` e `index.tsx`:

```typescript
import { useFocusEffect, useRouter } from 'expo-router';
import { getAuth, onAuthStateChanged, User } from 'firebase/auth';
import { collection, getFirestore, onSnapshot, orderBy, query } from 'firebase/firestore';
import React, { useCallback, useEffect, useState } from 'react';
import { FlatList, SafeAreaView } from 'react-native';
import { app } from '../../utils/firebaseConfig';

export default function ClientesScreen() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [clients, setClients] = useState<Cliente[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // 1. Pega usuário logado
  useEffect(() => {
    const auth = getAuth(app);
    const unsubscribeAuth = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      if (!currentUser) setIsLoading(false);
    });
    return () => unsubscribeAuth();
  }, []);

  // 2. Recarrega dados toda vez que a tela recebe foco
  useFocusEffect(
    useCallback(() => {
      if (!user) return;
      setIsLoading(true);

      const db = getFirestore(app);
      const appId = app.options.appId!;
      const ref = collection(db, 'artifacts', appId, 'users', user.uid, 'clientes');
      const q = query(ref, orderBy('ultimaVisita', 'desc'));

      const unsubscribeDB = onSnapshot(q, (snapshot) => {
        const list = snapshot.docs.map(d => ({ id: d.id, ...d.data() } as Cliente));
        setClients(list);
        setIsLoading(false);
      });

      return () => unsubscribeDB();
    }, [user])
  );

  return (
    <SafeAreaView style={tw`flex-1 bg-black`}>
      <FlatList
        data={clients}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (/* card da cliente */)}
      />
    </SafeAreaView>
  );
}
```

---

## ⚠️ Google Sign-In no Expo Go — REGRA DA FÁBRICA

### ❌ NUNCA usar (não funciona no Expo Go)
npm install @react-native-google-signin/google-signin
Esse pacote requer código nativo compilado. Crasha imediatamente no Expo Go com erro:
`TurboModuleRegistry.getEnforcing: 'RNGoogleSignin' could not be found`

### ✅ SEMPRE usar (funciona no Expo Go)
npx expo install expo-auth-session expo-web-browser

Implementação correta:
```typescript
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import { GoogleAuthProvider, signInWithCredential } from 'firebase/auth';

WebBrowser.maybeCompleteAuthSession();

const [request, response, promptAsync] = Google.useAuthRequest({
  androidClientId: process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID_ANDROID,
  iosClientId: process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID_IOS,
  webClientId: process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID_WEB,
});

useEffect(() => {
  if (response?.type === 'success') {
    const { id_token } = response.params;
    const credential = GoogleAuthProvider.credential(id_token);
    signInWithCredential(auth, credential);
  }
}, [response]);
```

Variáveis de ambiente necessárias:
EXPO_PUBLIC_GOOGLE_CLIENT_ID_WEB=
EXPO_PUBLIC_GOOGLE_CLIENT_ID_ANDROID=
EXPO_PUBLIC_GOOGLE_CLIENT_ID_IOS=

---