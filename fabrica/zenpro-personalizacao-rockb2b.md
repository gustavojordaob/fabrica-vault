# Zen Pro — câmera RockB2B (frames do print-h5)

**Agente Cursor — use MCP antes de codar**

Queries:
- `rag_buscar("zenpro rockb2b camera frames moldura")`
- `buscar_historico("rockb2b personalizacao camera")`

Repo: `projetos/zenpro`

## Importante

O [print-h5 RockB2B](https://print-h5.rockb2b.com/h5/#/hotCustom) **não entrega SVG**. O “wireframe” vermelho é o PNG `image` (e `floorImage`) da API `listModel`.

## Problemas comuns

1. **Câmera fantasma (iPhone)** — SVG + PNG Rock desenhados juntos. Com `cameraFrameUrl`, forçar `sem-camera` e **não** gerar SVG no CaseEditor/CasePreview.
2. **Modelo admin “teste2”** — `criarModeloAdmin` gerava id pelo nome (`xiaomi-teste2`) e perdia o frame. Usar **id do preset Rock** (`redmi-note-10-pro-max`) + gravar `cameraFrameUrl`.

## Silhueta do aparelho (body mask H5 — todos os 101 modelos)

Além da câmera, o [hotCustom H5](https://print-h5.rockb2b.com/h5/#/hotCustom) define o **formato** pelo contorno vermelho externo (`frameImage`): cantos, botões laterais, proporção.

| Campo | Origem |
|---|---|
| `bodyMaskUrl` | PNG branco+AA = dentro da capa (`{id}-body-mask.png?v=16`) |
| `bodyRimUrl` | filete da borda no mesmo contorno (`{id}-body-rim.png?v=16`) |
| `molduraAspect` | W/H do contorno externo |
| `caseRadius` | raio do canto (fração da largura) → fallback sem rim |

**Gerar:** `node scripts/process-rockb2b-body-masks.mjs` (ou `--only=iphone`)

Pipeline da máscara: dilata o filete vermelho (fecha gaps) → flood fill → morph close → anti-alias. **Nunca** desligar `usarBodyMask` no mock frontal — round-rect genérico foge do H5.

**Regra absoluta (câmera):** o PNG H5 das lentes é autoridade — **nunca** recolorir/clarear pixels da câmera em runtime. Branco “em volta” = só `bodyFill` / `corAparelho` sob o punch.

| Superfície | Como |
|---|---|
| `CasePreview` | `destination-in` H5 — **sem** filete/borda branca (`bodyRim` / CASE_BORDER) |
| `CaseEditor` | mesmo clip H5 sem borda branca; punch/overlay câmera |
| `CaseFake3dPreview` | CSS mask no wrapper (legado) |
| Export | `maskUrl` = `bodyMaskUrl` |

## Extração do módulo da câmera (v15 natural — 07/2026)

O `frameImage` traz **dois contornos vermelhos**: o externo é a capa, o segundo é a ilha da câmera. Regras que valem para os 101 modelos:

| Situação | Regra |
|---|---|
| Dois contornos | Ilha = 2º maior componente vermelho; interior por flood fill |
| Contorno único (S23 Ultra, iPhone X) | Ilha = bbox do hardware, com cantos arredondados (16%) |
| iPhone / mock claro | `--natural`: copiar pixels H5 **primeiro**; preencher buracos transparentes com platô claro |
| Android legado (escurecer) | Sem `--natural`: mapear platô claro para `L=46` com contraste 1.45 |
| Platô transparente (Redmi/Xiaomi) | Preencher buracos da ilha com o tom base |

**Erro que já aconteceu:** (1) apagar fill branco por limiar absoluto — some flash/aros; (2) `lightenCameraPlate` em runtime — destrói lentes. Use limiar **proporcional à área da ilha** e **não** altere o PNG das lentes no browser.

Validação: `node scripts/validate-rockb2b-camera-frames.mjs` conta lentes/flash por PNG e lista suspeitos (< 2 peças). Peça única não é erro quando as lentes ficam coladas ao módulo — conferir a imagem.

## Arte de produção (dono / impressão)

Arquivo pro dono = **retângulo full-bleed** (estilo [print-h5](https://print-h5.rockb2b.com/h5/#/hotCustom)), não o mock em formato de capa.

| Quem | O quê |
|---|---|
| Cliente | `CasePreview` — silhueta H5 |
| Admin (preview) | mesmo `CasePreview` (mock do cliente) |
| Dono (**só download** no pedido) | **Recorte H5** = `printGuideUrl` do frameImage Rock (vermelho + câmera, preto transparente) sobre fundo laranja + foto/texto. Script: `process-rockb2b-print-guides.mjs` |

`mapItem` do admin **deve** ler `arteProducaoUrl` / `arteFotoUrl` / `arteTextoUrl`. Sem isso o painel mostra “Artes ainda não geradas” mesmo com URL no Firestore.

Se faltar arte: botão **Gerar arte de produção** no detalhe do pedido (`regenerarArtesItemPedidoAdmin`). Storage: marca pode escrever em `artes-producao/{qualquerUid}/`.

## Preview “Ver na case”

Só **vista frontal** (`CasePreview`). Fake 3D / “Na capinha” removido.

## Branco em volta da câmera (sem tocar nas lentes)

Mock: punch + `bodyFill`/`contactShadow` + overlay H5 completo (como antes). Sem filete branco e **sem sombra fora** do contorno H5 (a aureola cinza vinha do `shadowBlur` no editor + AA suave da máscara).

Silhueta: `hardenBodyMaskAlpha` + `clipInset=0` — a foto vai até a borda do H5. Export mantém punch.

## Preview “Na capinha” (fake 3D CSS)

`CaseFake3dPreview.tsx` — legado / não usado no modal. Perspectiva CSS + casco TPU.
## Fluxo

1. `scripts/process-rockb2b-camera-frames.mjs` — baixa `image`, remove fundo preto/vermelho → `public/molduras/rock/{id}-camera.png`
2. `scripts/process-rockb2b-body-masks.mjs` — contorno externo → `{id}-body-mask.png` + aspect/radius (`--only=iphone` ok)
3. `scripts/generate-rockb2b-modelos.mjs` — gera catálogo (preservar campos de perso ao reprocessar frames)
4. Capinha nova / modelos — persiste `cameraFrameUrl` + id estável do preset
5. `resolveRockCameraFrameUrl` / `resolveRockBodyMaskUrl` — fallback por nome

## Checklist

- [ ] Nunca desenhar SVG se existir `cameraFrameUrl`
- [ ] Id do modelo = id Rock quando vier do catálogo H5
- [ ] Testar local (`npm run dev`) — iPhone e Redmi sem overlay duplo
- [ ] Após reprocessar, subir o `?v=` do `cameraFrameUrl` (cache do Hosting)
- [ ] Rodar `validate-rockb2b-camera-frames.mjs` e olhar iPhone 17 Pro Max, S26 Ultra e Redmi
