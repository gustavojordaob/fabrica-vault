---
tags:
  - estado
  - context
  - react
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "15. CONTEXT API — Compartilhar dados entre telas (Caio Eduardo — Vídeo 4)"
  - "15.1 Problema que o Context resolve"
  - "15.3 Criando o Context e Provider"
  - "15.4 Aplicar o Provider nas rotas"
  - "15.6 Context para sessão do usuário (caso de uso comum)"
---

## 15. CONTEXT API — Compartilhar dados entre telas (Caio Eduardo — Vídeo 4)

> Conceito central: **Context** evita "prop drilling" — passar props por vários níveis de componentes. Dados e funções ficam acessíveis em qualquer componente dentro do Provider, sem precisar passar manualmente.

---

### 15.1 Problema que o Context resolve
Sem Context, para compartilhar uma função entre telas você precisaria:
- Criar o estado/função no componente pai
- Passar como prop para filho → neto → bisneto...
- Replicar código em múltiplos lugares (gambiarra)

```
❌ Sem Context — prop drilling
BottomRoutes
  ├── CustomTabBar (botão +)  ← precisa da função abrirModal
  ├── List                    ← também precisa
  └── User                    ← também precisa

Solução errada: criar o botão dentro das duas telas, replicar modal...
```

```
✅ Com Context — um Provider, qualquer filho acessa
BottomRoutes
  └── ListContextProvider      ← define a função uma vez só
        ├── CustomTabBar       ← usa onOpen diretamente
        ├── List               ← usa onOpen diretamente
        └── User               ← usa onOpen diretamente
```

---

### 15.3 Criando o Context e Provider
```typescript
// src/context/listContext.tsx
import React, { createContext, useContext, useState } from 'react';

// 1. Definir o tipo das propriedades do Context
type ListContextProps = {
  onOpen: () => void;           // função para abrir o modal
  modalVisible: boolean;        // estado de visibilidade do modal
  onClose: () => void;          // função para fechar o modal
};

// 2. Criar o Context com valor inicial nulo
export const ListContext = createContext<ListContextProps>({} as ListContextProps);

// 3. Criar o Provider — envolve os componentes que terão acesso
export function ListContextProvider({ children }: { children: React.ReactNode }) {
  const [modalVisible, setModalVisible] = useState(false);

  // Funções que ficam disponíveis para todos os filhos
  const onOpen = () => setModalVisible(true);
  const onClose = () => setModalVisible(false);

  return (
    <ListContext.Provider value={{ onOpen, modalVisible, onClose }}>
      {children}
    </ListContext.Provider>
  );
}

// 4. Hook customizado para consumir o Context (boa prática)
export const useListContext = () => useContext(ListContext);
```

---

### 15.4 Aplicar o Provider nas rotas
O Provider envolve **apenas** as telas que precisam dos dados.
No caso do curso: só as telas autenticadas (list + user) precisam — não o login.

```typescript
// src/routes/bottomRoutes.tsx
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { List } from '../pages/list';
import { User } from '../pages/user';
import { CustomTabBar } from '../components/CustomTabBar';
import { ListContextProvider } from '../context/listContext'; // ← importar

const Tab = createBottomTabNavigator();

export function BottomRoutes() {
  return (
    // ← Provider envolve tudo dentro do Bottom Tab
    <ListContextProvider>
      <Tab.Navigator
        tabBar={(props) => <CustomTabBar {...props} />}
        screenOptions={{ headerShown: false }}
      >
        <Tab.Screen name="list" component={List} />
        <Tab.Screen name="user" component={User} />
      </Tab.Navigator>
    </ListContextProvider>
  );
}
```

> Se colocar o Provider no `app.tsx`, os dados ficam acessíveis em **toda** a aplicação (incluindo login).
> Se colocar em `bottomRoutes.tsx`, ficam acessíveis **somente** nas telas autenticadas.
> Escolha o nível correto conforme a necessidade.

---

### 15.6 Context para sessão do usuário (caso de uso comum)
O curso menciona que o Context no `app.tsx` normalmente guarda **sessão e dados do usuário**.

```typescript
// src/context/authContext.tsx — padrão para autenticação
import React, { createContext, useContext, useState, useEffect } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from '../config/firebaseConfig';

type AuthContextProps = {
  user: User | null;
  loading: boolean;
  signed: boolean;
};

export const AuthContext = createContext<AuthContextProps>({} as AuthContextProps);

export function AuthContextProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return unsubscribe; // cleanup obrigatório
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, signed: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

```typescript
// app.tsx — Provider de auth envolve tudo
export default function App() {
  return (
    <NavigationContainer>
      <AuthContextProvider>
        <Routes />
      </AuthContextProvider>
    </NavigationContainer>
  );
}

// Nas rotas — redirecionar baseado na sessão
export function Routes() {
  const { signed, loading } = useAuth();

  if (loading) return <LoadingScreen />;

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {signed
        ? <Stack.Screen name="bottomRoutes" component={BottomRoutes} />
        : <Stack.Screen name="login" component={Login} />
      }
    </Stack.Navigator>
  );
}
```

---

### 15.7 Onde colocar cada Provider
| Provider               | Onde colocar        | Acessível em              |
|------------------------|---------------------|---------------------------|
| Auth / Sessão usuário  | `app.tsx`           | Todo o app                |
| Dados de telas autenticadas | `bottomRoutes.tsx` | Só telas autenticadas |
| Dados de um fluxo específico | Componente pai do fluxo | Só esse fluxo  |