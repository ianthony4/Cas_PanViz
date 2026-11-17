# Lista de revisión (PE-04) · versión 2

**Artefacto revisado:** ______  **Versión / commit:** ______  **Autor:** ______  **Revisor:** ______  **Fecha:** ______

## A. Requisitos y trazabilidad
- [ ] Cada requisito tiene un criterio de aceptación medible
- [ ] Cada requisito tiene al menos una prueba en la matriz
- [ ] (v2) Se indica qué pasa si un registro vuelve a llegar inválido

## B. Código
- [ ] El código hace lo que dice el requisito; no hay lógica sin requisito
- [ ] Las reglas de validación están en `reglas.py` y no dispersas por el código
- [ ] La operación protegida comprueba el permiso en el servidor
- [ ] Los mensajes de error explican la causa al usuario

## C. Interfaz
- [ ] (v2) Todo dato externo se escapa antes de mostrarse (`esc()`)
- [ ] Los rechazados se ven con su causa
- [ ] El usuario puede llegar al resumen de un distrito sin ayuda

## D. Pruebas
- [ ] La prueba se diseñó desde el requisito o el oráculo, no desde el código
- [ ] (v2) Otro integrante revisó la prueba oráculo antes de usarla
- [ ] Se registran el resultado esperado y el observado

## Observaciones
| # | Ubicación | Observación | Severidad (alta/media/baja) | Acción | Estado |
|---|---|---|---|---|---|
| 1 | | | | | |

**Resultado:** Aprobado / Aprobado con observaciones / Rechazado
