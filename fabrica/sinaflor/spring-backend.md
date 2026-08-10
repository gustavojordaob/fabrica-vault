---
tags:
  - sinaflor
  - java
  - spring
  - jhipster
  - backend
fonte: sinaflor2/CLAUDE.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor backend — java 11 / spring boot 2.2.7")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# BACKEND — Java 11 / Spring Boot 2.2.7

### Regras obrigatórias

- **Java 11** — não usar features do Java 14+ (records, sealed classes, pattern matching avançado)
- Pode usar: `var`, `Optional`, Stream API, lambdas, `List.of()`, `Map.of()`
- Injeção de dependência **sempre via construtor** (sem `@Autowired` em campo)
- `@Transactional(readOnly = true)` em todos os métodos de leitura

### Padrão de controller (Resource)

```java
@RestController
@RequestMapping("/api")
public class MinhaEntidadeResource {

    private final Logger log = LoggerFactory.getLogger(MinhaEntidadeResource.class);
    private static final String ENTITY_NAME = "sinaflor2MinhaEntidade";

    private final MinhaEntidadeService service;

    public MinhaEntidadeResource(MinhaEntidadeService service) {
        this.service = service;
    }

    @GetMapping("/minha-entidade/{id}")
    @Timed
    @Secured({Roles.MINHA_PERMISSAO_VISUALIZAR})
    public ResponseEntity<MinhaEntidadeDTO> getOne(@PathVariable Long id) {
        log.debug("REST request to get MinhaEntidade : {}", id);
        return ResponseUtil.wrapOrNotFound(service.findOne(id));
    }

    @PostMapping("/minha-entidade")
    @Timed
    @Secured({Roles.MINHA_PERMISSAO_INCLUIR})
    public ResponseEntity<MinhaEntidadeDTO> create(@Valid @RequestBody MinhaEntidadeDTO dto)
            throws URISyntaxException {
        MinhaEntidadeDTO result = service.save(dto);
        return ResponseEntity.created(new URI("/api/minha-entidade/" + result.getId()))
            .headers(HeaderUtil.createEntityCreationAlert(ENTITY_NAME, result.getId().toString()))
            .body(result);
    }

    @PutMapping("/minha-entidade")
    @Timed
    @Secured({Roles.MINHA_PERMISSAO_ALTERAR})
    public ResponseEntity<MinhaEntidadeDTO> update(@Valid @RequestBody MinhaEntidadeDTO dto) {
        MinhaEntidadeDTO result = service.save(dto);
        return ResponseEntity.ok()
            .headers(HeaderUtil.createEntityUpdateAlert(ENTITY_NAME, dto.getId().toString()))
            .body(result);
    }
}
```

### Padrão de entidade JPA

```java
@Entity
@Table(name = "TB_MINHA_ENTIDADE")
@Cache(usage = CacheConcurrencyStrategy.NONSTRICT_READ_WRITE)
@Data
public class MinhaEntidade implements Serializable {

    @Id
    @GeneratedValue(generator = "sequenceMinhaEntidade")
    @SequenceGenerator(name = "sequenceMinhaEntidade", allocationSize = 1, sequenceName = "SQ_MINHA_ENTIDADE")
    @Column(name = "ID_MINHA_ENTIDADE")
    private Long id;

    @NotNull
    @Column(name = "DS_DESCRICAO", nullable = false)
    private String descricao;

    @Column(name = "DH_CRIACAO")
    private ZonedDateTime dhCriacao;      // datas: ZonedDateTime

    @Column(name = "VL_AREA")
    private BigDecimal area;              // decimais: BigDecimal

    @Column(name = "ST_ATIVO")
    private String stAtivo;              // flags: "S" ou "N"

    @ManyToOne
    @JoinColumn(name = "ID_AUTORIZACAO")
    @JsonIgnoreProperties("minhasEntidades")
    private Autorizacao autorizacao;
}
```

### Segurança — Roles

```java
@Secured({Roles.GESTAO_AUTORIZACAO_VISUALIZAR})
// Novas roles: editar br.gov.ibama.sinaflor2.service.util.Roles
String MINHA_PERMISSAO_VISUALIZAR = "ROLE_MOD_SF2_<MODULO>_FUN_SF2_<FUNCIONALIDADE>_VISUALIZAR";
```

### Exceções — usar as existentes

```java
return ResponseUtil.wrapOrNotFound(service.findOne(id));   // 404 automático
throw new ValidacaoException("Mensagem");
throw new BadRequestAlertException("Detalhe", ENTITY_NAME, "chave");
throw new AcessoRecursoException("Usuário sem acesso");
```

### Logs

```java
private final Logger log = LoggerFactory.getLogger(MinhaClasse.class);
log.debug("REST request to get MinhaEntidade : {}", id);
log.info("MinhaEntidade {} criada", id);
log.error("Erro ao processar MinhaEntidade {}", id, ex);
```

### O que NÃO fazer no backend

- Não usar `@Autowired` em campo — sempre injeção via construtor
- Não expor entidades JPA diretamente — sempre converter para DTO via MapStruct
- Não retornar `List` diretamente em listagens — usar `Page` + `PaginationUtil`
- Não usar `records`, `sealed classes` (Java 14+/17+)
- Não usar `System.out.println`

### Relatórios PDF — JasperReports (`.jrxml`)

Templates em `autorizacao/src/main/resources/templates/relatorio/`. Utilitário: `br.gov.ibama.sinaflor2.relatorio.util.JasperReportUtil`.

| PDF | Template | DTO | Service de montagem |
|---|---|---|---|
| Comprovante de envio | `ComprovanteEnvioProjeto.jrxml` | `ComprovanteEnvioProjetoDTO` | `ComprovanteEnvioLicenciamentoService` |
| Formulário de envio | `FormularioEnvioLicenciamento.jrxml` | `FormularioLicenciamentoEnvioDTO` | `FormularioEnvioLicenciamentoService` |

Endpoint: `ComprovanteEnvioLicenciamentoResource` (`GET /api/licenciamento/{id}/...`).

### Tramitação de Licenciamento (HU130)

Scripts: `autorizacao/src/main/resources/db/scripts/SPRINT_19/`.

| Peça | Detalhe |
|---|---|
| Catálogos | `TB_TIPO_TRAMITE_LIC` / `TB_TIPO_AVALIACAO_LIC` — PK = `CD_*` |
| Histórico | `TB_TRAMITE_LIC` + `TB_TRAMITE_LIC_DESTINATARIO` + `RL_TRAMITE_LIC_CONTEUDO` |
| Rascunho | `TB_TRAMITE_LIC_RASCUNHO` (1 por licenciamento + login) |
| Status | `TB_STATUS_LIC` id=2 `Em Análise` |
| Resource | `LicenciamentoTramitacaoResource` sob `/api/licenciamento/gestao/.../tramitacao` |
| Visibilidade | Analista = destinatário ativo; GO = unidade e `FL_MANTER_ABERTO_UNIDADE` |
| Analistas | SCA2 `GET api/unidadeibama/pessoa-orgao?idUnidadeIbama=` → login=CPF/CNPJ |

#### Regras de layout ao editar `.jrxml`

1. **Label + valor curto** (campos de uma linha): um `textField` com `markup="html"` — `"<b>Label:</b> " + valor`. Posição fixa (`y` sem `Float`) para não aumentar espaçamento vertical.
2. **Texto longo** (metodologia, resumo): `isStretchWithOverflow="true"` + `positionType="Float"`. Metodologia: rótulo em `<b>` + `<br/>` + valor com `textAlignment="Justified"`.
3. **Subreport após conteúdo expansível**: colocar em **band separada** (ex.: Volume Total separado da metodologia) — evita sumiço de tabela na quebra de página.
4. **Tabelas**: `stretchType="RelativeToTallestObject"` em todas as células da linha do subreport.
5. **Seções com caixa**: `rectangle` com `stretchType="ContainerHeight"`; espaçamento entre seções = **14px**.
6. **Não** separar label e valor em `staticText` + `textField` com `x` fixo distante — gera gap visual grande entre `:` e o valor.
7. **Não** colocar valor em `y` fora da altura inicial do frame sem `Float`/`stretch` — o conteúdo some.
8. Após alterar `.jrxml`, **reiniciar o backend** (compilação em runtime via `JasperCompileManager`).

---

## Painel de Gestão — visibilidade

*Atualizado em 28/07/2026*

Listagem em `LicenciamentoQueryService.findGestaoByCriteria`.

- Sempre: `excluirEmElaboracaoGestao` (sem statusLic e sem numeroRegistro).
- Meus (`meusProcessos` true/null): GO → `filtroMeusProcessosGerenteOperacional`; Analista → destinatário ativo.
- Todos (`meusProcessos=false`): GO/Analista/GA → `filtroPorUnidadesUsuario`; CG/AF → visão ampla.
- `isGestaoLicenciamentoSomenteProcessosAtribuidos()` / flag no perfil: **sempre false**.
- Front: checkbox **Todos os Processos** sempre renderizado no personalizar (sem `*ngIf`).
- Nota: `fabrica/sinaflor/gestao-visibilidade-perfis.md`.

---

## Tramitação — RN02 Tipo de Avaliação (Vistoria)

*Atualizado em 03/08/2026*

Script: `db/scripts/SPRINT_19/01_tb_tipo_avaliacao_lic_vistoria.sql` (VISTORIA_TECNICA, PREVIA, ACOMPANHAMENTO, POS_EXPLORATORIA, PMFS_AMAZONIA). `ANALISE_POA_AMAZONIA` também vale para Vistoria.

- `GET .../tramitacao/tipos-avaliacao?idTipoTramite=` filtra pelo enum `TipoAvaliacaoLicEnum`.
- Tipo Avaliação obrigatório para Análise (1) e Vistoria (2).
- Finalizar: último item Vistoria → status `Em Vistoria do Projeto` (id 3).

---
