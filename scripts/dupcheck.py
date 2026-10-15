#!/usr/bin/env python3
"""Detecta páginas con texto demasiado parecido (riesgo de contenido duplicado para Google).

Compara el texto visible dentro de <main> de cada par de páginas usando shingles de 5 palabras
(Jaccard). Marca los pares por encima del umbral. Sale con código 1 si hay alguno.
Uso: python3 scripts/dupcheck.py [--threshold 0.6]
"""
import argparse
import re
import sys
from html import unescape
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main_text(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    body = m.group(1) if m else html
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    text = unescape(re.sub(r"<[^>]+>", " ", body)).lower()
    return re.findall(r"[a-záéíóúñü0-9]+", text)


def shingles(words, k=5):
    return {" ".join(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.6)
    a = ap.parse_args()
    pages = {str(p.relative_to(ROOT)): shingles(main_text(p.read_text(encoding="utf-8")))
             for p in ROOT.rglob("*.html") if ".git" not in p.parts and p.name != "404.html"}
    worst = []
    for (r1, s1), (r2, s2) in combinations(sorted(pages.items()), 2):
        if not s1 or not s2: continue
        sim = len(s1 & s2) / len(s1 | s2)
        worst.append((sim, r1, r2))
    worst.sort(reverse=True)
    flagged = [w for w in worst if w[0] > a.threshold]
    print("Pares más parecidos:")
    for sim, r1, r2 in worst[:5]:
        print(f"  {sim:5.1%}  {r1}  ↔  {r2}{'   ❌ SUPERA EL UMBRAL' if sim > a.threshold else ''}")
    print(f"\n{len(flagged)} pares por encima de {a.threshold:.0%}")
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
