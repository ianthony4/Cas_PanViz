# Registro de riesgos · producto y proceso

**Versión:** 1.1 · **Fecha:** 16/11/2026 · **Elaboró:** Mario Champi · **Revisa:** Anthony Chaisa

Escala: probabilidad e impacto de 1 (bajo) a 3 (alto). La exposición es probabilidad × impacto. La prioridad es alta si la exposición es 6 o más, media si es 3 o 4, y baja si es menor.

| ID | Tipo | Riesgo | P | I | Exp. | Respuesta | Responsable | Vínculo | Seguimiento (después de v2) |
|---|---|---|---|---|---|---|---|---|---|
| RK1 | Producto | Se publican conteos inflados por registros duplicados o reenviados | 3 | 3 | 9 | **Mitigar:** control de duplicados por ID, reimportación idempotente y prueba con lote corregido | Jael | R2, R4 → T01, T05, D01 | **Se materializó** en v1 (D01). Se corrigió en v2 y queda controlado |
| RK2 | Producto | El resumen cuenta registros que no pasaron la validación | 2 | 3 | 6 | **Mitigar:** el resumen se calcula solo desde el conjunto aceptado y se compara con un oráculo manual | Mario | R3 → T02 | Controlado: T02 aprobada en v1 y v2 |
| RK3 | Proceso | El plazo de 24 horas impide ejecutar todas las pruebas | 2 | 2 | 4 | **Mitigar:** automatizar 10 de 12 pruebas y reservar 20 minutos para las de usuario | Alexander | R1, R6 → T03, T09, T10 | Parcial: 10 automatizadas; T09 y T10 dependen de la sesión |
| RK4 | Producto | Un usuario sin permiso publica, o la interfaz ejecuta datos maliciosos | 2 | 3 | 6 | **Evitar:** el permiso se comprueba en el servidor, se registran los accesos y se escapan los datos en la vista | Jael | R5 → T07, T08, D02 | La parte de interfaz **se materializó** en v1 (D02). Se corrigió en v2 |
| RK5 | Proceso | La evaluación pierde objetividad porque los autores se evalúan a sí mismos | 3 | 2 | 6 | **Aceptar y mitigar:** revisión cruzada en ciclo, muestra aleatoria con semilla y declaración de la limitación | Anthony | IPM, VAL → H06 | Se mantiene abierto como limitación (H06, A3) |
