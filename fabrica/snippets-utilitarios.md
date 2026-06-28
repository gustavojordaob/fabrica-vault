---
tags:
  - snippets
  - utilitarios
  - codigo
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "5.1 Operações CRUD básicas"
  - "11. COMANDOS FREQUENTES"
  - "12.3 Paleta de cores centralizada — `global/themes.ts`"
  - "12.5 Dimensões responsivas com `Dimensions`"
  - "12.8 Gerador de sombra para botões"
---

### 5.1 Operações CRUD básicas
```typescript
import {
  collection, doc, addDoc, setDoc, getDoc, getDocs,
  updateDoc, deleteDoc, query, where, orderBy, onSnapshot
} from 'firebase/firestore';
import { db } from '../firebaseConfig';

// CREATE — adicionar com ID automático
async function createPost(data: { title: string; userId: string }) {
  const docRef = await addDoc(collection(db, 'posts'), {
    ...data,
    createdAt: new Date(),
  });
  return docRef.id;
}

// CREATE — com ID definido
async function createUser(uid: string, data: object) {
  await setDoc(doc(db, 'users', uid), data);
}

// READ — documento único
async function getPost(id: string) {
  const docSnap = await getDoc(doc(db, 'posts', id));
  if (docSnap.exists()) return { id: docSnap.id, ...docSnap.data() };
  return null;
}

// READ — coleção com filtros
async function getPostsByUser(userId: string) {
  const q = query(
    collection(db, 'posts'),
    where('userId', '==', userId),
    orderBy('createdAt', 'desc')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
}

// UPDATE
async function updatePost(id: string, data: Partial<Post>) {
  await updateDoc(doc(db, 'posts', id), data);
}

// DELETE
async function deletePost(id: string) {
  await deleteDoc(doc(db, 'posts', id));
}
```

---

## 11. COMANDOS FREQUENTES

```bash

---

### 12.3 Paleta de cores centralizada — `global/themes.ts`
```typescript
// src/global/themes.ts
export const themes = {
  colors: {
    primary: '#4F67FB',      // azul principal — botões, links
    grey: '#A0A0A0',         // ícones, placeholders
    lightGrey: '#F5F5F5',    // background de inputs
    white: '#FFFFFF',
    black: '#1A1A1A',
    orange: '#FF6B35',       // destaques / alertas suaves
  },
};
```

**Regra do curso:** nunca usar cores hardcoded no componente. Sempre importar de `themes.ts`.
```typescript
// ✅ certo
color: themes.colors.primary

// ❌ errado
color: '#4F67FB'
```

Motivo: quando quiser mudar a cor primária do app inteiro, você muda em um único lugar.

---

### 12.5 Dimensões responsivas com `Dimensions`
```typescript
import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

// Usar nas styles para ser responsivo por tamanho de tela
const styles = StyleSheet.create({
  boxTop: {
    width: width,
    height: height * 0.4,    // 40% da altura da tela
  },
  boxMid: {
    width: width,
    height: height * 0.3,    // 30% da altura
  },
  boxBottom: {
    width: width,
    height: height * 0.3,    // 30% da altura
  },
});
```

> Nunca usar pixels fixos para altura de seções grandes — o app vai quebrar em telas diferentes.

---

### 12.8 Gerador de sombra para botões
O curso indica usar geradores online de `boxShadow` para React Native.
Padrão de sombra elegante para botões:
```typescript
button: {
  width: 250,
  height: 50,
  backgroundColor: themes.colors.primary,
  borderRadius: 40,
  alignItems: 'center',
  justifyContent: 'center',
  // sombra iOS
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 4 },
  shadowOpacity: 0.2,
  shadowRadius: 6,
  // sombra Android
  elevation: 5,
},
buttonText: {
  fontSize: 16,
  color: '#fff',
  fontWeight: 'bold',
},
```

---

### 18.1 Identidade visual e cores

```typescript
// Paleta principal do LashMatch — usar sempre estas cores
const COLORS = {
  primary:     '#D63384',   // rosa principal — botões, destaques, ícones
  background:  '#000000',   // fundo geral — telas são pretas
  surface:     '#1a1a1a',   // cards, modais, inputs
  border:      '#333333',   // bordas de cards e inputs
  borderLight: '#222222',   // bordas mais sutis
  text:        '#FFFFFF',   // texto principal
  textMuted:   '#9e9e9e',   // placeholders, subtítulos
  textSecond:  '#AAAAAA',   // textos secundários
  error:       '#ff4d4d',   // mensagens de erro
  success:     '#4ade80',   // confirmações, modo manual
};
```

---