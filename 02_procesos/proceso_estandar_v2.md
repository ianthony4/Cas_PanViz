# Proceso estándar del equipo · versión 2

**Código:** PE-04 · **Versión:** 2.0 · **Fecha:** 16/11/2026 · **Dueño:** Anthony Chaisa · **Cambio aprobado:** CP-01 (ver `registro_cambios.md`)

La versión 2 mantiene las seis actividades de la versión 1 y les agrega tres controles. Los tres salen de lo que aprendimos al verificar el prototipo v1.

## Qué cambia respecto de la versión 1

| Actividad | Cambio | Origen |
|---|---|---|
| 1 · Requisitos | Cada requisito que trate datos que pueden llegar más de una vez debe decir qué pasa con un registro ya aceptado si vuelve a llegar inválido | H01 (defecto D01) |
| 4 · Revisión | La lista de revisión de interfaz incluye un ítem obligatorio: "todo dato externo se escapa antes de mostrarse" | H02 (defecto D02) |
| 5 · Pruebas | Toda prueba nueva que actúe como oráculo pasa por la revisión de otro integrante antes de usarse para aceptar o rechazar código | H03 (falsos positivos en la prueba D02) |
| 5 · Pruebas | Se agrega una prueba exploratoria obligatoria de reimportación: el mismo lote dos veces y un lote corregido | H01 |

## Actividades (versión vigente)

Las actividades, entradas, salidas y responsables se mantienen igual que en `proceso_estandar_v1.md`, con los controles agregados arriba. La lista de revisión vigente está en `plantillas/plantilla_revision.md` (versión 2).
