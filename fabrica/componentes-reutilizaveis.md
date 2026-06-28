---
tags:
  - componentes
  - reutilizacao
  - ui
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "13. COMPONENTIZAÇÃO — Reutilização de Código (Caio Eduardo — Vídeo 2)"
  - "13.1 Por que componentizar?"
  - "13.3 Componente Input reutilizável — com ícone esquerda/direita"
  - "13.5 Componente Button reutilizável"
  - "13.8 Fragment — evitar wrapper desnecessário"
---

## 13. COMPONENTIZAÇÃO — Reutilização de Código (Caio Eduardo — Vídeo 2)

> Conceito central: **nunca copiar e colar o mesmo bloco de código**. Extraia em componente, passe props, reutilize.

---

### 13.1 Por que componentizar?
- Tela de login tem 2 inputs quase idênticos. A próxima tela terá mais.
- Copiar e colar gera código difícil de manter: mudar 1 detalhe = mudar em N lugares.
- Componente = bloco isolado, reutilizável, com suas próprias props e estilos.

---

### 13.3 Componente Input reutilizável — com ícone esquerda/direita

#### Tipagem das props com TypeScript
```typescript
// src/components/Input/index.tsx
import React from 'react';
import { View, TextInput, TextInputProps, TouchableOpacity } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { ComponentType } from 'react';

// Tipo para o componente de ícone (MaterialIcons, FontAwesome, Octicons...)
type IconComponent = ComponentType<{
  name: any;
  size?: number;
  color?: string;
}>;

// Props do nosso Input = todas as props nativas do TextInput + nossas customizações
type Props = TextInputProps & {
  title?: string;                        // label acima do input
  iconLeft?: IconComponent;             // componente de ícone à esquerda (opcional)
  iconLeftName?: string;                // nome do ícone esquerdo
  iconRight?: IconComponent;            // componente de ícone à direita (opcional)
  iconRightName?: string;               // nome do ícone direito
  onIconLeftPress?: () => void;         // ação ao clicar no ícone esquerdo
  onIconRightPress?: () => void;        // ação ao clicar no ícone direito
};
```

> O `?` em cada prop significa que ela é **opcional** — o componente funciona mesmo sem receber aquela prop.
> O `TextInputProps &` garante que todas as props nativas do TextInput (value, onChangeText, secureTextEntry, etc.) também funcionam.

#### Calculando tamanho dinâmico do input
```typescript
// Calcula width do input baseado em quantos ícones existem
function calculateInputWidth(iconLeft?: IconComponent, iconRight?: IconComponent): string {
  if (iconLeft && iconRight) return '80%';  // dois ícones → input menor
  if (iconLeft || iconRight) return '90%';  // um ícone → input médio
  return '100%';                             // sem ícone → input ocupa tudo
}

// Calcula paddingLeft baseado na presença de ícone esquerdo
function calculatePaddingLeft(iconLeft?: IconComponent): number {
  return iconLeft ? 10 : 5;
}
```

#### Componente Input completo
```typescript
export function Input(props: Props) {
  const {
    title,
    iconLeft: IconLeft,
    iconLeftName,
    iconRight: IconRight,
    iconRightName,
    onIconLeftPress,
    onIconRightPress,
    ...rest   // ← spread do restante: value, onChangeText, secureTextEntry, etc.
  } = props;

  return (
    <>
      {/* Label acima do input — só renderiza se title existir */}
      {title && (
        <Text style={styles.titleInput}>{title}</Text>
      )}

      <View style={styles.boxInput}>
        {/* Ícone esquerdo — só renderiza se existir */}
        {IconLeft && iconLeftName && (
          <TouchableOpacity onPress={onIconLeftPress} style={styles.iconWrapper}>
            <IconLeft name={iconLeftName} size={20} color={themes.colors.grey} />
          </TouchableOpacity>
        )}

        <TextInput
          style={[
            styles.input,
            { width: calculateInputWidth(IconLeft, IconRight) },
            { paddingLeft: calculatePaddingLeft(IconLeft) },
          ]}
          {...rest}   // ← passa todas as props nativas do TextInput
        />

        {/* Ícone direito — só renderiza se existir */}
        {IconRight && iconRightName && (
          <TouchableOpacity onPress={onIconRightPress} style={styles.iconWrapper}>
            <IconRight name={iconRightName} size={20} color={themes.colors.grey} />
          </TouchableOpacity>
        )}
      </View>
    </>
  );
}
```

> **`{...rest}`** é o segredo: passa `value`, `onChangeText`, `secureTextEntry`, `keyboardType` e qualquer outra prop nativa diretamente para o `TextInput` sem precisar declarar uma a uma.

#### Styles do Input
```typescript
// src/components/Input/styles.ts
import { StyleSheet } from 'react-native';
import { themes } from '../../global/themes';

export const styles = StyleSheet.create({
  titleInput: {
    marginTop: 20,
    marginLeft: 5,
    color: themes.colors.grey,
    fontSize: 14,
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
    height: '100%',
    paddingLeft: 5,
  },
  iconWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

---

### 13.5 Componente Button reutilizável
```typescript
// src/components/Button/index.tsx
import React from 'react';
import {
  TouchableOpacity, TouchableOpacityProps,
  Text, ActivityIndicator
} from 'react-native';
import { styles } from './styles';

type Props = TouchableOpacityProps & {
  text: string;          // texto do botão — obrigatório
  loading?: boolean;     // se true, mostra spinner ao invés do texto
};

export function Button({ text, loading, ...rest }: Props) {
  return (
    <TouchableOpacity
      style={[styles.button, { opacity: rest.disabled ? 0.6 : 1 }]}
      activeOpacity={0.8}
      disabled={loading}   // desabilita durante loading para evitar clique duplo
      {...rest}
    >
      {loading
        ? <ActivityIndicator color="#fff" size="small" />
        : <Text style={styles.buttonText}>{text}</Text>
      }
    </TouchableOpacity>
  );
}
```

```typescript
// src/components/Button/styles.ts
import { StyleSheet } from 'react-native';
import { themes } from '../../global/themes';

export const styles = StyleSheet.create({
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
});
```

---

### 13.8 Fragment — evitar wrapper desnecessário
```typescript
// ❌ Errado — View desnecessária que adiciona elemento ao layout
return (
  <View>
    <Text>Label</Text>
    <View style={styles.boxInput}>...</View>
  </View>
);

// ✅ Certo — Fragment não adiciona elemento real ao DOM
return (
  <>
    <Text>Label</Text>
    <View style={styles.boxInput}>...</View>
  </>
);

// Ou com import explícito (mesma coisa, mais legível para alguns)
import { Fragment } from 'react';
return (
  <Fragment>
    <Text>Label</Text>
    <View style={styles.boxInput}>...</View>
  </Fragment>
);
```

---

### 13.10 Spread de props com `...rest`
```typescript
// O ...rest captura TUDO que não foi desestruturado explicitamente
const { title, iconLeft, iconRight, ...rest } = props;

// E passa para o componente nativo automaticamente
<TextInput {...rest} />

// Assim o componente suporta qualquer prop do TextInput sem declarar:
// value, onChangeText, secureTextEntry, keyboardType, autoCapitalize,
// placeholder, maxLength, onFocus, onBlur, autoComplete, etc.
```

---

### 15.5 Consumir o Context em qualquer componente filho
```typescript
// src/components/CustomTabBar/index.tsx
import { useListContext } from '../../context/listContext';

export function CustomTabBar({ state, navigation }: BottomTabBarProps) {
  const { onOpen } = useListContext(); // ← desestrutura só o que precisa

  return (
    <View style={styles.tabArea}>
      {/* ... abas esquerda e direita ... */}

      {/* Botão central — abre o modal via Context */}
      <TouchableOpacity style={styles.tabItem} onPress={onOpen}>
        <View style={styles.buttonInner}>
          <AntDesign name="plus" size={24} color="#fff" />
        </View>
      </TouchableOpacity>

    </View>
  );
}
```

```typescript
// src/pages/list/index.tsx — também pode usar o mesmo Context
import { useListContext } from '../../context/listContext';

export function List() {
  const { modalVisible, onClose } = useListContext();

  return (
    <View style={{ flex: 1 }}>
      {/* Conteúdo da tela */}

      {/* Modal controlado pelo Context */}
      <Modal visible={modalVisible} onRequestClose={onClose}>
        {/* conteúdo do modal */}
      </Modal>
    </View>
  );
}
```

---

### 15.8 Diferença: Context vs Props

| Situação                              | Usar Props | Usar Context |
|---------------------------------------|------------|--------------|
| Componente pai → filho direto         | ✅          | ❌ desnecessário |
| Dados usados em 2+ níveis de profundidade | ❌ prop drilling | ✅ |
| Estado global (auth, tema, modal)     | ❌          | ✅ |
| Componente isolado e reutilizável     | ✅          | ❌ |

---

### 16.5 Componente Badge (bolinha colorida)
```typescript
// src/components/Badge/index.tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { themes } from '../../global/themes';

type Props = {
  color?: string;
};

export function Badge({ color }: Props) {
  return (
    <View style={[
      styles.badge,
      { borderColor: color || themes.colors.grey }
    ]} />
  );
}

const styles = StyleSheet.create({
  badge: {
    width: 20,
    height: 20,
    borderRadius: 10,   // metade do width/height = círculo perfeito
    borderWidth: 1,
  },
});
```

---

### 16.6 Componente Flag (etiqueta de status)
```typescript
// src/components/Flag/index.tsx
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { themes } from '../../global/themes';

type Props = {
  caption: string;
  color?: string;
};

export function Flag({ caption, color }: Props) {
  return (
    <TouchableOpacity style={[
      styles.container,
      { backgroundColor: color || themes.colors.grey }
    ]}>
      <Text style={styles.text}>{caption}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    height: 30,
    paddingHorizontal: 10,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: '#fff',
    fontSize: 12,
  },
});
```

> **Quando criar componente?** O curso ensina: observe quantas vezes o bloco se repete.
> - Card → aparece só na tela list → pode ficar inline como `renderCard`
> - Badge → pode aparecer em várias telas → vira componente
> - Flag → aparece no card e no modal → vira componente

---

### 16.8 Estender o componente Input para aceitar height

O modal precisa de um Input com altura maior (multiline). Adicionar prop `height` ao componente:

```typescript
// src/components/Input/index.tsx — adicionar à tipagem
type Props = TextInputProps & {
  title?: string;
  iconLeft?: IconComponent;
  iconLeftName?: string;
  iconRight?: IconComponent;
  iconRightName?: string;
  onIconLeftPress?: () => void;
  onIconRightPress?: () => void;
  height?: number;              // ← nova prop para altura variável
  labelStyle?: TextStyle;       // ← nova prop para estilo do label
};

// No StyleSheet do boxInput, calcular altura dinamicamente:
boxInput: {
  width: '90%',
  height: props.height || 40,  // ← usa height passado ou 40 por padrão
  // ... resto dos estilos
},
```

---

### 17.2 Propriedade `selected` no componente Flag
Adicionar feedback visual quando a flag está selecionada:

```typescript
// src/components/Flag/index.tsx — adicionar prop selected
type Props = {
  caption: string;
  color?: string;
  selected?: boolean;  // ← nova prop
};

export function Flag({ caption, color, selected }: Props) {
  return (
    <TouchableOpacity style={[
      styles.container,
      { backgroundColor: color || themes.colors.grey },
      selected && styles.selected,   // ← aplica borda se selecionado
    ]}>
      <Text style={styles.text}>{caption}</Text>
    </TouchableOpacity>
  );
}

// styles
selected: {
  borderWidth: 2,
  borderColor: '#000',
},
```

---

### 17.5 Componente CustomDateTimePicker
O DateTimePicker nativo tem comportamento diferente em iOS e Android.
A solução do curso: **envolver em um Modal transparente** para ter controle total:

```typescript
// src/components/CustomDateTimePicker/index.tsx
import React, { useEffect } from 'react';
import { Modal, View, Platform, StyleSheet } from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import { themes } from '../../global/themes';

type Props = {
  type: 'date' | 'time';             // modo do picker
  show: boolean;                     // se está visível
  setShow: (v: boolean) => void;     // fechar o picker
  date: Date;                        // valor atual
  setDate: (d: Date) => void;        // atualizar o Date bruto
  onDateChange: (d: Date) => void;   // callback com Date selecionado
};

export function CustomDateTimePicker({
  type, show, setShow, date, setDate, onDateChange
}: Props) {

  // Escuta mudanças no date e dispara o callback
  useEffect(() => {
    if (onDateChange) onDateChange(date);
  }, [date, onDateChange]);

  function handleChange(event: any, selectedDate?: Date) {
    setDate(selectedDate || date);
    setShow(false);   // fecha automaticamente após seleção no Android
  }

  return (
    <Modal
      transparent
      visible={show}
      onRequestClose={() => setShow(false)}
    >
      <View style={[
        styles.overlay,
        // Android: fundo transparente (picker tem fundo próprio)
        // iOS: sem fundo transparente
        Platform.OS === 'android' && { backgroundColor: themes.colors.transparent },
      ]}>
        <View style={styles.container}>
          <DateTimePicker
            value={date}
            mode={type}
            display={Platform.OS === 'ios' ? 'spinner' : 'default'}
            onChange={handleChange}
          />
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  container: {
    width: '80%',
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 10,
    elevation: 5,
  },
});
```

Adicionar cor transparente ao `themes.ts`:
```typescript
// src/global/themes.ts
export const themes = {
  colors: {
    // ... cores existentes ...
    transparent: 'rgba(0,0,0,0.5)',   // ← novo
  },
};
```