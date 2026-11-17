#!/usr/bin/env bash
# Descarga PANVIZ_Evaluacion.grist y exporta cada tabla a CSV. Uso: GRIST_KEY=... ./exportar_grist.sh <docId>
set -e
D=$1; U=${GRIST_URL:-http://localhost:8484}; H="Authorization: Bearer $GRIST_KEY"
cd "$(dirname "$0")"; mkdir -p export_csv
curl -sf -H "$H" "$U/api/docs/$D/download" -o PANVIZ_Evaluacion.grist
for t in Criterios Evidencias Pruebas Hallazgos Aportes Indicadores; do
  curl -sf -H "$H" "$U/api/docs/$D/download/csv?tableId=$t" -o "export_csv/$t.csv"
done
ls -la PANVIZ_Evaluacion.grist export_csv
