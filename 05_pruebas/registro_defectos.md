# Registro de defectos encontrados en la verificación de v1

## D01 · Un registro aceptado antes seguía contando aunque el lote nuevo lo rechazaba

- **Versión:** v1.0 (commit 9890135)
- **Cómo se encontró:** durante la prueba exploratoria de reimportación. Primero se importó el lote original. Luego se importó un lote corregido en el que IRAS-2026-001 llegaba con la fecha 2026-13-12, que no existe.
- **Observado:** el lote corregido rechazó IRAS-2026-001, pero el conjunto aceptado lo conservó. Ese ID aparecía a la vez como aceptado y como rechazado, y el tablero seguía contando ese caso en Cerro Colorado (4 casos en lugar de 3, y un menor de 1 año de más).
- **Esperado:** el último lote recibido manda. Si un ID llega inválido, sale de los aceptados.
- **Causa:** `servicio.importar` unía el conjunto anterior con los aceptados del lote nuevo, pero nunca retiraba los ID que ese lote rechazaba. El requisito R4 no decía qué hacer en este caso.
- **Corrección:** en v2 se retiran del conjunto los ID rechazados en el lote, salvo que el mismo lote también los haya aceptado (caso del duplicado). Además, R4 se aclaró en la versión 1.1.
- **Re-verificación:** la prueba D01 falla en v1 y pasa en v2. T01, T02, T05 y T12 se repitieron y pasan.
- **Hallazgo y acción:** H01 → A01 (cerrada).

## D02 · La tabla de rechazados ejecutaba HTML que venía en el CSV

- **Versión:** v1.0
- **Cómo se encontró:** en la revisión de la interfaz se importó un CSV cuyo campo grupo_etario contenía una etiqueta `<img>` con un manejador `onerror`.
- **Observado en v1:** el navegador interpretó el valor como HTML, creó 2 elementos `<img>` en la tabla y ejecutó el código, que cambió el título de la página a "INYECTADO".
- **Esperado:** el valor se muestra como texto.
- **Causa:** la plantilla armaba las filas con `innerHTML` e insertaba los valores sin escaparlos.
- **Corrección:** en v2 se agregó la función `esc()` y todo valor que viene del CSV pasa por ella.
- **Re-verificación en v2:** con el mismo CSV no se crea ningún `<img>`, el título no cambia y el valor se ve como texto. La prueba D02 pasa.
- **Nota (H03):** la primera versión de la prueba D02 marcaba como inseguras expresiones que ya estaban escapadas. Fue un falso positivo de la propia prueba y se corrigió en dos pasos.
- **Hallazgo y acción:** H02 → A02 (cerrada) y H03 → A1 (abierta, 7 días).
