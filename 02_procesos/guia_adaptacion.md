# Guía de adaptación del proceso estándar PE-04

**Versión:** 1.0 · **Fecha:** 16/11/2026 · **Elaboró:** Anthony Chaisa · **Revisa:** Mario Champi

## Reglas de adaptación

1. No se puede eliminar ninguna actividad del proceso. Lo que se adapta es la profundidad y el tipo de evidencia.
2. Toda adaptación se escribe aquí con su justificación, y otro integrante la revisa antes de aplicarla.
3. Si la adaptación cambia una prueba o un criterio de aceptación, se actualiza la matriz de trazabilidad.
4. Las lecciones aprendidas al aplicar el proceso se proponen como cambio al estándar (ver `registro_cambios.md`).

## Aplicación a los dos flujos

| Actividad | F1 · Captura y validación | F2 · Consolidación y visualización |
|---|---|---|
| Requisitos | R1, R2 y R4 (importar, validar, persistir) | R3, R5 y R6 (resumir, publicar con permiso, usabilidad) |
| Riesgos | Datos incompletos, duplicados, fechas inválidas | Publicación no autorizada, totales incorrectos, interfaz confusa |
| Implementación | `importador.py`, `reglas.py`, `validador.py`, `repositorio.py` | `resumen.py`, `seguridad.py`, `web.py`, `index.html` |
| Revisión | Revisión de código con la lista general | Revisión de código **y** revisión de interfaz con usuario simulado |
| Pruebas | Automatizadas contra el oráculo manual (T01, T02, T05, T06, T11) | Automatizadas (T03, T04, T07, T08, T12) y con usuario (T09, T10) |
| Evidencia principal | Registro de resultados y oráculo | Registro de resultados, log de acceso y medición de tareas |

## Adaptación justificada

**A-01 · Validación con usuario solo en F2.** En F1 la validación con usuario se reemplaza por pruebas automatizadas contra un oráculo calculado a mano. La razón es que F1 no tiene interfaz propia: su resultado es un conjunto de registros aceptados y rechazados, y eso se puede comprobar exactamente con datos. En cambio, F2 sí presenta información a una persona que debe decidir si la publica, así que se agrega una sesión con un usuario simulado (escenarios VAL-1 y VAL-2), en la que se miden el tiempo y los pasos.

| Elaboró | Revisó | Aprobó | Fecha |
|---|---|---|---|
| Anthony Chaisa | Mario Champi | Equipo | 16/11/2026 |
