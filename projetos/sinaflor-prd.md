---
tags:
  - sinaflor
  - prd
  - ibama
fonte: sinaflor2/PROJECT.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../fabrica/sinaflor/INDEX]]"
---

> **PRD SINAFLOR2** — espelho de `sinaflor2/PROJECT.md`. Atualize aqui e no repo ao mudar arquitetura.

# SINAFLOR2 — Documentação do projeto

Sistema do IBAMA para controle da origem de produtos florestais.

## Estrutura do monorepo

| Pasta | Descrição |
|---|---|
| `front_end/` | SPA Angular 7.2 |
| `autorizacao/` | Microsserviço Spring Boot (API REST principal) |
| `gateway/` | API Gateway Spring Cloud (roteamento, login automático em dev) |

---

# FRONTEND

## Visão geral

SPA Angular que se comunica com o backend Java via REST.

- **Nome**: `sinaflor2`
- **Versão**: `1.5.14`
- **Angular**: `7.2.x` (CLI `7.3.10`)
- **TypeScript**: `3.2.2`
- **RxJS**: `6.3.x` (com `rxjs-compat`)
- **Node**: requer npm >= 5.0

## Stack e bibliotecas principais

| Biblioteca | Versão | Uso |
|---|---|---|
| `@angular/core` | ~7.2.0 | Framework principal |
| `primeng` | ^7.0.5 | Componentes de UI (tabelas, formulários, modais, etc.) |
| `@nuvem/angular-base` | 7.3.0 | Auth (JWT, CAS), guards, segurança |
| `@nuvem/primeng-components` | 7.2.3 | Datatable, notificações, error stack |
| `ng-block-ui` | ^2.1.2 | Loading overlay (`@BlockUI()`) |
| `ng2-currency-mask` | ^5.3.1 | Máscara de moeda |
| `moment` | 2.18.1 | Formatação de datas |
| `chart.js` | 2.7.1 | Gráficos de estatísticas |
| `rxjs-compat` | ~6.3.3 | Compatibilidade com operadores legados |

## Estrutura de pastas

```
src/app/
├── app.module.ts                  # Módulo raiz
├── app-routing.module.ts          # Rotas raiz (login, logout, estatísticas, diário de erros)
├── app.component.ts               # Componente raiz
├── app.menu.component.ts          # Menu lateral
├── app.topbar.component.ts        # Barra superior
├── auth.guard.routes.ts           # Guard de permissões por role
├── primeng-imports.ts             # Barrel de imports PrimeNG
│
├── view/                          # Telas da aplicação (feature modules)
│   ├── autorizacao/               # Módulo principal de autorizações
│   │   ├── autorizacao.module.ts
│   │   ├── autorizacao-routing.module.ts
│   │   ├── gestao-autorizacao/    # Listagem/gestão interna IBAMA
│   │   ├── minhas-autorizacoes/   # Telas do usuário externo
│   │   ├── cabecalho/             # Cabeçalho da autorização
│   │   ├── solicitacoes/          # Solicitações de retificação/renovação
│   │   ├── imoveis/               # Imóveis rurais vinculados
│   │   ├── importacoes/           # Declaração de importação (DI), MIC, DIS
│   │   ├── dof/                   # Documento de Origem Florestal
│   │   └── licenciamento-exploracao/  # Licenciamento de exploração florestal
│   │       ├── editar-licenciamento/
│   │       ├── aba-info-tecnicas/
│   │       ├── aba-inventario-florestal/
│   │       ├── aba-levantamento-produtos-florestais/
│   │       ├── aba-informacoes-adicionais/
│   │       ├── aba-enviar-orgao-ambiental/  # PDFs de envio
│   │       └── gestao-exigencias/
│   │
│   └── autorizacao-esp-simpl/     # Autorizações especiais e simplificadas
│       ├── gestao-autorizacao/
│       ├── editar-autorizacao-especial/
│       ├── editar-autorizacao-simplificada/
│       ├── visualizar-autorizacao-esp-simpl/
│       ├── homologar-autorizacao/
│       ├── emitir-autorizacao/
│       ├── enviar-autorizacao-homologacao/
│       └── externo/               # Telas do usuário externo (exploração, registro)
│
├── components/                    # Componentes reutilizáveis entre módulos
│   ├── breadcrumb/
│   ├── datatable/                 # SinaflorDatatable customizado
│   ├── retificacao/               # Componentes shared de retificação (árvores, toras, volumetria)
│   └── visualizar-autorizacao/    # Componente shared de visualização completa
│
├── service/                       # Serviços HTTP (um por entidade de domínio)
├── domain/                        # Interfaces/models TypeScript
├── pipes/                         # Pipes customizados
├── directives/                    # Diretivas customizadas
└── util/                          # Utilitários, constantes, permissões
```

## Módulos Angular

- **`AutorizacaoModule`** — autorizações de exploração florestal padrão
- **`AutorizacaoEspSimplModule`** — autorizações especiais e simplificadas

O `AutorizacaoRoutingModule` usa `RouterModule.forRoot()` (não `forChild`) — atenção ao adicionar novas rotas.

## Autenticação e autorização

- Autenticação via **CAS** (SSO) com token **JWT**
- Biblioteca: `@nuvem/angular-base` (`SecurityModule`, `JWTTokenService`, `AuthenticationService`)
- Guard de rotas: `AuthGuard` (nuvem) + `AuthGuardRoutes` (local, verifica role)
- Permissões em `src/app/util/permissao.util.ts`, formato: `ROLE_MOD_SF2_<MODULO>_FUN_SF2_<FUNCIONALIDADE>_<ACAO>`

### Configuração de ambiente (`environment.ts`)
```typescript
auth: {
  baseUrl: '/api',
  authUrl: '/login/cas',
  loginUrl: '/api/login',
  logoutUrl: '/logout',
  detailsUrl: '/user/details',
  tokenValidationUrl: '/token/validate',
  loginSuccessRoute: '/#/login-success',
  storage: localStorage,
  tokenStorageIndex: 'token',
  userStorageIndex: 'user'
}
```

## Roteamento

- Usa `HashLocationStrategy` (`/#/rota`)
- URL base da API: `/api` (proxy para o backend em dev via `proxy.conf.json`)
- URL base do backend: `/sinaflor2autorizacao/api/`

### Principais rotas

| Rota | Componente | Acesso |
|---|---|---|
| `/autorizacao/gestao-autorizacao` | `GestaoAutorizacaoComponent` | Interno IBAMA |
| `/autorizacao/minhas-autorizacoes` | `MinhasAutorizacoesComponent` | Usuário externo |
| `/autorizacao/cabecalho` | `CabecalhoComponent` | Interno |
| `/autorizacao/solicitacoes` | `SolicitacoesComponent` | Interno |
| `/autorizacao/imoveis/listar-imoveis` | `ListarImoveisComponent` | Ambos |
| `/autorizacao/importacoes/...` | vários | Importações/DI/MIC |
| `/autorizacao/dof/emitir-dof` | `EmitirDofComponent` | Emissão DOF |
| `/autorizacao/licenciamento/...` | vários | Licenciamento |
| `/autorizacao/autorizacao-simplificada/...` | vários | Aut. Especial/Simpl. |

## Serviços HTTP

Padrão real do projeto — todos usam `{ observe: 'response' }`:

```typescript
@Injectable({ providedIn: 'root' })
export class AutorizacaoService {
    public resourceUrl = '/sinaflor2autorizacao/api/autorizacao';

    constructor(private http: HttpClient) {}

    find(id: number): Observable<HttpResponse<IAutorizacao>> {
        return this.http.get<IAutorizacao>(`${this.resourceUrl}/${id}`, { observe: 'response' });
    }

    query(req?: any): Observable<HttpResponse<IAutorizacao[]>> {
        const options = createRequestOption(req);
        return this.http.get<IAutorizacao[]>(this.resourceUrl, { params: options, observe: 'response' });
    }
}
```

- Para acessar o dado: `res.body`
- Paginação via `createRequestOption(req)` em `src/app/util/`

## Pipes disponíveis

| Pipe | Nome no template | Descrição |
|---|---|---|
| `BrDatePipe` | `brDate` | Converte data ISO para dd/mm/yyyy |
| `CpfCnpjPipe` | `cpfCnpjPipe` | Formata CPF ou CNPJ |
| `SimNaoPipe` | `simNaoPipe` | Converte "S"/"N" para "Sim"/"Não" |
| `NumeroDecimalPipe` | `numeroDecimal` | Decimal BR |
| `numAutPipe` | `numAut` | Número da autorização formatado |
| `numProtoPipe` | `numProto` | Número de protocolo formatado |
| `TamanhoArquivoPipe` | `tamanhoArquivo` | Tamanho de arquivo legível |
| `CoordenadaPipe` | `coordenada` | Exibição de coordenada geográfica |

## Utilitários importantes

| Arquivo | Descrição |
|---|---|
| `util/constants-util.ts` | Constantes globais (IDs fixos, limites geográficos BR, calendário PT-BR) |
| `util/permissao.util.ts` | Todas as roles do sistema |
| `util/mensagem.util.ts` | Mensagens padrão de BlockUI e tratamento de erros |
| `util/format.util.ts` | Formatações (datas, números) |
| `util/responsavel-util.service.ts` | Verifica se o usuário logado é RT vinculado ao licenciamento |

## Loading (BlockUI)

```typescript
@BlockUI() blockUI: NgBlockUI;

this.blockUI.start(MensagemUtil.BLOCKUI_CARREGANDO);
// chamada HTTP
this.blockUI.stop();
```

Mensagens: `BLOCKUI_CARREGANDO`, `BLOCKUI_SALVANDO`, `BLOCKUI_EXCLUINDO`, `BLOCKUI_RELATORIO`

## Execução local

```bash
npm install
npm start       # porta 4200, proxy para backend
npm run build   # build produção
```

---

# BACKEND

## Visão geral

Microsserviço Spring Boot gerado com **JHipster**. Expõe a API REST consumida pelo frontend.

- **Artefato**: `sinaflor2autorizacao`
- **Java**: `11`
- **Spring Boot**: `2.2.7.RELEASE`
- **JHipster**: `3.9.1`
- **MapStruct**: `1.4.2.Final`
- **Banco**: Oracle (`Oracle12cDialect`)
- **Cache**: Hazelcast (segundo nível do Hibernate)
- **Service discovery**: Eureka
- **Config server**: Spring Cloud Config (bootstrap)
- **Monitoramento**: Sentry + Spring Actuator

## Stack e bibliotecas principais

| Biblioteca | Uso |
|---|---|
| Spring Boot 2.2.7 | Framework base |
| Spring Data JPA + Hibernate | Persistência (dialect Oracle12c) |
| Spring Security + JWT | Autenticação |
| JHipster Framework | Utilitários (QueryService, PaginationUtil, HeaderUtil, ResponseUtil) |
| MapStruct 1.4.2 | Mapeamento entity ↔ DTO |
| Lombok | Boilerplate nas entidades (`@Data`) |
| OpenFeign | Clientes HTTP para microsserviços externos |
| Eureka Client | Descoberta de serviços |
| Hazelcast | Cache distribuído |
| Liquibase | Migrations (desabilitado em dev) |
| Dropwizard Metrics (`@Timed`) | Métricas nos endpoints |
| HikariCP | Pool de conexões |

## Estrutura de pacotes

```
br.gov.ibama.sinaflor2/
├── config/                    # Configurações Spring (JPA, segurança, properties)
│   ├── converters/            # Converters JPA customizados
│   └── jpa/impl/              # Repositório base customizado
│
├── domain/                    # Entidades JPA (@Entity + @Data Lombok)
│   ├── infotecnica/
│   └── sinaflor1/             # Entidades legadas do SINAFLOR 1
│
├── enums/                     # Enums do domínio
│
├── exceptions/                # Exceções de domínio
│
├── integration/               # Clientes de integração externa
│   ├── Sistaxon/
│   └── dof/rastreabilidade/
│
├── proxy/                     # Clientes Feign para outros microsserviços
│
├── redis/                     # Integração Redis/NATS para mensagens
│
├── relatorio/util/            # JasperReports — geração de PDFs (.jrxml)
│
├── repository/                # Repositórios Spring Data JPA
│
├── rotina/job/                # Jobs agendados (AutorizacoesJob, SituacaoJob)
│
├── service/
│   ├── *Service.java          # Interfaces de serviço
│   ├── *QueryService.java     # Consultas com Specification (padrão JHipster)
│   ├── dto/                   # DTOs por domínio (autorizacao, cabecalho, dof, licenciamento...)
│   ├── impl/                  # Implementações dos serviços
│   ├── inclusao/impl/         # Serviços de inclusão de autorizações
│   ├── mapper/                # MapStruct mappers
│   ├── filters/impl/          # Filtros de consulta
│   ├── handler/               # Handlers de operações específicas
│   └── util/                  # HeaderUtil, PaginationUtil, Roles
│
├── util/                      # Utilitários gerais
│   ├── ValoresConstantesUtil  # Interface com constantes de domínio
│   ├── FormatUtil
│   └── GenerateReportsUtil
│
└── web/rest/                  # Controllers REST
    ├── *Resource.java         # Padrão JHipster
    ├── *Controller.java       # Controllers fora do padrão JHipster
    ├── errors/                # Exceções HTTP customizadas
    └── vm/                    # View Models de request/response
```

## Padrão de controller (Resource)

```java
@RestController
@RequestMapping("/api")
public class AutorizacaoResource {

    private final Logger log = LoggerFactory.getLogger(AutorizacaoResource.class);
    private static final String ENTITY_NAME = "sinaflor2Autorizacao";

    private final AutorizacaoService autorizacaoService;
    private final AutorizacaoQueryService autorizacaoQueryService;

    // Injeção via construtor (sem @Autowired)
    public AutorizacaoResource(AutorizacaoService autorizacaoService,
                               AutorizacaoQueryService autorizacaoQueryService) {
        this.autorizacaoService = autorizacaoService;
        this.autorizacaoQueryService = autorizacaoQueryService;
    }

    @GetMapping("/autorizacao")
    @Timed
    @Secured({Roles.GESTAO_AUTORIZACAO_VISUALIZAR})
    public ResponseEntity<List<AutorizacaoDTO>> getAll(AutorizacaoCriteria criteria, Pageable pageable) {
        log.debug("REST request to get Autorizacaos by criteria: {}", criteria);
        Page<AutorizacaoDTO> page = autorizacaoQueryService.findByCriteria(criteria, pageable);
        HttpHeaders headers = PaginationUtil.generatePaginationHttpHeaders(page, "/api/autorizacao");
        return ResponseEntity.ok().headers(headers).body(page.getContent());
    }

    @GetMapping("/autorizacao/{id}")
    @Timed
    @Secured({Roles.GESTAO_AUTORIZACAO_VISUALIZAR})
    public ResponseEntity<AutorizacaoDTO> getOne(@PathVariable Long id) {
        log.debug("REST request to get Autorizacao : {}", id);
        return ResponseUtil.wrapOrNotFound(autorizacaoService.findOne(id));
    }

    @PostMapping("/autorizacao")
    @Timed
    @Secured({Roles.GESTAO_AUTORIZACAO_INCLUIR})
    public ResponseEntity<AutorizacaoDTO> create(@Valid @RequestBody AutorizacaoDTO dto)
            throws URISyntaxException {
        AutorizacaoDTO result = autorizacaoService.save(dto);
        return ResponseEntity.created(new URI("/api/autorizacao/" + result.getId()))
            .headers(HeaderUtil.createEntityCreationAlert(ENTITY_NAME, result.getId().toString()))
            .body(result);
    }

    @PutMapping("/autorizacao")
    @Timed
    @Secured({Roles.GESTAO_AUTORIZACAO_ALTERAR})
    public ResponseEntity<AutorizacaoDTO> update(@Valid @RequestBody AutorizacaoDTO dto) {
        AutorizacaoDTO result = autorizacaoService.save(dto);
        return ResponseEntity.ok()
            .headers(HeaderUtil.createEntityUpdateAlert(ENTITY_NAME, dto.getId().toString()))
            .body(result);
    }
}
```

## Padrão de entidade JPA

```java
@Entity
@Table(name = "tb_autorizacao")
@Cache(usage = CacheConcurrencyStrategy.NONSTRICT_READ_WRITE)
@Data
public class Autorizacao implements Serializable {

    @Id
    @GeneratedValue(generator = "sequenceAutorizacao")
    @SequenceGenerator(name = "sequenceAutorizacao", allocationSize = 1, sequenceName = "SQ_AUTORIZACAO")
    @Column(name = "id_autorizacao")
    private Long id;

    @NotNull
    @Column(name = "dh_validade", nullable = false)
    private ZonedDateTime validade;       // datas sempre ZonedDateTime

    @Column(name = "cd_area_autorizada")
    private BigDecimal areaAutorizada;    // decimais sempre BigDecimal

    @Column(name = "st_ativo")
    private String stAtivo;               // flags como String "S"/"N"

    @ManyToOne
    @JoinColumn(name = "id_cabecalho")
    @JsonIgnoreProperties("autorizacoes")
    private Cabecalho cabecalho;
}
```

## Padrão de MapStruct mapper

```java
@Mapper(componentModel = "spring", uses = {})
public interface AutorizacaoMapper extends EntityMapper<AutorizacaoDTO, Autorizacao> {

    @Mapping(target = "campoCalculado", ignore = true)
    @Mapping(source = "relacionamento.campo", target = "campoPlanificado")
    AutorizacaoDTO toDto(Autorizacao autorizacao);

    @Mapping(target = "colecao", ignore = true)
    Autorizacao toEntity(AutorizacaoDTO dto);

    default Autorizacao fromId(Long id) {
        if (id == null) return null;
        Autorizacao a = new Autorizacao();
        a.setId(id);
        return a;
    }
}
```

## Padrão de QueryService

Padrão JHipster — `QueryService` com `Specification` e classe `*Criteria`:

```java
@Service
@Transactional(readOnly = true)
public class AutorizacaoQueryService extends QueryService<Autorizacao> {

    public Page<AutorizacaoDTO> findByCriteria(AutorizacaoCriteria criteria, Pageable pageable) {
        Specification<Autorizacao> spec = createSpecification(criteria);
        return repository.findAll(spec, pageable).map(mapper::toDto);
    }

    private Specification<Autorizacao> createSpecification(AutorizacaoCriteria criteria) {
        Specification<Autorizacao> spec = Specification.where(null);
        if (criteria != null) {
            if (criteria.getId() != null) {
                spec = spec.and(buildSpecification(criteria.getId(), Autorizacao_.id));
            }
            if (criteria.getNumero() != null) {
                spec = spec.and(buildStringSpecification(criteria.getNumero(), Autorizacao_.numero));
            }
        }
        return spec;
    }
}
```

## Segurança — Roles

Interface `br.gov.ibama.sinaflor2.service.util.Roles`. Usada com `@Secured` nos controllers:

```java
@Secured({Roles.GESTAO_AUTORIZACAO_VISUALIZAR, Roles.MINHAS_AUTORIZACOES_VISUALIZAR})
```

Formato: `ROLE_MOD_SF2_<MODULO>_FUN_SF2_<FUNCIONALIDADE>_<ACAO>`

As mesmas roles usadas no frontend (`PermissaoUtil`) e no backend (`Roles`) são idênticas em valor.

## Exceções customizadas

Todas em `br.gov.ibama.sinaflor2.web.rest.errors/`:

| Exceção | Uso |
|---|---|
| `BadRequestAlertException` | Requisição inválida (400) |
| `AcessoRecursoException` | Usuário sem acesso ao recurso |
| `ApenasConsultaException` | Usuário só pode consultar, não alterar |
| `ValidacaoException` | Erro de validação de negócio |
| `RetificacaoException` | Erro em operação de retificação |
| `RenovacaoException` | Erro em operação de renovação |
| `InclusaoAutorizacaoException` | Erro ao incluir autorização |
| `DofException` / `DofIntegrationException` | Erros de integração com DOF |
| `ExportacaoException` | Erro ao exportar relatório |
| `PDFException` | Erro ao gerar PDF |
| `IntegrationException` | Erro genérico de integração externa |

## Integrações externas (Feign proxies)

| Proxy | Serviço | Uso |
|---|---|---|
| `SCA2ServiceProxy` | SCA2 | Unidades IBAMA, perfis de abrangência |
| `SCAServiceProxy` | SCA legado | Autenticação/autorização legada |
| `PessoaServiceProxy` | Pessoa | Dados de CPF/CNPJ |
| `CarServiceProxy` | CAR | Cadastro Ambiental Rural |
| `DofServiceProxy` | DOF | Documento de Origem Florestal |
| `DominioServiceProxy` | Domínio | Tabelas auxiliares/domínios |
| `McpServiceProxy` | MCP | — |
| `CtfAidaServiceProxy` | CTF/AIDA | Cadastro Técnico Federal |
| `SistaxonServiceProxy` | Sistaxon | Taxonomia de espécies |

## Convenções de banco Oracle

- **Dialect**: `Oracle12cDialect`
- **Tabelas**: `TB_` + nome em maiúsculo (ex: `TB_AUTORIZACAO`)
- **Sequences**: `SQ_` + nome da tabela, `allocationSize = 1`
- **Datas**: `ZonedDateTime` (Oracle `DATE` armazena data + hora)
- Strings vazias `''` são `NULL` no Oracle — validar com `StringUtils.isNotBlank()`

### Prefixos de colunas

| Prefixo | Tipo |
|---|---|
| `ID_` | Identificador / chave |
| `DS_` | Descrição (texto) |
| `NM_` | Nome |
| `DH_` | Data/hora (`ZonedDateTime`) |
| `DT_` | Somente data |
| `NU_` | Número alfanumérico |
| `QT_` | Quantidade |
| `CD_` / `VL_` | Código / valor numérico |
| `ST_` | Status / flag ("S"/"N") |

## Utilitários de serviço

| Classe | Uso |
|---|---|
| `HeaderUtil` | Headers de resposta (`createEntityCreationAlert`, `createEntityUpdateAlert`) |
| `PaginationUtil` | Headers de paginação HTTP |
| `ResponseUtil` | `wrapOrNotFound(optional)` — GET por ID |
| `ValoresConstantesUtil` | Interface com constantes de domínio (IDs de atividades, tipos, etc.) |

## Relatórios PDF (JasperReports)

Templates em `src/main/resources/templates/relatorio/`. Compilados em runtime por `JasperReportUtil`.

| Classe | Método | Template principal |
|---|---|---|
| `JasperReportUtil` | `gerarComprovante()` | `ComprovanteEnvioProjeto.jrxml` |
| `JasperReportUtil` | `gerarComprovanteFormularioLicenciamento()` | `FormularioEnvioLicenciamento.jrxml` |

### Endpoints de PDF — licenciamento

| Endpoint | Resource | Service de montagem do DTO |
|---|---|---|
| `GET /api/licenciamento/{id}/comprovante-envio-projeto` | `ComprovanteEnvioLicenciamentoResource` | `ComprovanteEnvioLicenciamentoService` |
| `GET /api/licenciamento/{id}/formulario-envio-licenciamento` | `ComprovanteEnvioLicenciamentoResource` | `FormularioEnvioLicenciamentoService` |

### Subreports do formulário de licenciamento (`sub/`)

| Arquivo | Uso |
|---|---|
| `SubResponsaveis.jrxml` | Responsáveis técnicos |
| `SubImoveis.jrxml` | Imóveis rurais |
| `SubAreas_Multi.jrxml` / `SubAreas_Single.jrxml` | Demonstrativo de áreas |
| `finalidadeProjeto.jrxml` | Finalidade do projeto |
| `destinacao.jrxml` | Destinação de produtos |
| `caracterizacaoVegetacao.jrxml` | Caracterização da vegetação |
| `SubVolumeInventario.jrxml` | Tabela Volume Total do inventário |
| `SubArvoresInventarioCai.jrxml` | Listagem de árvores (CAI) |
| `SubQuantitativoProdutosFlorestaisCai.jrxml` | Quantitativo de produtos (CAI) |
| `exigencia.jrxml` | Exigências do órgão ambiental |

### Convenções de layout nos `.jrxml`

- Seções com caixa arredondada: `rectangle radius="8"` + faixa verde `#2E6B3F` no topo
- Espaçamento padrão entre seções: **14px** (`y="14"` no frame interno da band)
- Campos label+valor curtos: um `textField` com `markup="html"` (`<b>Label:</b> valor`) — evita gap entre colunas fixas
- Textos longos (metodologia, resumo): `isStretchWithOverflow="true"` + `positionType="Float"`; metodologia com `textAlignment="Justified"`
- Tabelas (subreports): **band separada** quando o conteúdo acima pode crescer muito (ex.: metodologia longa + Volume Total)
- Células de tabela: `stretchType="RelativeToTallestObject"` em todas as colunas da mesma linha
- Borda da seção: `stretchType="ContainerHeight"` no `rectangle` externo

> Após alterar `.jrxml`, reiniciar o backend — os templates são recompilados na geração do PDF.

## Execução local

```bash
./mvnw spring-boot:run -Pdev
```

Variáveis necessárias: `DATABASE_URL`, `AUTORIZACAO_DATABASE_USERNAME`, `AUTORIZACAO_DATABASE_PASSWORD`

