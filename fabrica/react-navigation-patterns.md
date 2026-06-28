---
tags:
  - navegacao
  - react-navigation
  - tabs
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "3. Stack Navigator"
  - "4. Bottom Tab Navigator"
  - "14.4 Stack Navigator — raiz do app"
  - "14.5 Bottom Tab Navigator — telas autenticadas"
  - "14.8 Custom Tab Bar — barra personalizada"
---

# 3. Stack Navigator
npm install @react-navigation/native-stack

---

# 4. Bottom Tab Navigator
npm install @react-navigation/bottom-tabs
```

Adicionar no topo do `app.tsx` (obrigatório para finalizar instalação):
```typescript
// app.tsx — PRIMEIRA linha, antes de qualquer import
import 'react-native-gesture-handler';
```

---

### 14.4 Stack Navigator — raiz do app
```typescript
// src/routes/index.tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Login } from '../pages/login';
import { BottomRoutes } from './bottomRoutes';

const Stack = createNativeStackNavigator();

export function Routes() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false, backgroundColor: '#fff' }}>
      <Stack.Screen name="login" component={Login} />
      <Stack.Screen name="bottomRoutes" component={BottomRoutes} />
    </Stack.Navigator>
  );
}
```

---

### 14.5 Bottom Tab Navigator — telas autenticadas
```typescript
// src/routes/bottomRoutes.tsx
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { List } from '../pages/list';
import { User } from '../pages/user';
import { CustomTabBar } from '../components/CustomTabBar';

const Tab = createBottomTabNavigator();

export function BottomRoutes() {
  return (
    <Tab.Navigator
      tabBar={(props) => <CustomTabBar {...props} />}
      screenOptions={{ headerShown: false }}
    >
      <Tab.Screen name="list" component={List} />
      <Tab.Screen name="user" component={User} />
    </Tab.Navigator>
  );
}
```

---

### 14.8 Custom Tab Bar — barra personalizada
```typescript
// src/components/CustomTabBar/index.tsx
import React from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import { BottomTabBarProps } from '@react-navigation/bottom-tabs';
import { AntDesign, FontAwesome } from '@expo/vector-icons';
import { themes } from '../../global/themes';

export function CustomTabBar({ state, navigation }: BottomTabBarProps) {

  const go = (screen: string) => navigation.navigate(screen);

  return (
    <View style={styles.tabArea}>

      {/* Aba 0 — Lista */}
      <TouchableOpacity style={styles.tabItem} onPress={() => go('list')}>
        <AntDesign
          name="bars"
          size={32}
          color={themes.colors.primary}
          style={{ opacity: state.index === 0 ? 1 : 0.3 }}
        />
      </TouchableOpacity>

      {/* Botão central flutuante */}
      <TouchableOpacity style={styles.tabItem}>
        <View style={styles.buttonInner}>
          <AntDesign name="plus" size={24} color="#fff" />
        </View>
      </TouchableOpacity>

      {/* Aba 1 — Usuário */}
      <TouchableOpacity style={styles.tabItem} onPress={() => go('user')}>
        <FontAwesome
          name="user"
          size={32}
          color={themes.colors.primary}
          style={{ opacity: state.index === 1 ? 1 : 0.3 }}
        />
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  tabArea: {
    width: '80%',
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignSelf: 'center',
    backgroundColor: '#fff',
    borderRadius: 40,
    paddingVertical: 10,
    marginBottom: 10,
    // sombra iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    // sombra Android
    elevation: 8,
  },
  tabItem: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonInner: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: themes.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 99,      // sempre na frente
    marginTop: -30,  // flutua acima da tab bar
  },
});
```