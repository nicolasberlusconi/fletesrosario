# -*- coding: utf-8 -*-
"""Plantillas compartidas de las páginas generadas (servicios, blog e índices).

La home (index.html) y el cotizador (cotizador.html) se editan a mano; todo lo demás
se genera con scripts/build.py a partir de content/. Las rutas de assets son absolutas
("/img/...") para que funcionen a cualquier profundidad (/blog/<slug>/).
"""
import html
import json

SITE = "https://www.fletesrosario.ar"
BRAND = "Fletes & Mudanzas Rosario"
PHONE = "+5493413889017"
WA = "https://wa.me/5493413889017?text=Hola%2C%20quiero%20cotizar%20una%20mudanza."
GMAPS = ("https://www.google.com/maps/place/Fletes+Mudanzas+Rosario/@-32.908093,-60.6858341,17z/"
         "data=!4m8!3m7!1s0x95b6536591fc4619:0x755a717d0d95259d!8m2!3d-32.908093!4d-60.6858341!9m1!1b1!16s%2Fg%2F11byyk95l6")

ORG = {
    "@type": "MovingCompany", "@id": f"{SITE}/#negocio", "name": BRAND, "url": f"{SITE}/",
    "telephone": PHONE, "logo": f"{SITE}/img/logo.png",
    "address": {"@type": "PostalAddress", "streetAddress": "José C. Paz 767", "addressLocality": "Rosario",
                "addressRegion": "Santa Fe", "postalCode": "S2000", "addressCountry": "AR"},
    "sameAs": ["https://www.google.com/maps/place/Fletes+Mudanzas+Rosario/@-32.908093,-60.6858341,17z/data=!3m1!4b1!4m6!3m5!1s0x95b6536591fc4619:0x755a717d0d95259d!8m2!3d-32.908093!4d-60.6858341!16s%2Fg%2F11byyk95l6", "https://www.facebook.com/fletesmudanzasrosario/"],
}

CSS = """
@font-face{font-family:'Manrope';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/manrope-latin.woff2') format('woff2')}
:root{--navy:#12314e;--navy-2:#0c2439;--blue:#2268a9;--blue-l:#3d85c6;--sky:#eaf3fb;--red:#e6394a;--wa:#0d8140;--wa-d:#0a6b35;--ink:#1d2b3a;--mut:#5a6b7d;--line:#dde7f0;--bg:#f6f9fc;--card:#fff;--r:18px;--shadow:0 10px 30px rgba(18,49,78,.10)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Manrope',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}a{color:var(--blue);text-decoration:none}
.wrap{max-width:860px;margin:0 auto;padding:0 18px}
header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;gap:10px;height:58px}
.brand{display:flex;align-items:center;gap:8px;font-weight:800;color:var(--navy);font-size:14px;line-height:1.1;white-space:nowrap}
.brand img{width:32px;height:auto}
.nav .sp{margin-left:auto}
.nav .lnk{font-weight:700;font-size:14px;color:var(--ink);display:none}
@media(min-width:700px){.nav .lnk{display:inline}}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-weight:800;font-size:15px;border-radius:13px;padding:13px 20px;border:0;cursor:pointer;font-family:inherit}
.btn-blue{background:var(--blue);color:#fff;box-shadow:0 6px 18px rgba(34,104,169,.3)}
.btn-blue:hover{background:#1b568c;color:#fff}
.btn-wa{background:var(--wa);color:#fff;box-shadow:0 6px 18px rgba(13,129,64,.35)}
.btn-wa:hover{background:var(--wa-d);color:#fff}
.nav .btn{padding:9px 15px;font-size:14px}
.hero{padding:34px 0 10px}
.kicker{display:inline-block;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);margin-bottom:8px}
h1{font-size:clamp(27px,5.5vw,40px);line-height:1.12;letter-spacing:-.02em;color:var(--navy);margin-bottom:12px}
.lead{color:var(--mut);font-size:16.5px;max-width:640px}
.ctas{display:flex;flex-wrap:wrap;gap:11px;margin:20px 0 6px}
.badges{font-size:13px;color:var(--mut);margin-top:10px}
.heroimg{border-radius:18px;margin:22px 0 6px;width:100%;height:auto}
section{padding:26px 0}
h2{font-size:clamp(21px,4vw,27px);letter-spacing:-.015em;color:var(--navy);margin-bottom:10px}
h3{color:var(--navy)}
p+p{margin-top:10px}
.cards{display:grid;gap:14px;grid-template-columns:1fr;margin-top:16px}
@media(min-width:680px){.cards{grid-template-columns:1fr 1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px;box-shadow:0 4px 14px rgba(18,49,78,.05);display:block}
.card h3{font-size:16px;color:var(--navy);margin-bottom:5px}
.card p{font-size:14px;color:var(--mut)}
a.card:hover{border-color:var(--blue-l)}
ul.checks{list-style:none;margin-top:12px}
ul.checks li{padding:7px 0 7px 28px;position:relative;font-size:15px}
ul.checks li::before{content:"✓";position:absolute;left:0;color:var(--wa);font-weight:800}
.faq details{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:9px;overflow:hidden}
.faq summary{cursor:pointer;padding:15px 44px 15px 17px;font-weight:800;font-size:15px;color:var(--navy);list-style:none;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:16px;top:50%;transform:translateY(-50%);font-size:21px;color:var(--blue)}
.faq details[open] summary::after{content:"−"}
.faq details p{padding:0 17px 15px;font-size:14px;color:var(--mut)}
.cta-final{background:linear-gradient(120deg,var(--navy) 0%,#17456e 100%);border-radius:22px;color:#fff;padding:30px 24px;text-align:center;margin:10px 0 34px}
.cta-final h2{color:#fff}
.cta-final p{color:#b9d2e8;font-size:14.5px;max-width:520px;margin:6px auto 18px}
.cta-final .ctas{justify-content:center;margin:0}
footer{background:var(--navy-2);color:#b9d2e8;padding:26px 0 90px;font-size:13.5px;text-align:center}
footer a{color:#dbe9f7;font-weight:700}
footer nav{margin-bottom:8px;display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center}
.sticky-cta{position:fixed;bottom:0;left:0;right:0;z-index:60;display:flex;gap:9px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
.sticky-cta .btn{flex:1;padding:13px 8px;font-size:14.5px}
@media(min-width:900px){.sticky-cta{display:none}footer{padding-bottom:26px}}
.crumbs{font-size:12.5px;color:var(--mut);padding-top:14px}
.crumbs a{font-weight:700}
/* Artículos del blog */
.meta{font-size:13px;color:var(--mut);margin-top:6px}
.answer{background:var(--sky);border-left:4px solid var(--blue);border-radius:12px;padding:16px 18px;margin:18px 0 4px;font-size:16px}
.prose{font-size:16.5px}
.prose h2{margin-top:34px}
.prose h3{font-size:18px;margin:22px 0 6px}
.prose p,.prose ul,.prose ol{margin-top:12px}
.prose ul,.prose ol{padding-left:22px}
.prose li{margin:6px 0}
.prose figure{margin:24px 0}
.prose figure img{border-radius:14px;width:100%;height:auto}
.prose figcaption{font-size:12.5px;color:var(--mut);margin-top:6px}
.tip{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-top:16px}
.tip b:first-child{color:var(--navy)}
.toc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-top:20px;font-size:14.5px}
.toc ol{padding-left:20px;margin-top:6px}
.toc li{margin:0}
.toc a{display:inline-block;padding:9px 0;min-height:24px}
.prose a,ul.checks a,.sources a,.tip a,.card p a{text-decoration:underline;text-underline-offset:2px}
.sources{font-size:13px;color:var(--mut)}
.sources li{margin:4px 0}
"""

GTAG = """<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-K1YYD5M4XR');
gtag('config', 'AW-881512631');
(function(){var done=false;function load(){if(done)return;done=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-K1YYD5M4XR';document.head.appendChild(s);}
// 2 s después del load para no frenar el pintado de la foto principal (LCP); cualquier interacción lo carga en el acto.
if(document.readyState==='complete'){setTimeout(load,2000);}else{window.addEventListener('load',function(){setTimeout(load,2000);});}
['pointerdown','keydown','touchstart'].forEach(function(ev){window.addEventListener(ev,load,{once:true,passive:true});});})();
</script>"""

TRACK = """<script>
// Conversión lead_mudanza en clicks directos a WhatsApp (misma lógica que la home)
document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('a[href^="https://wa.me/"]');
  if (!a || typeof gtag !== 'function') return;
  gtag('event', 'click', { link_domain:'wa.me', link_url:a.href, outbound:true, event_source:'PAGEKEY' });
  gtag('event', 'conversion', { send_to: 'AW-881512631/D-NvCKS-sIAdELehq6QD' });
  gtag('event', 'lead_mudanza', { event_source: 'PAGEKEY' });
});
document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('a[href="/cotizador.html"]');
  if (!a || typeof gtag !== 'function') return;
  gtag('event', 'cotizador_click', { event_source: 'PAGEKEY' });
});
</script>"""

WAICON = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.6-6.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.4-3c-.3-.4 0-.5.1-.7l.4-.5c.1-.2.2-.3.3-.5v-.5L9.6 7.2c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.9.9-1.2 2.1-.6 3.4a11.6 11.6 0 0 0 4.5 4.7c1.6.9 2.7 1.1 3.6 1 .6-.1 1.5-.5 1.8-1.1.2-.5.2-1 .1-1.1-.1-.2-.3-.2-.6-.3z"/></svg>')

esc = html.escape


def ld(obj):
    obj = dict(obj)
    obj.setdefault("@context", "https://schema.org")
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def faq_ld(faqs):
    return ld({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})


def breadcrumb_ld(items):
    return ld({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{u}"} for i, (n, u) in enumerate(items)]})


def head(title, desc, path, schemas, og_image="/img/og-image.jpg", og_type="website", preload_img=None, preload_srcset=None):
    url = f"{SITE}{path}"
    pre = ""
    if preload_img:
        extra = f' imagesrcset="{preload_srcset}" imagesizes="(max-width: 520px) 100vw, 820px"' if preload_srcset else ""
        pre = f'<link rel="preload" as="image" href="{preload_img}"{extra} fetchpriority="high">\n'
    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#12314e">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="/fonts/manrope-latin.woff2" crossorigin>
{pre}{GTAG}
<style>{CSS}</style>
{chr(10).join(schemas)}
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="brand" href="/"><img src="/img/logo-80.webp" alt="{esc(BRAND)}" width="32" height="40"><span>Fletes &amp; Mudanzas<br>ROSARIO</span></a>
    <span class="sp"></span>
    <a class="lnk" href="/servicios/">Servicios</a>
    <a class="lnk" href="/blog/">Guías</a>
    <a class="btn btn-blue" href="/cotizador.html">Cotizar</a>
  </div>
</header>
"""


def ctas(primary="Cotizar mi mudanza →"):
    return f"""<div class="ctas">
      <a class="btn btn-blue" href="/cotizador.html">{primary}</a>
      <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{WAICON} WhatsApp directo</a>
    </div>"""


def faq_html(faqs):
    items = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    return f'<section class="faq">\n<h2>Preguntas frecuentes</h2>\n{items}\n</section>'


def cta_final():
    return f"""<div class="cta-final">
    <h2>Cotizá gratis, sin compromiso</h2>
    <p>Contanos tu mudanza en el cotizador online (2 minutos) o escribinos directo. Te respondemos en el día con precio cerrado.</p>
    <div class="ctas">
      <a class="btn btn-blue" href="/cotizador.html">Ir al cotizador →</a>
      <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{WAICON} WhatsApp</a>
    </div>
  </div>"""


def foot(pagekey):
    return f"""<footer>
  <div class="wrap">
    <nav><a href="/">Mudanzas en Rosario</a><a href="/servicios/">Servicios</a><a href="/blog/">Guías de mudanza</a><a href="/cotizador.html">Cotizador</a></nav>
    © <span id="y">2026</span> {esc(BRAND)} · <a href="tel:{PHONE}">341 388-9017</a>
  </div>
</footer>
<div class="sticky-cta">
  <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{WAICON} WhatsApp</a>
  <a class="btn btn-blue" href="/cotizador.html">Cotizar mudanza</a>
</div>
{TRACK.replace("PAGEKEY", pagekey)}
<script>document.getElementById('y').textContent=new Date().getFullYear();</script>
</body>
</html>
"""


# ---------------------------------------------------------------- servicios
def render_service(d):
    path = f"/{d['file']}"
    schema = ld({"@type": "Service", "name": d["schema_name"], "description": d["meta_desc"], "url": f"{SITE}{path}",
                 "serviceType": "Mudanzas", "areaServed": d["area"], "provider": ORG})
    crumbs = breadcrumb_ld([("Inicio", "/"), ("Servicios", "/servicios/"), (d["kicker"], path)])
    body = d["body_html"] if "body_html" in d else zone_body(d["intro2"], d["bloques"])
    srcset = (f'srcset="/img/{d["img_small"]} 480w, /img/{d["img"]} {d.get("img_w", 700)}w" sizes="(max-width: 520px) 100vw, 820px"'
              if d.get("img_small") else "")
    return (head(d["meta_title"], d["meta_desc"], path, [schema, faq_ld(d["faqs"]), crumbs],
                 preload_img=f"/img/{d['img']}",
                 preload_srcset=(f"/img/{d['img_small']} 480w, /img/{d['img']} {d.get('img_w', 700)}w" if d.get("img_small") else None))
            + f"""<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › <a href="/servicios/">Servicios</a> › {esc(d['kicker'])}</p>
  <div class="hero">
    <span class="kicker">{esc(d['kicker'])}</span>
    <h1>{esc(d['h1'])}</h1>
    <p class="lead">{esc(d['lead'])}</p>
    {ctas()}
    <p class="badges">★ 4.7 en Google · 20 años de experiencia · Cotización gratis en el día</p>
    <img class="heroimg" src="/img/{d['img']}" {srcset} alt="{esc(d['alt'])}" width="{d.get('img_w', 700)}" height="{d.get('img_h', 525)}" fetchpriority="high">
  </div>
  {body}
  {faq_html(d['faqs'])}
  {related(d.get('related', []))}
  {cta_final()}
</main>
""" + foot(d["pagekey"]))


def zone_body(intro2, bloques):
    cards = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in bloques)
    return f"""<section>
    <h2>Mudanzas de ida y de vuelta, todas las semanas</h2>
    <p>{esc(intro2)}</p>
    <div class="cards">{cards}</div>
  </section>
  <section>
    <h2>Qué incluye nuestro servicio</h2>
    <ul class="checks">
      <li><b>Mudanza completa con precio cerrado:</b> cargamos, trasladamos y descargamos todo, sin sorpresas.</li>
      <li><b>O solo camión y chofer</b>, si preferís cargar con tu gente.</li>
      <li><b>Desarme y armado de muebles</b>, y desinstalación/instalación de lavarropas y aires.</li>
      <li><b><a href="/izamiento-muebles-rosario.html">Izamiento por balcón</a></b> cuando algo no pasa por la escalera.</li>
      <li><b>Camión con caja cerrada</b>: tus cosas viajan protegidas, llueva o truene.</li>
    </ul>
  </section>"""


def related(links):
    if not links:
        return ""
    cards = "".join(f'<a class="card" href="{u}"><h3>{esc(t)}</h3><p>{esc(x)}</p></a>' for u, t, x in links)
    return f'<section><h2>También te puede servir</h2><div class="cards">{cards}</div></section>'


# ---------------------------------------------------------------- blog
def render_post(d):
    path = f"/blog/{d['slug']}/"
    img = d["images"][0]
    article = ld({"@type": "Article", "headline": d["h1"], "description": d["meta_desc"],
                  "image": f"{SITE}/img/blog/{img['file']}", "datePublished": d["date"],
                  "dateModified": d.get("updated", d["date"]), "inLanguage": "es-AR",
                  "mainEntityOfPage": f"{SITE}{path}",
                  "author": {"@type": "Organization", "name": BRAND, "url": f"{SITE}/"},
                  "publisher": ORG})
    crumbs = breadcrumb_ld([("Inicio", "/"), ("Guías", "/blog/"), (d["h1"], path)])
    toc = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in d.get("toc", []))
    toc_html = f'<nav class="toc" aria-label="Contenido"><b>En esta guía</b><ol>{toc}</ol></nav>' if toc else ""
    credits = "".join(
        f'<li>Foto: <a href="{im["photographer_url"]}" target="_blank" rel="noopener">{esc(im["photographer"])}</a> en Pexels</li>'
        for im in d["images"] if im.get("photographer"))
    sources = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in d.get("sources", []))
    hero = (f'<img class="heroimg" src="/img/blog/{img["file"]}" alt="{esc(img["alt"])}" '
            f'width="{img["w"]}" height="{img["h"]}" fetchpriority="high">')
    fecha = d.get("updated", d["date"])
    return (head(d["meta_title"], d["meta_desc"], path, [article, faq_ld(d["faqs"]), crumbs],
                 og_image=f"/img/blog/{img['file']}", og_type="article", preload_img=f"/img/blog/{img['file']}")
            + f"""<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › <a href="/blog/">Guías</a> › {esc(d['kicker'])}</p>
  <article>
    <div class="hero">
      <span class="kicker">{esc(d['kicker'])}</span>
      <h1>{esc(d['h1'])}</h1>
      <p class="meta">Por el equipo de {esc(BRAND)} · Actualizado el {fecha[8:10]}/{fecha[5:7]}/{fecha[:4]}</p>
      <div class="answer">{d['answer_html']}</div>
      {hero}
    </div>
    {toc_html}
    <div class="prose">
{d['body_html']}
    </div>
    {faq_html(d['faqs'])}
    {'<section><h2>Fuentes</h2><ul class="sources">' + sources + '</ul></section>' if sources else ''}
    {'<section><ul class="sources">' + credits + '</ul></section>' if credits else ''}
  </article>
  {related(d.get('related', []))}
  {cta_final()}
</main>
""" + foot(f"blog_{d['slug']}"))


def render_blog_index(posts):
    path = "/blog/"
    cards = "".join(
        f'<a class="card" href="/blog/{p["slug"]}/"><h3>{esc(p["h1"])}</h3><p>{esc(p["meta_desc"])}</p></a>' for p in posts)
    schema = ld({"@type": "CollectionPage", "name": "Guías de mudanza", "url": f"{SITE}{path}",
                 "hasPart": [{"@type": "Article", "headline": p["h1"], "url": f"{SITE}/blog/{p['slug']}/"} for p in posts]})
    crumbs = breadcrumb_ld([("Inicio", "/"), ("Guías", path)])
    return (head("Guías de mudanza: consejos prácticos | Fletes Rosario",
                 "Guías prácticas para mudarte en Rosario: cómo embalar, el consorcio, los electrodomésticos y más. Escritas por quienes hacen mudanzas todos los días.",
                 path, [schema, crumbs])
            + f"""<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › Guías</p>
  <div class="hero">
    <span class="kicker">Guías de mudanza</span>
    <h1>Guías para mudarte sin dolores de cabeza</h1>
    <p class="lead">Lo que aprendimos en más de 20 años mudando casas y departamentos en Rosario, explicado para que lo apliques en tu mudanza.</p>
  </div>
  <section><div class="cards">{cards}</div></section>
  <section class="prose">
    <h2>Para qué sirven estas guías</h2>
    <p>Una mudanza sale bien cuando se prepara bien. En estas guías juntamos lo que vemos todas las semanas en casas y departamentos de Rosario: cómo embalar para que no se rompa nada, qué hacer con la heladera y el lavarropas, qué preguntar al consorcio antes del día y qué hacer cuando un mueble no entra en el ascensor.</p>
    <p>Son consejos prácticos, sin vueltas, escritos por el equipo que hace las mudanzas. Cuando citamos un dato técnico, como cuánto esperar para enchufar una heladera, dejamos la fuente del fabricante. Y si después de leerlas preferís que nos ocupemos nosotros, podés <a href="/cotizador.html">cotizar tu mudanza online</a>.</p>
  </section>
  {cta_final()}
</main>
""" + foot("blog_index"))


def render_services_index(services):
    path = "/servicios/"
    cards = "".join(
        f'<a class="card" href="/{s["file"]}"><h3>{esc(s["h1"])}</h3><p>{esc(s["meta_desc"])}</p></a>' for s in services)
    schema = ld({"@type": "CollectionPage", "name": "Servicios de mudanza", "url": f"{SITE}{path}", "about": ORG})
    crumbs = breadcrumb_ld([("Inicio", "/"), ("Servicios", path)])
    return (head("Servicios de mudanza en Rosario y zona | Fletes Rosario",
                 "Mudanzas integrales, izamiento de muebles y mudanzas a Funes, Roldán, Villa Gobernador Gálvez y San Lorenzo. Precio cerrado y equipo propio.",
                 path, [schema, crumbs])
            + f"""<main class="wrap">
  <p class="crumbs"><a href="/">Inicio</a> › Servicios</p>
  <div class="hero">
    <span class="kicker">Servicios</span>
    <h1>Servicios de mudanza en Rosario y zona</h1>
    <p class="lead">Mudanzas completas con precio cerrado, o solo camión y chofer. Desarme y armado de muebles, instalaciones e izamiento cuando algo no pasa por la escalera.</p>
    {ctas()}
  </div>
  <section><div class="cards">{cards}</div></section>
  <section>
    <h2>Dos formas de mudarte con nosotros</h2>
    <p><b>Mudanza completa:</b> nuestro equipo carga, traslada y descarga todo, con desarme y armado de muebles y desinstalación de lavarropas y aires si los necesitás. Es la opción para despreocuparte: te pasamos un precio cerrado y el día de la mudanza no hay sorpresas.</p>
    <p><b>Solo camión y chofer:</b> si preferís cargar y descargar con tu gente, ponemos el camión adecuado y el chofer. Ideal para mudanzas chicas o cuando ya tenés quien ayude.</p>
    <p>En los dos casos el precio se arma con tu inventario y los accesos de cada lugar (piso, ascensor, distancia del camión). Lo cargás en el <a href="/cotizador.html">cotizador online</a> en 2 minutos y te respondemos por WhatsApp en el día. Trabajamos en todos los barrios de Rosario y en Funes, Roldán, Villa Gobernador Gálvez, Granadero Baigorria, Capitán Bermúdez, San Lorenzo, Pérez y alrededores, y también hacemos mudanzas de larga distancia.</p>
  </section>
  {cta_final()}
</main>
""" + foot("servicios_index"))
