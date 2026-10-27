# fletesrosario.ar — convenciones del proyecto

Web de **Fletes & Mudanzas Rosario** (negocio de Mario). Objetivo: leads de **mudanzas** en Rosario y zona.
Producción: https://www.fletesrosario.ar · repo `nicolasberlusconi/fletesrosario` · **push a `main` = deploy** (GitHub Pages, ~1 min). DNS y CDN en Cloudflare (cuenta nicolasberlusconi@gmail.com; la cuenta fletesmudanzasrosario@gmail.com está vacía).

**SSL de Cloudflare en "Full" (no strict), a propósito (27-oct-2026).** GitHub Pages no puede renovar su certificado Let's Encrypt con Cloudflare en modo proxy (queda en `bad_authz`); el 27-oct venció y con "Full (strict)" la web dio error 526 hasta pasar a "Full". No volver a "Full (strict)" sin antes tener un certificado válido en GitHub (`gh api repos/nicolasberlusconi/fletesrosario/pages --jq .https_certificate`).

## Arquitectura (decisión oct-2026)
- **HTML estático generado con Python, sin framework.** No se migra a Next.js/Vercel: el sitio ya da SEO 100 y hosting $0; un framework agrega peso de JS y riesgo sin ganar posiciones.
- `index.html` y `cotizador.html` se editan **a mano**.
- Todo lo demás se **genera**: `python3 scripts/build.py` lee `content/services/*.json` y `content/blog/*.json` y escribe las páginas, `/blog/`, `/servicios/`, `sitemap.xml` y la sección de páginas de `llms.txt`. **Nunca editar a mano un HTML generado**: se pisa en el próximo build.
- Plantillas en `scripts/templates.py` (CSS, header, footer, GA4, schema). Rutas de assets absolutas (`/img/...`).
- **Borradores**: `content/drafts/{services,blog}/` no se generan ni se publican. Para publicar, mover el JSON a `content/services/` o `content/blog/` y correr `publish.py` (así se respeta `max_per_day` sin perder el trabajo).
- URLs: servicios en la raíz (`/mudanzas-funes.html`, ya indexadas, no cambiarlas); blog en `/blog/<slug>/`.

## Tracking (no romper)
- GA4 `G-K1YYD5M4XR` + Google Ads `AW-881512631`, cargados diferido: **2 s después del load o al primer toque/tecla** (patrón en `templates.GTAG`, igual en index y cotizador). Cargarlo antes demora el pintado de la foto principal (LCP 5,5 s → 2,9 s al retrasarlo). Las conversiones no se pierden porque el click carga el script.
- PageSpeed (15-oct-2026): home 95/100/100/100, artículo 95-100/100/100/100, servicio 86/100/100/100. El techo de rendimiento es el bloqueo del script de Google (~300 ms de TBT): no se puede sacar sin perder la medición de conversiones.
- Conversión `lead_mudanza` = `AW-881512631/D-NvCKS-sIAdELehq6QD`: se dispara en clicks a `wa.me` y al enviar el cotizador. Toda página nueva debe incluir `templates.TRACK`.

## Scripts
| Script | Para qué |
|---|---|
| `scripts/keywords.py` | Normaliza `data/keywords-raw.csv` (Google Ads Keyword Planner, AR, español) + `data/semrush-*.csv` si existen; filtra informativas; agrupa por `data/topics.json` → `data/clusters.json` |
| `scripts/build.py` | Genera páginas, índices, sitemap y llms.txt |
| `scripts/audit.py` | 1 H1, title ≤60, description ≤155, canonical, JSON-LD válido, imágenes, links rotos, huérfanas, sitemap completo. Sale 1 si hay errores |
| `scripts/dupcheck.py` | Similitud de texto entre páginas (shingles de 5 palabras). Umbral 60% |
| `scripts/indexnow.py [url ...]` | Avisa a Bing/IndexNow de URLs nuevas o cambiadas (sin argumentos: todo el sitemap). Correr **después** del deploy. La clave es el archivo `<32 hex>.txt` de la raíz: no borrarlo ni renombrarlo |
| `scripts/publish.py blog\|service <slug>` | Puerta de publicación: checklist on-page + build + audit + dupcheck + límite diario + registro en `data/publish-log.json` + marca keywords usadas |

## Reglas de contenido
- **Nunca inventar datos**: precios, cantidades, clientes, reseñas, plazos. Solo lo que está en `references/stats.md` y `references/stories.md`, o datos de terceros **con fuente citada**. Si falta un dato, el tema no se escribe (por eso `topics.json` tiene `requires_data`).
- Voz: `references/voice.md` (rioplatense con voseo, directo, concreto). Opiniones reales: `references/opinions.md`.
- No mencionar la cantidad de reseñas de Google (cambia). Sí "4.7★ en Google".
- La empresa **no ofrece** embalaje completo, venta de cajas ni guardamuebles. Sí: desarme/armado, desinstalación/instalación de lavarropas y aires, izamiento.
- **No hay lista de precios**: todo se cotiza a medida. Nunca publicar montos, rangos, precio por hora o por km. Los artículos de "cuánto cuesta" explican qué define el precio y llevan al cotizador.
- Historias: solo lo que cada cliente escribió en su reseña real (ver regla en `references/stories.md`). Escenas inventadas solo como ejemplo explícito y sin nombre de cliente.
- Sin links pagos ni intercambiados.

## Checklist de un artículo (lo valida `publish.py`)
Keyword principal en H1, slug, meta title y primeras 100 palabras · meta title ≤60 · description ≤155 · ≥1200 palabras · 3-5 links internos · 2-3 externos de autoridad · 4-8 FAQs (schema FAQPage) · 2-4 imágenes de Pexels con alt, width/height, lazy y crédito · ≥3 keywords secundarias cubiertas · sin TODOs.
Antes de escribir: análisis de los 3 primeros resultados orgánicos en google.com.ar → `data/serp/<slug>.json`, y agregar al menos 2 cosas que no tengan.

## Páginas de servicio
- Tope `data/config.json → service_cap` (10). Solo crear una página si tiene ≥3 elementos locales reales (documentarlos en `local_elements`). Si no, se lista y se saltea.
- No crear páginas de "fletes" chicos: Mario solo quiere mudanzas.

## Semrush
Proyecto `www.fletesrosario.ar` (Site Audit id 31613167). La API/MCP no tiene unidades: consultar por la web en Chrome. Los "links externos rotos" a wa.me (HTTP 429) son falsos positivos. El email va envuelto en `<!--email_off-->` para que Cloudflare no lo ofusque (generaba un 404 en `/cdn-cgi/l/email-protection`). Snapshot de competencia, brecha de keywords y visibilidad en IA: `data/semrush-competencia-2026-10-15.md` (revisar una vez por trimestre). HSTS en Cloudflare: **apagado por decisión de Nico (15-oct-2026)**; el aviso "No HSTS support" de Semrush se ignora.

## Límites
- `data/config.json → max_per_day` (1 publicación por día).
- Imágenes: `~/.claude/skills/banco-imagenes/scripts/pexels.py`, convertir a WebP 960px (3:2) en `img/blog/`.
- Lighthouse local no corre en esta Mac (puppeteer no conecta con Chrome): medir con PageSpeed Insights sobre producción.

## Después de publicar
Commit + push a `main`, esperar el build de Pages, verificar la URL en producción (HTTP 200 + título) pedir indexación en Search Console (propiedad de dominio `fletesrosario.ar`) y correr `python3 scripts/indexnow.py <url>` (Bing, que es lo que usa ChatGPT para buscar).

## Visibilidad en IA
Bing Webmaster Tools: propiedad `https://www.fletesrosario.ar/` en la cuenta de Nico (existe desde 2023). Ahí está el reporte **AI Performance** (citas en Copilot) y el envío manual de URLs.
Los asistentes recomiendan negocios según fuentes externas (ficha de Google, Bing Places, directorios) tanto como por la web. `llms.txt` tiene el resumen del negocio y la lista de lo que NO se ofrece: mantenerla al día. `sameAs` del schema (home y `templates.ORG`) solo lleva perfiles propios del negocio: sumar cada directorio donde se dé de alta.
