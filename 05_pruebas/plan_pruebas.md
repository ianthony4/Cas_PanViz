# Plan y procedimiento de pruebas T01–T12

**Versión:** 1.0 · **Elaboró:** Alexander Villafuerte · **Revisa:** Anthony Chaisa

## Entorno para repetir las pruebas

- Sistema operativo: Linux (Debian 13, kernel 6.12). Las pruebas también corren en Windows.
- Python 3.13 en un entorno virtual con las dependencias de `04_prototipo/requirements.txt`.
- Datos: `04_prototipo/datos/iras_sinteticos_30.csv` (30 notificaciones sintéticas de IRAS, 6 inválidas sembradas; las 20 primeras son el dataset original del equipo) y el oráculo `oraculo_esperado.json`, que se calculó a mano antes de ejecutar el código.
- Versiones evaluadas: etiqueta git `v1.0` (antes) y `v2.0` (después).

## Cómo ejecutarlas

```
cd 04_prototipo
python scripts/ejecutar_pruebas.py v2      # genera 05_pruebas/resultados_v2.csv y log_pytest_v2.txt
```

Para T09 y T10:

1. `python -m src.app servidor`
2. Abrir http://127.0.0.1:8000.
3. El facilitador escribe el nombre del participante y pulsa "Iniciar tarea".
4. El participante hace la tarea sin ayuda.
5. Al terminar se pulsa "Terminar tarea". El tiempo y los pasos se guardan en `logs/usabilidad.csv` y la próxima ejecución del script los evalúa.

## Casos

| ID | Característica | Requisito | Procedimiento | Esperado |
|---|---|---|---|---|
| T01 | Adecuación funcional | R2 | Importar el CSV y comparar los rechazados (fila y campo) con el oráculo | 6 rechazados con la causa exacta y 24 aceptados |
| T02 | Adecuación funcional | R3 | Importar y comparar el resumen por distrito y grupo con el cálculo manual | Diferencia cero en los 9 distritos y 6 grupos etarios; 24 casos, 10 menores de 5 años y 6 de 60 a más |
| T03 | Eficiencia de desempeño | R1 | Importar las 30 filas tres veces desde un estado vacío y medir con `perf_counter` | Máximo de 2 s o menos |
| T04 | Eficiencia de desempeño | R3 | Tres veces: corregir una fila, reimportar y recalcular el resumen | Máximo de 2 s o menos |
| T05 | Fiabilidad | R4 | Importar dos veces el mismo archivo y contar | 24 antes y después, ID únicos y 24 casos en el resumen |
| T06 | Fiabilidad | R4 | Importar y publicar, y luego leer el estado desde un proceso de Python nuevo | Se recuperan 24 aceptados y la publicación v1 |
| T07 | Seguridad | R5 | Intentar publicar como digitador01 y como un usuario desconocido (por función y por HTTP) | HTTP 403 y 3 líneas DENEGADO en `acceso.log` |
| T08 | Seguridad | R5 | Publicar como responsable, cambiar los datos e intentar publicar como digitador | El hash de `publicado.json` no cambia y la versión sigue en 1 |
| T09 | Capacidad de interacción | R6 | El usuario simulado encuentra un rechazado y lo corrige desde la interfaz | Lo logra en 90 s o menos, sin ayuda |
| T10 | Capacidad de interacción | R6 | El usuario simulado encuentra el resumen de Majes | Lo logra en 90 s o menos, sin ayuda |
| T11 | Mantenibilidad | R2 | Agregar la regla RV6 (fecha no futura) solo en `reglas.py` | Rechaza una fecha de 2029 y la vista no cambia |
| T12 | Mantenibilidad | R1–R5 | Regresión: todo el flujo después del cambio | Se mantienen el oráculo y la seguridad |

Las pruebas D01 y D02 se agregaron después de la verificación de v1 para reproducir los defectos encontrados (ver `registro_defectos.md`).

Una prueba "No ejecutada" se mantiene visible en el registro y **no** se cuenta como aprobada.
