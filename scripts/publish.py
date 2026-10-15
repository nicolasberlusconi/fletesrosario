#!/usr/bin/env python3
"""Puerta de publicación: valida, construye, audita y registra. No hace git push (lo hace el flujo que lo llama).

  python3 scripts/publish.py blog <slug>       # artículo en content/blog/<slug>.json
  python3 scripts/publish.py service <slug>    # página en content/services/<slug>.json
  python3 scripts/publish.py --check-only blog <slug>   # valida sin registrar

Reglas (data/config.json): máximo max_per_day publicaciones por día; tope de service_cap páginas de servicio.
Si algo falla, sale con código 1 y no registra nada.
"""
import datetime
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def fail(msg):
    print("❌", msg)
    sys.exit(1)


def words(html):
    return re.findall(r"[a-záéíóúñü0-9]+", unescape(re.sub(r"<[^>]+>", " ", html)).lower())


def strip_accents(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def check_post(d):
    errs = []
    body = d["body_html"]
    pk = strip_accents(d["primary"])
    if len(d["meta_title"]) > 60: errs.append(f"meta_title de {len(d['meta_title'])} caracteres (máx 60)")
    if len(d["meta_desc"]) > 155: errs.append(f"meta_desc de {len(d['meta_desc'])} caracteres (máx 155)")
    if pk not in strip_accents(d["h1"]): errs.append("la keyword principal no está en el H1")
    if pk not in strip_accents(d["meta_title"]): errs.append("la keyword principal no está en el meta title")
    if pk.replace(" ", "-") not in d["slug"]: errs.append("la keyword principal no está en el slug")
    first100 = " ".join(words(d["answer_html"] + " " + body)[:100])
    if pk not in strip_accents(first100): errs.append("la keyword principal no aparece en las primeras 100 palabras")
    n_words = len(words(d["answer_html"] + body)) + sum(len(words(q + " " + a)) for q, a in d["faqs"])
    if n_words < 1200: errs.append(f"solo {n_words} palabras (mín 1200)")
    internal = set(re.findall(r'href="(/[^"]*)"', body)) | {r[0] for r in d.get("related", [])}
    external = set(re.findall(r'href="(https?://[^"]*)"', body)) | {u for _, u in d.get("sources", [])}
    if not 3 <= len(internal) <= 6: errs.append(f"{len(internal)} links internos (3-5)")
    if not 2 <= len(external) <= 3: errs.append(f"{len(external)} links externos (2-3)")
    if not 4 <= len(d["faqs"]) <= 8: errs.append(f"{len(d['faqs'])} FAQs (4-8)")
    if not 2 <= len(d["images"]) <= 4: errs.append(f"{len(d['images'])} imágenes (2-4)")
    for im in d["images"]:
        if not im.get("alt") or not im.get("w") or not im.get("h"): errs.append(f"imagen sin alt/medidas: {im.get('file')}")
        if not (ROOT / "img" / "blog" / im["file"]).exists(): errs.append(f"imagen inexistente: {im['file']}")
    body_imgs = re.findall(r"<img [^>]*>", body)
    for tag in body_imgs:
        if 'loading="lazy"' not in tag or "width=" not in tag or "alt=" not in tag:
            errs.append(f"imagen del cuerpo sin lazy/width/alt: {tag[:60]}")
    if re.search(r"\bTODO\b", body): errs.append("el cuerpo tiene un TODO sin resolver")
    # Una secundaria cuenta como usada si todas sus palabras de contenido aparecen en un mismo
    # bloque (párrafo, título o ítem): así se acepta español natural ("embalar los platos para la mudanza").
    stop = {"para", "una", "un", "la", "el", "los", "las", "de", "del", "en", "y", "a", "al"}
    blocks = [strip_accents(unescape(re.sub(r"<[^>]+>", " ", b))) for b in re.split(r"</(?:p|h2|h3|li)>", body)]
    def used(kw):
        toks = [t for t in strip_accents(kw).split() if t not in stop]
        stems = [t[:-1] if t.endswith("s") else t for t in toks]
        return any(all(st in bl for st in stems) for bl in blocks)
    sec_used = [s for s in d["secondary"] if used(s)]
    if len(sec_used) < min(3, len(d["secondary"])):
        errs.append(f"solo {len(sec_used)} keywords secundarias cubiertas (mín 3)")
    print(f"   {n_words} palabras · {len(internal)} links internos · {len(external)} externos · "
          f"{len(d['faqs'])} FAQs · {len(d['images'])} imágenes · {len(sec_used)}/{len(d['secondary'])} secundarias cubiertas")
    return errs


def check_service(d, cfg):
    errs = []
    n_services = len(list((ROOT / "content" / "services").glob("*.json")))
    if n_services > cfg["service_cap"]: errs.append(f"{n_services} páginas de servicio superan el tope de {cfg['service_cap']}")
    local = d.get("local_elements", [])
    if d.get("loc") and len(local) < 3:
        errs.append(f"solo {len(local)} elementos locales documentados en local_elements (mín 3)")
    if len(d["meta_title"]) > 60: errs.append("meta_title > 60")
    if len(d["meta_desc"]) > 155: errs.append("meta_desc > 155")
    if not 4 <= len(d["faqs"]) <= 8: errs.append(f"{len(d['faqs'])} FAQs (4-8)")
    return errs


def run(script):
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT)
    return r.returncode == 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check-only" in sys.argv
    if len(args) != 2 or args[0] not in ("blog", "service"):
        fail(__doc__)
    kind, slug = args
    cfg = json.loads((DATA / "config.json").read_text())
    src = ROOT / "content" / ("blog" if kind == "blog" else "services") / f"{slug}.json"
    if not src.exists(): fail(f"no existe {src.relative_to(ROOT)}")
    d = json.loads(src.read_text(encoding="utf-8"))

    log_p = DATA / "publish-log.json"
    log = json.loads(log_p.read_text()) if log_p.exists() else []
    today = datetime.date.today().isoformat()
    if any(e["slug"] == slug and e["kind"] == kind for e in log):
        print(f"ℹ️  {kind}/{slug} ya estaba publicado: se trata como actualización")
    elif sum(1 for e in log if e["date"] == today) >= cfg["max_per_day"] and not check_only:
        fail(f"ya se publicaron {cfg['max_per_day']} páginas hoy ({today}); límite diario alcanzado")

    print(f"▶ Checklist {kind}/{slug}")
    errs = check_post(d) if kind == "blog" else check_service(d, cfg)
    if errs:
        for e in errs: print("❌", e)
        sys.exit(1)
    print("✓ Checklist OK\n▶ Build")
    if not run("build.py"): fail("build falló")
    print("▶ Auditoría")
    if not run("audit.py"): fail("la auditoría encontró errores")
    print("▶ Duplicados")
    if not run("dupcheck.py"): fail("hay páginas demasiado parecidas: reescribir antes de publicar")
    if check_only:
        print("\n✓ Todo OK (modo --check-only: no se registró nada)")
        return

    if not any(e["slug"] == slug and e["kind"] == kind for e in log):
        url = f"/blog/{slug}/" if kind == "blog" else f"/{d['file']}"
        log.append({"date": today, "kind": kind, "slug": slug, "url": url,
                    "primary": d.get("primary", d.get("h1"))})
        log_p.write_text(json.dumps(log, ensure_ascii=False, indent=2))
    if kind == "blog":
        used_p = DATA / "used-keywords.json"
        used = set(json.loads(used_p.read_text())) if used_p.exists() else set()
        used.update([d["primary"]] + d.get("secondary", []))
        used_p.write_text(json.dumps(sorted(used), ensure_ascii=False, indent=2))
    print(f"\n✓ {kind}/{slug} listo para publicar (registrado en data/publish-log.json)")


if __name__ == "__main__":
    main()
