#!/usr/bin/env bash
# Regenera resultados, indicadores, informe y presentación desde los datos actuales.
# Variables opcionales: PY (python con dependencias), NODE_PATH (carpeta con pptxgenjs),
# GRIST_KEY y GRIST_DOC (para reconstruir y exportar el documento Grist).
set -e
cd "$(dirname "$0")"
RAIZ_TRABAJO="$(cd .. && pwd)"
if [ -z "${PY:-}" ]; then
  if [ -x "$PWD/04_prototipo/.venv/bin/python" ]; then PY="$PWD/04_prototipo/.venv/bin/python"
  elif [ -x "$RAIZ_TRABAJO/.venv/bin/python" ]; then PY="$RAIZ_TRABAJO/.venv/bin/python"
  else PY=python3; fi
fi
(cd 04_prototipo && $PY scripts/ejecutar_pruebas.py v2)
$PY 07_tablero/calcular_indicadores.py
if [ -n "$GRIST_KEY" ]; then
  DOC=$($PY 07_tablero/construir_grist.py | tail -1)
  ./07_tablero/exportar_grist.sh "$DOC"
  echo "Nuevo documento Grist: $DOC"
fi
$PY 08_informe/generar_informe.py
node 08_informe/generar_presentacion.js
echo "Listo: 08_informe/Informe_Equipo04_PANVIZ.docx y Presentacion_Equipo04_PANVIZ.pptx"
