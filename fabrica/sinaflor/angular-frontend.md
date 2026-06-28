---
tags:
  - sinaflor
  - angular
  - primeng
  - frontend
fonte: sinaflor2/CLAUDE.md
atualizado_em: 2026-06-12
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor frontend — angular 7.2")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# FRONTEND — Angular 7.2

### Regras obrigatórias

- Versão **Angular 7.2** — não usar nenhuma feature posterior
- **Proibido**: standalone components, signals, `inject()`, functional guards, `provideRouter()`, `@if`, `@for` (template syntax nova)
- **Usar**: `*ngIf`, `*ngFor`, `NgModule`, `OnInit`, `OnDestroy`
- Formulários sempre com **ReactiveFormsModule** (`FormGroup`, `FormBuilder`, `Validators`)
- Componentes: `kebab-case` para arquivos, `PascalCase` para classe, `app-` para seletor

### RxJS

- Versão **6.3.x com rxjs-compat** — importar operadores via `rxjs/operators`
- **Sempre** fazer unsubscribe: `takeUntil` + `Subject` no `ngOnDestroy`, ou `async pipe` no template
- Não usar operadores deprecated

### HTTP / Serviços

- Todos os métodos HTTP usam `{ observe: 'response' }` — retornam `HttpResponse<T>`
- Para acessar o dado sempre usar `.body`: `res.body`
- URL base: `/sinaflor2autorizacao/api/`
- Novos serviços em `src/app/service/`, com `providedIn: 'root'`
- Usar `createRequestOption(req)` para montar params de paginação/filtro

### Padrão real de componente

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { HttpResponse } from '@angular/common/http';
import { BlockUI, NgBlockUI } from 'ng-block-ui';
import { BreadcrumbService } from 'src/app/components/breadcrumb/breadcrumb.service';
import { MensagemUtil } from 'src/app/util/mensagem.util';
import { MessageService } from 'primeng/components/common/messageservice';
import { Message } from 'primeng/components/common/api';

@Component({
    selector: 'app-nome-componente',
    templateUrl: './nome-componente.component.html',
    providers: [MessageService]
})
export class NomeComponente implements OnInit, OnDestroy {

    @BlockUI() blockUI: NgBlockUI;
    private destroy$ = new Subject<void>();
    msgs: Message[] = [];

    constructor(
        private breadcrumbService: BreadcrumbService,
        private algumService: AlgumService
    ) {}

    ngOnInit() {
        this.breadcrumbService.set([...]);
        this.blockUI.start(MensagemUtil.BLOCKUI_CARREGANDO);

        this.algumService.find(id)
            .pipe(takeUntil(this.destroy$))
            .subscribe(
                (res: HttpResponse<ITipo>) => {
                    this.dado = res.body;
                },
                (error) => {
                    this.blockUI.stop();
                    const msg = MensagemUtil.resolveMensagem(error);
                    this.msgs = [{ severity: 'error', summary: 'Erro', detail: msg }];
                },
                () => { this.blockUI.stop(); }
            );
    }

    ngOnDestroy() {
        this.destroy$.next();
        this.destroy$.complete();
    }
}
```

### Padrão real de serviço HTTP

```typescript
type EntityResponseType = HttpResponse<IMinhaEntidade>;
type EntityArrayResponseType = HttpResponse<IMinhaEntidade[]>;

@Injectable({ providedIn: 'root' })
export class MinhaEntidadeService {
    public resourceUrl = '/sinaflor2autorizacao/api/minha-entidade';

    constructor(private http: HttpClient) {}

    find(id: number): Observable<EntityResponseType> {
        return this.http.get<IMinhaEntidade>(`${this.resourceUrl}/${id}`, { observe: 'response' });
    }

    query(req?: any): Observable<EntityArrayResponseType> {
        const options = createRequestOption(req);
        return this.http.get<IMinhaEntidade[]>(this.resourceUrl, { params: options, observe: 'response' });
    }

    create(entidade: IMinhaEntidade): Observable<EntityResponseType> {
        return this.http.post<IMinhaEntidade>(this.resourceUrl, entidade, { observe: 'response' });
    }

    update(entidade: IMinhaEntidade): Observable<EntityResponseType> {
        return this.http.put<IMinhaEntidade>(this.resourceUrl, entidade, { observe: 'response' });
    }
}
```

### UI / Templates

- Componentes de UI são do **PrimeNG 7** — não usar componentes de versões mais novas
- Tabelas: `p-table` ou `SinaflorDatatable`
- Loading: `@BlockUI()` + `blockUI.start()` / `blockUI.stop()` com mensagens de `MensagemUtil`
- Notificações: `MessageService` do PrimeNG com `p-messages`
- Confirmações: `ConfirmationService` do PrimeNG
- Calendário: sempre com `ConstantsUtil.calendarioLocale`

### Permissões no frontend

- Toda rota nova precisa de `canActivate: [AuthGuard, AuthGuardRoutes]`
- Role em `data: { role: [PermissaoUtil.NOME_DA_PERMISSAO] }`
- Novas permissões adicionadas em `src/app/util/permissao.util.ts`
- Controle no template com diretiva `*nucSecured` do `SecurityModule`

### Pipes — usar os existentes

| Necessidade | Pipe |
|---|---|
| Data para dd/mm/yyyy | `brDate` |
| Formatar CPF/CNPJ | `cpfCnpjPipe` |
| "S"/"N" para "Sim"/"Não" | `simNaoPipe` |
| Número decimal BR | `numeroDecimal` |
| Coordenada geográfica | `coordenada` |

### Constantes — usar `ConstantsUtil`

```typescript
ConstantsUtil.calendarioLocale   // config PT-BR para p-calendar
ConstantsUtil.ID_TORA            // 64
ConstantsUtil.AMOSTRAL           // 2
ConstantsUtil.NAO_APLICA         // 'N/A'
```

### O que NÃO fazer no frontend

- Não criar standalone components nem usar `bootstrapApplication()`
- Não retornar o body diretamente nos serviços — manter `observe: 'response'`
- Não criar pipes sem registrá-los no `PipesModule`
- Não usar `console.log` — remover antes de commitar

### PrimeNG 7 + Reactive Forms — campos desabilitados

No PrimeNG 7, `[disabled]="false"` em `p-dropdown` **não reativa** o controle quando ele já está `disable()` no `FormControl`. Usar uma destas abordagens:

- `[attr.disabled]="condicao ? true : null"` em `input`/`textarea` nativos
- `[disabled]="condicao"` no `p-dropdown` **sem** chamar `formControl.disable()` no TypeScript para o mesmo campo
- Recriar o `FormControl` ou usar `*ngIf` para forçar re-render do dropdown quando a condição mudar

### Licenciamento — inventário florestal (RT vs empreendedor)

- `ResponsavelUtilService.temResponsavelVinculado(responsaveis)` — retorna `true` se o usuário logado **não** está vinculado como RT
- Usado em `aba-inventario-florestal` e subcomponentes para bloquear edição de campos quando o empreendedor visualiza e o RT ainda não vinculou
- Campos afetados: processo de inventário, forma de parcela, metodologia, área de amostra, equação do volume, etc.
- `processoAmostragem` tem regra própria (`processoAmostragemInicial`) — pode ficar bloqueado mesmo com RT vinculado

### PDFs de envio do licenciamento (frontend)

Serviço: `src/app/service/licenciamento.ts`

```typescript
// Comprovante de envio
this.http.get<Blob>(`${resourceUrl}/${id}/comprovante-envio-projeto`, { responseType: 'blob' as 'json' });

// Formulário completo de envio
this.http.get<Blob>(`${resourceUrl}/${id}/formulario-envio-licenciamento`, { responseType: 'blob' as 'json' });
```

Tela: `aba-enviar-orgao-ambiental/`

---
