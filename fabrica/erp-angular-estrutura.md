---
tags:
  - fabrica
  - erp
  - angular
  - frontend
  - signals
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — frontend Angular 21 (padrão fábrica)

> Angular 21 LTS, **signal-first / zoneless / standalone**. Consultar
> `rag_buscar("erp angular padrao")` antes de criar componente ou tela.
> (LTS até maio/2027. Padrão de código idêntico ao 22; difere só em Signal Forms — ver abaixo.)

## Mentalidade 2026 (NÃO é o Angular antigo)

| Morto (não usar) | Padrão atual (usar) |
|------------------|---------------------|
| `NgModule` | **standalone components** (sem módulos) |
| `*ngIf` / `*ngFor` | **`@if` / `@for`** (control flow nativo) |
| `@Input()` decorator | **`input()`** (signal) |
| `@Output()` | **`output()`** |
| `BehaviorSubject` pra estado de tela | **`signal()` / `computed()`** |
| Zone.js | **zoneless** (signals dirigem o change detection) |
| Karma | **Vitest** |
| construtor com injeção | **`inject()`** |

> **Forms no Angular 21:** o padrão estável é **Reactive Forms tipados**. Signal Forms
> ainda é **experimental** no 21 (virou estável só no 22) — use só se topar a instabilidade.
> Ao migrar pro 22 depois, Signal Forms vira o caminho.

---

## Código de referência

### Componente standalone signal-first

```typescript
import { Component, signal, computed, inject } from '@angular/core';
import { PedidoService } from './pedido.service';

@Component({
  selector: 'app-lista-pedidos',
  // standalone é o default no Angular 21 — sem NgModule
  template: `
    @if (carregando()) {
      <app-spinner />
    } @else {
      <table>
        @for (p of pedidos(); track p.id) {
          <tr><td>{{ p.id }}</td><td>{{ p.total | currency:'BRL' }}</td></tr>
        } @empty {
          <tr><td colspan="2">Nenhum pedido</td></tr>
        }
      </table>
      <p>Total geral: {{ totalGeral() | currency:'BRL' }}</p>
    }
  `,
})
export class ListaPedidosComponent {
  private service = inject(PedidoService);

  pedidos = signal<Pedido[]>([]);
  carregando = signal(true);
  totalGeral = computed(() =>
    this.pedidos().reduce((acc, p) => acc + p.total, 0)
  );

  constructor() {
    this.service.listar().subscribe(ps => {
      this.pedidos.set(ps);
      this.carregando.set(false);
    });
  }
}
```

### Service com HttpClient

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class PedidoService {
  private http = inject(HttpClient);
  private base = '/api/pedidos';

  listar() { return this.http.get<Pedido[]>(this.base); }
  criar(req: CriarPedidoRequest) { return this.http.post<Pedido>(this.base, req); }
}
```

### Componente filho com input/output signals

```typescript
@Component({ selector: 'app-card-pedido', template: `...` })
export class CardPedidoComponent {
  pedido = input.required<Pedido>();      // <app-card-pedido [pedido]="p" />
  selecionado = output<number>();         // (selecionado)="..."
}
```

### Tela de organização (ERP tem MUITAS telas)

```
features/pedido/
├── lista-pedidos.component.ts
├── form-pedido.component.ts
├── pedido.service.ts
├── pedido.model.ts          ← interfaces/tipos
└── pedido.routes.ts         ← rotas lazy do módulo de feature
```

---

## Estado: signals, não RxJS pra tudo

- **Estado de tela** (lista carregada, loading, filtro selecionado) → `signal()` / `computed()`.
- **RxJS** só onde é fluxo assíncrono de verdade (HTTP, eventos, debounce de busca). Não use `BehaviorSubject` como "variável reativa" — isso virou `signal`.
- Estado compartilhado entre componentes → service `providedIn: 'root'` com signals dentro.

---

## Multi-tenant no front

- O tenant vem do **JWT** (login). Não tem seletor de tenant na URL nem na query.
- **Interceptor** anexa o token em toda request; o backend resolve o schema. O front **não** sabe de schema.

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token();
  return next(token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req);
};
```

---

## O que NUNCA fazer

- ❌ **Criar `NgModule`.** Standalone é o padrão. Módulo é legado.
- ❌ **`*ngIf` / `*ngFor`.** Use `@if` / `@for` com `track`.
- ❌ **`BehaviorSubject` pra estado de tela.** Use `signal`.
- ❌ **`@Input()` / `@Output()` decorator.** Use `input()` / `output()`.
- ❌ **Lógica de tenant/schema no front.** Tenant é o token; backend resolve.
- ❌ **Karma.** Teste com Vitest (default do 22).
- ❌ **Subscrever sem cleanup** em componente — use `takeUntilDestroyed()` ou `toSignal()`.

---

## Golden set sugerido

```
{"id":"erp-ng-01","query":"angular usa ngmodule ou standalone no erp","esperado_nota":"erp-angular-estrutura.md","tipo":"padrao"}
{"id":"erp-ng-02","query":"estado de tela signal ou behaviorsubject","esperado_nota":"erp-angular-estrutura.md","tipo":"padrao"}
{"id":"erp-ng-03","query":"como anexar token multi tenant angular","esperado_nota":"erp-angular-estrutura.md","tipo":"padrao"}
```

## Links
- [[erp-stack]] · [[erp-spring-camadas]]
