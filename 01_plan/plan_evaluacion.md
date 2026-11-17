# Plan de evaluación y muestra · Equipo 04 · PANVIZ IRAS

**Versión:** 1.0 · **Fecha:** 16/11/2026 · **Elaboró:** Anthony Chaisa (coordinación) · **Revisa:** Mario Champi

## 1. Propósito

Este plan organiza una autoevaluación académica inspirada en SCAMPI C sobre un piloto de adopción de procesos orientado a CMMI DEV v1.3 nivel 3. El objeto evaluado es el trabajo del equipo al construir un incremento pequeño de PANVIZ para la vigilancia de Infecciones Respiratorias Agudas (IRAS) en la Red Arequipa y la provincia de Caylloma, a partir del sistema y los datos sintéticos del trabajo anterior del equipo (Equipo04_Panviz_IRAS_CMMI). La evaluación busca saber qué tan bien el equipo define un proceso común, lo adapta a dos flujos de trabajo y lo sostiene con evidencia verificable. No es una evaluación oficial y no demuestra que PANVIZ alcance el nivel 3.

Para registrar la evaluación seguimos los elementos que pide ISO/IEC 33002: propósito, alcance, muestra, responsables, evidencias y resultados. Esta selección no declara conformidad completa con la norma.

## 2. Alcance

**Unidad organizativa:** el Equipo 04, que actúa como una pequeña organización con un proceso estándar común.

**Flujos evaluados:**

| Flujo | Qué cubre | Producto del incremento |
|---|---|---|
| F1 · Captura y validación de registros | Importación del CSV, reglas de validación, rechazo con causa visible, corrección de un registro | Validador con 6 reglas y control de duplicados por ID |
| F2 · Consolidación y visualización | Resumen por distrito y grupo etario, publicación protegida, persistencia | Tablero web con publicación sujeta a permiso |

**Incremento a implementar:** un validador de importación para 30 notificaciones sintéticas de IRAS. Revisa campos obligatorios, fechas válidas, duplicados por ID, evento IRAS, grupo etario del catálogo MINSA y distrito dentro del ámbito. Muestra solo los aceptados agrupados por distrito y grupo etario, mantiene visibles los rechazados con su causa y protege la publicación con una comprobación de permiso en la lógica del servidor.

**Áreas de proceso muestreadas (6 de 18):** OPD, IPM, RD, RSKM, VER y VAL. Las siete áreas de nivel 2 (REQM, PP, PMC, SAM, MA, PPQA y CM) y las otras cinco de nivel 3 (OPF, OT, TS, PI y DAR) quedan **fuera del alcance de esta evaluación**. Solo se registran como dependencias: algunas tienen evidencia parcial (control de versiones con git, seguimiento del cronograma) y otras quedan pendientes.

## 3. Roles

| Persona | Rol en el proyecto | Rol simulado en la evaluación | Revisa el trabajo de |
|---|---|---|---|
| Anthony Chaisa | Coordinación: plan, OPD, IPM, integración del informe | Patrocinador (Jefatura de Epidemiología) | Alexander (pruebas) |
| Mario Champi | Requisitos, riesgos y tablero: RD, RSKM, Grist | Usuario: responsable de vigilancia distrital | Anthony (plan) |
| Jael Huarca | Implementación: prototipo, versiones, README | Entrevistado sobre uso del proceso | Mario (trazabilidad y tablero) |
| Alexander Villafuerte | Pruebas y validación: 12 pruebas, entrevistas, acta de usuario | Evaluador líder de la sesión | Jael (código y logs) |

Como el PDF propone cinco roles y el equipo tiene cuatro integrantes, el rol de "Evidencias y tablero" se repartió entre Mario (tablero) y Anthony (consolidación de evidencias). La revisión cruzada sigue un ciclo cerrado para que nadie revise su propio trabajo. **Limitación declarada:** todos los evaluadores también son autores, así que la independencia de la evaluación es limitada.

## 4. Decisiones tomadas a partir de la lectura (TMMi, *The New MDD and TAMAR*, 2023)

1. **Tipo de evaluación.** En el MDD, la evaluación de tipo *Evaluation* reemplaza a SCAMPI B y C y no produce calificaciones. Por eso las etiquetas que usamos (Evidenciado, Parcial, No evidenciado, No evaluable) son una herramienta del equipo y no una calificación oficial. Este tipo de evaluación también admite el mayor grado de adaptación del método, y eso justifica que trabajemos con 24 criterios propios.
2. **Fases.** Seguimos las tres fases que el MDD mantiene de SCAMPI: planificar y preparar, conducir, y reportar. El enfoque es "basado en verificación": primero reunimos e indexamos la evidencia objetiva y después la verificamos. Las entrevistas se combinan con una demostración en vivo, como sugiere la lectura, y los hallazgos preliminares se validan con el equipo antes de cerrarlos.
3. **Muestreo.** El MDD agrupa el trabajo en proyectos de características similares y toma una muestra aleatoria de la evidencia para reducir el esfuerzo. En PANVIZ los dos flujos son nuestros "proyectos muestreados". Para la revisión cruzada no revisamos todas las evidencias. Sorteamos 8 de las 21 evidencias documentales con una semilla fija (2026), de modo que la selección se pueda repetir (ver sección 6).

Como complemento usamos la nota de calidad del CMMI Institute de marzo de 2026. Las fortalezas y debilidades se reportan siempre que existan. Una debilidad no se disfraza de oportunidad de mejora, y el simple cumplimiento no se presenta como fortaleza.

## 5. Criterios de preparación

Cada área tiene cuatro criterios observables, 24 en total: (1) el activo existe, (2) se aplicó, (3) otro integrante lo revisó y (4) quedó registrada una mejora o un seguimiento. El detalle está en `07_tablero/datos/criterios.csv`. Cada criterio se clasifica como Evidenciado, Parcial, No evidenciado o No evaluable, con su justificación y un enlace a la evidencia.

## 6. Muestra

- **Artefactos:** las 26 evidencias indexadas en `07_tablero/datos/evidencias.csv` (21 documentales + 5 que se completan en la sesión del equipo).
- **Muestra aleatoria para la revisión cruzada (semilla 2026):** E04, E08, E11, E13, E14, E17, E20 y E26. Se obtienen con `python 07_tablero/muestra_aleatoria.py`.
- **Pruebas:** las 12 pruebas T01–T12 definidas en `05_pruebas/plan_pruebas.md`, más 2 pruebas de regresión de defectos (D01 y D02).
- **Entrevistas:** dos de 5 minutos. La primera trata sobre el uso del proceso (entrevistada: Jael) y la segunda sobre la validación de resultados (entrevistado: Mario). Las conduce Alexander.

## 7. Reglas de confidencialidad

Solo se usan datos sintéticos. Las 20 primeras filas provienen del dataset sintético original del equipo (`sinteticos_20_filas.csv`, 15 válidas y 5 inválidas) y se agregaron 10 filas para llegar a 30, incorporando dos distritos de Caylloma (Majes y Chivay) que pide el caso. Los grupos etarios son las 6 categorías MINSA del catálogo original. El prototipo no se conecta a servicios externos. Las respuestas de las entrevistas se registran sin juicios personales y solo para este trabajo.

## 8. Riesgos de la evaluación

El plazo es corto (24 horas) y la independencia es limitada porque los roles rotan. La muestra es pequeña: 30 registros y 2 entrevistas. Los riesgos del producto y del proceso están en `03_requisitos_riesgos/riesgos.md`.

## 9. Cronograma

| Momento | Trabajo | Salida verificable |
|---|---|---|
| Día 1 · 17:00–17:30 | Lectura y acuerdo del equipo | Alcance y roles aprobados |
| 17:30–18:15 | Proceso, requisitos, riesgos y herramienta | Plan, criterios, estándar v1, Grist |
| 18:15–20:00 | Desarrollo, diseño de pruebas y acopio de evidencias | Prototipo v1, evidencias, datos |
| 20:00–21:00 | Ejecución, corrección y regresión | Resultados de v1 y v2 |
| 21:00–21:30 | Entrevistas, revisión cruzada y consenso | Hallazgos y acciones |
| 21:30–22:00 | Tablero, informe e integración | Paquete final y ensayo |
| Día 2 | Sustentación de 12 minutos | Demostración y defensa |

## 10. Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Patrocinador (simulado) | Anthony Chaisa | Aprobado | 16/11/2026 |
| Revisor del plan | Mario Champi | | |
