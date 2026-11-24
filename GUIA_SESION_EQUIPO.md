# Guía de la sesión del equipo (unos 25 minutos)

Estas son las partes de la evaluación que deben hacer personas reales. Todo lo demás ya está listo. Al terminar, ejecuten `./regenerar.sh` y el informe, la presentación y el tablero se actualizan solos.

**Antes de empezar:** levanten el prototipo (`cd 04_prototipo && python -m src.app servidor`) y abran http://127.0.0.1:8000. Los archivos CSV se pueden editar en LibreOffice Calc. Guárdenlos como CSV UTF-8, separado por comas.

## 1. Pruebas con usuario T09 y T10 (unos 5 min) · facilita Alexander, usuario Mario

1. Alexander escribe "Mario Champi" en el panel "Medición de tareas", elige **T09** y pulsa "Iniciar tarea".
2. Mario, sin ayuda, busca en la tabla de rechazados el registro IRAS-2026-017, que no tiene establecimiento, pulsa "Corregir" y escribe `CS Cerro Colorado`. Después elige el usuario `resp.vigilancia` y pulsa "Publicar".
3. Alexander pulsa "Terminar tarea", responde si se completó y anota cualquier observación de Mario.
4. Repiten el procedimiento con **T10**: Mario debe encontrar el resumen de Majes con el filtro de distrito y leer los casos (3 en total: 1 menor de 1 año, 1 de 5 a 9 y 1 de 60 a más).

El tiempo y los pasos se guardan solos en `04_prototipo/logs/usabilidad.csv`. Si alguna tarea pasa de 90 s, se registra tal cual: es un resultado válido y genera un hallazgo.

## 2. Acta de validación (2 min) · `06_evidencias/sesion_equipo/validacion_usuario.csv`

En la columna `decision`, Mario escribe "Aceptado" o "Rechazado" para VAL-1 (T10) y VAL-2 (T09). Si tiene alguna observación, la anota y se le asigna una acción derivada.

## 3. Entrevistas de 5 minutos (10 min) · `06_evidencias/sesion_equipo/entrevistas.csv`

- **E1 (uso del proceso):** Alexander entrevista a Jael.
- **E2 (validación de resultados):** Alexander entrevista a Mario.

Para cada pregunta se anotan la respuesta (en pocas palabras), la evidencia que se corroboró (por ejemplo "E12, commit 3dd2093 mostrado en vivo") y cualquier discrepancia entre lo que se dijo y lo que muestra la evidencia. Si no hubo discrepancia, la celda se deja vacía.

## 4. Revisión cruzada (5 min, en paralelo) · `06_evidencias/sesion_equipo/revisiones.csv`

Cada persona abre las evidencias que le tocan, aplica la lista `02_procesos/plantillas/plantilla_revision.md` y escribe el resultado: "Aprobado", "Aprobado con observaciones" o "Rechazado".

| Revisor | Revisa a | Evidencias (muestra aleatoria, semilla 2026) |
|---|---|---|
| Alexander | Jael | E11 (código v1), E17 (log de acceso) |
| Anthony | Alexander | E13, E14, E20 |
| Mario | Anthony | E04, E26 y el plan E01, la guía E03 y los riesgos E09 |
| Jael | Mario | E08 (trazabilidad), E21 (tablero) |

## 5. Registro de aportes (3 min) · formulario de Grist o `aportes.csv`

Cada estudiante registra al menos 3 aportes con estos campos: criterio (por ejemplo `RD-C1`), descripción de lo que aportó, evidencia (por ejemplo `E07`) y autor. Después, Anthony consolida y revisa que no haya duplicados.

## 6. Confirmar aprobaciones

Revisen los nombres que figuran en las columnas "Revisó" y "Aprobó" de `02_procesos/registro_cambios.md` y en la tabla de aprobación de `01_plan/plan_evaluacion.md`. Corrijan cualquier asignación que no corresponda.

## 7. Cerrar

```bash
./regenerar.sh
```

Revisen que el informe siga teniendo 8 páginas antes de los anexos y graben el video de respaldo de hasta 3 minutos con la demostración.
