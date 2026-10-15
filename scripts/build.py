#!/usr/bin/env python3
"""Genera las páginas de servicio, el blog, los índices, sitemap.xml y la sección de páginas de llms.txt.

Fuente: content/services/*.json y content/blog/*.json. index.html y cotizador.html se editan a mano.
Uso: python3 scripts/build.py
"""
import datetime
import json
import re
import subprocess
from pathlib import Path

import templates as S  # scripts/templates.py

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_FROM_SITEMAP = {"404.html"}


def load(folder):
    items = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "content" / folder).glob("*.json"))]
    return items


def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return rel


def lastmod(rel):
    """Fecha del último commit que tocó el archivo; si no está commiteado, hoy."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        if out and not dirty:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()


def url_for(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def build_sitemap():
    pages = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
                   if ".git" not in p.parts and "node_modules" not in p.parts
                   and str(p.relative_to(ROOT)) not in EXCLUDE_FROM_SITEMAP)

    def prio(rel):
        return {"index.html": "1.0", "cotizador.html": "0.9"}.get(rel, "0.8" if rel.startswith("blog/") else "0.7")

    rows = "\n".join(f"  <url><loc>{S.SITE}{url_for(r)}</loc><lastmod>{lastmod(r)}</lastmod>"
                     f"<changefreq>monthly</changefreq><priority>{prio(r)}</priority></url>" for r in pages)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    return len(pages)


def build_llms(services, posts):
    p = ROOT / "llms.txt"
    txt = p.read_text(encoding="utf-8")
    lines = ["## Páginas", "",
             f"- [Inicio — Empresa de mudanzas en Rosario]({S.SITE}/): servicios, flota, opiniones, zonas de trabajo y preguntas frecuentes",
             f"- [Cotizador de mudanzas online]({S.SITE}/cotizador.html): cotizá tu mudanza en 6 pasos y recibí el presupuesto por WhatsApp",
             f"- [Servicios]({S.SITE}/servicios/): índice de servicios y zonas"]
    lines += [f"- [{s['h1']}]({S.SITE}/{s['file']}): {s['meta_desc']}" for s in services]
    if posts:
        lines += ["", "## Guías de mudanza", "", f"- [Índice de guías]({S.SITE}/blog/)"]
        lines += [f"- [{b['h1']}]({S.SITE}/blog/{b['slug']}/): {b['meta_desc']}" for b in posts]
    block = "\n".join(lines) + "\n"
    txt = re.sub(r"## Páginas\n.*?(?=\n## Opiniones)", block, txt, flags=re.S)
    p.write_text(txt, encoding="utf-8")


def main():
    services = sorted(load("services"), key=lambda s: s.get("order", 99))
    posts = sorted(load("blog"), key=lambda b: b["date"], reverse=True)
    out = []
    for s in services:
        out.append(write(s["file"], S.render_service(s)))
    for b in posts:
        out.append(write(f"blog/{b['slug']}/index.html", S.render_post(b)))
    out.append(write("blog/index.html", S.render_blog_index(posts)))
    out.append(write("servicios/index.html", S.render_services_index(services)))
    n = build_sitemap()
    build_llms(services, posts)
    print(f"Generadas {len(out)} páginas · sitemap con {n} URLs · llms.txt actualizado")
    for r in out:
        print("  ", r)


if __name__ == "__main__":
    main()
