# Registro de cambios del proceso, los requisitos y el código

| ID | Fecha | Qué cambió | Motivo | Revisó | Aprobó | Evidencia |
|---|---|---|---|---|---|---|
| CP-00 | 16/11/2026 | Se aprueba el proceso estándar PE-04 v1 y la guía de adaptación | Inicio del piloto | Mario Champi | Equipo | `proceso_estandar_v1.md`, `guia_adaptacion.md` |
| CR-01 | 16/11/2026 | Nueva regla RV6: la fecha de notificación no puede ser posterior a la fecha de corte | El usuario pidió que no se publiquen registros con fecha futura. Además sirve para la prueba de mantenibilidad T11 | Alexander Villafuerte | Mario Champi (usuario) | commit "feat(CR-01)…", diff de `reglas.py` |
| CC-01 | 16/11/2026 | Corrección D01: el lote más reciente retira de los aceptados los ID que ahora llegan inválidos | Hallazgo H01 en la verificación de v1 | Alexander Villafuerte | Anthony Chaisa | commit "fix(H01,H02)…", `05_pruebas/registro_defectos.md` |
| CC-02 | 16/11/2026 | Corrección D02: la vista escapa todo valor que viene del CSV | Hallazgo H02 en la verificación de v1 | Alexander Villafuerte | Anthony Chaisa | commit "fix(H01,H02)…" |
| CC-03 | 16/11/2026 | Se corrige la prueba D02, que daba falsos positivos | Hallazgo H03 | Jael Huarca | Anthony Chaisa | commit "test(ver): corregir falso positivo…" |
| CRQ-01 | 16/11/2026 | Se aclara el requisito R4: el conjunto aceptado refleja el último lote recibido para cada ID | Hallazgo H01 | Jael Huarca | Mario Champi | `03_requisitos_riesgos/requisitos.md` (v1.1) |
| CP-01 | 16/11/2026 | Proceso estándar v2: se agregan tres controles (requisitos de reimportación, escape en la interfaz, revisión de pruebas oráculo) | Lecciones de H01, H02 y H03 | Mario Champi | Equipo | `proceso_estandar_v2.md` |
