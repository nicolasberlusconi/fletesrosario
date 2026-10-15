# Semrush — competencia, brecha de keywords y visibilidad en IA (15-oct-2026)

Base Argentina, consultado por la web (la API no tiene unidades).

## Competidores orgánicos
| Dominio | Keywords | Tráfico est. | Qué los mueve |
|---|---|---|---|
| rosariofletes.com | 58 | 591 | "fletes rosario" pos 1 y "fletes" pos 7 (14.800/mes). Casi todo fletes chicos: no es nuestro juego |
| mudanzasaba.com.ar | 72 | 336 | "mudanzas" (6.600/mes, KD 25) pos 7, "mudanzas rosario" pos 3, "empresas de mudanzas" pos 9, "servicio de mudanza" pos 8, "mudanzas larga distancia" pos 13, "mudanzas santa fe" pos 10. Todo con la home |
| mudateconabril.com.ar | 33 | 197 | Su marca + "mudanzas rosario" pos 7 + "empresas de mudanzas en rosario" pos 3 |
| fleteseym-rosario.com | 125 | 153 | "mudanzas rosario" pos 2, el resto fletes |

La brecha de keywords (Keyword Gap) no muestra filas en este plan; se reconstruyó leyendo las posiciones de cada competidor.

## Brecha útil (intención de mudanza, nosotros sin página)
| Keyword | Volumen | KD | Quién rankea | Acción |
|---|---|---|---|---|
| fletes larga distancia | 390 | 12 | rosariofletes 8 | Página /mudanzas-larga-distancia.html (borrador en content/drafts, sale 16-oct) |
| mudanzas larga distancia | 320 | 14 | mudanzasaba 13 | idem |
| mudanzas santa fe | 170 | 8 | mudanzasaba 10, abril 12 | idem (sección Santa Fe y Paraná) |
| mudanzas rosario buenos aires | 30 | 5 | mudanzasaba 2, abril 9 | idem |
| traslado de piano | 170 | s/d | — | Sección "Traslado de pianos" en /izamiento-muebles-rosario.html (15-oct) |
| empresas de mudanzas | 720 | 13 | mudanzasaba 9 | Ya en title/H1 de la home ("Empresa de Mudanzas en Rosario"); seguir |
| servicio de mudanza | 390 | 16 | mudanzasaba 8 | Home + /servicios/ |
| mudanzas | 6.600 | 25 | mudanzasaba 7 | Genérica nacional: solo con autoridad (reseñas, citations, links). No se fuerza |

Descartadas: fletes chicos/minifletes, marcas de otros (mudanzas abril, abad, july, pons), otras ciudades (Tucumán, Bahía Blanca, Venado Tuerto), "mudanzas compartidas" (Mario no lo ofrece, sin confirmar).

## Dificultad de los temas del blog (Keyword Overview, AR)
| Keyword | Volumen Semrush | KD |
|---|---|---|
| cambio de domicilio | 4.400 | 23 |
| como desinstalar aire acondicionado | 320 | s/d |
| como organizar una mudanza | 110 | 22 |
| cuanto sale una mudanza | 20 | s/d |

Todo por debajo del tope `max_kd` 30: los temas de `topics.json` siguen siendo alcanzables.

## Visibilidad en IA (AI Visibility)
- Puntaje 14/100 (bajo), 2 menciones (ChatGPT y AI Mode, ambas en Argentina), 5 citas, 1 página citada.
- Tema donde aparecemos: "Mudanzas y fletes en Rosario" (visibilidad 27).
- Fuentes que usan los asistentes al hablar de nosotros: fletesrosario.ar, google.com (ficha), fleteenrosario.com.ar y **dir.ar** (directorio). Conclusión: la ficha de Google y los directorios con datos consistentes pesan tanto como la web → ejecutar el kit de `fletes-gbp-kit/` (reseñas + citations).
