#!/usr/bin/env python3
"""Auditoría técnica de todas las páginas: corre antes de cada publicación.

Chequea: un H1, title <= 60, description <= 155, canonical correcto, JSON-LD válido,
imágenes con alt/width/height y existentes, links internos sin romper, páginas huérfanas
y que el sitemap tenga todas las páginas. Sale con código 1 si hay errores.
Uso: python3 scripts/audit.py
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.fletesrosario.ar"
SKIP = {"404.html"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.title = ""; self.desc = None; self.canonical = None
        self.ld = []; self.links = []; self.imgs = []
        self._in_title = self._in_ld = False; self._buf = ""

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1": self.h1 += 1
        elif tag == "title": self._in_title = True
        elif tag == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        elif tag == "script" and a.get("type") == "application/ld+json": self._in_ld = True; self._buf = ""
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        elif tag == "img": self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False; self.ld.append(self._buf)

    def handle_data(self, d):
        if self._in_title: self.title += d
        if self._in_ld: self._buf += d


def url_of(rel):
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def resolve(href, rel):
    """Devuelve la ruta de archivo local para un link interno, o None si es externo."""
    href = href.split("#")[0].split("?")[0]
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
        if href.startswith(SITE): href = href[len(SITE):] or "/"
        else: return None
    if href.startswith("/"):
        path = href.lstrip("/")
    else:
        path = str((Path(rel).parent / href))
    if path == "" or path.endswith("/"): path += "index.html"
    return path


def main():
    pages = {str(p.relative_to(ROOT)): p for p in ROOT.rglob("*.html") if ".git" not in p.parts}
    sitemap = (ROOT / "sitemap.xml").read_text()
    errors, warns, inbound = [], [], {r: 0 for r in pages}
    for rel, p in sorted(pages.items()):
        if rel in SKIP: continue
        pg = Page(); pg.feed(p.read_text(encoding="utf-8"))
        tag = f"[{rel}]"
        if pg.h1 != 1: errors.append(f"{tag} tiene {pg.h1} H1 (debe ser 1)")
        if not pg.title: errors.append(f"{tag} sin <title>")
        elif len(pg.title) > 60: warns.append(f"{tag} title de {len(pg.title)} caracteres (>60): {pg.title}")
        if pg.desc is None: errors.append(f"{tag} sin meta description")
        elif len(pg.desc) > 155: warns.append(f"{tag} description de {len(pg.desc)} caracteres (>155)")
        if pg.canonical != SITE + url_of(rel): errors.append(f"{tag} canonical {pg.canonical} != {SITE + url_of(rel)}")
        for raw in pg.ld:
            try:
                obj = json.loads(raw)
                if "@context" not in obj or "@type" not in obj: errors.append(f"{tag} JSON-LD sin @context/@type")
            except json.JSONDecodeError as e:
                errors.append(f"{tag} JSON-LD inválido: {e}")
        if not pg.ld: warns.append(f"{tag} sin JSON-LD")
        for im in pg.imgs:
            src = im.get("src", "")
            if not im.get("alt") and im.get("alt") != "": errors.append(f"{tag} imagen sin alt: {src}")
            if not (im.get("width") and im.get("height")): warns.append(f"{tag} imagen sin width/height: {src}")
            local = resolve(src, rel)
            if local and not (ROOT / local).exists(): errors.append(f"{tag} imagen inexistente: {src}")
        for href in pg.links:
            local = resolve(href, rel)
            if local is None: continue
            if not (ROOT / local).exists(): errors.append(f"{tag} link roto: {href}")
            elif local != rel and local in inbound: inbound[local] += 1
        if f"{SITE}{url_of(rel)}</loc>" not in sitemap and rel != "404.html":
            errors.append(f"{tag} no está en sitemap.xml")
    for rel, n in inbound.items():
        if n == 0 and rel not in SKIP and rel != "index.html":
            errors.append(f"[{rel}] huérfana: ninguna página la enlaza")
    for w in warns: print("⚠️ ", w)
    for e in errors: print("❌", e)
    print(f"\n{len(pages) - len(SKIP)} páginas · {len(errors)} errores · {len(warns)} avisos")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
