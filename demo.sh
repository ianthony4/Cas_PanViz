#!/usr/bin/env bash
# Prepara la demostración en vivo: estado limpio, prototipo web y tablero Grist.
# Uso: ./demo.sh            (Ctrl+C para cerrar todo al terminar)
# Variables opcionales: PY (python con dependencias), GRIST_APP (ruta a Grist Desktop .AppImage)
set -e
cd "$(dirname "$0")"
RAIZ_TRABAJO="$(cd .. && pwd)"
PY=${PY:-$RAIZ_TRABAJO/.venv/bin/python}
[ -x "$PY" ] || PY=python3
GRIST_APP=${GRIST_APP:-$RAIZ_TRABAJO/herramientas/grist-desktop-0.3.17-linux-x86_64.AppImage}

cd 04_prototipo
"$PY" -m src.app reiniciar >/dev/null          # estado vacío: la demo empieza desde cero
rm -f logs/acceso.log
"$PY" -m src.app servidor &                     # http://127.0.0.1:8000
SERVIDOR=$!
cd ..
trap 'kill $SERVIDOR 2>/dev/null' EXIT
sleep 2

if [ -x "$GRIST_APP" ]; then
  "$GRIST_APP" "$PWD/07_tablero/PANVIZ_Evaluacion.grist" >/dev/null 2>&1 &
else
  echo "Grist Desktop no encontrado: abra 07_tablero/PANVIZ_Evaluacion.grist manualmente."
fi
xdg-open http://127.0.0.1:8000 >/dev/null 2>&1 || echo "Abra http://127.0.0.1:8000 en el navegador."
echo "Demo lista: prototipo en http://127.0.0.1:8000 y Grist abriéndose. Ctrl+C para terminar."
wait $SERVIDOR
