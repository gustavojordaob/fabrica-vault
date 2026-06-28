# PROJECT.md — LashMatch

## 1) Visao Geral do App

LashMatch e um app mobile (Expo + React Native + Expo Router) para lash designers realizarem analise de rosto/olhos e receberem recomendacoes tecnicas de extensao de cilios. O app possui dois fluxos principais:

- Analise com IA: captura duas fotos (frente e perfil), envia para Cloud Function com Gemini, recebe classificacao tecnica e estilo recomendado.
- Assistente manual (9 passos): profissional responde perguntas guiadas (rosto, profundidade, eixo, alinhamento, distanciamento, palpebra, concavo, curvatura, ponto Z e colorimetria) e gera o mesmo tipo de relatorio final.

O resultado e salvo no Firestore como historico da cliente e pode ser revisitado no perfil individual da cliente.

### Stack Tecnica Atual

- Frontend: Expo SDK 54, React 19, React Native 0.81, Expo Router 6
- Estado/arquitetura: hooks React + navegacao file-based
- Estilo: mistura de `twrnc` (Tailwind RN) e `StyleSheet`
- Backend: Firebase Cloud Functions (Node 22, TypeScript)
- Banco/Storage/Auth: Firebase Auth + Firestore + Cloud Storage
- IA: Gemini via `@google/genai`
- Pagamentos: Mercado Pago (assinatura/preapproval)
- Lembretes: **WhatsApp Business API (Meta)** via Cloud Functions + notificacoes locais (`expo-notifications`, com limitacao no Expo Go)

---

## 2) Paleta de Cores Atual

Paleta predominante identificada no app:

- Primaria (brand): `#D63384` (tambem aparece como `#ff2f92` em varias telas)
- Fundo global: `#000000`
- Superficie/card: `#1a1a1a` e `#111111`
- Bordas: `#333333` / `#222222`
- Texto principal: `#FFFFFF`
- Texto secundario: `#AAAAAA`, `#BBBBBB`, `#9E9E9E`, `#777777`
- Erro: `#ff4d4d`
- Sucesso (fluxo manual): `#4ade80`

Observacao: a base visual e coerente (tema dark + rosa), mas ha pequenas variacoes de tonalidade de rosa (`#D63384` e `#ff2f92`) entre modulos.

---

## 3) Telas e Rotas Existentes

## Rotas raiz (`app/_layout.tsx`)

- `/` -> `app/index.tsx` (splash + redirecionamento por auth)
- `/Login` -> `app/Login.tsx`
- `/cadastroUsuario` -> `app/cadastroUsuario.tsx`
- `/recuperarSenha` -> `app/recuperarSenha.tsx`
- `/camera` -> `app/camera.tsx`
- `/analysisResult` -> `app/analysisResult.tsx`
- `/clientes/[id]` -> `app/clientes/[id].tsx`
- `/+not-found` -> `app/+not-found.tsx`

## Grupo de abas (`app/(tabs)/_layout.tsx`)

- `/(tabs)` ou `/(tabs)/index` -> `app/(tabs)/index.tsx` (home/painel)
- `/(tabs)/clientes` -> `app/(tabs)/clientes.tsx`
- `/(tabs)/estoque` -> `app/(tabs)/estoque.tsx` (controle de estoque de produtos)
- `/(tabs)/financeiro` -> grupo com stack em `app/(tabs)/financeiro/_layout.tsx`:
  - `/(tabs)/financeiro` ou `/(tabs)/financeiro/index` -> hub (atalhos)
  - `/(tabs)/financeiro/nova-venda` -> `app/(tabs)/financeiro/nova-venda.tsx` (venda + baixa de estoque em transacao)
  - `/(tabs)/financeiro/relatorio` -> `app/(tabs)/financeiro/relatorio.tsx` (periodo, resumo, despesas, lista de vendas)
- `/(tabs)/funcionarias` -> `app/(tabs)/funcionarias.tsx` (cadastro de funcionarias: nome, especialidade, ativa/inativa; padrao visual alinhado ao estoque)
- `/(tabs)/servicos` -> `app/(tabs)/servicos.tsx` (cadastro de servicos: nome, duracao em minutos, preco, ativo/inativo)
- `/(tabs)/agendamentos` -> `app/(tabs)/agendamentos.tsx` (agenda, lembretes, filtro por cliente/data)
- `/(tabs)/explore` -> `app/(tabs)/explore.tsx` (chat assistente IA)
- `/(tabs)/perfilUsuario` -> `app/(tabs)/perfilUsuario.tsx`
- `/(tabs)/pagamento` -> `app/(tabs)/pagamento.tsx`
- `/(tabs)/guia-mapeamentos` -> `app/(tabs)/guia-mapeamentos.tsx` (tabela e filtros do mapa eixo/profundidade/alinhamento/distanciamento -> estilo; rota registrada na aba com `href: null`, aberta a partir de outras telas)
- `/(tabs)/curvatura-espessuras` -> `app/(tabs)/curvatura-espessuras.tsx` (referencia curvatura/espessura; `href: null`)

## Arquivos auxiliares relevantes

- `hooks/useLembretesEnviados.ts` — escuta `resumoLembretes/ultimo` e dispara notificacao local quando lembretes automaticos rodam; em **Expo Go** o modulo `expo-notifications` nao e carregado (evita erro de push remoto removido no SDK 53+).
- `types/agendamento.ts` — tipos `AgendamentoFirestore` e `ResumoLembretesFirestore` alinhados ao Firestore de agendamentos/resumo.
- `types/financeiro.ts` — tipos de vendas, produtos usados, formas de pagamento e despesas.
- `utils/registrarVendaFirestore.ts` — `runTransaction`: grava venda em `vendas` e baixa `quantidade` no `estoque` (produtos ativos, estoque suficiente).
- Codigo das Cloud Functions em `functions/SRC/index.ts` (pasta `SRC` em maiusculo; build gera `functions/lib/`).
- `app/constants/mapaCilios.ts` — dados do **Guia de mapeamentos** (combinacoes visagismo -> estilo).

## Fluxo assistente manual (`app/assistente`)

- `/assistente/passo1_rosto`
- `/assistente/passo2_profundidade`
- `/assistente/passo3_eixo`
- `/assistente/passo4_alinhamento`
- `/assistente/passo5_distanciamento`
- `/assistente/passo6_palpebra_concavo`
- `/assistente/passo7_curvatura_natural`
- `/assistente/passo8_ponto_z`
- `/assistente/Passo9ColorimetriaScreen`

## Fluxo de pagamento (pasta com typo: `pagameto`)

- `/pagameto/cartao`
- `/pagameto/cancelamento`

Observacao importante: existe typo de pasta/rota (`pagameto` em vez de `pagamento`) e o app atualmente usa esse caminho em navegacao.

---

## 4) Schema Firestore Atual

Schema inferido do codigo frontend + Cloud Functions:

## Colecao de usuarias (lash designers)

`usuarios/{uid}` (criado no cadastro via `setDoc`)

Campos observados:
- `nome`, `sobrenome`, `email`
- `dataNascimento`, `estado`, `cidade`
- `senha` (atualmente vai para Firestore no cadastro, risco de seguranca)
- `plano` (objeto atualizado por pagamento / assinatura MP)
  - `id`: `mensal | anual`
  - `nome`: ex. `Plano Mensal`, `Plano Anual`
  - `status`: string em maiúsculas alinhada ao MP (`PENDING`, `AUTHORIZED`, `CANCELLED`, etc.)
  - `atualizadoEm`: ISO string (cliente)
  - `canceladoEm`: ISO string (opcional, cancelamento)
  - `mp_preapproval_id`, `mp_customer_id`, `mp_card_id`
  - `mp_preapproval_plan_id`: string (opcional) — quando a assinatura usa `preapproval_plan` criado via Cloud Function `criarPlanoMP`
  - `ultimaSincronizacaoWebhook`: ISO string (opcional) — último processamento do `webhookAssinatura`
- `pagamento` (objeto)
  - `status`
  - `metodo` (`MERCADO_PAGO`)
  - `atualizadoEm`

## Config Mercado Pago (planos de assinatura)

Documento único: `config/mercadopago_planos`

Chaves de primeiro nível: `mensal`, `anual` (cada uma um objeto):

- `mp_plan_id`: string — id do `preapproval_plan` no Mercado Pago (criado pela Cloud Function `criarPlanoMP`)
- `reason`: string — nome amigável do plano
- `auto_recurring`: objeto (frequency, frequency_type, transaction_amount, currency_id)
- `criadoEm`: string ISO — quando o plano foi registrado no Firestore

Valores de referência no código (`functions/SRC/planosConfig.ts` e `constants/planos.ts`): mensal **R$ 60,00** (cobrança todo mês); anual **R$ 600,00** (cobrança uma vez por ano). Copy de cancelamento nos primeiros **5 dias** sem cobrança: `constants/planoMarketing.ts`.

## Clientes por usuaria (subcolecao)

Path padrao no app:
`artifacts/{appId}/users/{uid}/clientes/{clienteId}`

Campos observados:
- `nome`, `nomeCompleto`, `nomePrimeiro`, `sobrenome`
- `telefone`, `dataNascimento`, `tomPele`
- `fotoUrl`
- `dataCadastro` (`serverTimestamp`)
- `ultimaVisita` (`serverTimestamp`)
- `ultimaAnalise` (objeto com snapshot da analise)

## Historico de analises da cliente

Subcolecao:
`artifacts/{appId}/users/{uid}/clientes/{clienteId}/historicoAnalises/{analiseId}`

Campos observados no salvamento:
- Base de classificacao: `estilo`, `formatoRosto`, `eixo`, `profundidade`, `alinhamento`, `distanciamento`
- Tecnicos: `PontoZ`, `Altura_palpebra`, `altura_concavo`, `tipo_curv_natural`
- Curvaturas derivadas: `curvTrad_natural`, `curvTrad_marcante`, `curvEsp`, `curvEspObs`
- Tamanho de fios: `tamanhoIdealFios`, `observacaoTamanhoFios`, `faixaMilimetragem`, `faixaNatural`, `faixaMarcante`
- Colorimetria:
  - IA: `colorometria`
  - Manual: `colorimetriaManual` (objeto completo)
- `modoAnalise`: `ia | manual`
- `data`: `serverTimestamp`

## Estoque — regras atualizadas

Path padrao no app:
`artifacts/{appId}/users/{uid}/estoque/{produtoId}`

- Sem produtos iniciais/mock
- Estado vazio quando nao tem produtos cadastrados
- Formulario: nome, quantidade, minimo, custo unitario (R$) — **SEM tipo**
- Filtros: busca por nome, opcao somente estoque baixo, ordenacao (nome A-Z, menor/maior quantidade, mais criticos)
- Schema produto: `{ nome, quantidade, minimo, custoUnitario?, ativo, criadoEm, atualizadoEm }` — **SEM campo tipo**

Comportamento:
- Lista em tempo real via `onSnapshot` + `orderBy('nome','asc')`
- CRUD: inserir, editar, ajustar quantidade (+1/-1), inativar e reativar (secao expansivel de inativos)
- Regra visual: `quantidade <= minimo` → alerta (card, banner e texto)
- `SafeAreaView` de `react-native-safe-area-context`
- Documentos antigos no Firestore podem ainda ter `tipo` legado; o app nao exibe nem grava esse campo

## Vendas por usuaria (modulo financeiro)

Path padrao:
`artifacts/{appId}/users/{uid}/vendas/{vendaId}`

Campos gravados pelo app:
- `clienteNome`: string
- `clienteId`: string | null (opcional, se escolhida cliente cadastrada)
- `servico`: string
- `valorVenda`: number
- `produtosUsados`: array de itens com `produtoId`, `produtoNome`, `quantidade`, `custoUnitario`, `custoTotal` (custo unitario vem do estoque no momento da venda)
- `custoTotal`: number (soma dos custos dos materiais)
- `lucroBruto`: number (`valorVenda - custoTotal`)
- `formaPagamento`: `pix | dinheiro | cartao_credito | cartao_debito`
- `dataVenda`: `serverTimestamp`
- `observacao`: string | null

Persistencia atomica: `utils/registrarVendaFirestore.ts` usa `runTransaction` para criar o documento de venda e atualizar `quantidade` em cada `estoque/{produtoId}` referenciado; linhas repetidas do mesmo produto sao mescladas antes da transacao.

## Despesas por usuaria (modulo financeiro)

Path padrao:
`artifacts/{appId}/users/{uid}/despesas/{despesaId}`

Campos gravados pelo app (tela de relatorio, modal rapido):
- `descricao`: string
- `valor`: number
- `categoria`: `aluguel | produto | marketing | equipamento | outros`
- `tipo`: `fixa | variavel`
- `data`: Timestamp (dia do lancamento)
- `criadoEm`: `serverTimestamp`

Consultas no relatorio: `where` em `dataVenda` (vendas) e `data` (despesas) entre inicio e fim do periodo; ordenacao das vendas na UI e feita no cliente apos `getDocs`.

## Funcionarias do salao (agendamento completo — CLAUDE.md secao 25)

Path padrao:
`artifacts/{appId}/users/{uid}/funcionarias/{funcId}`

Campos gravados pelo app:
- `nome`: string
- `especialidade`: string (texto livre, ex.: tecnicas oferecidas)
- `ativa`: boolean (`true` em novos cadastros; inativacao e soft via `ativa: false`)
- `criadoEm`: `serverTimestamp`
- `atualizadoEm`: `serverTimestamp` (em edicao, inativacao e reativacao)

Tela `app/(tabs)/funcionarias.tsx`: lista em tempo real (`onSnapshot`, `orderBy('nome','asc')`), busca por nome ou especialidade, secao expansivel de inativas com reativar, FAB e modal no mesmo estilo visual do estoque.

## Servicos do salao (agendamento completo — CLAUDE.md secao 25)

Path padrao:
`artifacts/{appId}/users/{uid}/servicos/{servicoId}`

Campos gravados pelo app:
- `nome`: string
- `duracaoMinutos`: number (inteiro > 0; ex.: 90, 150)
- `preco`: number (R$)
- `ativo`: boolean (`true` em novos cadastros; inativacao soft)
- `criadoEm`: `serverTimestamp`
- `atualizadoEm`: `serverTimestamp`

Tela `app/(tabs)/servicos.tsx`: lista em tempo real, busca por nome, secao de inativos com reativar, preco com entrada decimal estilo BR; duracao exibida com legenda legivel (minutos + horas quando aplicavel).

## Agendamentos por usuaria (lembretes automáticos)

Path padrao no app:
`artifacts/{appId}/users/{uid}/agendamentos/{agendamentoId}`

Schema oficial (atualizado jun/2026):
- `clienteId`: string (ref para `clientes/{id}`)
- `clienteNome`, `clienteTelefone`: string (desnormalizado; telefone só dígitos)
- `funcionariaId`, `funcionariaNome`: string
- `servicoId`, `servicoNome`: string
- `duracaoMinutos`, `preco`: number
- `dataHoraInicio`, `dataHoraFim`: Timestamp
- `status`: `'confirmado' | 'cancelado' | 'concluido'`
- `origem`: `'app' | 'link_publico'`
- `lembreteEnviado`: boolean (`false` por padrão)
- `lembreteEnviadoEm`: Timestamp | null
- `confirmacaoEnviadaEm`, `confirmacaoErro`: Timestamp | string | null
- `criadoEm`, `atualizadoEm`: serverTimestamp

Perfil `usuarios/{uid}` — campo **`telefoneSalao`** (obrigatório no cadastro em `cadastroUsuario.tsx`; editável em `perfilUsuario.tsx`). Usado na variável `{{8}}` dos templates WhatsApp v7/v2.

Tela `app/(tabs)/agendamentos.tsx` (MVP):
- Lista agendamentos em tempo real (`onSnapshot`, `orderBy('dataHora', 'asc')`).
- **Novo agendamento / editar**: modal com busca por nome da cliente (filtra `nomeCompleto`/`nome`), escolha por chip, servico, data/hora em `DD/MM/AAAA` e `HH:MM`.
- **Filtro por data** na lista (campo `DD/MM/AAAA` + botao limpar).
- **Excluir** agendamento especifico (Firestore `deleteDoc`, com confirmacao `Alert`).
- `SafeAreaView` de `react-native-safe-area-context`.

Colecao de resumo para notificação local no app:
`artifacts/{appId}/users/{uid}/resumoLembretes/ultimo`

Campos:
- `total`: number (quantos lembretes foram enviados no ciclo)
- `dataReferencia`: string (`YYYY-MM-DD`, dia dos agendamentos alvo)
- `notificado`: boolean (`false` até o app disparar notificação local)
- `atualizadoEm`: serverTimestamp

## Observacao de consistencia de path

- Frontend usa `app.options.appId` no path `artifacts/{appId}/...`
- A function `uploadClientPhoto` usa `projectId` para montar path de Storage: `artifacts/{projectId}/...`
- Isso pode gerar divergencia de namespace entre app e function dependendo do valor efetivo.

---

## 5) Navegacao

## Fluxo de autenticacao

- App inicia em `/`
- `onAuthStateChanged`:
  - com usuario -> `router.replace('/(tabs)')`
  - sem usuario -> `router.replace('/Login')`

## Fluxo de analise com IA

1. Home (`/(tabs)/index`) -> seleciona/ cria cliente
2. Escolhe modo "Analise com IA"
3. Camera (`/camera`)
   - captura foto frente
   - captura foto perfil
   - envia para Cloud Function `analisarRosto`
4. Resultado (`/analysisResult`)
   - mostra analise + **stickers** de cilios (Reanimated) arrastaveis, com moldura rosa/branco compacta
   - posicao inicial: olho esquerdo da cliente (lado direito da imagem) e olho direito (lado esquerdo), com largura maxima do PNG limitada para o **clamp** nao empurrar os dois ao centro; limites de arraste usam `onLayout` do container da foto (`boundsW`/`boundsH`)
   - **Persistencia**: gravacao Firestore + upload da foto com cilios **somente** ao tocar em **Voltar** ou **Voltar para a Home** (nao no gesto nativo de voltar). Em nativo, captura usa `react-native-view-shot` com camada estatica temporaria (transforms em `View` nativa) porque o snapshot pode nao compor `Animated` do Reanimated
   - toque na area da foto (ou botao fullscreen): **modal** com foto frontal em tela cheia (URI base64 da sessao; nao e o JPEG composto salvo)
   - salva historico e atualiza cliente no Firestore (`fotoComCiliosUrl`, etc.)

## Fluxo de assistente manual

1. Home -> seleciona/ cria cliente
2. Escolhe modo "Assistente Manual"
3. Camera (`/camera`)
   - captura foto frente
   - envia para `uploadClientPhoto`
4. Sequencia `passo1` ate `passo9`
5. Finaliza em `/analysisResult` com `modoAnalise=manual`

## Fluxo de clientes

- Lista geral em `/(tabs)/clientes`
- Perfil da cliente em `/clientes/[id]` com historico detalhado (cards completos)
- **Fotos em tela cheia**: toque na foto do card de analise (`fotoComCiliosUrl` ou fallback `fotoUrl`) ou no **avatar** (somente se houver `fotoUrl`) abre `Modal` fullscreen com `resizeMode="contain"` e botao fechar

## Guia de mapeamentos (`/(tabs)/guia-mapeamentos`)

- Leitura de `MAPA_CILIOS` em `app/constants/mapaCilios.ts`; filtros por estilo, eixo, profundidade, alinhamento, distanciamento + busca textual
- Layout em **duas faixas verticais** (`flex` ~52% filtros / ~48% lista) para equilibrar espaco; area de filtros com **ScrollView** vertical quando o conteudo excede a faixa
- Indicadores de que ha mais conteudo: aviso ao rolar filtros, chips com **scroll horizontal** visivel (`showsHorizontalScrollIndicator`), dicas na lista ("deslize...", "continue rolando...") enquanto houver overflow

## Fluxo de pagamentos

- Gestao em `/(tabs)/pagamento`
- Cartao em `/pagameto/cartao` (tokenizacao + assinatura)
- Cancelamento em `/pagameto/cancelamento`

## Fluxo de estoque

1. Acesso via aba `/(tabs)/estoque`
2. Snapshot em tempo real da colecao `artifacts/{appId}/users/{uid}/estoque`
3. Se vazio: estado vazio com CTA para o FAB (+) — sem seed automatico
4. Cadastro/edicao via modal: nome, quantidade, minimo, custo unitario (R$)
5. Ajuste rapido de quantidade nos cards (+1 / -1)
6. Inativacao de produto sem exclusao fisica
7. Alertas de estoque baixo em card e banner de resumo

## Fluxo financeiro

1. Acesso via aba `/(tabs)/financeiro` (header da aba oculto; titulos no stack interno).
2. Hub (`/(tabs)/financeiro`) com atalhos para **Nova venda** e **Relatorio**.
3. **Nova venda**: busca/digitacao de cliente, servico, valor, forma de pagamento, linhas de produto (filtro por nome), lista mostra custo unitario e estoque por item; preview de custo de materiais e lucro bruto; salvar dispara transacao Firestore (venda + baixa de estoque).
4. **Relatorio**: periodo (hoje, 7 dias, 30 dias, intervalo `DD/MM/AAAA`), cards de receita/custos/lucro/despesas/ticket, barras por forma de pagamento, lista de vendas, lista de despesas no periodo, FAB para lancar despesa rapida.

## Fluxo funcionarias e servicos (cadastro)

1. Abas **Equipe** (`/(tabs)/funcionarias`) e **Servicos** (`/(tabs)/servicos`) — mesma paleta e padroes de card/modal/FAB que o estoque.
2. Dados persistidos nas subcolecoes `funcionarias` e `servicos` sob `artifacts/{appId}/users/{uid}/`.
3. Inativacao sem exclusao fisica; reativacao a partir da lista de inativas/inativos.

## Fluxo de agendamentos e lembretes

1. Acesso via aba `/(tabs)/agendamentos`.
2. Cadastro com dados desnormalizados (`clienteNome`, `clienteTelefone`) para uso pelas Cloud Functions de WhatsApp.
3. Scheduler `enviarLembretesAgendamento` roda diariamente as **08:00** `America/Sao_Paulo`. Consulta `collectionGroup('agendamentos')` na janela `(agora, agora+30h]` com `lembreteEnviado == false`, envia template **`lembrete_agendamento_v2`** (9 variáveis) e atualiza o documento.
4. Trigger `enviarConfirmacaoAgendamento` dispara ao criar agendamento — template **`agendamento_confirmado_v7`** (9 variáveis, inclui `telefoneSalao` em `{{8}}`).
5. Apos envios com sucesso para um par `(namespace, uid)`, grava/atualiza `artifacts/{namespace}/users/{uid}/resumoLembretes/ultimo` para o app notificar a profissional (hook `useLembretesEnviados`, usado em `app/(tabs)/_layout.tsx`).

---

## 6) Regras de Negocio Identificadas

## Regras de classificacao visagismo

- Mapeamento de estilo por combinacao:
  - eixo + profundidade + alinhamento + distanciamento -> `estilo`
- Se nao houver match exato: estilo fallback `"Fazendo muito dinheiro"`
- Regras espelhadas em:
  - backend (`functions/SRC/index.ts`) para fluxo IA
  - frontend (`app/lib/visagismoRules.ts`) para fluxo manual

## Regras de tamanho ideal de fios

- Baseado em `Altura_palpebra` + `altura_concavo`
- Resultado inclui:
  - classificacao (ex. Pequeno, Medio a grande)
  - observacao tecnica
  - faixa geral e faixas natural/marcante
- Implementado em `app/lib/tamanhoFiosRules.ts`

## Regras de curvatura

- `tipo_curv_natural` -> curvaturas recomendadas:
  - tradicional natural
  - tradicional marcante
  - especial + observacao
- Implementado em `app/lib/curvaturaRules.ts`

## Regras de colorimetria manual

- Entrada: tom cabelo + tom pele + fundo pele + preferencia
- Processamento:
  - mapeia temperaturas (quente/frio/neutro) via mappers em `shared/mappers`
  - calcula temperatura final
  - sugere cor principal/combinacao/observacao
- Implementado em `app/lib/colorimetriaRules.ts`

## Regras de validacao de dados da cliente

- Nome/sobrenome obrigatorios
- WhatsApp BR (10/11 digitos)
- Data BR valida (`DD/MM/AAAA`)
- Tom de pele obrigatorio no cadastro de cliente da home
- Helpers na home (`app/(tabs)/index.tsx`)

## Regra de rollback de cliente recem-criada

- Se cliente foi criada e usuaria cancelar na tela de camera sem concluir foto/analise:
  - cliente e apagada de `artifacts/{appId}/users/{uid}/clientes/{clientId}`

## Regras de assistente/chat IA

- Prompt restritivo: responder apenas temas de visagismo/cilios
- Mensagem promocional adicional a cada 4 perguntas do usuario

---

## 7) Integracoes Externas

## Firebase

- Auth: login/cadastro/reset de senha/estado de sessao
- Firestore: usuarias, clientes, historico, dados de plano, estoque, agendamentos, vendas, despesas (paths sob `artifacts/{appId}/users/{uid}/...` quando aplicavel)
- Storage: upload de foto de cliente via Cloud Function
- Cloud Functions (HTTP):
  - `analisarRosto`
  - `assistenteVisagismo`
  - `uploadClientPhoto`
  - `criarAssinaturaMercadoPago`
  - `cancelarAssinaturaMercadoPago`
  - `excluirConta` — exclusão permanente de conta (LGPD / App Store)
- Cloud Functions (Scheduler):
  - `enviarLembretesAgendamento` (08:00 America/Sao_Paulo, WhatsApp Business API)
  - `enviarConfirmacaoAgendamento` (onDocumentCreated agendamentos)
  - `enviarRelatorioAnalisesWhatsApp` (scheduler horario)
- Cloud Functions (HTTP auxiliar):
  - `testarLembrete` — POST `{ telefone, nome, hora?, servico? }` para teste manual do template de lembrete
  - `testarLembrete24h` — POST `{ appId, uid, agendamentoId, marcarEnviado? }`
  - URL publica (ex.): `https://us-central1-lashmatch-627fd.cloudfunctions.net/testarLembrete`

## WhatsApp — Integração atual

Provedor: **WhatsApp Business API (Meta)** — migrado do Z-API em 24/05/2026

Credenciais (`functions/.env` e Firebase Secrets):

- `WHATSAPP_PHONE_ID`: `1190765630776115`
- `WHATSAPP_BUSINESS_ID`: `937817869078549`
- `WHATSAPP_TOKEN`: via Firebase Secret (não commitado)
- `WHATSAPP_VERIFY_TOKEN`: `lashmatch-webhook-2026`
- `WHATSAPP_TEMPLATE_CONFIRMACAO`: `agendamento_confirmado_v7`
- `WHATSAPP_TEMPLATE_LEMBRETE`: `lembrete_agendamento_v2`

Número produção: **+55 19 98963-1786**  
Status: aguardando verificação Meta

Templates necessários (pt_BR, UTILITY, **9 variáveis** cada):

- `agendamento_confirmado_v7` — confirmação ao criar agendamento
- `lembrete_agendamento_v2` — lembrete ~24h (scheduler 08:00)
- `mensagem_utilidade` — `{{1}}` corpo livre (relatórios)

Ordem das vars: nome cliente, salão, endereço, data, hora, serviço, profissional, **telefoneSalao**, assinatura.

Cloud Functions:

- `enviarLembretesAgendamento`, `enviarConfirmacaoAgendamento`, `enviarRelatorioAnalisesWhatsApp`
- `testarLembrete`, `testarConfirmacaoAgendamento`, `testarLembrete24h`, `webhookWhatsApp`

Guia técnico no repo: `docs/whatsapp-business-api.md`  
Obsidian: `fabrica/whatsapp-business-api.md`, `fabrica/lashmatch-schemas.md`

## Gemini (Google GenAI)

- Biblioteca: `@google/genai` no backend
- Modelo atual: `gemini-2.5-flash`
- Usos:
  - classificacao facial (frente + perfil)
  - chat especializado em visagismo
- Secret usado: `GEMINI_API_KEY`

## Mercado Pago

- Fluxo de assinatura recorrente (preapproval)
- Passos:
  1) tokenizacao de cartao em pagina externa (`EXPO_PUBLIC_MP_TOKENIZE_URL`)
  2) app recebe token (deep link / auth session)
  3) Cloud Function cria customer/cartao/preapproval
  4) atualiza Firestore em `usuarios`
- Secret usado: `MERCADOPAGO_ACCESS_TOKEN`

## Exclusão de conta (LGPD / App Store)

- Botão **Excluir minha conta** em `(tabs)/perfilUsuario.tsx`
- Cloud Function `excluirConta`: cancela preapproval MP → apaga dados → `deleteUser` Auth
- Padrão compartilhado com Cortejo: `obsidian/fabrica/excluir-conta-app-expo-padrao.md`
- Env: `EXPO_PUBLIC_EXCLUIR_CONTA_URL`

## APIs Web auxiliares

- IBGE Localidades:
  - `https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios`
  - usado no cadastro para listar cidades por estado

## Expo modules relevantes

- `expo-camera` (captura)
- `expo-web-browser` + `expo-linking` (pagamento tokenizado/deep link)
- `react-native-gesture-handler` + `react-native-reanimated` (ajuste de stickers de cilios)

---

## Observacoes Operacionais para Agentes

- Deploy de **varias** functions no Firebase CLI (PowerShell): usar aspas no filtro, por exemplo `firebase deploy --only "functions:testarLembrete,functions:enviarLembretesAgendamento"` (virgula sem aspas pode falhar no Windows).
- Apos alterar secrets (`firebase functions:secrets:set ...`), e necessario **redeploy** das functions que declaram esses secrets para carregar a nova versao.
- O projeto tem duas fontes de regra visagista (frontend e backend); manter sincronizadas.
- Paths sensiveis:
  - Firestore de clientes usa `artifacts/{appId}/users/{uid}/clientes`
  - Estoque, vendas e despesas: `artifacts/{appId}/users/{uid}/estoque|vendas|despesas`
  - Rota de pagamento usa pasta `pagameto` (typo intencional no estado atual)
- Arquivo central de Firebase no app: `utils/firebaseConfig.ts`.
- Endpoints de functions no app estao centralizados em `utils/config.ts` (exceto pagamento, que usa `EXPO_PUBLIC_INTERNAL_API`).
- O tema visual e dark-first; novas telas devem seguir o mesmo padrao.

