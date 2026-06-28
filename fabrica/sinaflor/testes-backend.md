---
tags:
  - sinaflor
  - testes
  - junit
  - mockito
  - java
fonte: sinaflor2/CLAUDE.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor testes — backend (junit 5 + mockito)")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# TESTES — BACKEND (JUnit 5 + Mockito)

### Filosofia dos testes no projeto

- **Testes unitários** com JUnit 5 (`@ExtendWith(MockitoExtension.class)`) — sem Spring context
- Mocks com **Mockito** (`@Mock`, `@InjectMocks`, `when/then`, `verify`)
- Foco em **services** — é onde está a lógica de negócio
- Controllers testados indiretamente via services; testes de integração são raros

### Estrutura padrão de um service test

```java
@ExtendWith(MockitoExtension.class)
class MinhaEntidadeServiceTest {

    @Mock
    private MinhaEntidadeRepository repository;

    @Mock
    private MinhaEntidadeMapper mapper;

    @Mock
    private OutroDependenciaService outroDependencia;

    @InjectMocks
    private MinhaEntidadeQueryService service; // ou ServiceImpl

    private MinhaEntidade entidadeBase;
    private MinhaEntidadeDTO dtoBase;

    @BeforeEach
    void setUp() {
        // Montar objetos de fixture reutilizáveis
        entidadeBase = new MinhaEntidade();
        entidadeBase.setId(1L);
        entidadeBase.setDescricao("Desc Teste");
        entidadeBase.setAtivo("S");

        dtoBase = new MinhaEntidadeDTO();
        dtoBase.setId(1L);
        dtoBase.setDescricao("Desc Teste");
    }

    @Test
    @DisplayName("save: deve mapear, salvar e retornar DTO")
    void save_ok() {
        // GIVEN
        when(mapper.toEntity(any())).thenReturn(entidadeBase);
        when(repository.save(any())).thenReturn(entidadeBase);
        when(mapper.toDto(any(MinhaEntidade.class))).thenReturn(dtoBase);

        // WHEN
        MinhaEntidadeDTO resultado = service.save(dtoBase);

        // THEN
        assertNotNull(resultado);
        assertEquals(1L, resultado.getId());
        verify(repository).save(entidadeBase);
    }

    @Test
    @DisplayName("findOne: deve retornar Optional vazio quando não encontrado")
    void findOne_naoEncontrado() {
        when(repository.findById(99L)).thenReturn(Optional.empty());

        Optional<MinhaEntidadeDTO> resultado = service.findOne(99L);

        assertFalse(resultado.isPresent());
        verify(repository).findById(99L);
    }
}
```

### Padrão de mock com Mockito

```java
// Retorno simples
when(repository.findById(1L)).thenReturn(Optional.of(entidadeBase));
when(repository.findAll()).thenReturn(List.of(entidadeBase));
when(repository.save(any())).thenReturn(entidadeBase);

// Retorno que ecoa o argumento (útil para save)
when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0));

// Retorno com Answer para modificar o argumento (ex: atribuir ID)
when(repository.saveAll(anyList())).thenAnswer(inv -> {
    List<MinhaEntidade> lista = inv.getArgument(0);
    long id = 1;
    for (MinhaEntidade e : lista) { e.setId(id++); }
    return lista;
});

// Lançar exceção
when(repository.findById(99L)).thenThrow(new EntityNotFoundException("Não encontrado"));

// Chamar múltiplas vezes com retornos diferentes
when(repository.findById(9L))
    .thenReturn(Optional.of(entidadeBase))  // 1ª chamada
    .thenReturn(Optional.empty());          // 2ª chamada

// Verificações
verify(repository).save(entidadeBase);                    // chamado exatamente 1x
verify(repository, times(2)).save(any());                 // chamado 2x
verify(repository, never()).deleteById(anyLong());        // nunca chamado
verify(repository).saveAll(anyList());
verifyNoMoreInteractions(repository);                     // não houve mais chamadas
```

### Testando exceções

```java
// JUnit 5 — assertThrows
@Test
@DisplayName("excluir: deve lançar IllegalStateException quando em uso")
void excluir_emUso() {
    MinhaEntidade e = new MinhaEntidade();
    e.setId(1L);
    e.setEmUso("S");
    when(repository.findById(1L)).thenReturn(Optional.of(e));

    IllegalStateException ex = assertThrows(
        IllegalStateException.class,
        () -> service.excluir(1L)
    );

    assertTrue(ex.getMessage().contains("não pode ser excluída"));
    verify(repository, never()).deleteById(anyLong());
}

// ResponseStatusException (Spring)
@Test
void buscar_inativo_deveLancarBadRequest() {
    MinhaEntidade inativa = new MinhaEntidade();
    inativa.setAtivo("N");
    when(repository.findById(1L)).thenReturn(Optional.of(inativa));

    ResponseStatusException ex = assertThrows(
        ResponseStatusException.class,
        () -> service.buscarPorId(1L)
    );

    assertEquals(HttpStatus.BAD_REQUEST, ex.getStatus());
    assertEquals("Entidade inativa", ex.getReason());
}
```

### Agrupando com `@Nested`

```java
@Nested
class Excluir {

    @Test
    @DisplayName("deve deletar quando não está em uso")
    void excluir_ok() {
        MinhaEntidade e = new MinhaEntidade();
        e.setId(1L);
        e.setEmUso("N");
        when(repository.findById(1L)).thenReturn(Optional.of(e));

        service.excluir(1L);

        verify(repository).deleteById(1L);
    }

    @Test
    @DisplayName("deve lançar exceção quando em uso")
    void excluir_emUso() {
        MinhaEntidade e = new MinhaEntidade();
        e.setId(2L);
        e.setEmUso("S");
        when(repository.findById(2L)).thenReturn(Optional.of(e));

        assertThrows(IllegalStateException.class, () -> service.excluir(2L));
        verify(repository, never()).deleteById(anyLong());
    }
}
```

### Testando com campos "S"/"N" (padrão Oracle do projeto)

```java
@Test
void ativar_deve_marcar_S_e_atualizar_data() {
    MinhaEntidade e = new MinhaEntidade();
    e.setId(1L);
    e.setAtivo("N");

    when(repository.findById(1L)).thenReturn(Optional.of(e));
    when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0));

    service.ativar(1L);

    assertEquals("S", e.getAtivo());
    assertNotNull(e.getDataAtualizacao()); // deve setar a data
    verify(repository).save(e);
}

@Test
void desativar_deve_marcar_N() {
    MinhaEntidade e = new MinhaEntidade();
    e.setId(1L);
    e.setAtivo("S");

    when(repository.findById(1L)).thenReturn(Optional.of(e));
    when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0));

    service.desativar(1L);

    assertEquals("N", e.getAtivo());
    verify(repository).save(e);
}
```

### Testando múltiplos cenários com `idInexistente`

```java
@Test
@DisplayName("métodos com findById: devem lançar quando id não existe")
void metodos_idInexistente() {
    when(repository.findById(anyLong())).thenReturn(Optional.empty());

    assertThrows(EntityNotFoundException.class, () -> service.ativar(100L));
    assertThrows(EntityNotFoundException.class, () -> service.desativar(100L));
    assertThrows(EntityNotFoundException.class, () -> service.excluir(100L));
    assertThrows(EntityNotFoundException.class, () -> service.buscarPorId(100L));
}
```

### Nomenclatura de testes no projeto

```java
// Padrão descritivo com @DisplayName
@Test
@DisplayName("criar: deve mapear e salvar todas as exigências")
void criar_ok() { ... }

// Padrão Given/When/Then sem @DisplayName
@Test
void shouldSaveEntidade() { ... }
void shouldReturnEmptyWhenNotFound() { ... }
void shouldThrowExceptionWhenInactive() { ... }
```

### Checklist ao criar um novo service test

1. `@ExtendWith(MockitoExtension.class)` na classe ✅
2. `@Mock` para cada dependência do service ✅
3. `@InjectMocks` no service sendo testado (não na interface — na implementação) ✅
4. `@BeforeEach void setUp()` com objetos de fixture ✅
5. `@DisplayName` em cada teste descrevendo comportamento esperado ✅
6. `verify()` para confirmar que o repositório foi chamado corretamente ✅
7. `verify(repository, never())` para confirmar que **não** foi chamado em cenários de erro ✅
8. Cobrir: caminho feliz, not found, inativo, em uso, lista vazia, erro de validação ✅

---
