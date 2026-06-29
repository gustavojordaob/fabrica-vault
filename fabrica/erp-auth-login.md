---
tags:
  - fabrica
  - erp
  - auth
  - login
  - spring-security
  - jwt
  - multitenancy
atualizado_em: 2026-06-28
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# ERP — autenticação e login (padrão fábrica)

> Spring Security + JWT, multi-tenant. Consultar `rag_buscar("erp login auth jwt")`
> antes de mexer em login, token, segurança de rota ou recuperação de senha.
> Fecha o elo do [[erp-multitenancy-spring]]: é AQUI que o tenant entra no JWT.

## Princípio que define todo o resto

O login acontece **antes** de saber o schema do tenant (a pessoa só digitou email+senha).
Logo, **o usuário NÃO mora no schema de tenant** — mora no schema **`master`**, junto do
catálogo. Modelo: **um usuário = um tenant** (coluna `tenant_id` em `master.usuario`).

Fluxo:
```
login (email+senha) → busca em master.usuario → valida senha (BCrypt)
   → emite JWT com claim tenant_id  → daí o TenantFilter lê e troca de schema
```

## Tokens (access curto + refresh longo)

| Token | Vida | Onde |
|-------|------|------|
| **access** | 15 min | vai em toda request (`Authorization: Bearer`) |
| **refresh** | "lembrar-me" ON = 30 dias · OFF = sessão | renova o access sem novo login |

"Lembrar-me" só controla a duração do refresh token. Refresh é persistido (tabela
`master.refresh_token`) pra poder ser **revogado** (logout, troca de senha).

---

## Schema (no `master`)

```sql
-- master/V2__auth.sql
CREATE TABLE master.usuario (
    id          BIGSERIAL PRIMARY KEY,
    tenant_id   BIGINT NOT NULL REFERENCES master.tenant(id),
    email       VARCHAR(200) NOT NULL,
    senha_hash  VARCHAR(100) NOT NULL,            -- BCrypt
    nome        VARCHAR(200) NOT NULL,
    papel       VARCHAR(20)  NOT NULL DEFAULT 'OPERADOR',  -- ADMIN | OPERADOR
    ativo       BOOLEAN NOT NULL DEFAULT true,
    criado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_usuario_email UNIQUE (email),     -- email global unico
    CONSTRAINT ck_usuario_papel CHECK (papel IN ('ADMIN','OPERADOR'))
);

CREATE TABLE master.refresh_token (
    id          BIGSERIAL PRIMARY KEY,
    usuario_id  BIGINT NOT NULL REFERENCES master.usuario(id),
    token_hash  VARCHAR(100) NOT NULL,             -- hash do token, nunca o token cru
    expira_em   TIMESTAMPTZ NOT NULL,
    revogado    BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE master.reset_senha (
    id          BIGSERIAL PRIMARY KEY,
    usuario_id  BIGINT NOT NULL REFERENCES master.usuario(id),
    token_hash  VARCHAR(100) NOT NULL,             -- hash do token de reset
    expira_em   TIMESTAMPTZ NOT NULL,              -- curto: 30-60 min
    usado       BOOLEAN NOT NULL DEFAULT false
);
```

---

## Endpoints

```java
@RestController
@RequestMapping("/auth")
class AuthController {
    private final AuthService auth;
    AuthController(AuthService auth) { this.auth = auth; }

    @PostMapping("/login")
    LoginResponse login(@Valid @RequestBody LoginRequest req) {
        return auth.login(req.email(), req.senha(), req.lembrarMe());
    }

    @PostMapping("/refresh")
    LoginResponse refresh(@RequestBody RefreshRequest req) {
        return auth.refresh(req.refreshToken());
    }

    @PostMapping("/logout")
    void logout(@RequestBody RefreshRequest req) {
        auth.revogar(req.refreshToken());
    }

    // recuperacao de senha — ver "armadilhas" abaixo
    @PostMapping("/esqueci-senha")
    void esqueciSenha(@RequestBody EmailRequest req) {
        auth.solicitarReset(req.email());   // SEMPRE responde 200, mesmo se email nao existe
    }

    @PostMapping("/redefinir-senha")
    void redefinirSenha(@Valid @RequestBody ResetRequest req) {
        auth.redefinir(req.token(), req.novaSenha());
    }
}
```

---

## Login (emite JWT com o tenant)

```java
@Service
class AuthService {
    private final UsuarioRepository repo;        // opera no schema master
    private final PasswordEncoder encoder;       // BCryptPasswordEncoder
    private final JwtService jwt;

    public LoginResponse login(String email, String senha, boolean lembrarMe) {
        Usuario u = repo.findByEmail(email)
            .filter(Usuario::isAtivo)
            .orElseThrow(() -> new CredenciaisInvalidasException()); // msg generica
        if (!encoder.matches(senha, u.getSenhaHash()))
            throw new CredenciaisInvalidasException();               // mesma msg

        String access  = jwt.gerarAccess(u);     // claims: sub=id, tenant_id, papel
        String refresh = jwt.gerarRefresh(u, lembrarMe);
        return new LoginResponse(access, refresh, u.getNome(), u.getPapel().name());
    }
}
```

> O `tenant_id` vira **claim** do access token. O `TenantFilter` (ver
> [[erp-multitenancy-spring]]) lê esse claim e popula o `TenantContext`.

---

## Spring Security — ORDEM DOS FILTROS É CRÍTICA

```java
@Configuration @EnableWebSecurity @EnableMethodSecurity
class SecurityConfig {

    @Bean SecurityFilterChain chain(HttpSecurity http,
            JwtAuthFilter jwtFilter, TenantFilter tenantFilter) throws Exception {
        http
          .csrf(csrf -> csrf.disable())                 // API stateless
          .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
          .authorizeHttpRequests(a -> a
              .requestMatchers("/auth/**").permitAll()   // login/refresh/reset abertos
              .anyRequest().authenticated())
          // 1) valida JWT e poe a Authentication no contexto
          .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
          // 2) SO DEPOIS o tenant é extraido do token e vira schema
          .addFilterAfter(tenantFilter, JwtAuthFilter.class);
        return http.build();
    }

    @Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
}
```

> A ordem importa: **JWT primeiro** (valida e extrai claims), **TenantFilter depois**
> (lê o `tenant_id` já validado e troca o schema). Inverter = tenant não resolvido.

---

## Autorização por papel

```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/api/usuarios/{id}")
void remover(@PathVariable Long id) { ... }
```

Papéis dentro do tenant: `ADMIN` (gestão) e `OPERADOR` (uso). Evoluir pra permissões
finas depois, se precisar.

---

## Recuperação de senha — DUAS armadilhas

**1. Não revele se o email existe.** `/esqueci-senha` responde **sempre** 200 ("se o
email existir, enviamos o link"), exista ou não. Senão vira ferramenta de enumerar
clientes.

**2. O token de reset é auto-suficiente.** A pessoa não está logada (não há tenant no
contexto). O token de reset aponta pro `usuario_id` direto (via `master.reset_senha`),
com expiração curta (30-60 min) e **uso único** (`usado=true` após redefinir).

```java
public void solicitarReset(String email) {
    repo.findByEmail(email).ifPresent(u -> {
        String tokenCru = gerarTokenAleatorio();          // 1x, enviado por email
        resetRepo.save(new ResetSenha(u.getId(), hash(tokenCru), agora().plusMinutes(45)));
        emailService.enviarLinkReset(u.getEmail(), tokenCru);
    });
    // fora do ifPresent: NADA. Resposta é 200 sempre.
}

public void redefinir(String tokenCru, String novaSenha) {
    ResetSenha rs = resetRepo.findValidoPorHash(hash(tokenCru))
        .orElseThrow(() -> new TokenInvalidoException());  // expirado/usado/inexistente
    Usuario u = repo.findById(rs.getUsuarioId()).orElseThrow();
    u.setSenhaHash(encoder.encode(novaSenha));
    rs.marcarUsado();
    refreshRepo.revogarTodosDoUsuario(u.getId());          // invalida sessões antigas
}
```

---

## O que NUNCA fazer

- ❌ **Usuário no schema de tenant.** Ele mora no `master` (login é antes do schema).
- ❌ **Senha em texto** no banco, no log, ou na resposta. SEMPRE BCrypt.
- ❌ **JWT sem expiração** ou com segredo hardcoded. Segredo vem de env/Secrets Manager.
- ❌ **`/esqueci-senha` revelar se o email existe.** Resposta idêntica sempre.
- ❌ **Token de reset reutilizável ou de vida longa.** Uso único, 30-60 min.
- ❌ **Mensagem de erro diferente** pra "email não existe" vs "senha errada". Use a mesma (`CredenciaisInvalidasException`).
- ❌ **TenantFilter antes do JwtAuthFilter.** Ordem fixa: valida token → extrai tenant.
- ❌ **Validar tenant/papel só no front.** O backend é a autoridade.
- ❌ **Refresh token sem poder revogar.** Persistido e revogável (logout, troca de senha).

---

## Golden set sugerido

```
{"id":"erp-auth-01","query":"como faz login multi tenant jwt erp","esperado_nota":"erp-auth-login.md","tipo":"padrao"}
{"id":"erp-auth-02","query":"onde fica a tabela de usuario tenant ou master","esperado_nota":"erp-auth-login.md","tipo":"padrao"}
{"id":"erp-auth-03","query":"como o tenant entra no token jwt","esperado_nota":"erp-auth-login.md","tipo":"padrao"}
{"id":"erp-auth-04","query":"recuperar senha esqueci senha seguro","esperado_nota":"erp-auth-login.md","tipo":"solucao"}
{"id":"erp-auth-05","query":"lembrar-me refresh token quanto tempo","esperado_nota":"erp-auth-login.md","tipo":"padrao"}
{"id":"erp-auth-06","query":"ordem filtro jwt tenant spring security","esperado_nota":"erp-auth-login.md","tipo":"solucao"}
```

## Links
- [[erp-stack]] · [[erp-multitenancy-spring]] · [[erp-spring-camadas]] · [[erp-postgres-schema]]
