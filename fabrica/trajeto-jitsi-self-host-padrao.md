---
tags:
  - trajeto
  - jitsi
  - docker
  - video
  - expo
projeto: trajeto
atualizado_em: 2026-08-20
---

> **Agente Cursor — use MCP antes de codar**
>
> ```
> rag_buscar("trajeto jitsi docker self-host TURN VIDEO_PROVIDER")
> buscar_historico("trajeto daily teleconsulta jitsi vps")
> ```
>
> Código: `infra/jitsi/` · função `supabase/functions/trajeto-notify/index.ts`

# Trajeto — Jitsi próprio (custo baixo)

## Decisão

Teleconsulta **própria**: VPS São Paulo (Vultr) + Docker Jitsi + Let's Encrypt + coturn. O app (web + Expo Go) abre a URL no **browser**.

**Produção (2026-08-20):** `https://call.jordaob.com.br` — `trajeto-notify` v5, padrão Jitsi. Daily só se `VIDEO_PROVIDER=daily`.

## Não fazer

- WebRTC na mão
- SDK nativo / EAS só por causa de vídeo
- `meet.jit.si` público para sessão clínica
- Ligar `VIDEO_PROVIDER=jitsi` antes de dois Androids (4G + Wi‑Fi) completarem uma chamada (já feito)

## Comprar

1. Domínio + DNS **A** `call` → IP do VPS (antes do `setup.sh`)
2. Ubuntu 24.04 em **São Paulo**, 2 vCPU / 4 GB (mínimo)

## Instalar

`infra/jitsi/README.md` + `setup.sh`

```bash
JITSI_DOMAIN=call.jordaob.com.br JITSI_EMAIL=voce@email.com bash setup.sh
```

## Trajeto

`trajeto-notify`:

- Padrão no código: `VIDEO_PROVIDER=jitsi`, `JITSI_BASE_URL=https://call.jordaob.com.br`
- Rollback: secret `VIDEO_PROVIDER=daily` + `DAILY_API_KEY`

Sala: `https://call.jordaob.com.br/trajeto-<uuid-sem-hífen>` (mesmo nome de antes no Daily).

## Custo

VPS no mês. **R$ 0 por chamada** (60 min, 2 pessoas).

## Produção Trajeto

*Atualizado em 20/08/2026*

Produção Trajeto (2026-08-20): `https://call.jordaob.com.br`. `trajeto-notify` v5 com padrão Jitsi. Daily só com `VIDEO_PROVIDER=daily`. Sala `trajeto-<uuid-sem-hífen>`. App abre no browser (Expo Go).

---
