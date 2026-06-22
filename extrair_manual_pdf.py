
"""Extrai texto de um PDF e gera data/manual_credenciape_paginas.json.
Uso:
    python tools/extrair_manual_pdf.py caminho/do/manual.pdf
"""
import json
import re
import shutil
import sys
from pathlib import Path

from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

if len(sys.argv) < 2:
    print("Informe o caminho do PDF do manual.")
    raise SystemExit(1)

pdf_path = Path(sys.argv[1])
if not pdf_path.exists():
    print(f"PDF não encontrado: {pdf_path}")
    raise SystemExit(1)

reader = PdfReader(str(pdf_path))
pages = []
for idx, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s*\|\s*", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = text.strip()
    pages.append({"page": idx, "text": text})

with open(DATA_DIR / "manual_credenciape_paginas.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

shutil.copy(pdf_path, DATA_DIR / "manual_credenciape.pdf")
print(f"Manual extraído com {len(pages)} páginas.")
