# fletesrosario.ar — Web de Fletes & Mudanzas Rosario

Web estática (un solo `index.html`), hosteada gratis en **GitHub Pages**.

- **Preview:** https://nicolasberlusconi.github.io/fletesrosario/
- **Producción (cuando se delegue el dominio):** https://www.fletesrosario.ar/

## Cómo editar

Todo el sitio vive en `index.html` (HTML + CSS + JS en un archivo). Las imágenes están en `img/` (WebP optimizado) y la tipografía en `fonts/`.

Para publicar cambios:

```bash
git add -A && git commit -m "cambio" && git push
```

GitHub Pages redeploya solo en ~1 minuto.

## Cosas que NO hay que tocar (tracking de Google Ads)

- El tag de GA4 `G-K1YYD5M4XR` en el `<head>`: alimenta la conversión
  `lead_whatsapp` (clicks salientes a `wa.me`) que usa Google Ads para optimizar.
- Los links a `https://wa.me/5493413889017`: son el evento de conversión.
- La URL raíz `https://www.fletesrosario.ar/`: es la URL final de todos los anuncios.

## Lanzamiento (pendiente, se hace junto con Nico)

1. Crear archivo `CNAME` en la raíz del repo con el contenido `www.fletesrosario.ar` y pushear.
2. En el DNS del dominio (hoy en Wix): `www` CNAME → `nicolasberlusconi.github.io`,
   y apex `fletesrosario.ar` → A `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
3. En GitHub → Settings → Pages: custom domain `www.fletesrosario.ar` + Enforce HTTPS.
4. Verificar render en `https://www.fletesrosario.ar/` y recién después dar de baja el plan de Wix (no borrar el dominio si está registrado vía Wix).
