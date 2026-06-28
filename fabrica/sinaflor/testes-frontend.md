---
tags:
  - sinaflor
  - testes
  - jasmine
  - karma
  - angular
fonte: sinaflor2/CLAUDE.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor testes — frontend (jasmine + karma)")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# TESTES — FRONTEND (Jasmine + Karma)

### Filosofia dos testes no projeto

- **Testes unitários** com Jasmine + Karma (Angular TestBed)
- Todos os serviços são **mockados** — nunca fazer chamadas HTTP reais nos testes
- Sempre usar `overrideTemplate` ou `overrideComponent` para zerar o template HTML — evita erros de compilação por componentes PrimeNG não declarados e warnings de `ExpressionChangedAfterItHasBeenCheckedError`
- Usar `NO_ERRORS_SCHEMA` ou `CUSTOM_ELEMENTS_SCHEMA` para ignorar componentes filhos desconhecidos
- Executar: `npm test` (Karma abre browser) ou `ng test --watch=false` (CI)

### Estrutura padrão de um spec de componente

```typescript
import { ComponentFixture, TestBed, fakeAsync, tick, flushMicrotasks } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ActivatedRoute } from '@angular/router';
import { of, throwError } from 'rxjs';

import { ConfirmationService, MessageService } from 'primeng/api';
import { PageNotificationService } from '@nuvem/primeng-components';
import { AbstractAuthorization } from '@nuvem/angular-base';

import { MeuComponenteComponent } from './meu-componente.component';
import { MeuService } from 'src/app/service/meu.service';

describe('MeuComponenteComponent', () => {
    let component: MeuComponenteComponent;
    let fixture: ComponentFixture<MeuComponenteComponent>;
    let mockService: any;
    let mockPageNotificationService: any;
    let mockAuthorization: any;

    beforeEach(async () => {
        // 1. Montar mocks ANTES do TestBed
        mockService = {
            findAll: jasmine.createSpy().and.returnValue(of({ body: [] })),
            findById: jasmine.createSpy().and.returnValue(of({ body: { id: 1 } })),
            save: jasmine.createSpy().and.returnValue(of({ body: { id: 1 } })),
            delete: jasmine.createSpy().and.returnValue(of({}))
        };

        mockPageNotificationService = jasmine.createSpyObj(
            'PageNotificationService',
            ['addSuccessMessage', 'addErrorMessage', 'addInfoMessage']
        );

        mockAuthorization = {
            getUser: jasmine.createSpy().and.returnValue({ nome: 'Usuário Teste', login: '12345678900' }),
            hasRole: jasmine.createSpy().and.returnValue(true)
        };

        // 2. Configurar TestBed
        await TestBed.configureTestingModule({
            declarations: [MeuComponenteComponent],
            imports: [
                ReactiveFormsModule,
                FormsModule,
                HttpClientTestingModule,
                RouterTestingModule,
                NoopAnimationsModule,
                // Importar apenas os módulos PrimeNG que o componente usa diretamente
            ],
            providers: [
                { provide: ActivatedRoute, useValue: { params: of({ id: '123' }) } },
                { provide: MeuService, useValue: mockService },
                { provide: PageNotificationService, useValue: mockPageNotificationService },
                { provide: AbstractAuthorization, useValue: mockAuthorization },
                { provide: MessageService, useValue: {} },
                ConfirmationService,
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]  // ignora componentes filhos
        })
        // 3. OBRIGATÓRIO: zerar o template para evitar erros de compilação PrimeNG
        .overrideTemplate(MeuComponenteComponent, '')
        .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(MeuComponenteComponent);
        component = fixture.componentInstance;
        // NÃO chamar fixture.detectChanges() aqui a menos que queira disparar ngOnInit
    });

    it('deve criar o componente', () => {
        expect(component).toBeTruthy();
    });

    // ... demais testes
});
```

### Estratégias de mock

#### 1. `jasmine.createSpy()` — para funções individuais

```typescript
// Spy simples que retorna um Observable
mockService = {
    findAll: jasmine.createSpy().and.returnValue(of({ body: [] })),
    save:    jasmine.createSpy().and.returnValue(of({ body: { id: 1 } })),
    delete:  jasmine.createSpy().and.returnValue(of({}))
};

// Spy que retorna erro
mockService.save.and.returnValue(throwError({ status: 500, error: 'Erro interno' }));

// Spy que retorna valores diferentes a cada chamada
mockService.find
    .and.returnValues(
        of({ body: { id: 1 } }),   // 1ª chamada
        of({ body: { id: 2 } })    // 2ª chamada
    );
```

#### 2. `jasmine.createSpyObj()` — para objetos inteiros

```typescript
// Cria objeto com vários métodos mockados de uma vez
const mockService = jasmine.createSpyObj(
    'MeuService',
    ['findAll', 'save', 'delete', 'export']
);
// Configurar retorno depois
mockService.findAll.and.returnValue(of({ body: [] }));
```

#### 3. Classe mock — para dependências complexas ou com herança

```typescript
// Útil para AbstractAuthorization e classes base do @nuvem
class MockAuth extends (AbstractAuthorization as any) {
    getUser() { return { nome: 'Teste', login: '12345678900' }; }
    hasRole() { return true; }
}

// No providers:
{ provide: AbstractAuthorization, useClass: MockAuth }
```

#### 4. `spyOn()` — espionar método já existente

```typescript
// Espionar método de instância
const spy = spyOn(component, 'meuMetodo').and.callThrough(); // executa o original
const spy = spyOn(component, 'meuMetodo').and.returnValue(42); // substitui retorno
const spy = spyOn(component, 'meuMetodo'); // bloqueia execução (retorna undefined)

// Espionar método privado (cast para any)
spyOn(component as any, 'metodoPrivado').and.returnValue('valor');

// Espionar método estático de utilitário
spyOn(UploadUtil, 'geraArquivo').and.returnValue({ nome: 'arquivo.txt' } as any);

// Espionar localStorage
spyOn(localStorage, 'getItem').and.callFake((key: string) => {
    if (key === 'idLicenciamento') return '123';
    return null;
});
spyOn(localStorage, 'setItem');
spyOn(localStorage, 'removeItem');
```

#### 5. Mock de `ConfirmationService` com auto-aceitação

```typescript
// Simula o usuário clicando "Confirmar"
mockConfirmationService = jasmine.createSpyObj('ConfirmationService', ['confirm']);
mockConfirmationService.confirm.and.callFake((cfg: any) => cfg?.accept && cfg.accept());

// No providers:
{ provide: ConfirmationService, useValue: mockConfirmationService }
```

#### 6. Mock de `Subject` para Observables de eventos

```typescript
// Para serviços que expõem um Observable (ex: change service)
const atividade$ = new Subject<void>();
const mockAtividadeChangeService = {
    atividadeAlterada$: atividade$.asObservable(),
    notificarAlteracao: jasmine.createSpy('notificarAlteracao')
};

// No teste, disparar o evento:
atividade$.next();
fixture.detectChanges();
```

#### 7. Mock de `ActivatedRoute`

```typescript
// Rota com parâmetro simples
{ provide: ActivatedRoute, useValue: { params: of({ id: '123' }) } }

// Rota com snapshot
{ provide: ActivatedRoute, useValue: { snapshot: { params: { id: 123 } } } }

// Rota com vários params e queryParams
{ provide: ActivatedRoute, useValue: {
    params: of({ id: '1', acao: 'retificar' }),
    queryParams: of({ origem: 'gestao' })
}}
```

#### 8. Mock de `Router`

```typescript
// No spec, depois do TestBed:
const router = TestBed.get(Router);
const navigateSpy = spyOn(router, 'navigate');

// Verificar navegação:
expect(navigateSpy).toHaveBeenCalledWith(['/autorizacao/gestao-autorizacao']);
expect(navigateSpy).toHaveBeenCalledWith(['/autorizacao/licenciamento/visualizar-historico', 123, 10]);
```

#### 9. Mock de `Location`

```typescript
{ provide: Location, useValue: jasmine.createSpyObj('Location', ['back']) }

// Verificar:
const location = TestBed.get(Location);
expect(location.back).toHaveBeenCalled();
```

#### 10. Mock de `DataProviderFactory` (SinaflorDatatable)

```typescript
class MockDataProviderFactory {
    create() {
        return {
            getData: () => of([]),
            getTotalRecords: () => of(0),
            setFilters: () => {},
            setSort: () => {},
            reload: () => {},
            load: () => of([]).toPromise(),
            reset: () => {}
        };
    }
}
// No providers:
{ provide: DataProviderFactory, useClass: MockDataProviderFactory }
```

### Verificações (`expect`) mais usadas no projeto

```typescript
// Existência e truthiness
expect(component).toBeTruthy();
expect(resultado).toBeDefined();
expect(valor).toBeNull();
expect(lista).toBeTruthy();

// Igualdade
expect(component.idLicenciamento).toBe(123);         // igualdade estrita (===)
expect(component.descricao).toEqual('Texto');         // deep equal para objetos
expect(component.dados).toEqual(jasmine.objectContaining({ id: 1, nome: 'Teste' }));

// Arrays
expect(component.lista.length).toBe(3);
expect(component.lista).toContain(jasmine.objectContaining({ id: 1 }));

// Booleanos
expect(component.modalVisible).toBe(true);
expect(component.showErrors).toBeFalse();

// Chamadas de spy
expect(mockService.save).toHaveBeenCalled();
expect(mockService.save).toHaveBeenCalledTimes(1);
expect(mockService.save).toHaveBeenCalledWith(jasmine.objectContaining({ id: 1, nome: 'Teste' }));
expect(mockService.delete).not.toHaveBeenCalled();

// Mensagens de notificação
expect(mockPageNotificationService.addSuccessMessage).toHaveBeenCalledWith('Salvo com sucesso');
expect(mockPageNotificationService.addErrorMessage).toHaveBeenCalledWith(MensagensEnum.ERRO_GENERICO);
```

### Testes com operações assíncronas

#### `fakeAsync` + `tick()` — para Observables e Promises

```typescript
it('deve navegar após salvar', fakeAsync(() => {
    const router = TestBed.get(Router);
    const navigateSpy = spyOn(router, 'navigate');

    component.salvar();
    tick(); // avança o tempo virtual — resolve microtasks e macrotasks pendentes

    expect(mockService.save).toHaveBeenCalled();
    expect(navigateSpy).toHaveBeenCalledWith(['/autorizacao/gestao-autorizacao']);
}));

// Para setTimeout/setInterval: passar milissegundos
it('deve executar após delay', fakeAsync(() => {
    component.iniciarComDelay();
    tick(500); // avança 500ms
    expect(component.executado).toBeTrue();
}));
```

#### `fakeAsync` + `flushMicrotasks()` — para Promises puras

```typescript
it('deve resolver promise', fakeAsync(() => {
    let resultado: any;
    component.criarLicenciamentoVazioPromise().then(r => { resultado = r; });

    flushMicrotasks(); // resolve Promises pendentes

    expect(component.idLicenciamento).toBe(456);
}));

it('deve rejeitar promise em caso de erro', fakeAsync(() => {
    mockService.criarLicenciamento.and.returnValue(throwError({ message: 'Erro' }));

    let erroCapturado: any;
    component.criarLicenciamentoVazioPromise().catch(e => { erroCapturado = e; });

    flushMicrotasks();

    expect(erroCapturado.message).toBe('Erro ao criar licenciamento vazio');
}));
```

#### `async` + `await fixture.whenStable()` — para inicialização do componente

```typescript
it('deve inicializar corretamente', async () => {
    await fixture.whenStable();
    fixture.detectChanges();

    expect(component.dados).toBeDefined();
    expect(mockService.findAll).toHaveBeenCalled();
});
```

### Testando fluxos de erro

```typescript
it('deve exibir erro quando o serviço falhar', () => {
    mockService.findAll.and.returnValue(throwError({ status: 500, error: 'Erro interno' }));

    fixture.detectChanges(); // dispara ngOnInit

    expect(mockPageNotificationService.addErrorMessage).toHaveBeenCalled();
});

it('deve logar erro ao carregar tipo', () => {
    const consoleSpy = spyOn(console, 'error');
    mockService.getTipo.and.returnValue(throwError(new Error('Erro')));

    component.carregarTipo(1);

    expect(consoleSpy).toHaveBeenCalledWith('Erro ao carregar tipo');
});
```

### Testando formulários reativos

```typescript
it('deve configurar formulário corretamente', () => {
    component['buildForm'](); // método privado via cast

    expect(component.cadastroForm).toBeTruthy();
    expect(component.cadastroForm.get('descricao')).toBeTruthy();
    expect(component.cadastroForm.get('descricao').validator).toBeTruthy(); // tem validação
});

it('deve marcar formulário como tocado se inválido ao submeter', () => {
    component['buildForm']();
    component.cadastroForm.get('descricao').setValue(''); // campo obrigatório vazio

    const markSpy = spyOn(component.cadastroForm, 'markAsTouched');
    component.onSubmit();

    expect(markSpy).toHaveBeenCalled();
});

it('deve validar campo obrigatório', () => {
    component['buildForm']();
    const ctrl = component.cadastroForm.get('descricao');

    ctrl.setValue('');
    expect(ctrl.valid).toBeFalse();
    expect(ctrl.errors?.required).toBeTruthy();

    ctrl.setValue('Valor válido');
    expect(ctrl.valid).toBeTrue();
});
```

### Testando métodos com condicionais de negócio

```typescript
// Cenário de sucesso
it('deve salvar quando dados são válidos', () => {
    component.idLicenciamento = 1;
    component.descricao = 'Empreendimento Teste';

    component.salvar();

    expect(mockService.save).toHaveBeenCalledWith(
        jasmine.objectContaining({ id: 1, descricao: 'Empreendimento Teste' })
    );
    expect(mockPageNotificationService.addSuccessMessage).toHaveBeenCalled();
});

// Cenário de erro de validação
it('não deve salvar quando campo obrigatório estiver vazio', () => {
    component.descricao = '';

    component.salvar();

    expect(mockService.save).not.toHaveBeenCalled();
    expect(component.showErrors).toBeTrue();
    expect(mockPageNotificationService.addErrorMessage).toHaveBeenCalled();
});

// Guardar condicionais de domínio específicas do SINAFLOR
it('deve abrir modal para atividade AUMPF mesmo sem permissão de empreendedor', async () => {
    component.idAtividade = 1497; // ConstantsUtil.ATIVIDADE_AUMPF
    mockAuthorization.hasRole.and.returnValue(false);

    await component.showModal();

    expect(component.modalVisible).toBe(true);
    expect(mockPageNotificationService.addErrorMessage).not.toHaveBeenCalled();
});
```

### Testando pipes

```typescript
// Pipes puros: instanciar diretamente, sem TestBed
import { BrDatePipe } from './br-date.pipe';

describe('BrDatePipe', () => {
    let pipe: BrDatePipe;

    beforeEach(() => {
        pipe = new BrDatePipe();
    });

    it('deve criar instância', () => {
        expect(pipe).toBeTruthy();
    });

    it('deve converter data ISO para formato BR', () => {
        expect(pipe.transform('2024-03-15')).toBe('15/03/2024');
    });

    it('deve retornar string vazia para valor nulo', () => {
        expect(pipe.transform(null)).toBe('');
    });

    it('deve retornar o valor original se não for data válida', () => {
        expect(pipe.transform('não é data')).toBe('não é data');
    });
});
```

### Testando funções utilitárias/helpers

```typescript
// Funções puras: importar e testar direto, sem TestBed
import { minhaFuncaoHelper, outraFuncao } from './meu-helper';

describe('meu-helper', () => {
    it('deve retornar true quando condição A', () => {
        const ctx: any = { campo: false };
        minhaFuncaoHelper(ctx, true);
        expect(ctx.campo).toBeTrue();
    });

    it('deve limpar campos dependentes quando condição é falsa', () => {
        const ctx: any = { campo1: 1, campo2: 2, enabled: true };
        outraFuncao(ctx, false);
        expect(ctx.campo1).toBeNull();
        expect(ctx.campo2).toBeNull();
        expect(ctx.enabled).toBeFalse();
    });
});
```

### Erros comuns e como resolver

| Erro | Causa | Solução |
|---|---|---|
| `NullInjectorError: No provider for XService` | Serviço não declarado em `providers` | Adicionar mock do serviço em `providers` |
| `Can't bind to 'xxx' since it isn't a known property` | Módulo PrimeNG não importado | Importar o módulo ou usar `NO_ERRORS_SCHEMA` |
| `ExpressionChangedAfterItHasBeenCheckedError` | Template complexo + detectChanges | Usar `.overrideTemplate(Comp, '')` |
| `TypeError: Cannot read property 'subscribe' of undefined` | Spy retornando `undefined` | Adicionar `.and.returnValue(of({}))` |
| `Error: Template parse errors` | Componente filho não reconhecido | Adicionar `CUSTOM_ELEMENTS_SCHEMA` ou declarar o componente |
| `flush() called when there is nothing to flush` | `fakeAsync` sem tarefas pendentes | Remover o `flush()` desnecessário |

### Checklist ao criar um novo spec

1. `overrideTemplate` ou `overrideComponent` com template vazio ✅
2. Todos os serviços mockados com `jasmine.createSpy` ou `jasmine.createSpyObj` ✅
3. `{ provide: AbstractAuthorization, useValue: mockAuthorization }` se o componente usa auth ✅
4. `{ provide: ActivatedRoute, useValue: { params: of({...}) } }` se usa route params ✅
5. `NO_ERRORS_SCHEMA` ou `CUSTOM_ELEMENTS_SCHEMA` declarado ✅
6. Primeiro teste é sempre `deve criar o componente` + `expect(component).toBeTruthy()` ✅
7. Cenários de erro com `throwError` para cada chamada HTTP importante ✅

---
