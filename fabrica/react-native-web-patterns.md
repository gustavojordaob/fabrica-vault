---
tags:
  - react-native-web
  - expo-web
  - responsivo
  - compatibilidade
fonte: fabrica-knowledge
gerado_em: 2026-05-17
---

# React Native Web — Padrões da Fábrica

> Regras obrigatórias para garantir que o app funcione
> tanto no celular quanto no navegador web.

---

## ⚠️ Regra geral da fábrica

**Antes de gerar qualquer componente, verifique:**
- Funciona no iOS/Android? ✅
- Funciona no navegador web? ✅
- Ícones carregam no web? ✅
- Layout não quebra no desktop? ✅

---

## 1. Ícones — o problema mais comum

### ❌ NUNCA usar assim (quebra no web)
```typescript
import { Ionicons } from '@expo/vector-icons';

<Ionicons name="home" size={24} color="white" />
```

### ✅ SEMPRE usar com fallback web
```typescript
import { Ionicons } from '@expo/vector-icons';
import { Platform } from 'react-native';

// Opção 1 — forçar carregamento da fonte no web
import * as Font from 'expo-font';
import { useEffect } from 'react';

export function useIconFont() {
  useEffect(() => {
    if (Platform.OS === 'web') {
      Font.loadAsync({
        IoniconsFont: require('@expo/vector-icons/build/vendor/react-native-vector-icons/Fonts/Ionicons.ttf'),
      });
    }
  }, []);
}

// Opção 2 — usar emoji como fallback no web
const IconHome = () => Platform.OS === 'web'
  ? <Text>🏠</Text>
  : <Ionicons name="home" size={24} color="white" />;
```

### ✅ Melhor solução — configurar no app.json
```json
{
  "expo": {
    "web": {
      "bundler": "metro",
      "favicon": "./assets/favicon.png"
    },
    "plugins": [
      [
        "expo-font",
        {
          "fonts": [
            "node_modules/@expo/vector-icons/build/vendor/react-native-vector-icons/Fonts/Ionicons.ttf",
            "node_modules/@expo/vector-icons/build/vendor/react-native-vector-icons/Fonts/MaterialIcons.ttf",
            "node_modules/@expo/vector-icons/build/vendor/react-native-vector-icons/Fonts/FontAwesome.ttf"
          ]
        }
      ]
    ]
  }
}
```

---

## 2. Dimensões e Layout Responsivo

### ❌ NUNCA usar dimensões fixas
```typescript
const styles = StyleSheet.create({
  container: {
    width: 390,   // largura fixa do iPhone
    height: 844,  // altura fixa
  }
});
```

### ✅ SEMPRE usar dimensões relativas
```typescript
import { useWindowDimensions, Platform } from 'react-native';

export function useResponsive() {
  const { width, height } = useWindowDimensions();

  return {
    isMobile:  width < 768,
    isTablet:  width >= 768 && width < 1024,
    isDesktop: width >= 1024,
    width,
    height,
    // Largura máxima para conteúdo no web
    contentWidth: Platform.OS === 'web'
      ? Math.min(width, 480)  // limita a 480px no web
      : width,
  };
}

// Uso no componente:
const { isMobile, isDesktop, contentWidth } = useResponsive();

<View style={{ width: contentWidth, alignSelf: 'center' }}>
  {/* conteúdo */}
</View>
```

---

## 3. Container Principal — Web vs Mobile

### ✅ Layout padrão da fábrica para web
```typescript
import { Platform, View, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export function AppContainer({ children }) {
  if (Platform.OS === 'web') {
    return (
      <View style={styles.webContainer}>
        <View style={styles.webContent}>
          {children}
        </View>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.mobileContainer}>
      {children}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  // Web: centraliza o app como se fosse um celular
  webContainer: {
    flex: 1,
    backgroundColor: '#0F0F0F', // fundo escuro fora do app
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
  },
  webContent: {
    width: '100%',
    maxWidth: 480,    // simula largura de celular
    minHeight: '100vh',
    backgroundColor: Colors.background,
    overflow: 'hidden',
  },
  // Mobile: normal
  mobileContainer: {
    flex: 1,
    backgroundColor: Colors.background,
  },
});
```

---

## 4. Sombras — diferente no web

### ❌ Sombra que só funciona no mobile
```typescript
const styles = StyleSheet.create({
  card: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,  // só Android
  }
});
```

### ✅ Sombra que funciona em todos
```typescript
import { Platform } from 'react-native';

const cardShadow = Platform.select({
  web: {
    boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.3)',
  },
  ios: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  android: {
    elevation: 5,
  },
});

const styles = StyleSheet.create({
  card: {
    ...cardShadow,
    borderRadius: 12,
  }
});
```

---

## 5. Cursor e Hover no Web

### ✅ Adicionar cursor pointer em botões no web
```typescript
import { Platform, TouchableOpacity } from 'react-native';

export function Button({ onPress, children, style }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={[
        styles.button,
        style,
        // cursor pointer só no web
        Platform.OS === 'web' && { cursor: 'pointer' },
      ]}
    >
      {children}
    </TouchableOpacity>
  );
}
```

---

## 6. ScrollView e overflow no Web

### ❌ ScrollView que vaza no web
```typescript
<ScrollView>
  <View style={{ height: 2000 }}>
    {/* conteúdo longo */}
  </View>
</ScrollView>
```

### ✅ ScrollView compatível com web
```typescript
import { Platform } from 'react-native';

<ScrollView
  showsVerticalScrollIndicator={false}
  contentContainerStyle={{ flexGrow: 1 }}
  style={[
    { flex: 1 },
    Platform.OS === 'web' && {
      overflow: 'auto',   // web precisa disso
      height: '100vh',
    }
  ]}
>
  {/* conteúdo */}
</ScrollView>
```

---

## 7. Inputs e Teclado no Web

### ✅ Input sem outline azul no web
```typescript
<TextInput
  style={[
    styles.input,
    Platform.OS === 'web' && {
      outlineStyle: 'none',  // remove outline azul padrão do browser
    }
  ]}
/>
```

---

## 8. Imagens Responsivas

### ✅ Imagem que adapta ao container
```typescript
import { Image, useWindowDimensions } from 'react-native';

export function ResponsiveImage({ source, aspectRatio = 1 }) {
  const { width } = useWindowDimensions();
  const imageWidth = Math.min(width, 480);  // máximo 480px no web

  return (
    <Image
      source={source}
      style={{
        width: imageWidth,
        height: imageWidth / aspectRatio,
        resizeMode: 'cover',
      }}
    />
  );
}
```

---

## 9. Navegação no Web — URLs amigáveis

### ✅ Configurar linking no Expo Router
```typescript
// app.json
{
  "expo": {
    "scheme": "setmatch",
    "web": {
      "bundler": "metro"
    }
  }
}

// Expo Router já gera URLs automáticas:
// /            → app/(tabs)/home
// /perfil      → app/(tabs)/perfil
// /jogador/123 → app/jogador/[uid]
```

---

## 10. Checklist antes de subir feature com web

- [ ] Testou no navegador com `npx expo start --web`?
- [ ] Ícones aparecem no web?
- [ ] Layout não quebra em tela larga (1440px)?
- [ ] Layout não quebra em tela estreita (375px)?
- [ ] Botões têm `cursor: pointer` no web?
- [ ] Inputs sem outline azul?
- [ ] Sombras aparecem no web?
- [ ] ScrollView funciona no web?
- [ ] Imagens não saem do container?
- [ ] Fontes customizadas carregam no web?

---

## 11. Testar localmente no web

```bash
# Rodar no web
npx expo start --web

# Rodar web em porta específica
npx expo start --web --port 3000

# Build web para produção
npx expo export --platform web
```

---

## 12. Problemas mais comuns e soluções rápidas

| Problema | Causa | Solução |
|----------|-------|---------|
| Ícones não aparecem | Fonte não carregada | Adicionar no `app.json plugins` |
| Layout todo centralizado estranhamente | `alignItems: center` no root | Usar `AppContainer` da fábrica |
| Botão sem feedback visual | Sem `cursor: pointer` | Adicionar via `Platform.select` |
| Input com borda azul | Outline padrão do browser | `outlineStyle: none` |
| Scroll não funciona | `overflow: hidden` no container | `overflow: auto` no web |
| Sombra não aparece | `elevation` só funciona no Android | Usar `boxShadow` no web |
| App muito largo no desktop | Sem `maxWidth` | Container com `maxWidth: 480` |
| Fonte customizada não carrega | Não configurada para web | `expo-font` no `app.json` |

---

*Última atualização: 17/05/2026 | Fábrica de Software*
