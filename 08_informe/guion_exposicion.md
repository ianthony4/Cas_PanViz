# Guion de exposición · Equipo 04 · PANVIZ IRAS

Unos 10 minutos y 5 de preguntas, con `Presentacion_Equipo04_PANVIZ.pptx` (21 diapositivas).

| Diapositivas | Expone |
|---|---|
| 1–5 | Anthony |
| 6–8 | Jael |
| 9–12 | Mario |
| 13–14 (demo) | Jael |
| 15–17 | Alexander |
| 18 | Mario |
| 19–20 | Anthony |
| 21 | Alexander |

---

**1 · Portada (Anthony).** Somos el Equipo 04 y presentamos la revisión SCAMPI de un piloto orientado a CMMI nivel 3 sobre PANVIZ, un sistema de vigilancia de IRAS. Es una autoevaluación académica, no una evaluación oficial.

**2 · El problema.** Las notificaciones de IRAS llegan con errores: sin establecimiento, repetidas o con fechas imposibles. Usamos 30 notificaciones sintéticas; 6 son inválidas a propósito.

**3 · Alcance.** Evaluamos 6 de las 18 áreas de CMMI: OPD, IPM, RD, RSKM, VER y VAL, en dos flujos: captura y visualización.

**4 · Roles.** Somos cuatro y cada uno revisa el trabajo de otro. Como todos somos autores, la independencia es limitada.

**5 · Lectura.** Seguimos el tipo de evaluación *Evaluation* de TMMi, sorteamos 8 evidencias con semilla fija y no disfrazamos debilidades como mejoras.

**6 · Proceso PE-04 (Jael).** Seis actividades, de requisitos a cierre, cada una con dueño y revisor. La versión 1 del código es el "antes" y la 2 el "después".

**7 · Adaptación.** El mismo proceso para los dos flujos; solo la validación con usuario se hace en visualización, donde alguien decide publicar.

**8 · El proceso cambió.** Las pruebas de la versión 1 hallaron dos fallas con causa en el proceso, así que publicamos el proceso v2 con tres controles nuevos.

**9 · Criterios (Mario).** 24 criterios: 15 evidenciados, 1 parcial y 8 pendientes, casi todos de la sesión con usuario.

**10 · Trazabilidad.** Ejemplo: requisito R4 → criterio VER-C4 → evidencia E16 → pruebas T05 y D01 → hallazgo H01 → acción A01, cerrada.

**11 · Evidencias.** 26 evidencias indexadas; las actas de la sesión figuran como pendientes, no inventadas.

**12 · Antes y después.** Los criterios evidenciados pasaron de 9 a 15. Un indicador en verde no significa nivel 3.

**13 · El incremento (Jael).** Un validador con seis reglas y control de duplicados: acepta 24 y rechaza 6, igual que el cálculo hecho a mano.

**14 · Demo en vivo (Jael).** Ver la demo de 1 minuto abajo.

**15 · Publicación protegida (Alexander).** Solo el responsable publica; el servidor bloquea al digitador y lo registra.

**16 · Doce pruebas.** Dos por cada característica de ISO 25010. Las diez automáticas pasan; T09 y T10 necesitan un usuario y siguen sin ejecutar.

**17 · Dos fallas.** D01: Cerro Colorado mostraba 4 casos en vez de 3. D02: la tabla ejecutaba código HTML. Ambas fallan en v1 y pasan en v2.

**18 · Tablero Grist (Mario).** Los indicadores son fórmulas: evidenciados de 38 a 63 % y debilidades abiertas de 5 a 3.

**19 · Hallazgos (Anthony).** Seis debilidades (tres cerradas), una fortaleza y una oportunidad de mejora.

**20 · Plan de mejora.** A 7 días, revisión de pruebas por otro integrante y validación con un usuario externo; a 30 días, usar el proceso v2 en otro proyecto.

**21 · Cierre (Alexander).** Fue un solo equipo, un día y datos sintéticos. Lo más valioso fueron las dos fallas, porque cambiaron el proceso y no solo el código. Gracias.

---

## Demo de 1 minuto (en la diapositiva 14)

**Antes:** ejecutar `./demo.sh` en `Equipo04_Panviz`, abrir la página **Tablero** en Grist y empezar con el usuario **digitador01**. Si algo falla, seguir con las capturas.

| Tiempo | Acción | Se dice |
|---|---|---|
| 0:00 | **Importar datos** | "Acepta 24 y rechaza 6." |
| 0:10 | Distrito → **Majes** | "Majes tiene 3 casos." |
| 0:20 | Fila 17 → **Corregir** → `CS Cerro Colorado` | "Corregido: ahora son 25." |
| 0:30 | **Publicar** (denegado) → **resp.vigilancia** → **Publicar** | "El digitador no puede publicar; el responsable sí." |
| 0:45 | Alt+Tab a **Grist** | "Los indicadores son fórmulas y muestran el antes y el después." |

---

## Preguntas probables

**¿Demuestra nivel 3?** No. Es una autoevaluación de 6 áreas, en un solo equipo.

**¿Por qué T09 y T10 no están ejecutadas?** Necesitan una persona midiendo tiempos; preferimos no inventarlos.

**¿Verificación o validación?** Verificación: cumple lo especificado. Validación: sirve al usuario para decidir si publica.
