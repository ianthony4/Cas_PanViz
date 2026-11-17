"""Persistencia local en JSON del conjunto aceptado, rechazados y publicado (R4)."""

import json
import os
from pathlib import Path
from typing import Any

from src import config


def _escribir(ruta: Path, datos: Any) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, ruta)  # escritura atómica


def _leer(ruta: Path, defecto: Any) -> Any:
    if not ruta.is_file():
        return defecto
    return json.loads(ruta.read_text(encoding="utf-8"))


def guardar_aceptados(registros: list) -> None:
    _escribir(config.ARCHIVO_ACEPTADOS, registros)


def leer_aceptados() -> list:
    return _leer(config.ARCHIVO_ACEPTADOS, [])


def guardar_rechazados(rechazados: list) -> None:
    _escribir(config.ARCHIVO_RECHAZADOS, rechazados)


def leer_rechazados() -> list:
    return _leer(config.ARCHIVO_RECHAZADOS, [])


def guardar_publicado(datos: dict) -> None:
    _escribir(config.ARCHIVO_PUBLICADO, datos)


def leer_publicado() -> dict:
    return _leer(config.ARCHIVO_PUBLICADO, {"version": 0, "registros": []})
