"""Pruebas de regresión de defectos encontrados en la verificación de v1.

D01 (H01): un registro aceptado en un lote anterior y rechazado en el lote corregido
           seguía contando en el tablero (aparecía como aceptado y rechazado a la vez).
D02 (H02): valores del CSV se insertaban sin escapar en la tabla de rechazados
           (inyección HTML en el navegador).
"""

import json
import re
from pathlib import Path

from src import config, servicio

ROOT = Path(__file__).resolve().parent.parent


def test_d01_lote_corregido_no_deja_registros_obsoletos(entorno, oraculo, tmp_path, observar):
    servicio.importar(config.ARCHIVO_ENTRADA_DEFAULT)
    texto = config.ARCHIVO_ENTRADA_DEFAULT.read_text(encoding="utf-8")
    lote = tmp_path / "lote_corregido.csv"
    lote.write_text(texto.replace("IRAS-2026-001,2026-01-12", "IRAS-2026-001,2026-13-12"), encoding="utf-8")
    servicio.importar(lote)
    aceptados = {r["id"] for r in json.loads(config.ARCHIVO_ACEPTADOS.read_text(encoding="utf-8"))}
    # los rechazos por ID duplicado conviven legítimamente con el primer registro aceptado
    rechazados = {r["id"] for r in servicio.estado()["rechazados"] if r["campo"] != "id"}
    cerro = next(f for f in servicio.estado()["resumen"] if f["distrito"] == "Cerro Colorado")
    observar({"aceptados": len(aceptados), "en_ambos": sorted(aceptados & rechazados), "casos_cerro_colorado": cerro["casos"]})
    assert not (aceptados & rechazados)
    assert len(aceptados) == oraculo["aceptados"] - 1
    assert cerro["casos"] == oraculo["totales_por_distrito"]["Cerro Colorado"]["casos"] - 1


def test_d02_vista_escapa_valores_del_csv(observar):
    html = (ROOT / "src" / "templates" / "index.html").read_text(encoding="utf-8")
    interpolaciones = re.findall(r"\$\{(r\.[a-z_]+|r\['[^']+'\]|r\.valor[^}]*)\}", html)
    sin_escapar = [i for i in interpolaciones if not i.startswith("esc(")]
    observar({"interpolaciones_sin_escapar": sin_escapar})
    assert not sin_escapar
