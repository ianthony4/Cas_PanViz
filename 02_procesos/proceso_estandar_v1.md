# Proceso estándar del equipo · versión 1

**Código:** PE-04 · **Versión:** 1.0 · **Fecha:** 16/11/2026 · **Dueño:** Anthony Chaisa · **Aprobado por:** el equipo completo, en la reunión de inicio

Este proceso describe cómo el equipo pasa de una necesidad a un incremento probado. Es el mismo para cualquier flujo de PANVIZ. Lo que cambia entre flujos se decide con la guía de adaptación.

## Actividades

| # | Actividad | Entradas | Qué se hace | Salida | Responsable | Revisión |
|---|---|---|---|---|---|---|
| 1 | Requisitos | Necesidad del usuario y caso de estudio | Se escribe cada requisito con la plantilla, incluido su criterio de aceptación, y se le asigna un ID (R1, R2…) | Lista de requisitos | Requisitos (Mario) | La revisa Jael con la lista de revisión de requisitos |
| 2 | Riesgos | Requisitos y plan | Se identifican los riesgos del producto y del proceso, con su probabilidad, impacto, respuesta y responsable | Registro de riesgos | Requisitos (Mario) | La revisa Anthony |
| 3 | Implementación | Requisitos aprobados | Se programa en una rama con commits pequeños cuyo mensaje explica el porqué | Código versionado | Implementación (Jael) | La revisa Alexander con la lista de revisión de código |
| 4 | Revisión | Código y artefactos | Se aplica la lista de revisión correspondiente y se registran los hallazgos | Acta de revisión | Revisor asignado | El coordinador verifica que las observaciones se cierren |
| 5 | Pruebas | Requisitos y código | Se diseñan las pruebas desde los requisitos y el oráculo, se ejecutan y se registran el resultado esperado y el observado | Registro de resultados | Pruebas (Alexander) | La revisa Anthony |
| 6 | Cierre del ciclo | Resultados y hallazgos | Se acuerdan acciones, se actualiza el tablero y se proponen mejoras al proceso | Hallazgos, acciones y propuesta de cambio | Coordinación (Anthony) | La aprueba el equipo |

## Convenciones

- **Nombres de archivo:** en minúsculas, con guion bajo y prefijo de carpeta (`01_plan`, `02_procesos`…).
- **Identificadores:** R (requisito), C (criterio de proceso), E (evidencia), T (prueba), D (defecto), H (hallazgo) y A (acción). Siguen una sola cadena: R → C → E → T → H → A.
- **Versiones:** el código se versiona con git y etiquetas (`v1.0`, `v2.0`). Los documentos llevan su versión en la cabecera y, si cambian, en el nombre del archivo (`_v1`, `_v2`).
- **Cambios:** todo cambio al proceso, a los requisitos o al código registra su motivo, quién lo revisó y quién lo aprobó (ver `registro_cambios.md`).

## Plantillas

Las plantillas de requisito, revisión y prueba están en `02_procesos/plantillas/`.

## Criterio de terminado

Un incremento se da por terminado cuando todas sus pruebas automatizadas pasan, las pruebas manuales tienen resultado registrado (o quedan visibles como "No ejecutada"), no queda ninguna observación de revisión abierta y la evidencia está indexada.
