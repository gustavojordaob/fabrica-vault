---
tags:
  - fabrica
  - capinhas
  - personalizacao
  - editor
  - canvas
  - firebase-storage
atualizado_em: 2026-07-01
autor: Gustavo
status: padrao-canonico
tipo_doc: padrao
---

# Capinhas — editor de personalização (padrão fábrica)

> O coração do produto e o "uau" da demo. A pessoa sobe a foto e a ALINHA na
> capinha (arrasta, zoom, posiciona). Consultar `rag_buscar("capinhas editor foto")`
> antes de mexer no editor. Ver stack em [[capinhas-stack]].

## Conceito

Todo o ajuste é **no browser** — sem processamento no servidor, sem IA. A pessoa:
1. Escolhe o modelo de celular (define o formato/moldura e o recorte da câmera).
2. Sobe a foto (Firebase Storage).
3. **Arrasta, dá zoom e gira** a foto dentro da área útil da capinha.
4. Vê o preview em tempo real com a moldura do celular por cima.
5. Compra.

O que se salva no fim: **a foto original + a transformação** (posição, escala, rotação).
Isso basta pra reproduzir/produzir a capinha depois.

## Anatomia da tela

```
┌─────────────────────────────┐
│   [moldura do modelo PNG]    │  ← overlay fixo por cima (área câmera transparente)
│   ┌───────────────────────┐  │
│   │   foto do cliente      │  │  ← camada arrastável/zoom (embaixo da moldura)
│   │   (transform aplicado) │  │
│   └───────────────────────┘  │
│   área útil = onde a foto     │
│   pode aparecer               │
└─────────────────────────────┘
   [ zoom - ][ + ]  [girar]  [trocar foto]  [COMPRAR]
```

Camadas (z-order) — preview realista (zenpro, browser only):
1. **Fundo estúdio** `#ececec` (sem moldura preta externa)
2. **Drop shadow** — silhueta da máscara (`iphone-mask.png`) deslocada + blur (só embaixo, fora da capa)
3. **Foto blur** (cover fixo) + escurecimento leve **só na camada blur** (não cobre a foto nítida)
4. **Foto nítida** — arrastável / zoom / rotação (por cima do blur)
5. **Clip** — `destination-in` com `iphone-mask.png` (silhueta apenas)
6. **Sombra interna** — anel inset ~8px, opacidade máx **15%** (só bordas)
7. **Borda fina** — linha clara 1–2px no contorno
8. **Lentes câmera** — só traços das lentes extraídos do overlay (topo 30%), **nunca** corpo azul do PNG

> **Não** desenhar `iphone-overlay.png` opaco por cima — o corpo azul tapa a foto. Overlay serve só para extrair círculos das lentes.

Camadas (legado / conceito):
1. **Fundo** (área da capinha)
2. **Foto do cliente** — camada manipulável (drag / pinch-zoom / rotação)
3. **Moldura do modelo** (PNG com transparência na área da câmera e bordas) — FIXA por cima

## Modelo de celular (dado)

```
modelos_celular/{id} = {
  marca: "Apple",
  modelo: "iPhone 15",
  moldura_url: "...",      // PNG transparente: borda + recorte câmera
  largura_px: 1000,        // dimensão do canvas de produção
  altura_px: 2000,
  area_util: { x, y, w, h } // onde a foto pode aparecer
}
```

## Estado do editor (o que salvar)

```typescript
type Personalizacao = {
  modeloId: string;
  fotoUrl: string;              // Firebase Storage (foto original)
  transform: {
    x: number;                  // deslocamento
    y: number;
    scale: number;              // zoom
    rotation: number;           // graus
  };
};
```

> Salvar a **foto original + transform** (não a imagem "achatada"). Assim a produção
> renderiza em alta resolução depois, e o cliente pode reeditar.

## Implementação (recomendado)

- **Preview:** `<canvas>` ou biblioteca de canvas (Konva.js / react-konva é ótimo pra
  drag+zoom+rotação de camadas). Konva resolve o arrastar/zoom/gestos sem reinventar.
- **Upload:** Firebase Storage. Comprimir no client antes (browser-image-compression)
  pra não subir 10MB de foto de celular.
- **Preview vs produção:** a tela mostra em baixa resolução; a produção reaplica o
  mesmo `transform` sobre a foto original em `largura_px × altura_px`.

### Upload pro Storage (padrão)

```typescript
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import imageCompression from "browser-image-compression";

async function subirFoto(file: File): Promise<string> {
  const comprimida = await imageCompression(file, { maxSizeMB: 2, maxWidthOrHeight: 2000 });
  const r = ref(storage, `personalizacoes/${crypto.randomUUID()}.jpg`);
  await uploadBytes(r, comprimida);
  return getDownloadURL(r);
}
```

### Preview com react-konva (esqueleto)

```tsx
<Stage width={W} height={H}>
  <Layer>
    {/* foto manipulável */}
    <KonvaImage image={foto} draggable
      x={t.x} y={t.y} scaleX={t.scale} scaleY={t.scale} rotation={t.rotation}
      onDragEnd={e => setT({...t, x: e.target.x(), y: e.target.y()})} />
  </Layer>
  <Layer listening={false}>
    {/* moldura do modelo por cima, não interativa */}
    <KonvaImage image={moldura} width={W} height={H} />
  </Layer>
</Stage>
```

## Para a DEMO (mínimo que impressiona)

Não precisa de loja, pagamento nem login pra mostrar o "uau":
1. Uma tela `/personalizar` com 1-2 modelos de celular.
2. Botão "escolher foto" → sobe → aparece no preview.
3. Arrasta / zoom / gira com a moldura por cima.
4. Botão "comprar" pode só levar pro carrinho (mockado).

Isso sozinho já mostra pro cliente o diferencial que o Shopify dele não faz.

## O que NÃO fazer

- ❌ Processar/recortar imagem no servidor — tudo no browser.
- ❌ Salvar a imagem "achatada" (foto+moldura mesclada) como único registro — perde resolução e reedição. Salvar foto original + transform.
- ❌ Subir a foto sem comprimir — fotos de celular são enormes.
- ❌ Depender de IA pra "encaixar" — o alinhamento é manual (arrasta/zoom), simples e confiável.
- ❌ Construir loja/checkout antes de o editor estar convincente.

## Golden set sugerido

```
{"id":"cap-edit-01","query":"como a pessoa alinha a foto na capinha","esperado_nota":"capinhas-personalizacao.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-edit-02","query":"editor de capinha canvas konva drag zoom","esperado_nota":"capinhas-personalizacao.md","esperado_secao":null,"tipo":"padrao"}
{"id":"cap-edit-03","query":"o que salvar da personalizacao foto ou transform","esperado_nota":"capinhas-personalizacao.md","esperado_secao":null,"tipo":"solucao"}
{"id":"cap-edit-04","query":"subir foto firebase storage comprimir capinha","esperado_nota":"capinhas-personalizacao.md","esperado_secao":null,"tipo":"padrao"}
```

## Links
- [[capinhas-stack]]
