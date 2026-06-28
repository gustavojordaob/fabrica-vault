"""
dividir_claude_md.py
--------------------
Divide o CLAUDE.md da Fábrica de Software em notas temáticas
prontas para o Obsidian, organizadas para alimentar o RAG.

Uso:
    python dividir_claude_md.py
    python dividir_claude_md.py --input outro_claude.md --vault C:/Obsidian/fabrica

Dependências: apenas biblioteca padrão do Python 3.8+
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Mapeamento: palavras-chave no título da seção → nome da nota no Obsidian
# ---------------------------------------------------------------------------
MAPA_NOTAS = [
    # (lista de palavras-chave para detectar, nome do arquivo de saída, tags)
    (["react native", "fundamentos", "flexbox", "stylesheet", "safe area", "core components"],
     "react-native-fundamentos",
     ["react-native", "fundamentos", "ui"]),

    (["expo", "expo go", "expo router", "file-based", "tabs", "navegação"],
     "expo-router-navegacao",
     ["expo", "router", "navegacao"]),

    (["firebase", "firestore", "realtime", "config", "inicializ"],
     "firebase-setup-patterns",
     ["firebase", "firestore", "setup"]),

    (["autenticação", "auth", "login", "logout", "google sign", "usuario"],
     "auth-patterns",
     ["firebase", "auth", "seguranca"]),

    (["storage", "upload", "download", "arquivo", "imagem", "bucket"],
     "storage-patterns",
     ["firebase", "storage", "arquivos"]),

    (["cloud function", "functions", "onrequest", "oncall", "deploy", "secrets"],
     "cloud-functions-patterns",
     ["firebase", "functions", "backend"]),

    (["mercado pago", "mercadopago", "pagamento", "checkout", "webhook", "preapproval",
      "assinatura", "plano", "sandbox"],
     "mercadopago-integration",
     ["pagamentos", "mercadopago", "assinatura"]),

    (["z-api", "whatsapp", "zapi", "mensagem", "instancia"],
     "zapi-whatsapp",
     ["integracao", "whatsapp", "zapi"]),

    (["schema", "coleção", "collection", "modelo de dados", "estrutura", "firestore schema"],
     "firestore-schemas",
     ["firestore", "schema", "dados"]),

    (["checklist", "deploy", "publicar", "configurar", "setup key"],
     "checklists-deploy",
     ["checklist", "deploy", "qualidade"]),

    (["padrão", "padrao", "lashmatch", "fábrica", "fabrica", "projeto", "convenção"],
     "padroes-fabrica",
     ["padroes", "fabrica", "lashmatch"]),

    (["componentiz", "componente", "reutiliz", "button", "input reutiliz",
      "fragment", "spread", "props"],
     "componentes-reutilizaveis",
     ["componentes", "reutilizacao", "ui"]),

    (["context api", "context", "provider", "usecontext", "compartilhar dados",
      "estado global"],
     "context-api-estado",
     ["estado", "context", "react"]),

    (["stack navigator", "bottom tab", "tab navigator", "custom tab", "deep link",
      "navegação", "navigator", "react navigation"],
     "react-navigation-patterns",
     ["navegacao", "react-navigation", "tabs"]),

    (["snippet", "utilitário", "utilitario", "helper", "theme", "paleta",
      "cores", "dimensões", "sombra", "shadow", "comandos frequentes", "crud"],
     "snippets-utilitarios",
     ["snippets", "utilitarios", "codigo"]),
]

NOTA_GENERICA = "outros"

# ---------------------------------------------------------------------------

def slugify(texto: str) -> str:
    """Converte título para nome de arquivo seguro."""
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE)
    texto = re.sub(r"[\s_]+", "-", texto).strip("-")
    return texto[:80]


def detectar_nota(titulo_secao: str) -> tuple[str, list[str]]:
    """Retorna (nome_arquivo, tags) com base no título da seção."""
    titulo_lower = titulo_secao.lower()
    for palavras_chave, nome, tags in MAPA_NOTAS:
        if any(p in titulo_lower for p in palavras_chave):
            return nome, tags
    return NOTA_GENERICA, ["geral"]


def gerar_frontmatter(titulo: str, tags: list[str], secoes_incluidas: list[str]) -> str:
    """Gera o bloco YAML de frontmatter para o Obsidian."""
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    secoes_yaml = "\n".join(f"  - \"{s}\"" for s in secoes_incluidas[:5])
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    return f"""---
tags:
{tags_yaml}
fonte: CLAUDE.md
gerado_em: {data_hoje}
secoes:
{secoes_yaml}
---

"""


def dividir_por_secoes(conteudo: str) -> list[tuple[str, str]]:
    """
    Retorna lista de (titulo_secao, conteudo_secao).
    Reconhece ## e ### como separadores de seção.
    """
    partes = re.split(r'\n(?=#{1,3} )', conteudo)
    secoes = []
    for parte in partes:
        if not parte.strip():
            continue
        match = re.match(r'^(#{1,3})\s+(.+)', parte)
        if match:
            titulo = match.group(2).strip()
            secoes.append((titulo, parte.strip()))
        else:
            # Conteúdo antes do primeiro heading
            secoes.append(("_intro", parte.strip()))
    return secoes


def agrupar_em_notas(secoes: list[tuple[str, str]]) -> dict:
    """
    Agrupa as seções em notas temáticas.
    Retorna dict: nome_arquivo → { 'tags': [...], 'conteudo': [...], 'titulos': [...] }
    """
    notas: dict = {}

    for titulo, conteudo in secoes:
        nome_nota, tags = detectar_nota(titulo)

        if nome_nota not in notas:
            notas[nome_nota] = {"tags": tags, "conteudo": [], "titulos": []}

        notas[nome_nota]["conteudo"].append(conteudo)
        if titulo != "_intro":
            notas[nome_nota]["titulos"].append(titulo)

    return notas


def salvar_notas(notas: dict, vault_path: Path, dry_run: bool = False):
    """Salva cada nota como arquivo .md no vault do Obsidian."""
    vault_path.mkdir(parents=True, exist_ok=True)

    stats = {"criados": 0, "bytes": 0}

    for nome_arquivo, dados in notas.items():
        conteudo_completo = "\n\n---\n\n".join(dados["conteudo"])
        frontmatter = gerar_frontmatter(
            titulo=nome_arquivo.replace("-", " ").title(),
            tags=dados["tags"],
            secoes_incluidas=dados["titulos"]
        )
        texto_final = frontmatter + conteudo_completo

        caminho = vault_path / f"{nome_arquivo}.md"

        if dry_run:
            print(f"  [dry-run] Criaria: {caminho.name}  ({len(texto_final):,} chars, "
                  f"{len(dados['titulos'])} seções)")
        else:
            caminho.write_text(texto_final, encoding="utf-8")
            print(f"  ✅  {caminho.name}  ({len(texto_final):,} chars, "
                  f"{len(dados['titulos'])} seções)")
            stats["criados"] += 1
            stats["bytes"] += len(texto_final.encode("utf-8"))

    return stats


def gerar_indice(notas: dict, vault_path: Path, fonte: str):
    """Gera um arquivo INDEX.md com links para todas as notas criadas."""
    linhas = [
        "# 📚 Índice — Base de Conhecimento Fábrica",
        "",
        f"> Gerado automaticamente a partir de `{fonte}`  ",
        f"> Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "## Notas criadas",
        "",
    ]
    for nome, dados in sorted(notas.items()):
        titulo_legivel = nome.replace("-", " ").title()
        qtd = len(dados["titulos"])
        tags = ", ".join(f"`{t}`" for t in dados["tags"])
        linhas.append(f"- [[{nome}]] — {qtd} seção(ões) · {tags}")

    linhas += [
        "",
        "## Como usar no RAG",
        "",
        "1. Instale o plugin **Smart Connections** no Obsidian",
        "2. Ou rode o script `indexar_obsidian.py` para gerar embeddings no Chroma",
        "3. Configure `rag_buscar()` no seu MCP para consultar essa base",
        "",
        "## Tags disponíveis",
        "",
    ]

    todas_tags = sorted({t for d in notas.values() for t in d["tags"]})
    for tag in todas_tags:
        linhas.append(f"- `#{tag}`")

    indice_path = vault_path / "INDEX.md"
    indice_path.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  📋  INDEX.md criado em {indice_path}")


def gerar_script_indexacao(vault_path: Path):
    """Gera um script auxiliar para indexar o vault no Chroma (RAG)."""
    script = '''"""
indexar_obsidian.py
-------------------
Indexa as notas do Obsidian no ChromaDB para uso como RAG.
Chame este script sempre que atualizar notas no vault.

Instalar dependências:
    pip install chromadb sentence-transformers

Uso:
    python indexar_obsidian.py
"""

import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

VAULT_PATH = Path(__file__).parent  # mesma pasta do vault
CHROMA_PATH = Path(__file__).parent / ".chroma_db"
COLLECTION_NAME = "fabrica-knowledge"
CHUNK_SIZE = 600    # caracteres por chunk
CHUNK_OVERLAP = 100 # sobreposição entre chunks

def chunkar(texto: str, tamanho: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        chunks.append(texto[inicio:fim])
        inicio += tamanho - overlap
    return chunks

def main():
    print("🔍 Iniciando indexação do vault Obsidian...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")  # suporta PT-BR
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    arquivos_md = list(VAULT_PATH.glob("*.md"))
    arquivos_md = [f for f in arquivos_md if f.name != "INDEX.md"]

    total_chunks = 0
    for md_file in arquivos_md:
        texto = md_file.read_text(encoding="utf-8")
        chunks = chunkar(texto)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{md_file.stem}_{i}"
            embedding = model.encode(chunk).tolist()
            collection.upsert(
                documents=[chunk],
                embeddings=[embedding],
                ids=[chunk_id],
                metadatas=[{"arquivo": md_file.name, "chunk": i}]
            )

        total_chunks += len(chunks)
        print(f"  ✅  {md_file.name} → {len(chunks)} chunks")

    print(f"\\n🎉 Indexação concluída! {len(arquivos_md)} arquivos, {total_chunks} chunks.")
    print(f"   Base salva em: {CHROMA_PATH}")

if __name__ == "__main__":
    main()
'''
    script_path = vault_path / "indexar_obsidian.py"
    script_path.write_text(script, encoding="utf-8")
    print(f"  🛠️   indexar_obsidian.py gerado em {script_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Divide CLAUDE.md em notas temáticas para o Obsidian RAG"
    )
    parser.add_argument(
        "--input", "-i",
        default="CLAUDE.md",
        help="Caminho para o arquivo CLAUDE.md (padrão: CLAUDE.md)"
    )
    parser.add_argument(
        "--vault", "-v",
        default="./obsidian-vault/fabrica-knowledge",
        help="Pasta de destino no vault do Obsidian"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Mostra o que seria criado sem salvar nada"
    )
    parser.add_argument(
        "--sem-scripts", "-s",
        action="store_true",
        help="Não gera os scripts auxiliares (INDEX.md e indexar_obsidian.py)"
    )
    args = parser.parse_args()

    # Lê o arquivo de entrada
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌  Arquivo não encontrado: {input_path}")
        print("    Passe o caminho correto com --input caminho/para/CLAUDE.md")
        sys.exit(1)

    vault_path = Path(args.vault)

    print(f"""
╔══════════════════════════════════════════════════════╗
║   CLAUDE.md  →  Obsidian RAG  |  Fábrica de Software ║
╚══════════════════════════════════════════════════════╝
  Entrada : {input_path}
  Vault   : {vault_path}
  Dry-run : {args.dry_run}
""")

    conteudo = input_path.read_text(encoding="utf-8")
    print(f"📄  Arquivo lido: {len(conteudo):,} caracteres\n")

    secoes = dividir_por_secoes(conteudo)
    print(f"🔪  Seções encontradas: {len(secoes)}\n")

    notas = agrupar_em_notas(secoes)
    print(f"📁  Notas a criar: {len(notas)}\n")

    stats = salvar_notas(notas, vault_path, dry_run=args.dry_run)

    if not args.dry_run and not args.sem_scripts:
        print()
        gerar_indice(notas, vault_path, input_path.name)
        gerar_script_indexacao(vault_path)

    if not args.dry_run:
        print(f"""
✨  Concluído!
   • {stats['criados']} notas criadas
   • {stats['bytes'] / 1024:.1f} KB no total
   • Vault: {vault_path.resolve()}

Próximos passos:
  1. Abra a pasta '{vault_path}' no Obsidian como vault
  2. Instale o plugin Smart Connections para busca semântica imediata
  3. Ou rode: python {vault_path}/indexar_obsidian.py  (para usar com Chroma)
""")


if __name__ == "__main__":
    main()
