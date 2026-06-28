#!/usr/bin/env python3
"""
Divide sinaflor2/CLAUDE.md em notas temáticas em obsidian/fabrica/sinaflor/.
Copia PROJECT.md → obsidian/projetos/sinaflor-prd.md

Uso:
    python C:/Users/gusta/obsidian/dividir_sinaflor_claude.py
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from datetime import date

SRC_CLAUDE = Path("C:/Users/gusta/sinaflor2/CLAUDE.md")
SRC_PROJECT = Path("C:/Users/gusta/sinaflor2/PROJECT.md")
OUT_DIR = Path("C:/Users/gusta/obsidian/fabrica/sinaflor")
PRD_OUT = Path("C:/Users/gusta/obsidian/projetos/sinaflor-prd.md")

SECTION_FILES = {
    "REGRAS GERAIS": ("regras-gerais.md", ["sinaflor", "ibama", "legado", "regras"]),
    "FRONTEND — Angular 7.2": ("angular-frontend.md", ["sinaflor", "angular", "primeng", "frontend"]),
    "BACKEND — Java 11 / Spring Boot 2.2.7": ("spring-backend.md", ["sinaflor", "java", "spring", "jhipster", "backend"]),
    "TESTES — FRONTEND (Jasmine + Karma)": ("testes-frontend.md", ["sinaflor", "testes", "jasmine", "karma", "angular"]),
    "TESTES — BACKEND (JUnit 5 + Mockito)": ("testes-backend.md", ["sinaflor", "testes", "junit", "mockito", "java"]),
    "Mapeamento frontend ↔ backend": ("mapeamento-frontend-backend.md", ["sinaflor", "mapeamento", "api"]),
}


def split_h2_sections(text: str) -> dict[str, str]:
    parts: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            current = title
            parts[current] = [line]
        elif current:
            parts[current].append(line)
    return {k: "\n".join(v).strip() + "\n" for k, v in parts.items()}


def yaml_frontmatter(title: str, filename: str, tags: list[str]) -> str:
    tag_lines = "\n".join(f"  - {t}" for t in tags)
    return f"""---
tags:
{tag_lines}
fonte: sinaflor2/CLAUDE.md
atualizado_em: {date.today().isoformat()}
projeto: SINAFLOR2
links:
  - "[[../projetos/sinaflor-prd]]"
---

> **Agente Cursor — use MCP antes de codar**
>
> 1. MCP **fabrica-apps** — `rag_buscar("sinaflor {title.lower()}")` + `buscar_historico("sinaflor")`
> 2. Leia `obsidian/projetos/sinaflor-prd.md` para estrutura do monorepo
> 3. Projeto **legado** — não modernizar sem pedido explícito

# {title}

"""


def main():
    if not SRC_CLAUDE.exists():
        raise SystemExit(f"Não encontrado: {SRC_CLAUDE}")

    raw = SRC_CLAUDE.read_text(encoding="utf-8")
    # Remove cabeçalho introdutório (antes do primeiro ##)
    intro_end = raw.find("\n## ")
    body = raw[intro_end + 1 :] if intro_end >= 0 else raw
    sections = split_h2_sections(body)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for title, (fname, tags) in SECTION_FILES.items():
        content = sections.get(title)
        if not content:
            print(f"⚠️  Seção ausente: {title}")
            continue
        # Remove duplicate ## title line — frontmatter já tem título
        content_lines = content.splitlines()
        if content_lines and content_lines[0].startswith("## "):
            content_body = "\n".join(content_lines[1:]).strip()
        else:
            content_body = content.strip()

        out = OUT_DIR / fname
        out.write_text(
            yaml_frontmatter(title, fname, tags) + content_body + "\n",
            encoding="utf-8",
        )
        written.append(fname)
        print(f"✅ {fname}")

    # INDEX da pasta sinaflor
    index = f"""---
tags:
  - sinaflor
  - index
  - fabrica
atualizado_em: {date.today().isoformat()}
---

# SINAFLOR2 — Base de conhecimento (fábrica)

> Monorepo: `C:/Users/gusta/sinaflor2` · PRD: [[../projetos/sinaflor-prd]]

## Notas (CLAUDE.md dividido)

| Nota | Conteúdo |
|------|----------|
| [[regras-gerais]] | Legado, o que não fazer |
| [[angular-frontend]] | Angular 7.2, PrimeNG, RxJS, HTTP |
| [[spring-backend]] | Java 11, Spring Boot 2.2, JPA, Jasper |
| [[testes-frontend]] | Jasmine + Karma |
| [[testes-backend]] | JUnit 5 + Mockito |
| [[mapeamento-frontend-backend]] | Services ↔ Resources |

## Atualizar

Após mudar padrões no repo: editar notas aqui + `python C:/Users/gusta/obsidian/indexar_rapido.py`
"""
    (OUT_DIR / "INDEX.md").write_text(index, encoding="utf-8")
    print("✅ INDEX.md")

    if SRC_PROJECT.exists():
        prd_body = SRC_PROJECT.read_text(encoding="utf-8")
        prd = f"""---
tags:
  - sinaflor
  - prd
  - ibama
fonte: sinaflor2/PROJECT.md
atualizado_em: {date.today().isoformat()}
projeto: SINAFLOR2
links:
  - "[[../fabrica/sinaflor/INDEX]]"
---

> **PRD SINAFLOR2** — espelho de `sinaflor2/PROJECT.md`. Atualize aqui e no repo ao mudar arquitetura.

{prd_body}
"""
        PRD_OUT.parent.mkdir(parents=True, exist_ok=True)
        PRD_OUT.write_text(prd, encoding="utf-8")
        print(f"✅ {PRD_OUT.name}")

    print(f"\nPronto: {len(written)} notas em {OUT_DIR}")


if __name__ == "__main__":
    main()
