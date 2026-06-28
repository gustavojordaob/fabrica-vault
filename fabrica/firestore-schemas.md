---
tags:
  - firestore
  - schema
  - dados
fonte: CLAUDE.md
gerado_em: 2026-05-11
secoes:
  - "5.3 Modelo de dados recomendado (coleções)"
  - "10. ESTRUTURA DE PASTAS RECOMENDADA"
  - "12.2 Estrutura de pastas do curso"
  - "12.6 Estrutura de layout em 3 blocos (padrão do curso)"
  - "13.2 Estrutura de pasta para componentes"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **firebase** (plugin) — rules, indexes compostos, modelagem validada no projeto
> 2. MCP **fabrica-apps** — `rag_buscar("firestore schema")` + `buscar_historico("firestore")`

---

### 5.3 Modelo de dados recomendado (coleções)
```
/users/{uid}
  - name: string
  - email: string
  - createdAt: Timestamp
  - photoURL: string | null

/posts/{postId}
  - title: string
  - content: string
  - authorId: string (ref para users/{uid})
  - createdAt: Timestamp
  - likes: number

/chats/{chatId}/messages/{messageId}
  - text: string
  - senderId: string
  - createdAt: Timestamp
```

---

---

## 10. ESTRUTURA DE PASTAS RECOMENDADA

```
meu-app/
├── app/                    # Expo Router — telas e layouts
│   ├── _layout.tsx         # Layout raiz
│   ├── index.tsx           # Tela inicial (splash/redirect)
│   ├── (auth)/
│   │   ├── _layout.tsx
│   │   ├── login.tsx
│   │   └── register.tsx
│   └── (tabs)/
│       ├── _layout.tsx
│       ├── home.tsx
│       └── profile.tsx
├── components/             # Componentes reutilizáveis
├── hooks/                  # Hooks customizados (useAuth, usePosts...)
├── services/               # Lógica Firebase (firestore, storage...)
├── config/
│   └── firebaseConfig.ts   # Inicialização Firebase
├── types/                  # TypeScript interfaces
├── constants/              # Cores, tamanhos, strings
├── .env                    # Chaves Firebase (não commitar)
└── app.json                # Configuração Expo
```

---

---

### 12.2 Estrutura de pastas do curso
```
src/
  assets/
    images/
      logo.png          ← imagens do app
  components/           ← componentes reutilizáveis
  global/
    themes.ts           ← paleta de cores centralizada
  pages/
    login/
      index.tsx         ← tela de login
      styles.ts         ← estilos separados da tela
```

> Padrão do curso: **separar styles.ts do index.tsx** para cada tela. Mantém o código mais limpo e organizado.

---

### 12.6 Estrutura de layout em 3 blocos (padrão do curso)
O curso ensina a dividir telas em 3 `View`s: topo, meio e base.
```typescript
<View style={styles.container}>
  {/* Topo: logo + título */}
  <View style={styles.boxTop}>
    <Image source={logo} style={styles.logo} resizeMode="contain" />
    <Text style={styles.title}>Bem-vindo de volta</Text>
  </View>

  {/* Meio: formulário */}
  <View style={styles.boxMid}>
    {/* inputs aqui */}
  </View>

  {/* Base: botão + link */}
  <View style={styles.boxBottom}>
    {/* botão e texto de cadastro */}
  </View>
</View>
```

---

### 13.2 Estrutura de pasta para componentes
```
src/
  components/
    Input/
      index.tsx       ← lógica e JSX do componente
      styles.ts       ← estilos isolados
    Button/
      index.tsx
      styles.ts
```

> Padrão do curso: **cada componente em sua própria pasta**, com `index.tsx` e `styles.ts` separados.

---

### 14.3 Estrutura de pastas de rotas
```
src/
  routes/
    index.tsx          ← Stack Navigator principal (raiz)
    bottomRoutes.tsx   ← Bottom Tab Navigator (telas autenticadas)
  pages/
    login/
    list/
    user/
```

---

### 15.2 Estrutura de pastas
```
src/
  context/
    listContext.tsx    ← cria o Context e o Provider
```

---

### 18.2 Estrutura de pastas real do projeto

```
LashMatch/
├── app/
│   ├── _layout.tsx              ← Stack raiz com tema dark
│   ├── index.tsx                ← Splash/redirect com onAuthStateChanged
│   ├── Login.tsx                ← Login + cadastro
│   ├── cadastroUsuario.tsx      ← Formulário de cadastro
│   ├── recuperarSenha.tsx       ← Recuperação de senha
│   ├── camera.tsx               ← Câmera + captura de foto
│   ├── analysisResult.tsx       ← Resultado da análise IA
│   ├── (tabs)/
│   │   ├── _layout.tsx          ← Tab Navigator com tema dark
│   │   ├── index.tsx            ← Home (clientes recentes + nova análise)
│   │   ├── clientes.tsx         ← Lista completa de clientes
│   │   ├── explore.tsx          ← Explorar/Discover
│   │   ├── guia-mapeamentos.tsx ← Tabela/filtros do mapa visagismo → estilo (rota oculta na tab bar)
│   │   ├── curvatura-espessuras.tsx ← Referência curvatura/espessura (rota oculta)
│   │   ├── pagamento.tsx        ← Gestão de plano/pagamento
│   │   └── perfilUsuario.tsx    ← Perfil da lash designer
│   ├── constants/
│   │   └── mapaCilios.ts        ← Dados do guia de mapeamentos (MAPA_CILIOS)
│   ├── assistente/              ← Assistente manual (9 passos)
│   │   ├── _layout.tsx
│   │   ├── passo1_rosto.tsx
│   │   └── ... passo9
│   ├── clientes/
│   │   └── [id].tsx             ← Perfil + histórico da cliente
│   ├── pagameto/                ← Fluxo de pagamento
│   │   ├── cartao.tsx
│   │   └── cancelamento.tsx
│   └── lib/                     ← Regras de negócio puras
│       ├── tamanhoFiosRules.ts
│       ├── colorimetriaRules.ts
│       ├── curvaturaRules.ts
│       └── visagismoRules.ts
├── components/
│   ├── CameraMolds.tsx          ← Moldes de rosto para câmera
│   ├── ModalConfirmacaoGlobal.tsx
│   ├── ModalDatePicker.tsx
│   └── SelectModal.tsx
├── utils/
│   ├── firebaseConfig.ts        ← Inicialização Firebase (fonte única)
│   ├── config.ts                ← URLs das Cloud Functions
│   ├── options.ts               ← Opções de selects
│   └── calcularIdade.ts / formatarData.ts / etc
├── shared/mappers/              ← Conversões de dados
├── functions/SRC/index.ts       ← Cloud Functions (Node.js + Gemini)
└── assets/
    ├── logos/lashmatch.svg
    └── lashes/                  ← Imagens dos estilos de cílios
```

---

### 24.6 Tela de Nova Venda — estrutura

```typescript
// app/(tabs)/financeiro/nova-venda.tsx
// Campos do formulário:
// 1. Cliente (busca na lista de clientes)
// 2. Serviço (texto livre ou seleção de lista)
// 3. Valor da venda (R$)
// 4. Forma de pagamento (chips: Pix, Dinheiro, Cartão crédito, Cartão débito)
// 5. Produtos usados (seleção do estoque com quantidade e custo unitário)
// 6. Observação (opcional)
// 7. Preview automático: Custo total / Lucro bruto
// 8. Botão Salvar → runTransaction(venda + baixa estoque)
```

---

### 24.7 Tela de Relatório — estrutura

```typescript
// app/(tabs)/financeiro/relatorio.tsx
// Filtros de período: Hoje / Esta semana / Este mês / Personalizado
// Cards de resumo:
//   - Total de receita (verde)
//   - Total de custos de produtos (vermelho)
//   - Lucro bruto (rosa)
//   - Total de despesas (vermelho)
//   - Lucro líquido (rosa — destaque maior)
//   - Ticket médio (cinza)
//   - Quantidade de vendas (cinza)
// Gráfico de formas de pagamento (barras simples com View proporcional)
// Lista de vendas do período (FlatList)
```