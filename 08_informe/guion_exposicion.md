# Guion de exposición · Equipo 04 · PANVIZ IRAS

Unos 12 minutos de exposición y 5 de preguntas, con `Presentacion_Equipo04_PANVIZ.pptx` (21 diapositivas).

| Bloque | Diapositivas | Tiempo | Expone |
|---|---|---|---|
| Contexto y alcance | 1–5 | 1 min 30 s | Anthony |
| Proceso estándar | 6–8 | 2 min | Jael |
| Evidencia y evaluación | 9–12 | 2 min | Mario |
| Incremento, demo y pruebas | 13–18 | 4 min | Jael (13–14), Alexander (15–17), Mario (18) |
| Resultados y mejora | 19–20 | 1 min 30 s | Anthony |
| Cierre | 21 | 1 min | Alexander |

---

## Bloque 1 · Contexto y alcance (Anthony)

**1 · Portada.** Buenos días, somos el Equipo 04: Mario Champi, Jael Huarca, Alexander Villafuerte y yo, Anthony Chaisa. Presentamos la revisión SCAMPI de un piloto orientado a CMMI nivel 3, aplicado a PANVIZ, un sistema de vigilancia de Infecciones Respiratorias Agudas. Aclaramos desde el inicio que es una autoevaluación académica inspirada en SCAMPI C: no es oficial y no demuestra que PANVIZ sea nivel 3.

**2 · El problema.** El responsable de vigilancia recibe notificaciones de IRAS que no se pueden publicar tal como llegan: algunas sin establecimiento, otras repetidas o con fechas que no existen. Necesita ver casos confiables por distrito y por edad, sobre todo de niños menores de cinco años y adultos mayores. Trabajamos con 30 notificaciones sintéticas, 20 de nuestro trabajo anterior y 10 nuevas para incluir Caylloma; seis son inválidas a propósito.

**3 · Alcance.** De las 18 áreas de proceso de CMMI hasta el nivel 3 evaluamos seis: OPD, IPM, RD, RSKM, VER y VAL. El trabajo se dividió en dos flujos: uno que captura y valida los registros y otro que los consolida, los muestra y los publica.

**4 · Roles.** El enunciado pedía cinco roles y somos cuatro, así que Mario y yo compartimos el de evidencias y tablero. Cada uno revisa el trabajo de otro, en ciclo. Como todos somos autores, la independencia de la evaluación es limitada, y lo decimos.

**5 · Decisiones de la lectura.** De TMMi tomamos el tipo de evaluación *Evaluation*, que reemplaza a SCAMPI B y C y no da calificación, y el muestreo aleatorio: sorteamos ocho evidencias con una semilla fija para que se pueda repetir. De la nota del CMMI Institute aplicamos que una debilidad no se disfraza de oportunidad de mejora. Le paso la palabra a Jael.

## Bloque 2 · Proceso estándar (Jael)

**6 · Proceso PE-04.** Nuestro proceso tiene seis actividades: requisitos, riesgos, implementación, revisión, pruebas y cierre, cada una con un dueño y un revisor distinto. Usamos plantillas e identificadores para seguir todo desde el requisito hasta la acción. En git, la versión 1 es el "antes" y la versión 2 el "después".

**7 · Un estándar, dos flujos.** Aplicamos el mismo proceso a los dos flujos con una sola adaptación. En la captura no hay pantalla que validar con un usuario, porque el resultado se compara contra un cálculo hecho a mano. Por eso la validación con usuario se hace solo en la visualización, donde alguien decide si publica.

**8 · El proceso cambió.** Al probar la versión 1 encontramos dos fallas reales, y las dos tenían causa en el proceso: no obligaba a pensar qué pasa si un dato vuelve a llegar ni a revisar la seguridad de la pantalla. Por eso publicamos el proceso versión 2 con tres controles nuevos, registrando quién lo revisó y aprobó. Le paso la palabra a Mario.

## Bloque 3 · Evidencia y evaluación (Mario)

**9 · 24 criterios.** Para cada área preguntamos si el activo existe, si se aplicó, si otro integrante lo revisó y si hay mejora o seguimiento. Eso da 24 criterios: 15 evidenciados, 1 parcial y 8 sin evidencia, casi todos de revisión y validación con usuario, que dependen de la sesión del equipo.

**10 · Trazabilidad.** Un ejemplo de la cadena: el requisito R4 pide no duplicar datos; se mide con el criterio VER-C4, su evidencia es E16, lo prueban T05 y D01, generó el hallazgo H01 y terminó en la acción A01, ya cerrada. Los seis requisitos tienen su cadena completa.

**11 · Evidencias y muestra.** Indexamos 26 evidencias con archivo, versión, fecha, autor y revisor, y sorteamos ocho para la revisión cruzada. Las actas de la sesión aparecen como pendientes: preferimos mostrarlas así antes que presentar algo que no ocurrió.

**12 · Antes y después.** Con la misma muestra y las mismas reglas, los criterios evidenciados pasaron de 9 a 15 de 24, sobre todo por corregir las fallas y publicar el proceso v2. Ojo: un indicador en verde mide la preparación del piloto, no la madurez de una organización. Jael empieza la demostración.

## Bloque 4 · Incremento, demo y pruebas

**13 · El incremento (Jael).** Es un validador de importación con seis reglas, cada una en su propia función: campos obligatorios, fecha real, evento IRAS, grupo etario MINSA, distrito de Arequipa o Caylloma y fecha no futura, además del control de duplicados. Con las 30 notificaciones acepta 24 y rechaza 6, exactamente lo que calculamos a mano antes de programar.

**14 · Demo en vivo (Jael).** *(Hacer la demo de 1 minuto de abajo.)*

**15 · Publicación protegida (Alexander).** Solo el responsable de vigilancia puede publicar, y el permiso se revisa en el servidor, no solo en la pantalla. Como vimos, el digitador recibe "operación denegada" y el intento queda registrado. Las pruebas T07 y T08 lo comprueban. No hay inicio de sesión real, así que la protección es solo local.

**16 · Doce pruebas.** Diseñamos dos pruebas por cada característica de calidad de ISO 25010. Las diez automatizadas pasan en la versión 2. T09 y T10 miden a un usuario haciendo tareas en menos de 90 segundos y siguen sin ejecutar, así que no las contamos como aprobadas.

**17 · Dos fallas reales.** D01: si un registro ya aceptado volvía inválido en un lote corregido, se rechazaba pero se seguía contando; Cerro Colorado mostraba 4 casos en vez de 3. D02: si el archivo traía código HTML, la tabla de rechazados lo ejecutaba. Ambas se reprodujeron con pruebas que fallan en v1 y pasan en v2. Mario muestra el tablero.

**18 · Tablero en Grist (Mario).** Es el tablero de la evaluación en Grist Community, software libre. Las tablas de criterios, evidencias, pruebas y hallazgos están enlazadas y los indicadores son fórmulas. Los criterios evidenciados pasaron de 38 a 63 %, las pruebas ejecutadas de 75 a 83 % y las debilidades abiertas de 5 a 3. Anthony presenta los resultados.

## Bloque 5 · Resultados y mejora (Anthony)

**19 · Hallazgos.** Registramos seis debilidades, una fortaleza y una oportunidad de mejora. Tres debilidades ya están cerradas: las dos fallas y la falta de controles del proceso v1. Siguen abiertas la prueba que daba falsos positivos, que el proceso se usó un solo día y que usuario y revisores somos los mismos autores.

**20 · Plan de mejora.** A siete días, que otro integrante revise toda prueba nueva y repetir la validación con un usuario externo. A treinta días, aplicar el proceso v2 en un segundo proyecto. Para una adopción real faltaría usarlo varios ciclos y tener auditorías externas. Alexander cierra.

## Bloque 6 · Cierre (Alexander)

**21 · Limitaciones y conclusión.** Fue un solo equipo, en un solo día, evaluando su propio trabajo, con 30 registros sintéticos en una computadora local. Lo más valioso no fueron las pruebas que pasaron, sino las dos fallas que encontró la verificación, porque cambiaron el proceso y no solo el código. Muchas gracias, quedamos atentos a sus preguntas.

---

## Demo de 1 minuto (diapositiva 14)

**Antes de exponer:** ejecutar `./demo.sh` en `Equipo04_Panviz`, abrir la página **Tablero** en Grist y dejar el prototipo con el usuario **digitador01**. Si algo falla, seguir con las capturas de las diapositivas.

| Tiempo | Acción | Se dice |
|---|---|---|
| 0:00 | **Importar datos** | "Importamos las 30 notificaciones: acepta 24 y rechaza 6, cada una con su causa." |
| 0:10 | Distrito → **Majes**, luego **Todos** | "Majes, en Caylloma, tiene 3 casos, uno de un adulto mayor." |
| 0:20 | Fila 17 → **Corregir** → `CS Cerro Colorado` | "Llegó sin establecimiento; la corregimos y pasa a aceptados: ahora son 25." |
| 0:30 | **Publicar** (denegado) → **resp.vigilancia** → **Publicar** | "El digitador no puede publicar, el servidor lo bloquea; el responsable sí." |
| 0:45 | Alt+Tab a **Grist**, filtro Área **VER** | "Los indicadores son fórmulas, y desde cada criterio abrimos su evidencia." |

Al terminar, volver a PowerPoint en la diapositiva 15.

---

## Preguntas probables

**¿Demuestra que PANVIZ es nivel 3?** No. Es una autoevaluación de seis de las 18 áreas, y el nivel 3 exige procesos sostenidos en toda una organización.

**¿Por qué no indujeron una falla?** El enunciado lo pide solo si todas las pruebas pasan, y nosotros encontramos dos fallas reales.

**¿Por qué T09 y T10 no están ejecutadas?** Necesitan a una persona haciendo las tareas mientras se mide el tiempo; preferimos dejarlas pendientes antes que inventar tiempos.

**¿Verificación o validación?** Verificación es comprobar que construimos lo especificado; validación, que le sirve al usuario para decidir si publica.

**¿Por qué Grist?** Es libre, funciona sin cuenta en la computadora y sus indicadores son fórmulas que se pueden recalcular.
