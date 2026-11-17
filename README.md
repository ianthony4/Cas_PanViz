# Equipo 04 · PANVIZ IRAS · Trabajo Parcial 9 (Revisión SCAMPI)

Piloto de adopción de procesos orientado a CMMI DEV v1.3 nivel 3 sobre un microprototipo de PANVIZ para la vigilancia de Infecciones Respiratorias Agudas (IRAS) en la Red Arequipa y Caylloma, construido sobre el sistema y los datos sintéticos del trabajo anterior del equipo. Es una autoevaluación académica inspirada en SCAMPI C: no es una evaluación oficial y no demuestra que PANVIZ alcance el nivel 3. Todos los datos son sintéticos.

**Integrantes:** Anthony Chaisa (coordinación) · Mario Champi (requisitos, riesgos y tablero) · Jael Huarca (implementación) · Alexander Villafuerte (pruebas y validación)

## Contenido del paquete

| Carpeta | Qué contiene |
|---|---|
| `01_plan` | Plan de evaluación y muestra; seguimiento del plan |
| `02_procesos` | Proceso estándar PE-04 v1 y v2, guía de adaptación, registro de cambios y plantillas |
| `03_requisitos_riesgos` | 6 requisitos, 5 riesgos, matriz de trazabilidad y matriz de características |
| `04_prototipo` | Código, datos sintéticos, oráculo y pruebas (versiones en git: `v1.0` y `v2.0`) |
| `05_pruebas` | Plan de pruebas, resultados de v1 y v2, logs, registro de defectos y escenarios de validación |
| `06_evidencias` | Capturas antes y después, log de acceso, historial git y actas de la sesión del equipo |
| `07_tablero` | `PANVIZ_Evaluacion.grist`, exportación CSV, datos fuente, gráficos y scripts de indicadores |
| `08_informe` | Informe (.docx), presentación (.pptx) y sus generadores |

## Cómo ejecutar el prototipo

Requiere Python 3.10 o superior.

```bash
cd 04_prototipo
python -m venv .venv
.venv/bin/pip install -r requirements.txt         # En Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/python -m src.app importar datos/iras_sinteticos_30.csv
.venv/bin/python -m src.app resumen
.venv/bin/python -m src.app publicar --usuario digitador01      # debe responder DENEGADO
.venv/bin/python -m src.app publicar --usuario resp.vigilancia
.venv/bin/python -m src.app servidor                            # abrir http://127.0.0.1:8000
```

En la interfaz web: elija un usuario, pulse "Importar datos" (sin archivo se usa el CSV de ejemplo), filtre por distrito, corrija un registro rechazado y publique. Para medir T09 y T10 se usa el panel "Medición de tareas de usuario".

## Cómo reproducir las pruebas y las métricas

```bash
cd 04_prototipo
.venv/bin/python scripts/ejecutar_pruebas.py v2      # escribe 05_pruebas/resultados_v2.csv y log_pytest_v2.txt
git checkout v1.0 -- src && .venv/bin/python scripts/ejecutar_pruebas.py v1 && git checkout v2.0 -- src   # versión anterior
cd ..
python 07_tablero/calcular_indicadores.py           # indicadores antes y después y gráficos
```

Los indicadores también se calculan con fórmulas dentro de Grist. Para abrirlos, abra `07_tablero/PANVIZ_Evaluacion.grist` con Grist Desktop (no requiere cuenta) o impórtelo en una instalación de Grist Community.

## Cómo abrir las evidencias

El índice está en `07_tablero/datos/evidencias.csv` (E01–E26). En Grist, la tabla Criterios enlaza cada criterio con su evidencia. Las rutas del índice son relativas a la raíz de este paquete.

## Regenerar el informe y la presentación

Después de llenar las actas de la sesión del equipo (ver `GUIA_SESION_EQUIPO.md`):

```bash
./regenerar.sh
```

Este script vuelve a ejecutar las pruebas, recalcula los indicadores y regenera el informe y la presentación con los resultados de la sesión.

## Fuentes

TMMi Foundation (2023), *The New MDD and TAMAR*; CMMI Institute (2026), *Quality Tip: Appraisal Findings*; ISO/IEC 33002:2015; ISO/IEC 25010:2023; Grist Community (Apache 2.0). Los datos son sintéticos: las 20 primeras notificaciones provienen del dataset original del equipo y se agregaron 10 (incluido Caylloma) para llegar a 30. Grupos etarios según el catálogo MINSA de IRAS.
