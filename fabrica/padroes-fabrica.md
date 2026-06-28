---
tags:
  - padroes
  - fabrica
  - lashmatch
fonte: obsidian/fabrica/padroes-fabrica.md
gerado_em: 2026-05-11
secoes:
  - "2.2 Criar projeto"
  - "12.1 Setup inicial do projeto"
  - "Criar projeto com template TypeScript limpo (sem boilerplate)"
  - "12.7 Input com ícone — padrão `boxInput`"
  - "14.11 Remover header padrão"
---

### 2.2 Criar projeto
```bash
npx create-expo-app@latest MeuApp
cd MeuApp
npx expo start        # abre o dev server

---

### 12.1 Setup inicial do projeto
```bash

---

# Criar projeto com template TypeScript limpo (sem boilerplate)
npx create-expo-app@latest --template blank-typescript my-list

---

### 12.7 Input com ícone — padrão `boxInput`
Não existe como colocar ícone dentro do `TextInput` nativo. A solução do curso é criar uma `View` em `flexDirection: 'row'` que agrupa o `TextInput` + ícone:

```typescript
import { MaterialIcons } from '@expo/vector-icons';
import { themes } from '../../global/themes';

// Dentro do JSX:
<View style={styles.boxInput}>
  <TextInput
    style={styles.input}
    placeholder="Endereço de e-mail"
    value={email}
    onChangeText={setEmail}
    keyboardType="email-address"
    autoCapitalize="none"
  />
  <MaterialIcons name="email" size={20} color={themes.colors.grey} />
</View>

<View style={styles.boxInput}>
  <TextInput
    style={styles.input}
    placeholder="Senha"
    value={password}
    onChangeText={setPassword}
    secureTextEntry
  />
  <MaterialIcons name="lock" size={20} color={themes.colors.grey} />
</View>
```

```typescript
// styles.ts
boxInput: {
  width: '90%',
  height: 40,
  borderWidth: 1,
  borderRadius: 40,
  borderColor: themes.colors.lightGrey,
  backgroundColor: themes.colors.lightGrey,
  flexDirection: 'row',         // ← ícone e input lado a lado
  alignItems: 'center',
  paddingHorizontal: 10,
  marginTop: 10,
},
input: {
  width: '90%',
  paddingLeft: 5,
},
```

Instalar biblioteca de ícones:
```bash
npx expo install @expo/vector-icons

---

### 14.11 Remover header padrão
```typescript
// Para todas as telas do Navigator
<Stack.Navigator screenOptions={{ headerShown: false }}>
<Tab.Navigator screenOptions={{ headerShown: false }}>

// Para uma tela específica
<Stack.Screen name="login" component={Login} options={{ headerShown: false }} />
```

---

## 18. PADRÕES DO PROJETO REAL — LashMatch (Referência Principal)

> Esta seção documenta os padrões reais usados no app **LashMatch** — um app de análise facial com IA para lash designers. Todo código novo deve seguir esses padrões.

---

---

### 18.10 Interfaces TypeScript do projeto

```typescript
// Tipos principais do LashMatch
type TomPele = 'Muito clara' | 'Clara' | 'Média' | 'Morena clara' | 'Morena' | 'Preta';

interface Cliente {
  id: string;
  nome: string;
  nomeCompleto?: string;
  nomePrimeiro?: string;
  sobrenome?: string;
  telefone?: string | null;
  dataNascimento?: string | null;
  tomPele?: TomPele;
  fotoUrl?: string;
  dataCadastro?: any;       // Timestamp do Firestore
  ultimaVisita?: any;       // Timestamp do Firestore
  ultimaAnalise?: {
    estilo: string;
    formatoRosto: string;
  } | null;
}

interface AnaliseHistorico {
  id: string;
  data: any;
  modoAnalise?: 'ia' | 'manual';
  estilo: string;
  formatoRosto: string;
  eixo: string;
  profundidade: string;
  alinhamento: string;
  distanciamento: string;
  // ... demais campos de análise
}

// Enum para controle de views no modal (padrão LashMatch)
enum ModalView {
  OPTIONS    = 'options',
  NEW        = 'new',
  EXISTING   = 'existing',
  SELECT_MODE = 'select_mode',
}
```

---

---

### 18.11 Modal nativo com múltiplas views (padrão LashMatch)

O LashMatch usa um único `<Modal>` com um `enum` controlando o conteúdo — evita abrir múltiplos modais:

```typescript
const [isModalVisible, setIsModalVisible] = useState(false);
const [modalView, setModalView] = useState<ModalView>(ModalView.OPTIONS);

// Função que renderiza o conteúdo correto baseado no estado
const renderModalContent = () => {
  if (modalView === ModalView.OPTIONS) return <OptionsView />;
  if (modalView === ModalView.NEW)     return <NewClientForm />;
  if (modalView === ModalView.EXISTING) return <ExistingClientList />;
  if (modalView === ModalView.SELECT_MODE) return <SelectModeView />;
  return null;
};

// JSX do modal
<Modal
  animationType="slide"
  transparent
  visible={isModalVisible}
  onRequestClose={() => setIsModalVisible(false)}
>
  <KeyboardAvoidingView
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    style={styles.modalBackdrop}
  >
    <View style={styles.modalContainer}>
      {/* Lista usa View direta; formulários usam ScrollView */}
      {modalView === ModalView.EXISTING ? (
        <View>{renderModalContent()}</View>
      ) : (
        <ScrollView keyboardShouldPersistTaps="handled">
          {renderModalContent()}
        </ScrollView>
      )}
    </View>
  </KeyboardAvoidingView>
</Modal>
```

> **Insight do LashMatch:** quando o modal contém uma `FlatList`, colocá-la dentro de `ScrollView` quebra a rolagem. Usar `View` direta com `height` fixo para o container da lista.

---

---

### 18.13 Formatação e validação de dados BR (padrão LashMatch)

```typescript
// Telefone brasileiro — máscara automática
function normalizePhoneBR(input: string): string {
  const d = input.replace(/\D/g, '').slice(0, 11);
  if (!d) return '';
  if (d.length <= 2)  return `(${d}`;
  if (d.length <= 7)  return `(${d.slice(0,2)}) ${d.slice(2)}`;
  return `(${d.slice(0,2)}) ${d.slice(2,7)}-${d.slice(7)}`;
}

function isValidPhoneBR(v: string): boolean {
  const d = v.replace(/\D/g, '');
  return d.length === 10 || d.length === 11;
}

// Data de nascimento — máscara DD/MM/AAAA
function formatBirthDateBR(value: string): string {
  const digits = value.replace(/\D/g, '').slice(0, 8);
  if (digits.length <= 2) return digits;
  if (digits.length <= 4) return `${digits.slice(0,2)}/${digits.slice(2)}`;
  return `${digits.slice(0,2)}/${digits.slice(2,4)}/${digits.slice(4)}`;
}

function isValidBirthDateBR(v: string): boolean {
  if (!/^\d{2}\/\d{2}\/\d{4}$/.test(v)) return false;
  const [dd, mm, yyyy] = v.split('/').map(Number);
  const d = new Date(yyyy, mm - 1, dd);
  return d.getFullYear() === yyyy && d.getMonth() === mm - 1 && d.getDate() === dd;
}

// Nome — capitalizar cada palavra
function capitalizeName(name: string): string {
  return name.trim().split(/\s+/)
    .map(p => p.charAt(0).toUpperCase() + p.slice(1).toLowerCase())
    .join(' ');
}

// Primeiro nome
function getFirstName(fullName: string | null): string {
  if (!fullName) return 'Lash';
  const first = fullName.split(' ')[0];
  return first.charAt(0).toUpperCase() + first.slice(1).toLowerCase();
}
```

---

---

### 18.15 Padrão de input com opacity baseado em validação

```typescript
// Botão desabilitado visualmente quando campos vazios — padrão LashMatch
<TouchableOpacity
  style={[styles.button, { opacity: !email || !senha ? 0.4 : 1 }]}
  onPress={handleLogin}
  disabled={!email || !senha}
>
  <Text style={styles.buttonText}>Entrar</Text>
</TouchableOpacity>
```

---

---

### 18.16 Chips de seleção (tom de pele, flags) — padrão LashMatch

```typescript
// Chips com estado selecionado — grid responsivo
<View style={styles.toneGrid}>
  {TONS_PELE.map((tone) => (
    <TouchableOpacity
      key={tone}
      onPress={() => setNewClientSkinTone(tone)}
      style={[
        styles.toneChip,
        newClientSkinTone === tone && styles.toneChipSelected,
      ]}
    >
      <Text style={[
        styles.toneChipText,
        newClientSkinTone === tone && styles.toneChipTextSelected,
      ]}>
        {tone}
      </Text>
    </TouchableOpacity>
  ))}
</View>

// styles
toneGrid:             { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 10 },
toneChip:             { paddingVertical: 10, paddingHorizontal: 12, borderRadius: 999, backgroundColor: '#111', borderWidth: 1, borderColor: '#333' },
toneChipSelected:     { backgroundColor: '#D63384', borderColor: '#D63384' },
toneChipText:         { color: '#ddd', fontWeight: '600', fontSize: 13 },
toneChipTextSelected: { color: '#fff' },
```

---

---

### 18.18 Padrão de módulo de estoque (LashMatch)

> Implementação base registrada em `app/(tabs)/estoque.tsx`.

#### Rota e navegação
- Nova aba: `/(tabs)/estoque`
- Registrar no `app/(tabs)/_layout.tsx` com ícone (`Ionicons`, ex.: `cube-outline`).

#### Path Firestore (padrão obrigatório)
```typescript
const appId = app.options.appId;
const ref = collection(firestore, 'artifacts', appId, 'users', user.uid, 'estoque');
```

> Nunca hardcodar `appId`; sempre usar `app.options.appId`.

#### Estrutura do documento de produto
```typescript
interface ProdutoEstoque {
  id: string;
  nome: string;
  tipo: 'Cílios' | 'Cola para cílios';
  quantidade: number;
  minimo: number;
  ativo: boolean;
}
```

Campos persistidos:
- `nome`, `tipo`, `quantidade`, `minimo`, `ativo`
- `criadoEm`, `atualizadoEm` com `serverTimestamp()`

#### Seed inicial de produtos
- Ao abrir a tela e a coleção estar vazia, inserir automaticamente:
  - `Cílios`
  - `Cola para cílios`

#### Comportamento de tela (MVP estoque)
- Listagem com `FlatList` e cards por produto
- CRUD básico:
  - inserir produto
  - editar produto
  - ajustar quantidade (`+1` / `-1`)
  - inativar produto (sem delete físico)
- Busca por nome (`TextInput`)
- Filtro por tipo com chips (`Todos`, `Cílios`, `Cola para cílios`)
- Regra de alerta: `quantidade <= minimo`
  - destacar card
  - badge de "Estoque baixo"
  - banner de alerta no topo

#### Padrões visuais
- Tela em fundo preto (`#000`)
- Destaques e CTA com primária `#D63384`
- Superfície de cards/modais em tons escuros (`#1a1a1a` / `#0d0d0d`)
- Modal com `KeyboardAvoidingView` + `ScrollView keyboardShouldPersistTaps="handled"`

---

---

### 20.1 Quando usar no LashMatch

Use calendário quando precisar de:
- seleção de data para agendamento de retorno;
- filtro de histórico por dia;
- definição de prazo/validade em fluxo de estoque/serviços.

---

### 20.3 Padrão mínimo de implementação

```typescript
import { useState } from 'react';
import { Calendar, CalendarUtils } from 'react-native-calendars';

const INITIAL_DATE = CalendarUtils.getCalendarDateString(new Date()); // YYYY-MM-DD

export function LashCalendar() {
  const [selectedDate, setSelectedDate] = useState(INITIAL_DATE);

  return (
    <Calendar
      current={INITIAL_DATE}
      onDayPress={(day) => setSelectedDate(day.dateString)}
      markedDates={{
        [selectedDate]: { selected: true },
      }}
    />
  );
}
```

---

### 20.4 Tema visual obrigatório (LashMatch)

Para manter consistência com Seção 18:
- fundo da tela `#000000`;
- cards/superfícies `#1a1a1a`;
- cor primária de destaque `#D63384`;
- textos claros (`#FFFFFF`) e secundários em cinza.

Exemplo de tema do calendário:
```typescript
theme={{
  calendarBackground: '#1a1a1a',
  monthTextColor: '#FFFFFF',
  dayTextColor: '#FFFFFF',
  textDisabledColor: '#666666',
  selectedDayBackgroundColor: '#D63384',
  selectedDayTextColor: '#FFFFFF',
  todayTextColor: '#D63384',
  arrowColor: '#D63384',
}}
```

---

# Dentro da pasta do projeto
cd functions

---

## 24. CONTROLE FINANCEIRO + ESTOQUE — LashMatch

> Caso de uso: dona de salão registra vendas de serviços e produtos, controla custo do estoque consumido e visualiza lucro líquido por período.

---

## 25. SISTEMA DE AGENDAMENTO COMPLETO — LashMatch

> Caso de uso: salão de cílios com múltiplas funcionárias, serviços com durações variadas, agendamento pela dona no app E pela cliente via link público. Confirmação e lembrete automáticos via Z-API.

## Validação de formulários — padrão da fábrica

Sempre usar `hooks/useFormValidation.ts`
Sempre usar `components/ui/InputComErro.tsx`
Campos obrigatórios: asterisco * no label
Erro: borda #FF5252, fundo rgba(255,82,82,0.1)
Mensagem: ⚠ texto em #FF5252 abaixo do campo
Web: sempre ScrollContainer nas telas com formulário

## Regras de formulário — padrão fábrica

SEMPRE usar ScrollContainer com scrollRef
SEMPRE scrollTo(y:0) quando tiver erros de validação
SEMPRE bloquear submit quando formulário inválido
ScrollContainer usa ScrollView em TODAS plataformas
(não só web) — garante scroll em celulares pequenos

---


| Funcionalidade | ❌ Não usar | ✅ Usar |
|----------------|------------|--------|
| Google Sign-In | @react-native-google-signin/google-signin | expo-auth-session |
| Auth persistence | getAuth() | initializeAuth() + AsyncStorage |
| Câmera | react-native-camera | expo-camera |
| Notificações | react-native-push-notification | expo-notifications |
| Armazenamento local | react-native-async-storage direto | @react-native-async-storage/async-storage via expo install |

Regra geral: sempre prefira pacotes do ecossistema Expo (`expo install`) sobre pacotes React Native puros quando existir alternativa — garante compatibilidade com Expo Go sem precisar de dev build.
## Sincronização repo ↔ Obsidian (agente)

*Atualizado em 12/06/2026*

Após qualquer implementação que altere schema, integração ou fluxo:

1. **Antes:** `rag_buscar` + `buscar_historico` (MCP fabrica-apps)
2. **Durante:** código no repo
3. **Depois:** atualizar `docs/*.md` do projeto + espelho em `C:/Users/gusta/obsidian/fabrica/`
4. **PRD:** `obsidian/projetos/<projeto>-prd.md` se mudou comportamento visível
5. **Erros:** `registrar_erro_solucao` → `erros-e-solucoes.md`
6. **Reindexar:** `python C:/Users/gusta/obsidian/indexar_rapido.py` (ou automático via MCP)

LashMatch: ver também `fabrica/lashmatch-schemas.md`, [[lashmatch-modulos-assinatura-jun2026]], [[lashmatch-mercadopago-assinatura]], [[lashmatch-revenuecat-assinatura]] e regra `LashMatch/.cursor/rules/rag-memoria-fabrica.mdc` (alwaysApply).

---
