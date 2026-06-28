---
tags:
  - react-native
  - calendario
  - agenda
  - expo
fonte: wix/react-native-calendars + prática LashMatch/Cortejo
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("react-native-calendars Calendar Agenda markedDates LocaleConfig")`
> 2. MCP **fabrica-apps** — `buscar_historico("agenda calendario")`
> 3. Ler **protocolo**: `obsidian/fabrica/rag-protocolo-antes-de-codar.md` (caso Cortejo 09/06/2026)
> 4. Layout aba Agenda + slots: **[[agenda-salao-expo-padrao]]**
>
> **Não** implemente calendário só de memória. Escolha o componente (`Calendar` vs `Agenda` vs `ExpandableCalendar`) **depois** de consultar este guia.

---

# react-native-calendars — Guia de Implementação

> Lib: `react-native-calendars` (Wix)  
> Docs oficiais: https://wix.github.io/react-native-calendars/docs/Intro  
> GitHub: https://github.com/wix/react-native-calendars  
> Versão estável atual: 1.1314.0  
> Compatível com: Expo Go (sem bare workflow), iOS e Android  
> Pure JS — sem native module linking

---

## Instalação

```bash
npx expo install react-native-calendars
```

> **IMPORTANTE:** Use `npx expo install` (não `npm install`) para garantir compatibilidade com a versão do Expo SDK do projeto.

---

## Componentes disponíveis

| Componente | Uso ideal |
|---|---|
| `Calendar` | Calendário mensal estático, seleção de dia |
| `CalendarList` | Lista scrollável de meses (infinita) |
| `Agenda` | Split: calendário + lista de itens por dia (estilo iOS) |
| `AgendaList` | Lista de eventos agrupada por data, usa `CalendarProvider` |
| `ExpandableCalendar` | Calendário recolhível (semana ↔ mês) — mais próximo do iOS Calendar |
| `WeekCalendar` | Apenas a linha de semana |
| `Timeline` | View de horários tipo Google Calendar (blocos de tempo) |
| `CalendarProvider` | Context wrapper obrigatório para `ExpandableCalendar`, `AgendaList`, `WeekCalendar` |

---

## Localização para pt-BR

Sempre configure antes de usar qualquer componente (geralmente no `App.tsx` ou na raiz do app):

```typescript
import { LocaleConfig } from 'react-native-calendars';

LocaleConfig.locales['pt-br'] = {
  monthNames: [
    'Janeiro','Fevereiro','Março','Abril','Maio','Junho',
    'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
  ],
  monthNamesShort: [
    'Jan','Fev','Mar','Abr','Mai','Jun',
    'Jul','Ago','Set','Out','Nov','Dez'
  ],
  dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
  dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'],
  today: 'Hoje'
};
LocaleConfig.defaultLocale = 'pt-br';
```

---

## Formato de datas

Todas as datas usam o formato `YYYY-MM-DD` (string).  
Callbacks retornam um objeto `DateData`:

```typescript
type DateData = {
  day: number;      // 1-31
  month: number;    // 1-12
  year: number;
  timestamp: number; // UTC timestamp 00:00 AM
  dateString: string; // 'YYYY-MM-DD'
}
```

---

## 1. Calendar — Seleção de data simples

Melhor para: escolha de data pelo cliente antes de listar horários.

```typescript
import React, { useState } from 'react';
import { Calendar } from 'react-native-calendars';

const DatePicker = () => {
  const [selected, setSelected] = useState('');
  const today = new Date().toISOString().split('T')[0];

  return (
    <Calendar
      // Data mínima: hoje (bloqueia datas passadas)
      minDate={today}
      // Semana começa na segunda (padrão BR)
      firstDay={1}
      // Swipe entre meses
      enableSwipeMonths={true}
      // Esconde dias de outros meses
      hideExtraDays={true}
      // Dia selecionado
      markedDates={{
        [selected]: {
          selected: true,
          selectedColor: '#A855F7', // cor primária do app
          disableTouchEvent: true,
        }
      }}
      onDayPress={(day) => {
        setSelected(day.dateString);
      }}
      // Tema customizado
      theme={{
        backgroundColor: '#ffffff',
        calendarBackground: '#ffffff',
        textSectionTitleColor: '#6B7280',
        selectedDayBackgroundColor: '#A855F7',
        selectedDayTextColor: '#ffffff',
        todayTextColor: '#A855F7',
        dayTextColor: '#1F2937',
        textDisabledColor: '#D1D5DB',
        arrowColor: '#A855F7',
        monthTextColor: '#1F2937',
        textDayFontWeight: '400',
        textMonthFontWeight: '700',
        textDayHeaderFontWeight: '600',
      }}
    />
  );
};
```

### Props importantes do Calendar

| Prop | Tipo | Descrição |
|---|---|---|
| `minDate` | string | Data mínima selecionável |
| `maxDate` | string | Data máxima selecionável |
| `firstDay` | number | 0=Domingo, 1=Segunda |
| `markedDates` | object | Objeto com datas marcadas |
| `enableSwipeMonths` | boolean | Swipe lateral entre meses |
| `hideExtraDays` | boolean | Oculta dias de outros meses |
| `onDayPress` | function | Callback ao pressionar dia |
| `onMonthChange` | function | Callback ao mudar mês |
| `theme` | object | Customização visual completa |

---

## 2. Agenda — Split calendário + lista (estilo iOS)

Melhor para: profissional ver agenda do dia com lista de agendamentos.

```typescript
import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Agenda } from 'react-native-calendars';

// Tipo dos itens
type AgendaItem = {
  name: string;
  height: number;
  clienteNome?: string;
  horario?: string;
  servico?: string;
};

type AgendaItems = {
  [date: string]: AgendaItem[];
};

const AgendaProfissional = () => {
  const [items, setItems] = useState<AgendaItems>({});

  // Carrega itens quando mês fica visível
  const loadItemsForMonth = (month: { dateString: string }) => {
    // Aqui você busca do Firestore
    // Exemplo com dados mock:
    const newItems: AgendaItems = {};
    for (let i = -15; i < 85; i++) {
      const time = month.timestamp + i * 24 * 60 * 60 * 1000;
      const strTime = new Date(time).toISOString().split('T')[0];
      if (!newItems[strTime]) {
        newItems[strTime] = [];
      }
    }
    // Adiciona agendamentos reais
    newItems['2026-06-15'] = [
      { name: 'Extensão de cílios', height: 80, clienteNome: 'Ana Silva', horario: '09:00', servico: 'Volume Russo' },
      { name: 'Manutenção', height: 80, clienteNome: 'Carla Souza', horario: '11:00', servico: 'Fio a Fio' },
    ];
    setItems(newItems);
  };

  const renderItem = (item: AgendaItem) => (
    <View style={styles.item}>
      <Text style={styles.horario}>{item.horario}</Text>
      <Text style={styles.cliente}>{item.clienteNome}</Text>
      <Text style={styles.servico}>{item.servico}</Text>
    </View>
  );

  const renderEmptyDate = () => (
    <View style={styles.emptyDate}>
      <Text style={styles.emptyText}>Nenhum agendamento</Text>
    </View>
  );

  return (
    <Agenda
      items={items}
      selected={new Date().toISOString().split('T')[0]}
      loadItemsForMonth={loadItemsForMonth}
      renderItem={renderItem}
      renderEmptyDate={renderEmptyDate}
      rowHasChanged={(r1, r2) => r1.name !== r2.name}
      // Mostra só itens do dia selecionado
      showOnlySelectedDayItems={true}
      // Botão knob customizado
      showClosingKnob={true}
      pastScrollRange={3}
      futureScrollRange={3}
      theme={{
        agendaDayTextColor: '#6B7280',
        agendaDayNumColor: '#1F2937',
        agendaTodayColor: '#A855F7',
        agendaKnobColor: '#A855F7',
        dotColor: '#A855F7',
        selectedDayBackgroundColor: '#A855F7',
      }}
    />
  );
};

const styles = StyleSheet.create({
  item: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginRight: 16,
    marginTop: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  horario: { fontSize: 12, color: '#6B7280', marginBottom: 4 },
  cliente: { fontSize: 16, fontWeight: '600', color: '#1F2937' },
  servico: { fontSize: 14, color: '#A855F7', marginTop: 2 },
  emptyDate: { height: 15, flex: 1, paddingTop: 30, paddingLeft: 16 },
  emptyText: { color: '#9CA3AF', fontSize: 14 },
});
```

> **ATENÇÃO com o Agenda:** O objeto `items` deve ter uma chave para cada dia do range visível, mesmo que o array seja vazio `[]`. Dias sem chave são tratados como "não carregados" (mostra loading). Dias com array vazio `[]` mostram `renderEmptyDate`.

---

## 3. ExpandableCalendar — Mais próximo do iOS Calendar

Melhor para: tela principal do cliente escolher dia de forma fluida.  
Requer `CalendarProvider` como wrapper obrigatório.

```typescript
import React, { useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import {
  CalendarProvider,
  ExpandableCalendar,
  AgendaList,
} from 'react-native-calendars';

// Dados de agendamentos disponíveis
const SLOTS = [
  { title: '2026-06-15', data: [{ hour: '09:00', disponivel: true }, { hour: '10:00', disponivel: false }] },
  { title: '2026-06-16', data: [{ hour: '14:00', disponivel: true }] },
];

const AgendamentoScreen = () => {
  const today = new Date().toISOString().split('T')[0];
  const [selectedDate, setSelectedDate] = useState(today);

  // Datas marcadas com pontos (têm disponibilidade)
  const markedDates = {
    '2026-06-15': { marked: true, dotColor: '#A855F7' },
    '2026-06-16': { marked: true, dotColor: '#A855F7' },
    [selectedDate]: { selected: true, selectedColor: '#A855F7' },
  };

  const renderItem = ({ item }: { item: { hour: string; disponivel: boolean } }) => (
    <View style={[styles.slot, !item.disponivel && styles.slotOcupado]}>
      <Text style={styles.slotHour}>{item.hour}</Text>
      <Text style={styles.slotStatus}>{item.disponivel ? 'Disponível' : 'Ocupado'}</Text>
    </View>
  );

  return (
    <CalendarProvider
      date={selectedDate}
      onDateChanged={(date) => setSelectedDate(date)}
      showTodayButton
      todayButtonStyle={{ backgroundColor: '#A855F7' }}
    >
      <ExpandableCalendar
        firstDay={1}
        markedDates={markedDates}
        // Começa na posição fechada (só semana visível)
        initialPosition="closed"
        closeOnDayPress={true}
        allowShadow={true}
        theme={{
          selectedDayBackgroundColor: '#A855F7',
          todayTextColor: '#A855F7',
          dotColor: '#A855F7',
          arrowColor: '#A855F7',
        }}
      />
      <AgendaList
        sections={SLOTS}
        renderItem={renderItem}
        sectionStyle={styles.section}
      />
    </CalendarProvider>
  );
};

const styles = StyleSheet.create({
  section: {
    backgroundColor: '#F3F4F6',
    color: '#6B7280',
    textTransform: 'uppercase',
    fontSize: 12,
    fontWeight: '600',
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  slot: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginVertical: 4,
    padding: 16,
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#A855F7',
  },
  slotOcupado: {
    opacity: 0.4,
    borderLeftColor: '#D1D5DB',
  },
  slotHour: { fontSize: 18, fontWeight: '700', color: '#1F2937' },
  slotStatus: { fontSize: 14, color: '#6B7280' },
});
```

---

## 4. Fluxo de Agendamento com Firestore

Padrão recomendado para integração com Firebase:

```typescript
// hooks/useDisponibilidade.ts
import { useEffect, useState } from 'react';
import { collection, query, where, getDocs } from 'firebase/firestore';
import { db } from '../config/firebase';

type MarkedDates = { [date: string]: { marked?: boolean; dotColor?: string; disabled?: boolean } };

export const useDisponibilidade = (profissionalId: string, mes: string) => {
  const [markedDates, setMarkedDates] = useState<MarkedDates>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const buscarDisponibilidade = async () => {
      setLoading(true);
      // Busca agendamentos do mês no Firestore
      const q = query(
        collection(db, 'agendamentos'),
        where('profissionalId', '==', profissionalId),
        where('mes', '==', mes),
        where('status', '!=', 'cancelado')
      );
      const snap = await getDocs(q);
      
      const ocupados: { [date: string]: number } = {};
      snap.forEach(doc => {
        const { data } = doc.data();
        ocupados[data] = (ocupados[data] || 0) + 1;
      });

      // Marca dias com disponibilidade
      const marked: MarkedDates = {};
      const MAX_SLOTS_DIA = 8;
      Object.entries(ocupados).forEach(([date, count]) => {
        if (count >= MAX_SLOTS_DIA) {
          marked[date] = { disabled: true }; // lotado
        } else {
          marked[date] = { marked: true, dotColor: '#A855F7' };
        }
      });
      setMarkedDates(marked);
      setLoading(false);
    };

    buscarDisponibilidade();
  }, [profissionalId, mes]);

  return { markedDates, loading };
};
```

---

## Marking Types — Estilos de marcação

> **ATENÇÃO:** Só é possível usar UM tipo de marking por calendário. Não misture.

### `simple` (padrão)
```javascript
markedDates={{
  '2026-06-15': { marked: true, dotColor: '#A855F7', selected: true, selectedColor: '#A855F7' }
}}
```

### `multi-dot`
```javascript
// No componente: markingType='multi-dot'
markedDates={{
  '2026-06-15': {
    dots: [
      { key: 'servico1', color: '#A855F7' },
      { key: 'servico2', color: '#10B981' }
    ]
  }
}}
```

### `period`
```javascript
// No componente: markingType='period'
markedDates={{
  '2026-06-10': { startingDay: true, color: '#A855F7' },
  '2026-06-11': { color: '#C4B5FD' },
  '2026-06-12': { endingDay: true, color: '#A855F7' },
}}
```

---

## Pitfalls comuns e soluções

### 1. Warning: missing key prop no AgendaList
```typescript
// ERRADO
sections={[{ title: '2026-06-15', data: [...] }]}

// CERTO — garanta que cada item tem id único
sections={[{ title: '2026-06-15', data: items.map(i => ({ ...i, key: i.id })) }]}
// E no renderItem use keyExtractor
```

### 2. Agenda mostrando loading infinito
O `items` prop deve ter chave para TODOS os dias do range visible, mesmo vazio:
```typescript
// ERRADO: só dias com itens
items={{ '2026-06-15': [...] }}

// CERTO: todos os dias do range com array vazio se sem itens
items={{
  '2026-06-14': [],
  '2026-06-15': [...agendamentos],
  '2026-06-16': [],
}}
```

### 3. ExpandableCalendar sem CalendarProvider
```typescript
// SEMPRE envolva com CalendarProvider
<CalendarProvider date={selectedDate}>
  <ExpandableCalendar {...props} />
</CalendarProvider>
```

### 4. Datas de outros fusos horários
```typescript
// Nunca use new Date().toISOString() diretamente — pode dar dia errado
// USE:
const getLocalDateString = () => {
  const now = new Date();
  const offset = now.getTimezoneOffset();
  const local = new Date(now.getTime() - offset * 60 * 1000);
  return local.toISOString().split('T')[0];
};
```

### 5. Performance — memo no renderItem
```typescript
import { memo } from 'react';
const AgendaItemComponent = memo(({ item }) => (
  <View>...</View>
));
// rowHasChanged é obrigatório no Agenda para evitar re-renders
rowHasChanged={(r1, r2) => r1.id !== r2.id}
```

---

## Escolha de componente por caso de uso

| Caso de uso | Componente recomendado |
|---|---|
| Cliente escolhe data → vê horários disponíveis | `Calendar` + `FlatList` de horários |
| Profissional vê agenda do dia (lista de atendimentos) | `Agenda` |
| Tela principal com calendário recolhível estilo iOS | `CalendarProvider` + `ExpandableCalendar` + `AgendaList` |
| Blocos de horário estilo Google Calendar | `Timeline` |
| Seleção de período (férias, disponibilidade) | `Calendar` com `markingType='period'` |

---

## Dependências peer

Nenhuma dependência nativa extra. Funciona direto no Expo Go.  
Se usar `Timeline`, pode requerer `react-native-gesture-handler` (já incluso no Expo).

---

## Links de referência

- Docs: https://wix.github.io/react-native-calendars/docs/Intro
- Exemplos de código: https://github.com/wix/react-native-calendars/tree/master/example/src/screens
- npm: https://www.npmjs.com/package/react-native-calendars
