---
tags:
  - checklist
  - deploy
  - qualidade
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "9. CHECKLIST DO AGENTE ANTES DE GERAR CÓDIGO"
  - "12.16 Checklist de boas práticas aprendidas no curso"
  - "13.11 Checklist de componentização"
  - "15.9 Checklist de Context API"
  - "16.10 Checklist desta aula"
---

## 9. CHECKLIST DO AGENTE ANTES DE GERAR CÓDIGO

Antes de gerar qualquer tela, confirmar:

- [ ] Usa `StyleSheet.create` (não inline styles espalhados)
- [ ] `KeyboardAvoidingView` em formulários com TextInput
- [ ] `useSafeAreaInsets()` para padding do topo/bottom
- [ ] `onAuthStateChanged` com `return unsubscribe` no cleanup
- [ ] `onSnapshot` com `return unsubscribe` no cleanup
- [ ] Estados: `loading`, `error`, e dado principal sempre declarados
- [ ] `FlatList` com `keyExtractor` e `showsVerticalScrollIndicator={false}`
- [ ] Variáveis Firebase em `.env` com prefixo `EXPO_PUBLIC_`
- [ ] `npx expo install` para pacotes (não `npm install` direto)
- [ ] Touch targets mínimo de 44px de altura (acessibilidade)
- [ ] Tratar diferenças iOS vs Android com `Platform.OS`

---

---

### 12.16 Checklist de boas práticas aprendidas no curso

- [ ] Cores sempre em `global/themes.ts` — nunca hardcoded
- [ ] Styles sempre em `styles.ts` separado do `index.tsx`
- [ ] Dimensões responsivas com `Dimensions.get('window')`
- [ ] Declarar tipos de imagens em `src/@types/png.d.ts`
- [ ] Input com ícone: `View` em `flexDirection: 'row'` agrupando `TextInput` + ícone
- [ ] Sempre ter: `value` + `onChangeText` nos `TextInput` (campos controlados)
- [ ] Botão com `disabled={loading}` para evitar clique duplo
- [ ] `ActivityIndicator` inline no botão durante loading
- [ ] `Alert.alert('Título', 'Mensagem')` para feedbacks do usuário
- [ ] Função de login: validar campos → setLoading(true) → try/catch → finally setLoading(false)

---

---

### 13.11 Checklist de componentização

- [ ] Identificar padrão de repetição (mesmo bloco de código em 2+ lugares)
- [ ] Criar pasta `components/NomeComponente/` com `index.tsx` e `styles.ts`
- [ ] Definir `type Props` com TypeScript para todas as props recebidas
- [ ] Usar `?` para props opcionais
- [ ] Usar `& TextInputProps` ou `& TouchableOpacityProps` para herdar props nativas
- [ ] Usar `{...rest}` para passar props nativas sem declarar uma a uma
- [ ] Renderização condicional `{prop && <Componente />}` para props opcionais
- [ ] Usar `<>...</>` (Fragment) quando não precisar de wrapper real
- [ ] Calcular tamanhos dinâmicos com função utilitária quando necessário
- [ ] Importar sempre de `'react-native'` — nunca de `'react-native-paper'` por engano

---

---

---

### 15.9 Checklist de Context API

- [ ] Criar arquivo em `src/context/nomeContext.tsx`
- [ ] Definir `type ContextProps` com todas as propriedades tipadas
- [ ] Criar o Context com `createContext<ContextProps>({} as ContextProps)`
- [ ] Criar o Provider com `{ children: React.ReactNode }` como prop
- [ ] Exportar hook customizado `export const useXxx = () => useContext(XxxContext)`
- [ ] Envolver as rotas/telas corretas com o Provider (nem mais nem menos)
- [ ] Consumir com `const { prop } = useXxx()` — desestruturar só o necessário
- [ ] Auth Context no `app.tsx` — para toda a aplicação
- [ ] Modal/Feature Context no componente pai mais próximo — não poluir o global
- [ ] Cleanup no `useEffect` do `onAuthStateChanged` — sempre `return unsubscribe`

---

---

---

### 16.10 Checklist desta aula

- [ ] Header com `height: height / 6` — nunca altura fixa para blocos grandes
- [ ] `FlatList` com `keyExtractor` usando valor único (`item.toString()`)
- [ ] `renderItem` extraído como função separada — mantém JSX limpo
- [ ] Componentes Badge e Flag em pastas próprias com `styles.ts`
- [ ] `useRef<Modalize>` para controlar modal — não useState
- [ ] Modal declarado UMA VEZ no Provider do Context, não em cada tela
- [ ] `adjustToContentHeight` no Modalize para altura automática
- [ ] `multiline + numberOfLines` para Input de texto longo
- [ ] `gap` no lugar de `marginRight` para espaçamento entre itens em linha
- [ ] Cores adicionais (`red`, `green`, `blueLight`) centralizadas em `themes.ts`

---

---

---

### 17.11 Checklist do formulário modal

- [ ] Um `useState` por campo do formulário
- [ ] Estados separados para: valor exibido (string) e valor bruto (Date)
- [ ] `editable={false}` em inputs preenchidos por picker
- [ ] `onPress` no Input de data/hora para abrir o picker
- [ ] `.toLocaleDateString('pt-BR')` para formatar data para exibição
- [ ] `.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })` para hora
- [ ] `Platform.OS === 'ios'` para comportamento diferente entre plataformas
- [ ] `CustomDateTimePicker` encapsulado em Modal transparente
- [ ] `useEffect([date, onDateChange])` para sincronizar callbacks
- [ ] `KeyboardAvoidingView` dentro do modal para evitar bug do teclado
- [ ] `snapPoint={height / 1.7}` no Modalize em vez de `adjustToContentHeight`
- [ ] Flags renderizadas com `.map()` a partir de array — nunca hardcoded uma a uma

---

---

---

### 18.17 Checklist de código — padrões LashMatch

**Sempre fazer:**
- [ ] Importar `auth`, `firestore`, `storage` do `utils/firebaseConfig.ts`
- [ ] Usar `app.options.appId` para montar o path do Firestore
- [ ] Usar `serverTimestamp()` para campos de data no Firestore
- [ ] Usar `useFocusEffect` + `useCallback` para recarregar dados ao voltar para a tela
- [ ] Cleanup de `onSnapshot` e `onAuthStateChanged` com `return () => unsubscribe()`
- [ ] Usar `tw` para layouts e `StyleSheet` para componentes com muitos estilos
- [ ] Fundo preto (`#000`) em todas as telas
- [ ] Cor primária `#D63384` em destaques e botões de ação principal
- [ ] `SafeAreaView` como wrapper principal das telas — preferir `react-native-safe-area-context` (o `SafeAreaView` de `react-native` está **deprecated** no RN novo)
- [ ] `KeyboardAvoidingView` + `ScrollView keyboardShouldPersistTaps="handled"` em modais com formulário
- [ ] `Platform.OS === 'ios' ? 'padding' : 'height'` no `behavior` do `KeyboardAvoidingView`

**Nunca fazer:**
- [ ] ❌ `const auth = getAuth(app)` dentro de componentes
- [ ] ❌ `const db = getFirestore(app)` dentro de componentes
- [ ] ❌ Hardcodar `appId` no path do Firestore
- [ ] ❌ Colocar `FlatList` dentro de `ScrollView` (quebra a rolagem)
- [ ] ❌ Cores fora da paleta definida em `COLORS`
- [ ] ❌ Usar `navigation.navigate` após login — sempre `router.replace`

---

---

### 21.11 Checklist de notificações

- [ ] `Notifications.setNotificationHandler` no topo do `_layout.tsx`
- [ ] Canal Android criado antes de qualquer notificação (`setNotificationChannelAsync`)
- [ ] Pedir permissão contextualmente — não na abertura do app
- [ ] Salvar `notificationId` no Firestore para cancelar depois
- [ ] Cleanup dos listeners com `return () => listener.remove()`
- [ ] Testar sempre em **dispositivo físico** — emuladores não suportam
- [ ] Para protótipo: notificações **locais** — no Expo Go o LashMatch evita import estático do pacote (§21.12); para testar banner local de verdade, use **development build**
- [ ] Para produção: usar **EAS Build** + push token para notificações remotas
- [ ] `channelId` em todas as notificações Android
- [ ] Não usar push remota no Expo Go SDK 53+ — vai falhar silenciosamente

---

### 24.10 Checklist do módulo financeiro

- [ ] Campo `custoUnitario` adicionado ao schema do estoque
- [ ] Schema de `vendas` e `despesas` criado no Firestore
- [ ] `runTransaction` para venda + baixa de estoque — nunca separados
- [ ] Verificar estoque suficiente ANTES de salvar a venda
- [ ] Calcular `custoTotal` e `lucroBruto` no momento do registro
- [ ] Desnormalizar `clienteNome` e `produtoNome` nas vendas
- [ ] Relatório busca vendas E despesas do período
- [ ] `lucroLiquido = lucroBruto - despesas` (não receita - despesas)
- [ ] Valores formatados com `toLocaleString('pt-BR')` — nunca `toFixed(2)` sem formatação
- [ ] Cores financeiras: verde=receita, vermelho=custo, rosa=lucro
- [ ] `ticketMedio` só calculado se `qtdVendas > 0` — evitar divisão por zero

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · Curso React Native Expo Go — Caio Eduardo · Projeto LashMatch (referência principal) · developer.z-api.io · docs.expo.dev/push-notifications/overview*

---

---

### 25.11 Checklist do sistema de agendamento completo

**Parte 1 — Cadastros base (fazer primeiro):**
- [ ] `funcionarias.tsx` — CRUD completo com ativa/inativa
- [ ] `servicos.tsx` — CRUD com `duracaoMinutos` e `preco`
- [ ] Ambas as abas adicionadas no `_layout.tsx`

**Parte 2 — Refatorar agendamentos:**
- [ ] Seleção de funcionária no formulário
- [ ] Seleção de serviço com exibição de duração e preço
- [ ] `dataHoraFim` calculado e salvo obrigatoriamente
- [ ] `verificarDisponibilidade` chamado antes de salvar
- [ ] Campos `funcionariaNome` e `servicoNome` desnormalizados
- [ ] `status: 'confirmado'` e `origem: 'app'` ao criar

**Parte 3 — Página pública:**
- [ ] `app/agendar/index.tsx` sem login
- [ ] `gerarSlotsDisponiveis` — só mostrar horários livres
- [ ] `origem: 'link_publico'` ao salvar
- [ ] Regras Firestore permitindo leitura pública e criação sem auth
- [ ] `enviarConfirmacaoAgendamento` — Cloud Function onDocumentCreated
- [ ] Deploy: `firebase deploy --only functions:enviarConfirmacaoAgendamento`

**Regras gerais:**
- [ ] Ignorar `status: 'cancelado'` em todas as queries de conflito
- [ ] Ao editar, passar `agendamentoExcluidoId` para não conflitar consigo mesmo
- [ ] Integrar `preco` com módulo financeiro (Seção 24) ao marcar como `'concluido'`

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · Curso React Native Expo Go — Caio Eduardo · Projeto LashMatch (referência principal) · developer.z-api.io · docs.expo.dev/push-notifications/overview*

---

---

### 27.5 Checklist

- [ ] `MP_PLANO_SETUP_KEY` definido no ambiente das functions antes de usar `criarPlanoMP`
- [ ] Após criar planos no MP, documento `config/mercadopago_planos` preenchido (ou rodar `criarPlanoMP` por plano)
- [ ] Painel MP ou preapproval com URL de `webhookAssinatura` para sincronizar status
- [ ] App usa `PLANO_IDS` / tipos de `constants/planos.ts` ao chamar `criarAssinatura`

---

*Última atualização: abril 2026 | Fontes: reactnative.dev/docs · docs.expo.dev/guides/using-firebase · Curso React Native Expo Go — Caio Eduardo · Projeto LashMatch (referência principal) · developer.z-api.io · mercadopago.com.br/developers/pt/docs*