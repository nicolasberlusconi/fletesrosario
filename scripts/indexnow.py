"""Avisa a Bing (y a los buscadores que usan IndexNow) de páginas nuevas o cambiadas.

Uso: python3 scripts/indexnow.py [url ...]
Sin argumentos manda todas las URLs del sitemap. Correrlo DESPUÉS de que el deploy esté en producción.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "www.fletesrosario.ar"


def key():
    keys = [p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(keys) != 1:
        sys.exit(f"se esperaba exactamente 1 archivo de clave IndexNow en la raíz, hay {len(keys)}")
    return keys[0]


def main():
    urls = sys.argv[1:] or re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
    urls = [u if u.startswith("http") else f"https://{HOST}/{u.lstrip('/')}" for u in urls]
    k = key()
    body = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: HTTP {r.status} · {len(urls)} URLs enviadas")


if __name__ == "__main__":
    main()
