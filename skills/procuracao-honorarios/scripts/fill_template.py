#!/usr/bin/env python3
"""
Preenche um template .docx (com tokens {{CAMPO}}) com os dados de um cliente.

Uso:
    python3 fill_template.py --template modelo.docx --output final.docx \
        --field OUTORGANTE_NOME="RW SPORTS E EVENTOS LTDA" \
        --field OUTORGANTE_QUALIFICACAO="pessoa jurídica..." \
        --field REU="Natal/RN" \
        --field PERCENTUAL="25% (vinte e cinco por cento)" \
        --field DATA="07 de agosto de 2026"

Ou, com um JSON de dados:
    python3 fill_template.py --template modelo.docx --output final.docx --data dados.json

O script:
  1. Descompacta o .docx
  2. Substitui {{TOKEN}} pelo valor correspondente em todos os arquivos XML relevantes
     (document.xml, headers, footers) com o devido escape de caracteres XML
  3. Recompacta como um novo .docx válido
  4. Avisa se sobrar algum token {{...}} não preenchido, ou se algum campo passado
     não existir no template (sinal de erro de digitação)
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TOKEN_RE = re.compile(r"\{\{([A-Z_]+)\}\}")


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def find_xml_parts(unpacked_dir):
    parts = []
    word_dir = os.path.join(unpacked_dir, "word")
    if not os.path.isdir(word_dir):
        return parts
    for fname in os.listdir(word_dir):
        if fname == "document.xml" or fname.startswith("header") or fname.startswith("footer"):
            if fname.endswith(".xml"):
                parts.append(os.path.join(word_dir, fname))
    return parts


def fill(template_path: str, output_path: str, data: dict, strict: bool = True):
    tmp_dir = tempfile.mkdtemp(prefix="fill_template_")
    try:
        with zipfile.ZipFile(template_path) as zf:
            zf.extractall(tmp_dir)

        xml_parts = find_xml_parts(tmp_dir)
        if not xml_parts:
            raise RuntimeError(f"Não encontrei word/document.xml em {template_path} — é mesmo um .docx?")

        tokens_found = set()
        for part in xml_parts:
            with open(part, encoding="utf-8") as f:
                content = f.read()
            tokens_found |= set(TOKEN_RE.findall(content))
            for key, value in data.items():
                content = content.replace("{{%s}}" % key, xml_escape(str(value)))
            with open(part, "w", encoding="utf-8") as f:
                f.write(content)

        # Sanity checks
        unused_fields = set(data.keys()) - tokens_found
        remaining_tokens = set()
        for part in xml_parts:
            with open(part, encoding="utf-8") as f:
                remaining_tokens |= set(TOKEN_RE.findall(f.read()))

        if unused_fields:
            print(f"AVISO: campos passados que não existem neste template: {sorted(unused_fields)}", file=sys.stderr)
        if remaining_tokens:
            msg = f"AVISO: tokens não preenchidos no documento final: {sorted(remaining_tokens)}"
            if strict:
                raise RuntimeError(msg + " — corrija os dados antes de entregar o documento.")
            print(msg, file=sys.stderr)

        # Repack
        if os.path.exists(output_path):
            os.remove(output_path)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _dirs, files in os.walk(tmp_dir):
                for fname in files:
                    full = os.path.join(root, fname)
                    arcname = os.path.relpath(full, tmp_dir)
                    zf.write(full, arcname)

        return remaining_tokens
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", required=True, help="Caminho do template .docx com tokens {{CAMPO}}")
    parser.add_argument("--output", required=True, help="Caminho do .docx final a ser gerado")
    parser.add_argument("--field", action="append", default=[], metavar="CHAVE=VALOR",
                         help="Um campo a preencher (pode repetir). Ex: --field REU=\"Natal/RN\"")
    parser.add_argument("--data", help="Caminho de um JSON com os campos {chave: valor}")
    parser.add_argument("--allow-missing", action="store_true",
                         help="Não falhar se sobrar algum token {{...}} sem preencher")
    args = parser.parse_args()

    data = {}
    if args.data:
        with open(args.data, encoding="utf-8") as f:
            data.update(json.load(f))
    for item in args.field:
        if "=" not in item:
            parser.error(f"--field precisa ser CHAVE=VALOR, recebi: {item!r}")
        key, value = item.split("=", 1)
        data[key.strip()] = value

    remaining = fill(args.template, args.output, data, strict=not args.allow_missing)
    print(f"Gerado: {args.output}")
    if remaining:
        print(f"(gerado com tokens pendentes: {sorted(remaining)})")


if __name__ == "__main__":
    main()
