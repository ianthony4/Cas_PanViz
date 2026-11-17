"""Configuración común de las pruebas T01-T12.

Cada prueba trabaja en un directorio temporal de estado y registra lo observado
en logs/observaciones_pruebas.json para alimentar el reporte de resultados.
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config  # noqa: E402

ARCHIVO_OBS = ROOT / "logs" / "observaciones_pruebas.json"


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    estado = tmp_path / "estado"
    logs = tmp_path / "logs"
    monkeypatch.setattr(config, "ESTADO_DIR", estado)
    monkeypatch.setattr(config, "LOGS_DIR", logs)
    monkeypatch.setattr(config, "ARCHIVO_ACEPTADOS", estado / "conjunto_aceptado.json")
    monkeypatch.setattr(config, "ARCHIVO_RECHAZADOS", estado / "rechazados.json")
    monkeypatch.setattr(config, "ARCHIVO_PUBLICADO", estado / "publicado.json")
    monkeypatch.setattr(config, "ARCHIVO_TRABAJO", estado / "entrada_trabajo.csv")
    monkeypatch.setattr(config, "LOG_ACCESO", logs / "acceso.log")
    return tmp_path


@pytest.fixture(scope="session")
def oraculo():
    return json.loads(config.ARCHIVO_ORACULO.read_text(encoding="utf-8"))


@pytest.fixture
def observar(request):
    """Guarda el valor observado de la prueba actual, indexado por su ID (T01...T12)."""
    callspec = getattr(request.node, "callspec", None)
    tid = callspec.params["tarea"] if callspec and "tarea" in callspec.params else request.node.name.split("_")[1].upper()

    def _registrar(observado):
        ARCHIVO_OBS.parent.mkdir(exist_ok=True)
        datos = json.loads(ARCHIVO_OBS.read_text(encoding="utf-8")) if ARCHIVO_OBS.is_file() else {}
        datos[tid] = observado
        ARCHIVO_OBS.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    return _registrar
