---
tags:
  - geral
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "2.5 Instalação dependências essenciais"
  - "5.2 Listener em tempo real (onSnapshot)"
  - "Iniciar dev server"
  - "Instalar dependência com verificação de compatibilidade"
  - "Build para produção (iOS)"
---

### 2.5 Instalação dependências essenciais
```bash
npx expo install expo-router react-native-safe-area-context react-native-screens
npx expo install expo-status-bar expo-linking expo-constants
npx expo install nativewind tailwindcss  # se usar NativeWind
```

---

---

### 5.2 Listener em tempo real (onSnapshot)
```typescript
import { useEffect, useState } from 'react';
import { onSnapshot, collection, query, orderBy } from 'firebase/firestore';
import { db } from '../firebaseConfig';

export function usePosts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'));

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const data = snapshot.docs.map(d => ({ id: d.id, ...d.data() } as Post));
      setPosts(data);
      setLoading(false);
    });

    return unsubscribe; // cleanup obrigatório
  }, []);

  return { posts, loading };
}
```

---

# Iniciar dev server
npx expo start

---

# Instalar dependência com verificação de compatibilidade
npx expo install <pacote>

---

# Build para produção (iOS)
eas build --platform ios

---

# Build para produção (Android)
eas build --platform android

---

# Preview channel (URL temporária por branch)
firebase hosting:channel:deploy preview-branch

---

# Entrar na pasta e abrir no VS Code
cd my-list
code .

---

### 12.4 Declaração de tipos para imagens (TypeScript)
Ao importar `.png` no TypeScript, ele reclama que o módulo não existe. Solução:
```typescript
// src/@types/png.d.ts
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.svg';
declare module '*.gif';
```
Crie a pasta `src/@types/` e o arquivo acima. O erro vermelho some sem precisar de configurações extras.

---

### 12.9 Gerenciamento de estado com `useState`
```typescript
import { useState } from 'react';

// Declaração
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [loading, setLoading] = useState(false);

// Vincular ao TextInput — duas formas ensinadas no curso:

// Forma 1 — com arrow function (mais explícita, recomendada)
<TextInput
  value={email}
  onChangeText={(text) => setEmail(text)}
/>

// Forma 2 — passando o setter direto (mais curta)
<TextInput
  value={password}
  onChangeText={setPassword}
/>
```

> Sem `value` + `onChangeText`, o campo fica "travado" e não aceita digitação do usuário.

---

### 12.11 Botão com estado de loading inline
```typescript
// Mostrar spinner no botão enquanto carrega
<TouchableOpacity
  style={styles.button}
  onPress={handleLogin}
  disabled={loading}   // ← desabilitar clique duplo
>
  {loading
    ? <ActivityIndicator color="#fff" size="small" />
    : <Text style={styles.buttonText}>Entrar</Text>
  }
</TouchableOpacity>
```

---

### 12.12 Texto com parte clicável (link inline)
```typescript
// "Não tem conta? Crie agora"
// Só a parte "Crie agora" é clicável e colorida
<Text style={styles.textBottom}>
  Não tem conta?{' '}
  <Text
    style={{ color: themes.colors.primary }}
    onPress={() => router.push('/register')}
  >
    Crie agora
  </Text>
</Text>
```

---

### 12.13 `flexDirection` — coluna vs linha (resumo visual do curso)
```
flexDirection: 'column' (padrão)    flexDirection: 'row'
┌─────────┐                          ┌────┬────┬────┐
│  Item 1 │                          │ I1 │ I2 │ I3 │
│  Item 2 │                          └────┴────┴────┘
│  Item 3 │
└─────────┘
```

Casos de uso:
- `column` → seções da tela, listas, formulários (padrão)
- `row` → input + ícone, botões lado a lado, navbar

---

### 12.14 `justifyContent` vs `alignItems` — resumo do curso
```
                    flexDirection: 'column'
justifyContent      → alinha no eixo VERTICAL (cima/baixo)
alignItems          → alinha no eixo HORIZONTAL (esquerda/direita)

                    flexDirection: 'row'
justifyContent      → alinha no eixo HORIZONTAL
alignItems          → alinha no eixo VERTICAL
```

Para centralizar tudo:
```typescript
container: {
  flex: 1,
  justifyContent: 'center',   // centro vertical
  alignItems: 'center',       // centro horizontal
}
```

---

### 13.7 Lógica de mostrar/esconder senha
```typescript
const [showPassword, setShowPassword] = useState(false);

// Toggle simples — usando valor anterior (prev)
const togglePassword = () => setShowPassword(prev => !prev);

// No componente Input:
<Input
  iconRightName={showPassword ? 'visibility' : 'visibility-off'}
  onIconRightPress={togglePassword}
  secureTextEntry={!showPassword}
  value={password}
  onChangeText={setPassword}
/>
```

> Ícones usados: `'visibility'` (olho aberto) e `'visibility-off'` (olho fechado) — ambos do `MaterialIcons`.

---

### 13.9 Renderização condicional inline
```typescript
// Padrão do curso — só renderiza se a prop existir
{title && <Text style={styles.titleInput}>{title}</Text>}

// Equivalente ao if, mas em uma linha (operador &&)
// Se title for undefined/null/'' → não renderiza nada
// Se title tiver valor → renderiza o <Text>

// Para dois valores opcionais:
{iconLeft && iconLeftName && (
  <IconLeft name={iconLeftName} size={20} color={themes.colors.grey} />
)}
```

> Sem essa verificação, o espaço do título ficaria reservado mesmo quando não há título — gerando espaço em branco indesejado.

---

### 14.2 Instalação completa
```bash

---

### 14.9 Indicador de aba ativa com state.index
```typescript
// state.index === 0 → primeira aba ativa (list)
// state.index === 1 → segunda aba ativa (user)

// Controlar opacidade do ícone baseado na aba ativa
style={{ opacity: state.index === 0 ? 1 : 0.3 }}

// Se tiver 3+ abas: índices 0, 1, 2...
```

---

## 16. FLATLIST, CARDS, HEADER E MODAL (Caio Eduardo — Vídeo 5)

> Conceito central: **FlatList** para listas performáticas, **componentes Badge/Flag** reutilizáveis, **react-native-modalize** para modal bottom sheet, e **useRef** para controlar componentes imperativos.

---

### 16.1 Header com Dimensions responsivo
```typescript
import { Dimensions, View, Text } from 'react-native';
import { Input } from '../../components/Input';
import { MaterialIcons } from '@expo/vector-icons';
import { themes } from '../../global/themes';

const { width, height } = Dimensions.get('window');

// No JSX:
<View style={styles.header}>
  <Text style={styles.greeting}>
    Bom dia, <Text style={{ fontWeight: 'bold' }}>Caio</Text>
  </Text>

  <View style={styles.boxInput}>
    <Input
      iconLeft={MaterialIcons}
      iconLeftName="search"
    />
  </View>
</View>

// styles
header: {
  width: '100%',
  height: height / 6,          // ← responsivo: divide a altura da tela
  backgroundColor: themes.colors.primary,
  paddingTop: 20,
  paddingHorizontal: 20,
  alignItems: 'center',
},
greeting: {
  fontSize: 20,
  color: '#fff',
  marginTop: 20,
},
boxInput: {
  width: '80%',
},
```

> Nunca usar altura fixa (ex: `height: 300`) para o header — usar `height / 6` para ser responsivo em qualquer dispositivo.

---

### 16.2 FlatList vs .map() — quando usar cada um

| Critério             | `.map()`                        | `FlatList`                         |
|----------------------|---------------------------------|------------------------------------|
| Renderização         | Tudo de uma vez                 | Lazy — só o que está visível       |
| Performance          | Ruim com muitos itens           | Ótima com milhares de itens        |
| Quando usar          | Listas pequenas e estáticas     | Listas dinâmicas e longas          |
| Sintaxe              | JavaScript puro                 | Componente React Native            |

> O curso ensina `.map()` como conceito, mas usa **FlatList** na prática por ser a boa prática.

---

### 16.3 Tipagem dos dados da lista
```typescript
// Definir o tipo do item antes de criar a variável
type PropCard = {
  item: number;          // identificador único (usado como key)
  title: string;
  description: string;
  flag?: 'urgente' | 'opcional' | 'concluído'; // flags opcionais
};

// Dados temporários (futuramente virão do Firestore)
const data: PropCard[] = [
  { item: 0, title: 'Tarefa 1', description: 'Descrição da tarefa 1', flag: 'urgente' },
  { item: 1, title: 'Tarefa 2', description: 'Descrição da tarefa 2', flag: 'opcional' },
  { item: 2, title: 'Tarefa 3', description: 'Descrição da tarefa 3' },
];
```

---

### 16.4 FlatList com renderItem extraído
```typescript
// Extrair o renderItem para função separada — mantém o JSX limpo
function renderCard({ item }: { item: PropCard }) {
  return (
    <TouchableOpacity style={styles.card} key={item.item}>
      <View style={styles.rowCardLeft}>
        {/* Badge de cor */}
        <Badge color={themes.colors.primary} />

        <View>
          <Text style={styles.titleCard}>{item.title}</Text>
          <Text style={styles.descriptionCard}>{item.description}</Text>
        </View>
      </View>

      {/* Flag — só renderiza se existir */}
      {item.flag && <Flag caption={item.flag} color={themes.colors.red} />}
    </TouchableOpacity>
  );
}

// No JSX:
<FlatList
  data={data}
  keyExtractor={(item) => item.item.toString()}  // ← único, nunca repetido
  renderItem={renderCard}
  style={styles.boxList}
  contentContainerStyle={{ paddingBottom: 20 }}
  showsVerticalScrollIndicator={false}
/>
```

```typescript
// styles
boxList: {
  marginTop: 40,
  paddingHorizontal: 30,
},
card: {
  width: '100%',
  height: 60,
  backgroundColor: '#fff',
  marginTop: 6,
  borderRadius: 10,
  justifyContent: 'center',
  padding: 10,
  borderWidth: 1,
  borderColor: themes.colors.lightGrey,
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'space-between',
},
rowCardLeft: {
  width: '70%',
  flexDirection: 'row',
  alignItems: 'center',
  gap: 10,                 // ← gap: espaçamento entre filhos (RN 0.71+)
},
titleCard: {
  fontSize: 16,
  fontWeight: 'bold',
},
descriptionCard: {
  color: themes.colors.grey,
},
```

> **`gap`** é a propriedade de espaçamento entre filhos no flexbox — mais limpo que usar `marginRight` em cada filho. Disponível no React Native 0.71+.

---

### 16.7 Modal com react-native-modalize

#### Instalação
```bash
npm install react-native-modalize

---

# Se não estiver:
npx expo install react-native-reanimated
```

#### Controle com useRef (não useState)
```typescript
// O Modalize é controlado por ref, não por estado
import { useRef } from 'react';
import { Modalize } from 'react-native-modalize';

const modalizeRef = useRef<Modalize>(null);

// Abrir
modalizeRef.current?.open();

// Fechar
modalizeRef.current?.close();
```

#### Integração com Context — abrir modal de qualquer tela
```typescript
// src/context/listContext.tsx — adicionar ref do modal
import { useRef } from 'react';
import { Modalize } from 'react-native-modalize';

export function ListContextProvider({ children }: { children: React.ReactNode }) {
  const modalizeRef = useRef<Modalize>(null);

  const onOpen = () => modalizeRef.current?.open();
  const onClose = () => modalizeRef.current?.close();

  return (
    <ListContext.Provider value={{ onOpen, onClose }}>
      {children}
      {/* Modal declarado UMA VEZ no Provider — acessível de qualquer tela */}
      <Modalize ref={modalizeRef} adjustToContentHeight>
        <ModalContent onClose={onClose} />
      </Modalize>
    </ListContext.Provider>
  );
}
```

#### Estrutura do conteúdo do Modal
```typescript
// src/components/ModalContent/index.tsx
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import { MaterialIcons, AntDesign } from '@expo/vector-icons';
import { Input } from '../Input';
import { Flag } from '../Flag';
import { themes } from '../../global/themes';

const { width } = Dimensions.get('window');

type Props = {
  onClose: () => void;
};

export function ModalContent({ onClose }: Props) {
  return (
    <View style={styles.container}>
      {/* Header do modal */}
      <View style={styles.header}>
        <TouchableOpacity onPress={onClose}>
          <MaterialIcons name="close" size={30} color={themes.colors.grey} />
        </TouchableOpacity>

        <Text style={styles.title}>Criar tarefa</Text>

        <TouchableOpacity>
          <AntDesign name="check" size={30} color={themes.colors.primary} />
        </TouchableOpacity>
      </View>

      {/* Campos */}
      <View style={styles.content}>
        <Input title="Título" />

        {/* Input maior para descrição */}
        <Input
          title="Descrição"
          multiline
          numberOfLines={5}
          height={100}        // ← prop customizada que implementamos no Input
        />

        <Input title="Tempo limite" />

        {/* Flags de prioridade */}
        <View style={styles.containerFlag}>
          <Text style={styles.labelFlag}>Flags</Text>
          <View style={styles.flagRow}>
            <Flag caption="urgente"   color={themes.colors.red} />
            <Flag caption="opcional"  color={themes.colors.primary} />
            <Flag caption="concluído" color={themes.colors.green} />
          </View>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    paddingBottom: 40,
  },
  header: {
    width: '100%',
    height: 40,
    paddingHorizontal: 40,
    marginTop: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  content: {
    width: '100%',
    paddingHorizontal: 20,
  },
  containerFlag: {
    width: '100%',
    padding: 10,
  },
  labelFlag: {
    fontWeight: 'bold',
    marginBottom: 8,
  },
  flagRow: {
    flexDirection: 'row',
    gap: 10,
  },
});
```

---

## 17. FORMULÁRIO DO MODAL — Flags, DateTimePicker e Estado (Caio Eduardo — Vídeo 6)

> Conceito central: **gerenciar estado de formulários complexos** com múltiplos `useState`, renderização dinâmica de arrays com `.map()`, e lidar com **DateTimePicker** em iOS e Android.

---

### 17.1 Renderização dinâmica de flags com .map()
Em vez de declarar cada Flag manualmente, criar um array de dados e mapear:

```typescript
// Array de flags — adicionar novas flags aqui, aparece automaticamente na UI
const flags = [
  { cap: 'urgente',   color: themes.colors.red     },
  { cap: 'opcional',  color: themes.colors.primary  },
  { cap: 'concluído', color: themes.colors.green    },
];

// renderFlags — função de renderização extraída
const renderFlags = flags.map((item, index) => (
  <TouchableOpacity key={index}>
    <Flag
      caption={item.cap}
      color={item.color}
      selected={selectedFlag === item.cap}  // destaca a flag selecionada
    />
  </TouchableOpacity>
));

// No JSX:
<View style={styles.rowFlags}>
  {renderFlags}
</View>
```

```typescript
// styles
rowFlags: {
  flexDirection: 'row',
  gap: 10,
  marginTop: 10,
},
```

> Padrão do curso: arrays de dados + `.map()` eliminam repetição de código. Adicionar um novo item no array é suficiente.

---

### 17.3 Estado completo do formulário do modal
```typescript
// Dentro do ListContextProvider ou do componente modal
const [title, setTitle]               = useState('');
const [description, setDescription]  = useState('');
const [selectedFlag, setSelectedFlag] = useState<'urgente' | 'opcional' | 'concluído' | ''>('');
const [selectDate, setSelectDate]     = useState('');     // data formatada (string)
const [selectTime, setSelectTime]     = useState('');     // hora formatada (string)

// Estados de controle dos pickers
const [showDatePicker, setShowDatePicker] = useState(false);
const [showTimePicker, setShowTimePicker] = useState(false);

// Datas brutas (tipo Date — necessário para o DateTimePicker)
const [date, setDate] = useState(new Date());
const [time, setTime] = useState(new Date());
```

---

### 17.4 Instalação do DateTimePicker
```bash
npx expo install @react-native-community/datetimepicker
```

---

### 17.6 Handlers de data e hora
```typescript
// Converter Date para string legível
function handleDateChange(selectedDate: Date) {
  setSelectDate(selectedDate.toLocaleDateString('pt-BR'));
  // Resultado: "13/04/2026"
}

function handleTimeChange(selectedTime: Date) {
  setSelectTime(selectedTime.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  }));
  // Resultado: "14:30"
}
```

> **Importante:** o DateTimePicker retorna um objeto `Date`, não uma string.
> Sempre usar `.toLocaleDateString()` ou `.toLocaleTimeString()` para exibir ao usuário.
> Nunca exibir o objeto `Date` diretamente — ficará como `[object Object]`.

---

### 17.7 Inputs de data/hora — somente leitura com onPress
Os inputs de data e hora não são editáveis pelo teclado — abrirão o picker:

```typescript
<View style={{ flexDirection: 'row', gap: 10, width: '100%' }}>

  {/* Input de data — somente leitura */}
  <Input
    title="Data limite"
    editable={false}          // ← não permite teclado
    value={selectDate}        // ← exibe a data formatada
    onPress={() => setShowDatePicker(true)}   // ← abre o picker
    labelStyle={styles.label}
    width={200}
  />

  {/* Input de hora — somente leitura */}
  <Input
    title="Hora limite"
    editable={false}
    value={selectTime}
    onPress={() => setShowTimePicker(true)}
    labelStyle={styles.label}
    width={100}
  />

</View>

{/* Pickers — renderizam apenas quando show=true */}
{showDatePicker && (
  <CustomDateTimePicker
    type="date"
    show={showDatePicker}
    setShow={setShowDatePicker}
    date={date}
    setDate={setDate}
    onDateChange={handleDateChange}
  />
)}

{showTimePicker && (
  <CustomDateTimePicker
    type="time"
    show={showTimePicker}
    setShow={setShowTimePicker}
    date={time}
    setDate={setTime}
    onDateChange={handleTimeChange}
  />
)}
```

---

### 17.8 Corrigir bug do KeyboardAvoidingView no modal
O modal bugava quando o teclado subia. Solução do curso:

```typescript
import { KeyboardAvoidingView, Platform, Dimensions } from 'react-native';

const { height } = Dimensions.get('window');

// Envolver o conteúdo do modal com KeyboardAvoidingView
<Modalize
  ref={modalizeRef}
  snapPoint={height / 1.7}       // ← altura dinâmica (não fixa)
  // adjustToContentHeight foi removido pois causava bug
>
  <KeyboardAvoidingView
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  >
    {/* conteúdo do modal */}
  </KeyboardAvoidingView>
</Modalize>
```

> `adjustToContentHeight` no Modalize causa bugs quando o teclado sobe.
> Usar `snapPoint={height / 1.7}` como alternativa mais estável.

---

### 17.9 `editable={false}` nos TextInputs de exibição
```typescript
// Impede o usuário de digitar diretamente no campo
// Útil para campos que só são preenchidos via picker ou seleção
<TextInput
  editable={false}    // ← campo somente leitura
  value={selectDate}
/>

// A diferença de onPress vs onChangeText:
// onChangeText → usuário digita → atualiza estado
// onPress → usuário toca → abre picker/modal → atualiza estado indiretamente
```

---

### 17.10 useEffect para sincronizar callbacks
```typescript
// Padrão do curso para notificar o pai quando um valor interno muda
useEffect(() => {
  if (onDateChange) {
    onDateChange(date);   // dispara callback sempre que 'date' muda
  }
}, [date, onDateChange]); // ← array de dependências: executa quando esses valores mudam
```

> `useEffect` com array de dependências executa:
> - Na montagem do componente (sempre)
> - Toda vez que qualquer valor do array de dependências mudar

---

### 18.2.1 Comportamentos — `analysisResult`, perfil da cliente e guia de mapeamentos

- **`app/analysisResult.tsx`**: stickers de cílios com Reanimated; limites de pan usam dimensões reais do frame da foto (`onLayout` → `boundsW`/`boundsH`). Largura exibida do PNG limitada para o clamp horizontal não colapsar os dois olhos no centro. Persistência da análise + foto composta **apenas** nos botões explícitos Voltar / Voltar para Home; captura nativa pode exigir camada estática temporária para compor os cílios no JPEG. Modal fullscreen mostra a foto frontal da sessão (base64), não necessariamente o mesmo arquivo que sobe como `fotoComCiliosUrl`.
- **`app/clientes/[id].tsx`**: toque na foto do histórico ou no avatar (se existir URL) abre modal fullscreen da imagem.
- **`app/(tabs)/guia-mapeamentos.tsx`**: filtros + lista; layout em duas faixas verticais (flex ~52/48), scroll na área de filtros quando necessário, dicas e indicadores de scroll horizontal/vertical para o usuário perceber mais conteúdo. Dados em `app/constants/mapaCilios.ts` (não confundir com `LASH_IMAGES` / `lashStyleVariations`).

---

---

### 18.7 Pattern de layout raiz — `app/_layout.tsx`

```typescript
// app/_layout.tsx — tema dark global
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: '#000' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: '600' },
        }}
      >
        <Stack.Screen name="index"          options={{ headerShown: false }} />
        <Stack.Screen name="Login"          options={{ headerShown: false }} />
        <Stack.Screen name="(tabs)"         options={{ headerShown: false }} />
        <Stack.Screen name="camera"         options={{ headerShown: false }} />
        <Stack.Screen name="analysisResult" options={{ headerShown: false }} />
        <Stack.Screen name="clientes/[id]"  options={{ title: 'Perfil da Cliente', headerBackTitle: 'Voltar' }} />
      </Stack>
    </>
  );
}
```

---

---

## 19. ERROS CONHECIDOS E SOLUÇÕES

---

### 20.5 Boas práticas para agentes ao gerar tela com calendário

- sempre controlar data selecionada com `useState`;
- usar `markedDates` para feedback visual da data ativa;
- quando necessário, usar `minDate` para bloquear datas passadas;
- envolver a tela em `SafeAreaView` com fundo preto;
- manter mistura de `twrnc` + `StyleSheet` (padrão LashMatch);
- se houver formulário junto, usar `KeyboardAvoidingView` com:
  - iOS: `padding`
  - Android: `height`

---

### 20.6 Não fazer

- não quebrar paleta da Seção 18 com tema claro;
- não usar cores hardcoded fora do padrão (`#D63384`, `#000`, `#1a1a1a`, etc.);
- não gerar calendário isolado do contexto de negócio (sempre pensar em agendamento, histórico, prazos ou filtros reais do LashMatch).

---

---

---

### 21.1 Dois tipos de notificação

| Tipo | Quando usar | Funciona no Expo Go? |
|------|-------------|----------------------|
| **Local** | Agendadas no próprio dispositivo (ex: lembrete de consulta) | ✅ Sim |
| **Push (remota)** | Enviadas por servidor externo para o dispositivo | ❌ Não no SDK 53+ — precisa de development build |

> **Regra crítica (SDK 53+):** Push notifications remotas **não funcionam mais no Expo Go** a partir do SDK 53. Para prototipar, use **notificações locais**. Para produção, use **EAS Build** com `expo-dev-client`.

---

### 21.2 Instalação

```bash
npx expo install expo-notifications expo-device expo-constants
```

---

### 21.4 Canal de notificação Android (obrigatório)

Android 8.0+ **descarta notificações silenciosamente** sem canal configurado — sem erro, sem log.

```typescript
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

async function configurarCanalAndroid() {
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('agendamentos', {
      name: 'Agendamentos',
      importance: Notifications.AndroidImportance.HIGH, // aparece como banner
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#D63384',
    });
  }
}
```

> Sempre chamar `configurarCanalAndroid()` antes de agendar qualquer notificação no Android.

---

### 21.5 Notificação local agendada (caso de uso: salão de beleza)

```typescript
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Agendar lembrete para 1 hora antes do horário da cliente
async function agendarLembrete(
  nomeCliente: string,
  dataAgendamento: Date
): Promise<string> {

  // Criar canal Android se necessário
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('agendamentos', {
      name: 'Agendamentos',
      importance: Notifications.AndroidImportance.HIGH,
    });
  }

  // 1 hora antes do agendamento
  const dataLembrete = new Date(dataAgendamento.getTime() - 60 * 60 * 1000);

  const notificationId = await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Lembrete de Agendamento',
      body: `${nomeCliente} tem horário em 1 hora!`,
      sound: true,
      data: { clienteNome: nomeCliente },
    },
    trigger: {
      type: Notifications.SchedulableTriggerInputTypes.DATE,
      date: dataLembrete,
      channelId: 'agendamentos', // obrigatório no Android
    },
  });

  return notificationId; // salvar no Firestore para poder cancelar depois
}

// Cancelar lembrete (ex: quando agendamento for cancelado)
async function cancelarLembrete(notificationId: string) {
  await Notifications.cancelScheduledNotificationAsync(notificationId);
}

// Cancelar todos os lembretes
async function cancelarTodosLembretes() {
  await Notifications.cancelAllScheduledNotificationsAsync();
}
```

---

### 21.7 Pedir permissão ao usuário

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

async function pedirPermissaoNotificacao(): Promise<boolean> {
  // Notificações não funcionam em emuladores
  if (!Device.isDevice) {
    console.warn('Notificações só funcionam em dispositivo físico');
    return false;
  }

  const { status: statusAtual } = await Notifications.getPermissionsAsync();

  if (statusAtual === 'granted') return true;

  // Pedir permissão apenas se ainda não foi decidido
  if (statusAtual === 'undetermined') {
    const { status } = await Notifications.requestPermissionsAsync();
    return status === 'granted';
  }

  // Se já foi negado, não perguntar de novo
  return false;
}
```

> Pedir permissão **após** o usuário ter uma ação positiva (ex: ao criar o primeiro agendamento), não na abertura do app.

---

### 21.8 Hook customizado — `hooks/useNotificacoes.ts`

```typescript
import { useEffect, useRef } from 'react';
import * as Notifications from 'expo-notifications';
import { useRouter } from 'expo-router';

export function useNotificacoes() {
  const notificationListener = useRef<any>();
  const responseListener = useRef<any>();
  const router = useRouter();

  useEffect(() => {
    // Listener: notificação recebida com app aberto
    notificationListener.current = Notifications.addNotificationReceivedListener(
      (notification) => {
        console.log('Notificação recebida:', notification);
      }
    );

    // Listener: usuário tocou na notificação
    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;
        // Navegar para tela de agendamentos ao tocar
        if (data?.clienteNome) {
          router.push('/(tabs)/agendamentos');
        }
      }
    );

    // Cleanup obrigatório
    return () => {
      notificationListener.current?.remove();
      responseListener.current?.remove();
    };
  }, []);
}
```

---

### 21.9 Listar notificações agendadas (debug)

```typescript
async function listarNotificacoesAgendadas() {
  const notificacoes = await Notifications.getAllScheduledNotificationsAsync();
  console.log('Notificações agendadas:', notificacoes.length);
  notificacoes.forEach(n => {
    console.log('-', n.identifier, n.content.title);
  });
}
```

---

### 21.10 Push remota para produção (EAS Build)

Para notificações enviadas do servidor (ex: lembrete automático 24h antes):

```bash

---

# 2. Build de desenvolvimento
eas build --profile development --platform android

---

# 3. Obter token do dispositivo
```

```typescript
import Constants from 'expo-constants';

async function obterExpoPushToken(): Promise<string | null> {
  const permissao = await pedirPermissaoNotificacao();
  if (!permissao) return null;

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: Constants.expoConfig?.extra?.eas?.projectId,
  });

  return token.data; // salvar no Firestore em usuarios/{uid}.pushToken
}
```

Enviar do servidor:
```typescript
// No backend (Cloud Function ou servidor Node)
await fetch('https://exp.host/--/api/v2/push/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    to: expoPushToken,
    title: 'Lembrete',
    body: 'Você tem um agendamento amanhã!',
    sound: 'default',
    data: { tela: 'agendamentos' },
  }),
});
```

---

### 22.1 Como funciona

Usa o `Linking` nativo do React Native para abrir o WhatsApp com mensagem e número pré-preenchidos. A dona do salão **confirma e toca em enviar** — não é automático. Zero custo, zero API, zero risco de banimento.

---

### 22.2 Instalação

Nenhuma — `Linking` já vem no React Native. Nada a instalar.

---

### 22.4 Caso de uso — lembrete de agendamento de salão

```typescript
import { abrirWhatsApp } from '../utils/whatsapp';

// Montar mensagem de lembrete personalizada
function montarMensagemLembrete(
  nomeCliente: string,
  servico: string,
  dataHora: Date
): string {
  const data = dataHora.toLocaleDateString('pt-BR');
  const hora = dataHora.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    `Olá ${nomeCliente}! 💅\n\n` +
    `Lembrando do seu agendamento:\n` +
    `📅 Data: ${data}\n` +
    `⏰ Hora: ${hora}\n` +
    `✂️ Serviço: ${servico}\n\n` +
    `Caso precise reagendar, entre em contato. Te esperamos! 😊`
  );
}

// Usar no componente
async function enviarLembrete(cliente: Cliente, agendamento: Agendamento) {
  if (!cliente.telefone) {
    Alert.alert('Atenção', 'Cliente sem telefone cadastrado.');
    return;
  }

  const mensagem = montarMensagemLembrete(
    cliente.nome,
    agendamento.servico,
    agendamento.dataHora.toDate(), // Timestamp do Firestore → Date
  );

  await abrirWhatsApp(cliente.telefone, mensagem);
}
```

---

### 22.5 Notificação local para a dona do salão

Quando a dona envia o lembrete, registrar no Firestore e disparar notificação local para ela mesma:

```typescript
import * as Notifications from 'expo-notifications';
import { updateDoc, doc, serverTimestamp } from 'firebase/firestore';
import { app, firestore } from '../utils/firebaseConfig';

async function registrarEnvioLembrete(
  uid: string,
  agendamentoId: string,
  nomeCliente: string
) {
  const appId = app.options.appId!;

  // 1. Salvar no Firestore que o lembrete foi enviado
  await updateDoc(
    doc(firestore, 'artifacts', appId, 'users', uid, 'agendamentos', agendamentoId),
    {
      lembreteEnviadoEm: serverTimestamp(),
      lembreteEnviado: true,
    }
  );

  // 2. Notificação local para a dona confirmar que foi enviado
  await Notifications.scheduleNotificationAsync({
    content: {
      title: '✅ Lembrete enviado',
      body: `Lembrete de agendamento enviado para ${nomeCliente}`,
      sound: true,
    },
    trigger: null, // dispara imediatamente
  });
}
```

---

### 22.6 Tela de agendamentos com botão de lembrete

```typescript
import { TouchableOpacity, Text, Alert } from 'react-native';
import tw from 'twrnc';
import { abrirWhatsApp } from '../../utils/whatsapp';
import { registrarEnvioLembrete } from '../../utils/lembretes';

function CardAgendamento({ agendamento, cliente, uid }: Props) {
  async function handleEnviarLembrete() {
    // Confirmar antes de abrir WhatsApp
    Alert.alert(
      'Enviar lembrete',
      `Enviar mensagem para ${cliente.nome}?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Enviar',
          onPress: async () => {
            const mensagem = montarMensagemLembrete(
              cliente.nome,
              agendamento.servico,
              agendamento.dataHora.toDate(),
            );
            // Abre WhatsApp com mensagem pronta
            await abrirWhatsApp(cliente.telefone, mensagem);
            // Registra no Firestore + notifica a dona
            await registrarEnvioLembrete(uid, agendamento.id, cliente.nome);
          },
        },
      ]
    );
  }

  return (
    <TouchableOpacity
      style={tw`bg-[#1a1a1a] border border-[#333] rounded-2xl p-4 mb-3`}
      onPress={() => {/* abrir detalhe */}}
    >
      <Text style={tw`text-white text-base font-bold`}>{cliente.nome}</Text>
      <Text style={tw`text-gray-400 mt-1`}>{agendamento.servico}</Text>

      {/* Botão WhatsApp */}
      <TouchableOpacity
        style={tw`bg-[#25D366] rounded-xl py-3 mt-3 items-center flex-row justify-center gap-2`}
        onPress={handleEnviarLembrete}
        disabled={agendamento.lembreteEnviado}
      >
        <Text style={tw`text-white font-bold`}>
          {agendamento.lembreteEnviado ? '✅ Lembrete enviado' : '💬 Enviar lembrete WhatsApp'}
        </Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );
}
```

---

### 23.1 Como funciona o fluxo completo

```
Firebase Scheduler          Cloud Function              Z-API
(todo dia 08:00)    →    busca agendamentos     →    envia WhatsApp
                         de amanhã no Firestore        para cada cliente
                                ↓
                         salva no Firestore             Notificação local
                         lembreteEnviado: true   →    para a dona do salão
```

---

### 23.4.1 Header `Client-Token` (obrigatório com segurança da conta ativa)

Quando a validação por token de conta está ativa na Z-API, **toda** requisição `fetch` deve incluir:

```typescript
headers: {
  'Content-Type': 'application/json',
  'Client-Token': zapiClientToken.value(), // secret ZAPI_CLIENT_TOKEN
}
```

No LashMatch isso está centralizado em `zApiHeaders()` em `functions/SRC/index.ts`.

---

### 23.7 Notificação local para a dona quando lembretes são enviados

A Cloud Function grava/atualiza `artifacts/{appId}/users/{uid}/resumoLembretes/ultimo` após envios no ciclo. O app escuta com **`hooks/useLembretesEnviados.ts`** (montado em `app/(tabs)/_layout.tsx`): `onSnapshot` no doc `ultimo`, checagem de `notificado`, `scheduleNotificationAsync` com `trigger: null`, depois `update({ notificado: true })`.

**Não** copie o exemplo antigo com `import * as Notifications from 'expo-notifications'` no topo — no LashMatch o módulo só é carregado fora do Expo Go (ver **§21.12**).

---

# Instalar dependências
npm install

---

# Build TypeScript (pasta fonte SRC -> lib)
npm run build

---

# Ver logs em tempo real
firebase functions:log --only enviarLembretesAgendamento
```

> **Atenção:** Cloud Functions com chamadas externas (fetch para Z-API) requerem o plano **Blaze (pay-as-you-go)** do Firebase. Para um salão pequeno com poucos agendamentos por dia, o custo fica em centavos por mês.

---

### 24.1 Conceitos financeiros do app

| Conceito | Descrição | Exemplo |
|---|---|---|
| **Receita** | Valor cobrado da cliente | R$ 150 por extensão de cílios |
| **Custo do produto** | Valor pago pelo produto consumido | R$ 30 em cílios usados |
| **Lucro bruto** | Receita − Custo do produto | R$ 120 |
| **Despesa** | Gasto fixo ou variável (aluguel, luz) | R$ 500/mês |
| **Lucro líquido** | Lucro bruto − Despesas | R$ 120 − parcela de R$ 500 |

---

### 24.3 Integração venda + estoque

Ao registrar uma venda, **sempre** baixar o estoque automaticamente:

```typescript
import {
  addDoc, collection, doc, runTransaction,
  serverTimestamp, Timestamp
} from 'firebase/firestore';
import { app, firestore } from '../utils/firebaseConfig';

interface ProdutoUsado {
  produtoId:     string;
  produtoNome:   string;
  quantidade:    number;
  custoUnitario: number;
  custoTotal:    number;
}

interface NovaVenda {
  clienteNome:    string;
  clienteId?:     string;
  servico:        string;
  valorVenda:     number;
  produtosUsados: ProdutoUsado[];
  formaPagamento: 'pix' | 'dinheiro' | 'cartao_credito' | 'cartao_debito';
  observacao?:    string;
}

async function registrarVenda(uid: string, dados: NovaVenda): Promise<void> {
  const appId = app.options.appId!;
  const basePath = `artifacts/${appId}/users/${uid}`;

  const custoTotal = dados.produtosUsados.reduce(
    (acc, p) => acc + p.custoTotal, 0
  );
  const lucroBruto = dados.valorVenda - custoTotal;

  // runTransaction garante que venda + baixa de estoque são atômicos
  // se um falhar, nenhum é salvo
  await runTransaction(firestore, async (transaction) => {

    // 1. Verificar estoque suficiente antes de qualquer escrita
    for (const produto of dados.produtosUsados) {
      const estoqueRef = doc(
        firestore, basePath, 'estoque', produto.produtoId
      );
      const estoqueSnap = await transaction.get(estoqueRef);

      if (!estoqueSnap.exists()) {
        throw new Error(`Produto ${produto.produtoNome} não encontrado.`);
      }

      const qtdAtual = estoqueSnap.data().quantidade as number;
      if (qtdAtual < produto.quantidade) {
        throw new Error(
          `Estoque insuficiente para ${produto.produtoNome}. ` +
          `Disponível: ${qtdAtual}, necessário: ${produto.quantidade}`
        );
      }
    }

    // 2. Criar a venda
    const vendaRef = doc(collection(firestore, basePath, 'vendas'));
    transaction.set(vendaRef, {
      ...dados,
      custoTotal,
      lucroBruto,
      dataVenda: serverTimestamp(),
    });

    // 3. Baixar estoque de cada produto usado
    for (const produto of dados.produtosUsados) {
      const estoqueRef = doc(
        firestore, basePath, 'estoque', produto.produtoId
      );
      const estoqueSnap = await transaction.get(estoqueRef);
      const qtdAtual = estoqueSnap.data()!.quantidade as number;

      transaction.update(estoqueRef, {
        quantidade: qtdAtual - produto.quantidade,
        atualizadoEm: serverTimestamp(),
      });
    }
  });
}
```

> **Por que `runTransaction`?** Se a venda for salva mas o estoque falhar (ou vice-versa), os dados ficam inconsistentes. A transaction garante que os dois acontecem juntos ou nenhum acontece.

---

### 24.4 Cálculo de relatório por período

```typescript
import {
  collection, query, where, getDocs,
  Timestamp, orderBy
} from 'firebase/firestore';
import { app, firestore } from '../utils/firebaseConfig';

interface RelatorioFinanceiro {
  totalReceita:    number;
  totalCustos:     number;
  totalLucroBruto: number;
  totalDespesas:   number;
  lucroLiquido:    number;
  qtdVendas:       number;
  ticketMedio:     number;
  porFormaPagamento: Record<string, number>;
}

async function calcularRelatorio(
  uid: string,
  inicio: Date,
  fim: Date
): Promise<RelatorioFinanceiro> {
  const appId = app.options.appId!;
  const basePath = `artifacts/${appId}/users/${uid}`;

  // Buscar vendas do período
  const vendasSnap = await getDocs(query(
    collection(firestore, basePath, 'vendas'),
    where('dataVenda', '>=', Timestamp.fromDate(inicio)),
    where('dataVenda', '<=', Timestamp.fromDate(fim)),
    orderBy('dataVenda', 'desc')
  ));

  // Buscar despesas do período
  const despesasSnap = await getDocs(query(
    collection(firestore, basePath, 'despesas'),
    where('data', '>=', Timestamp.fromDate(inicio)),
    where('data', '<=', Timestamp.fromDate(fim))
  ));

  let totalReceita    = 0;
  let totalCustos     = 0;
  let totalLucroBruto = 0;
  const porFormaPagamento: Record<string, number> = {};

  vendasSnap.docs.forEach(d => {
    const v = d.data();
    totalReceita    += v.valorVenda   || 0;
    totalCustos     += v.custoTotal   || 0;
    totalLucroBruto += v.lucroBruto   || 0;

    const forma = v.formaPagamento || 'outros';
    porFormaPagamento[forma] = (porFormaPagamento[forma] || 0) + v.valorVenda;
  });

  const totalDespesas = despesasSnap.docs.reduce(
    (acc, d) => acc + (d.data().valor || 0), 0
  );

  const qtdVendas  = vendasSnap.size;
  const lucroLiquido = totalLucroBruto - totalDespesas;
  const ticketMedio  = qtdVendas > 0
    ? totalReceita / qtdVendas
    : 0;

  return {
    totalReceita,
    totalCustos,
    totalLucroBruto,
    totalDespesas,
    lucroLiquido,
    qtdVendas,
    ticketMedio,
    porFormaPagamento,
  };
}
```

---

### 24.5 Padrões de UI do módulo financeiro

Seguir a mesma identidade visual do estoque já existente:

```typescript
// Cores para valores financeiros — padrão LashMatch
const FINANCIAL_COLORS = {
  receita:   '#4ade80',   // verde — entradas
  custo:     '#f87171',   // vermelho — saídas/custos
  lucro:     '#D63384',   // rosa primário — lucro
  neutro:    '#9e9e9e',   // cinza — valores neutros
  pix:       '#00B4D8',   // azul claro — Pix
  dinheiro:  '#4ade80',   // verde — dinheiro
  cartao:    '#a78bfa',   // roxo — cartão
};

// Card de resumo financeiro
function CardFinanceiro({
  label, valor, cor, prefixo = 'R$'
}: {
  label: string;
  valor: number;
  cor: string;
  prefixo?: string;
}) {
  return (
    <View style={[styles.card, { borderLeftWidth: 3, borderLeftColor: cor }]}>
      <Text style={styles.cardLabel}>{label}</Text>
      <Text style={[styles.cardValor, { color: cor }]}>
        {prefixo} {valor.toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })}
      </Text>
    </View>
  );
}
```

---

### 24.8 Adicionar campo custoUnitario no estoque existente

O estoque já existe — só precisa adicionar o campo `custoUnitario` ao modal de edição:

```typescript
// No modal de produto (estoque.tsx já existente)
// Adicionar campo:
<Text style={styles.label}>Custo unitário (R$)</Text>
<TextInput
  value={custoUnitario}
  onChangeText={setCustoUnitario}
  keyboardType="decimal-pad"
  placeholder="0,00"
  placeholderTextColor={COLORS.textMuted}
  style={styles.input}
/>

// Ao salvar, incluir custoUnitario no updateDoc/addDoc:
custoUnitario: parseFloat(custoUnitario.replace(',', '.')) || 0,
```

---

### 25.1 Visão geral da arquitetura

```
DONA DO SALÃO (app React Native)
  ├── Cadastra funcionárias
  ├── Cadastra serviços + duração + preço
  ├── Agenda manualmente pelo app
  └── Vê agenda do dia por funcionária

CLIENTE (link público — Firebase Hosting)
  ├── Acessa: seuapp.web.app/agendar
  ├── Escolhe serviço → vê duração e preço
  ├── Escolhe funcionária
  ├── Vê apenas horários DISPONÍVEIS
  ├── Informa nome + WhatsApp
  └── Confirma → Z-API envia confirmação automática

CLOUD FUNCTIONS (automático)
  ├── enviarConfirmacaoAgendamento → dispara ao criar agendamento
  └── enviarLembretesAgendamento  → todo dia 08:00, 24h antes
```

---

### 25.3 Lógica de verificação de conflito

```typescript
import { collection, query, where, getDocs, Timestamp } from 'firebase/firestore';
import { app, firestore } from '../utils/firebaseConfig';

/**
 * Conflito ocorre quando os intervalos se sobrepõem:
 * novoInício < existenteFim  E  novoFim > existenteInício
 */
async function verificarDisponibilidade(
  uid: string,
  funcionariaId: string,
  inicio: Date,
  duracaoMinutos: number,
  agendamentoExcluidoId?: string  // para edição — ignorar o próprio
): Promise<{ disponivel: boolean; conflito?: string }> {

  const fim = new Date(inicio.getTime() + duracaoMinutos * 60 * 1000);
  const appId = app.options.appId!;

  const ref = collection(
    firestore, 'artifacts', appId, 'users', uid, 'agendamentos'
  );

  const snap = await getDocs(query(
    ref,
    where('funcionariaId', '==', funcionariaId),
    where('status', '!=', 'cancelado'),
    where('dataHoraFim', '>', Timestamp.fromDate(inicio)),
  ));

  for (const docSnap of snap.docs) {
    if (docSnap.id === agendamentoExcluidoId) continue;

    const ag = docSnap.data();
    const existenteInicio = ag.dataHoraInicio.toDate();

    if (inicio < ag.dataHoraFim.toDate() && fim > existenteInicio) {
      return {
        disponivel: false,
        conflito: `${ag.clienteNome} já tem horário das ` +
          `${existenteInicio.toLocaleTimeString('pt-BR', {
            hour: '2-digit', minute: '2-digit'
          })}`,
      };
    }
  }

  return { disponivel: true };
}
```

---

### 25.4 Gerar slots de horário disponíveis (página pública)

```typescript
const HORARIO_ABERTURA   = 8;   // 08:00
const HORARIO_FECHAMENTO = 19;  // 19:00
const INTERVALO_SLOT     = 30;  // slots de 30 em 30 minutos

async function gerarSlotsDisponiveis(
  uid: string,
  funcionariaId: string,
  data: Date,
  duracaoMinutos: number
): Promise<Date[]> {

  const appId = app.options.appId!;
  const inicioDia = new Date(data); inicioDia.setHours(0, 0, 0, 0);
  const fimDia    = new Date(data); fimDia.setHours(23, 59, 59, 999);

  const ref = collection(
    firestore, 'artifacts', appId, 'users', uid, 'agendamentos'
  );
  const snap = await getDocs(query(
    ref,
    where('funcionariaId', '==', funcionariaId),
    where('status', '!=', 'cancelado'),
    where('dataHoraInicio', '>=', Timestamp.fromDate(inicioDia)),
    where('dataHoraInicio', '<=', Timestamp.fromDate(fimDia)),
  ));

  const existentes = snap.docs.map(d => ({
    inicio: d.data().dataHoraInicio.toDate(),
    fim:    d.data().dataHoraFim.toDate(),
  }));

  const slots: Date[] = [];
  let slotAtual = new Date(data);
  slotAtual.setHours(HORARIO_ABERTURA, 0, 0, 0);

  const fimPossivel = new Date(data);
  fimPossivel.setHours(HORARIO_FECHAMENTO, 0, 0, 0);

  while (slotAtual < fimPossivel) {
    const slotFim = new Date(slotAtual.getTime() + duracaoMinutos * 60 * 1000);

    if (slotFim <= fimPossivel) {
      const temConflito = existentes.some(ag =>
        slotAtual < ag.fim && slotFim > ag.inicio
      );
      if (!temConflito) slots.push(new Date(slotAtual));
    }

    slotAtual = new Date(slotAtual.getTime() + INTERVALO_SLOT * 60 * 1000);
  }

  return slots;
}
```

---

### 25.6 Refatoração obrigatória do agendamentos.tsx

```typescript
// ADICIONAR ao formulário existente:

// 1. Buscar e selecionar FUNCIONÁRIA (igual ao padrão de busca de clientes)

// 2. Buscar e selecionar SERVIÇO (chips de seleção)
// Ao selecionar: mostrar duração e preço

// 3. Calcular dataHoraFim automaticamente
const dataHoraFim = new Date(
  dataHoraInicio.getTime() + servicoSelecionado.duracaoMinutos * 60 * 1000
);

// 4. Verificar conflito ANTES de salvar
const { disponivel, conflito } = await verificarDisponibilidade(
  uid, funcionariaId, dataHoraInicio, servicoSelecionado.duracaoMinutos
);
if (!disponivel) {
  Alert.alert('Horário indisponível', conflito);
  return;
}

// 5. Salvar com novos campos obrigatórios
await addDoc(ref, {
  ...payloadBase,
  funcionariaId,
  funcionariaNome,        // desnormalizado
  servicoId,
  servicoNome,            // desnormalizado
  duracaoMinutos: servicoSelecionado.duracaoMinutos,
  preco: servicoSelecionado.preco,
  dataHoraInicio: Timestamp.fromDate(dataHoraInicio),
  dataHoraFim:    Timestamp.fromDate(dataHoraFim),   // OBRIGATÓRIO
  origem: 'app',
  status: 'confirmado',
});
```

---

### 25.8 Página pública — fluxo da cliente

```typescript
// app/agendar/index.tsx — sem login, acessível via Firebase Hosting
// Passo 1: cliente escolhe o serviço → vê duração e preço
// Passo 2: cliente escolhe a funcionária
// Passo 3: cliente escolhe a data (calendário, mínimo hoje)
// Passo 4: app mostra slots disponíveis (gerarSlotsDisponiveis)
// Passo 5: cliente seleciona o horário
// Passo 6: cliente informa nome + WhatsApp
// Passo 7: confirmar → addDoc com origem: 'link_publico'
// Passo 8: Cloud Function dispara confirmação automática via Z-API

// UID do salão: passar via parâmetro de URL
// Ex: seuapp.web.app/agendar?uid=abc123
```

---

### 25.10 Agrupamento por funcionária na tela da dona

```typescript
// Visualização da agenda do dia agrupada por funcionária
const agendamentosPorFuncionaria = useMemo(() => {
  const grupos: Record<string, Agendamento[]> = {};
  agendamentosFiltrados.forEach(ag => {
    if (!grupos[ag.funcionariaId]) grupos[ag.funcionariaId] = [];
    grupos[ag.funcionariaId].push(ag);
  });
  return grupos;
}, [agendamentosFiltrados]);
```

---

### 26.1 Como funciona o fluxo completo

```
APP (React Native)          Cloud Function              Mercado Pago
       ↓                          ↓                          ↓
Usuário toca "Pagar"   →   cria preferência de    →   retorna init_point
                            pagamento via API           (URL do checkout)
       ↓                                                     ↓
openBrowserAsync(url)  ←────────────────────────   usuário paga no browser
       ↓
Deep Link retorna ao app
       ↓
Webhook confirma pagamento no backend
       ↓
Firestore atualizado com status do pagamento
```

> **Regra de segurança crítica:** o ACCESS_TOKEN do Mercado Pago NUNCA vai no app. Fica apenas no backend (Cloud Function). O app só recebe o init_point (URL) para abrir o browser.

---

### 26.2 Credenciais necessárias

| Credencial | Onde usar | Como obter |
|---|---|---|
| PUBLIC_KEY | Frontend — identificar a conta | Painel MP → Credenciais |
| ACCESS_TOKEN | Backend — criar preferências | Painel MP → Credenciais |

```bash

---

# Único pacote necessário no app
npx expo install expo-web-browser

---

### 27.2 Credenciais

- `MERCADOPAGO_ACCESS_TOKEN` (secret) — assinaturas e planos.
- `MP_PLANO_SETUP_KEY` (variável de ambiente, não secret) — chave esperada no body `setupKey` de `criarPlanoMP`. Sem valor, a função responde 503.

---

### 27.4 App

- `constants/planos.ts` — `PLANO_IDS`, `PLANO_NOMES`, valores de referência em BRL.
- `constants/planoMarketing.ts` — copy de trial, cancelamento nos primeiros 5 dias e textos de preço (espelha regras abaixo).

**Regras comerciais LashMatch (assinatura Mercado Pago):**

| Regra | Valor |
|--------|--------|
| Prazo para cancelar sem cobrança | **5 dias** (período inicial; conforme condições do MP) |
| Plano mensal | **R$ 60,00** por mês, **cobrança recorrente mensal** (uma vez por mês) |
| Plano anual | **R$ 600,00** por ano, **cobrança recorrente anual** (uma cobrança por ano) |

Os valores numéricos devem coincidir com `functions/SRC/planosConfig.ts` (`transaction_amount` + `frequency` / `frequency_type`).