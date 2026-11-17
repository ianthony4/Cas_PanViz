"""Ejecuta T01-T12 y genera el registro de resultados en 05_pruebas.

Uso: python scripts/ejecutar_pruebas.py v1
Salida: ../05_pruebas/resultados_<version>.csv y ../05_pruebas/log_pytest_<version>.txt
"""

import csv
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT.parent / "05_pruebas"
OBS = ROOT / "logs" / "observaciones_pruebas.json"

CATALOGO = [
    ("T01", "R2", "Adecuación funcional", "iras_sinteticos_30.csv (6 inválidos sembrados)", "6 rechazados con causa exacta del oráculo; 24 aceptados", "test_t01"),
    ("T02", "R3", "Adecuación funcional", "iras_sinteticos_30.csv + oraculo_esperado.json", "Casos por distrito y grupo etario idénticos al cálculo manual (24; 10 menores de 5; 6 de 60+)", "test_t02"),
    ("T03", "R1", "Eficiencia de desempeño", "Importación de 30 filas, 3 repeticiones", "Máximo <= 2 s", "test_t03"),
    ("T04", "R3", "Eficiencia de desempeño", "Corrección + reimportación + resumen, 3 repeticiones", "Máximo <= 2 s", "test_t04"),
    ("T05", "R4", "Fiabilidad", "Mismo archivo importado dos veces", "24 aceptados antes y después, IDs únicos, 24 casos en el resumen", "test_t05"),
    ("T06", "R4", "Fiabilidad", "Importar, publicar y leer desde un proceso nuevo", "Proceso nuevo recupera 24 aceptados y publicación v1", "test_t06"),
    ("T07", "R5", "Seguridad", "digitador01 e intruso intentan publicar", "HTTP 403 y 3 líneas DENEGADO en acceso.log", "test_t07"),
    ("T08", "R5", "Seguridad", "Publicación denegada tras cambiar el conjunto aceptado", "Hash de publicado.json idéntico; versión sigue en 1", "test_t08"),
    ("T09", "R6", "Capacidad de interacción", "Usuario simulado corrige un registro rechazado", "Completada en <= 90 s sin ayuda", "test_t09_t10_tareas_de_usuario[T09]"),
    ("T10", "R6", "Capacidad de interacción", "Usuario simulado localiza el resumen de un distrito", "Completada en <= 90 s sin ayuda", "test_t09_t10_tareas_de_usuario[T10]"),
    ("T11", "R2", "Mantenibilidad", "Nueva regla regla_fecha_no_futura en reglas.py", "Rechaza fecha futura sin cambiar web.py ni index.html", "test_t11"),
    ("T12", "R1-R5", "Mantenibilidad", "Flujo completo tras el cambio", "Oráculo y seguridad se mantienen", "test_t12"),
    ("D01", "R3/R4", "Fiabilidad (defecto H01)", "Lote corregido donde IRAS-2026-001 pasa a fecha inválida", "Ningún ID aceptado y rechazado a la vez; 23 aceptados", "test_d01"),
    ("D02", "R5", "Seguridad (defecto H02)", "Plantilla index.html", "Todo valor del CSV se inserta escapado", "test_d02"),
]


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else "actual"
    SALIDA.mkdir(exist_ok=True)
    if OBS.is_file():
        OBS.unlink()
    junit = ROOT / "logs" / f"junit_{version}.xml"
    proc = subprocess.run([sys.executable, "-m", "pytest", "-v", f"--junitxml={junit}"], cwd=ROOT, capture_output=True, text=True)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (SALIDA / f"log_pytest_{version}.txt").write_text(
        f"Ejecución {datetime.now().isoformat(timespec='seconds')} · versión {version} · commit {commit}\n\n{proc.stdout}{proc.stderr}",
        encoding="utf-8")

    casos = {}
    for tc in ET.parse(junit).getroot().iter("testcase"):
        if tc.find("skipped") is not None:
            estado = "No ejecutada"
        elif tc.find("failure") is not None or tc.find("error") is not None:
            estado = "Fallida"
        else:
            estado = "Aprobada"
        casos[tc.get("name")] = (estado, float(tc.get("time", 0)))
    obs = json.loads(OBS.read_text(encoding="utf-8")) if OBS.is_file() else {}

    with (SALIDA / f"resultados_{version}.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "version", "commit", "requisito", "caracteristica", "entrada", "esperado", "observado", "duracion_s", "resultado", "evidencia"])
        for tid, req, car, ent, esp, nombre in CATALOGO:
            estado, dur = next(((v) for k, v in casos.items() if k == nombre or k.startswith(nombre + "_") or k.startswith(nombre)), ("No ejecutada", 0))
            w.writerow([tid, version, commit, req, car, ent, esp, json.dumps(obs.get(tid, ""), ensure_ascii=False),
                        round(dur, 3), estado, f"05_pruebas/log_pytest_{version}.txt"])
            print(f"{tid} {estado:<12} {car}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
