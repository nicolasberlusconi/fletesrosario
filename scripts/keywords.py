#!/usr/bin/env python3
"""Normaliza keywords, filtra las informativas para el blog y las agrupa en clusters.

Entrada: data/keywords-raw.csv (Google Ads Keyword Planner, Argentina, español) y,
opcionalmente, exports de Semrush en data/semrush-*.csv (columnas Keyword, Volume, KD %, Intent).
Salida: data/clusters.json. No toca data/used-keywords.json (eso lo marca el flujo de publicación).

Uso: python3 scripts/keywords.py [--min-vol 20] [--max-kd 30]
"""
import argparse, csv, glob, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Marcas de competidores y términos que nunca queremos atacar con contenido.
BRANDS = ["verga", "vergahnos", "lavaque", "mudadora", "july", "miranda", "abril", "premium",
          "neutral", "sbrizzi", "fletalo", "transportes argentinos", "mudanzas argentinas",
          "luis", "f44", "abacan", "mudanzas af", "expreso tas", "mudamos todo",
          "guardamuebles", "baulera"]  # guardamuebles: Mario no lo ofrece
EXCLUDE = [r"\ben ingles\b", r"\bcomo ser\b", r"\bconvertirse en\b", r"\btrabajo de\b",
           r"\bempleo\b", r"\bsueldo\b", r"\bsignificado\b", r"\bsinonimo\b"]
INFO = re.compile(r"\b(como|que|cuanto|cuantas|cual|checklist|lista|consejos|tips|guia|pasos|organizar|"
                  r"desinstalar|desinstala|trasladar|transportar|desarmar|mudarse|requisitos|tramite|cambio de domicilio|"
                  r"embalar|empacar|preparar|ideas|antes de|despues de|cuando|donde|requisitos|"
                  r"precio|precios|costo|cuesta|sale|presupuesto)\b")

# Temas: data/topics.json (editable). Cada keyword va al primer tema cuyo "pattern" matchea.
TOPICS = json.loads((DATA / "topics.json").read_text(encoding="utf-8"))


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().strip())
    return "".join(c for c in s if not unicodedata.combining(c))


def load():
    rows = {}
    raw = DATA / "keywords-raw.csv"
    if raw.exists():
        for r in csv.DictReader(raw.open()):
            k = norm(r["keyword"])
            rows[k] = dict(keyword=k, volume=int(r["volume"] or 0), kd=None,
                           competition=r.get("competition", ""), cpc_high=int(r.get("cpc_high") or 0))
    for f in glob.glob(str(DATA / "semrush-*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            k = norm(r.get("Keyword") or r.get("keyword", ""))
            if not k:
                continue
            kd = r.get("Keyword Difficulty") or r.get("KD %") or r.get("KD")
            vol = int(float(r.get("Volume") or r.get("Search Volume") or 0))
            cur = rows.setdefault(k, dict(keyword=k, volume=vol, kd=None, competition="", cpc_high=0))
            cur["volume"] = max(cur["volume"], vol)
            cur["kd"] = int(float(kd)) if kd not in (None, "", "n/a") else cur["kd"]
    return list(rows.values())


def keep(r, min_vol, max_kd):
    k = r["keyword"]
    if r["volume"] < min_vol or not INFO.search(k):
        return False
    if any(b in k for b in BRANDS) or any(re.search(p, k) for p in EXCLUDE):
        return False
    if r["kd"] is not None and r["kd"] > max_kd:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-vol", type=int, default=20)
    ap.add_argument("--max-kd", type=int, default=30)
    a = ap.parse_args()

    kws = [r for r in load() if keep(r, a.min_vol, a.max_kd)]
    used = set(json.loads((DATA / "used-keywords.json").read_text())) if (DATA / "used-keywords.json").exists() else set()
    clusters = []
    taken = set()
    for tp in TOPICS:
        slug, title, requires = tp["slug"], tp["title"], tp.get("requires_data", [])
        prefer = [tp["prefer"]] if tp.get("prefer") else []
        group = sorted([r for r in kws if r["keyword"] not in taken and re.search(tp["pattern"], r["keyword"])
                        and not (tp.get("exclude") and re.search(tp["exclude"], r["keyword"]))],
                       key=lambda r: -r["volume"])
        # La keyword "cabeza" del tema manda aunque una variante tenga más volumen.
        if prefer:
            head = [r for r in group if re.search(prefer[0], r["keyword"])]
            if head:
                group.remove(head[0]); group.insert(0, head[0])
        if not group:
            continue
        taken.update(r["keyword"] for r in group)
        clusters.append(dict(
            slug=slug, title=title, requires_data=requires, notes=tp.get("notes", ""),
            primary=group[0]["keyword"], primary_volume=group[0]["volume"],
            secondary=[r["keyword"] for r in group[1:9]],
            total_volume=sum(r["volume"] for r in group),
            used=group[0]["keyword"] in used,
        ))
    clusters.sort(key=lambda c: (bool(c["requires_data"]), -c["total_volume"]))
    (DATA / "clusters.json").write_text(json.dumps(clusters, ensure_ascii=False, indent=2))
    if not (DATA / "used-keywords.json").exists():
        (DATA / "used-keywords.json").write_text("[]")
    for c in clusters:
        flag = f" (necesita: {', '.join(c['requires_data'])})" if c["requires_data"] else ""
        print(f"{c['slug']:18s} {c['total_volume']:>5}/mes  primaria: {c['primary']}{flag}{'  [USADO]' if c['used'] else ''}")


if __name__ == "__main__":
    main()
