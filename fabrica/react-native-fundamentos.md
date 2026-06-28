---
tags:
  - react-native
  - fundamentos
  - ui
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "CONTEXT.md — Agente React Native + Firebase + Expo"
  - "1. FUNDAMENTOS REACT NATIVE"
  - "1.1 O que é React Native"
  - "1.2 Core Components essenciais"
  - "1.3 Estilo com StyleSheet"
---

# CONTEXT.md — Agente React Native + Firebase + Expo
> Base de conhecimento consolidada para o Agente Dev de Telas (AGT-03) e Agente Firebase (AGT-04).
> Fontes: reactnative.dev/docs, docs.expo.dev/guides/using-firebase, docs.expo.dev/tutorial
> Versões de referência: React Native 0.85 · Expo SDK 54 · Firebase JS SDK ^12.0.0

---

---

## 1. FUNDAMENTOS REACT NATIVE

---

### 1.1 O que é React Native
- Framework open-source da Meta para criar apps Android e iOS com React + JavaScript/TypeScript.
- Componentes React são mapeados para Views nativas reais (não WebView).
- Um único codebase roda em iOS, Android e Web (com Expo).

---

### 1.2 Core Components essenciais
| Componente RN     | Equivalente Android | Equivalente iOS  | Equivalente Web      | Uso                              |
|-------------------|---------------------|------------------|----------------------|----------------------------------|
| `<View>`          | ViewGroup           | UIView           | `<div>` não-scrollável| Container de layout (flexbox)    |
| `<Text>`          | TextView            | UITextView       | `<p>`                | Exibir texto; suporta onPress    |
| `<Image>`         | ImageView           | UIImageView      | `<img>`              | Imagens locais e remotas         |
| `<ScrollView>`    | ScrollView          | UIScrollView     | `<div>` com scroll   | Container com scroll livre       |
| `<FlatList>`      | RecyclerView        | UICollectionView | Virtual list         | Listas longas com boa performance|
| `<TextInput>`     | EditText            | UITextField      | `<input type="text">`| Campo de entrada de texto        |
| `<TouchableOpacity>` / `<Pressable>` | — | — | `<button>`        | Elementos clicáveis com feedback |
| `<ActivityIndicator>` | ProgressBar    | UIActivityIndicator | spinner CSS       | Loading spinner                  |
| `<Modal>`         | Dialog              | UIModalPresentationController | dialog | Sobreposição modal             |
| `<KeyboardAvoidingView>` | —          | —                | —                    | Evitar teclado virtual sobrepor conteúdo |

---

### 1.3 Estilo com StyleSheet
- Estilos são objetos JavaScript — não CSS. Propriedades em camelCase: `backgroundColor`, não `background-color`.
- Use sempre `StyleSheet.create({})` para melhor performance (valida em tempo de desenvolvimento).
- O prop `style` aceita objeto único ou array: `style={[styles.base, styles.extra]}` — o último tem precedência.

```typescript
import { StyleSheet, View, Text } from 'react-native';

export default function Card() {
  return (
    <View style={[styles.container, styles.shadow]}>
      <Text style={styles.title}>Olá</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16,
  },
  shadow: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    elevation: 3, // Android
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
  },
});
```

---

### 1.4 Flexbox no React Native (diferenças do CSS web)
| Propriedade       | Padrão RN        | Padrão CSS Web  |
|-------------------|------------------|-----------------|
| `flexDirection`   | `'column'`       | `'row'`         |
| `alignContent`    | `'flex-start'`   | `'stretch'`     |
| `flexShrink`      | `0`              | `1`             |
| `flex`            | número único     | shorthand       |

Regras fundamentais:
- `flexDirection: 'column'` → filhos empilham verticalmente (padrão).
- `flexDirection: 'row'` → filhos ficam lado a lado.
- `justifyContent` → alinha no eixo principal.
- `alignItems` → alinha no eixo cruzado.
- `flex: 1` em filho → ocupa todo o espaço disponível.

```typescript
// Centralizar conteúdo na tela
container: {
  flex: 1,
  justifyContent: 'center',
  alignItems: 'center',
},
// Linha com espaçamento
row: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
},
```

---

### 1.5 Safe Areas e Teclado
- **Sempre** usar `useSafeAreaInsets()` ou `<SafeAreaView>` para respeitar notch e home indicator.
- **Sempre** envolver formulários em `<KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>`.

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function FormScreen() {
  const insets = useSafeAreaInsets();
  return (
    <KeyboardAvoidingView
      style={{ flex: 1, paddingTop: insets.top }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* conteúdo do formulário */}
    </KeyboardAvoidingView>
  );
}
```

---

---

### 3.1 Dois caminhos: JS SDK vs React Native Firebase

| Critério                          | Firebase JS SDK              | React Native Firebase         |
|-----------------------------------|------------------------------|-------------------------------|
| Funciona no Expo Go               | ✅ Sim                        | ❌ Não (precisa dev build)     |
| Setup                             | Simples (npm install)        | Complexo (native code)        |
| Auth, Firestore, Storage          | ✅ Suportado                  | ✅ Suportado                   |
| Analytics, Crashlytics            | ❌ Não suportado              | ✅ Suportado                   |
| Performance nativa                | JS bridge                    | SDK nativo                    |
| **Recomendação para começar**     | **✅ Use este**               | Só se precisar de Analytics   |

---

## 7. REACT NATIVE FIREBASE (quando usar)

---

## 12. APRENDIZADOS DO CURSO — React Native com Expo Go (Caio Eduardo)
> Extraído da transcrição do curso em vídeo da playlist PLN5FV-HmjCA8UKWLep7O31PtQYqML8-Wd

---

### 14.1 Tipos de navegação no React Native
| Tipo              | Uso                                          | Biblioteca                          |
|-------------------|----------------------------------------------|-------------------------------------|
| **Stack**         | Pilha de telas (login → home → detalhe)      | `@react-navigation/native-stack`    |
| **Bottom Tabs**   | Abas na parte inferior (home, perfil, etc.)  | `@react-navigation/bottom-tabs`     |
| **Drawer**        | Gaveta lateral (menu hambúrguer)             | `@react-navigation/drawer`          |

---

### 16.9 Propriedade `gap` no Flexbox
```typescript
// gap — espaçamento uniforme entre todos os filhos
// Alternativa mais limpa que usar marginRight/marginBottom em cada filho

rowCardLeft: {
  flexDirection: 'row',
  alignItems: 'center',
  gap: 10,   // 10px entre cada filho
},

flagRow: {
  flexDirection: 'row',
  gap: 8,    // 8px entre as flags
},

// Disponível no React Native 0.71+ / Expo SDK 48+
```

---

### 18.8 Sistema de estilos — mistura proposital de `twrnc` + `StyleSheet`

O LashMatch usa **dois sistemas de estilo** intencionalmente:
- `twrnc` (`tw`) para layouts rápidos e responsivos inline
- `StyleSheet.create` para componentes complexos e reutilizáveis

```typescript
import tw from 'twrnc';
import { StyleSheet } from 'react-native';

// tw() — para layouts inline, cores dinâmicas do tema
<View style={tw`flex-1 bg-black px-4`}>
<Text style={tw`text-white text-xl font-bold`}>

// StyleSheet.create — para estilos fixos e reutilizados
<View style={styles.modalContainer}>
<Text style={styles.modalTitle}>

// Mistura (padrão frequente no LashMatch)
<TouchableOpacity style={[styles.modalButton, tw`bg-[#D63384] border-0`]}>
```

```typescript
// styles padrão de modal no LashMatch
const styles = StyleSheet.create({
  modalBackdrop: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContainer: {
    backgroundColor: '#0d0d0d',
    borderTopLeftRadius: 26,
    borderTopRightRadius: 26,
    padding: 24,
    maxHeight: '82%',
    borderWidth: 1,
    borderColor: '#222',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
    marginTop: 24,
  },
  modalInput: {
    borderWidth: 1,
    borderColor: '#333',
    backgroundColor: '#111',
    padding: 16,
    borderRadius: 12,
    fontSize: 16,
    color: '#fff',
    marginBottom: 14,
  },
  modalButton: {
    backgroundColor: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#333',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
});
```

---

---

## 20. CALENDÁRIO NO REACT NATIVE — Padrão para agentes (react-native-calendars)

> Baseado em prática de implementação com `react-native-calendars`, adaptado para os padrões visuais e arquiteturais do LashMatch.