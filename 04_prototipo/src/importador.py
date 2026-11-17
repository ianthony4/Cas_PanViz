"""Importación CSV con verificación de contrato de columnas (R1)."""

import csv
from pathlib import Path
from typing import Dict, List, Union

from src.config import COLUMNAS_OBLIGATORIAS


class ErrorContrato(Exception):
    """El archivo no tiene las columnas obligatorias."""


def importar_csv(ruta: Union[str, Path]) -> List[Dict[str, str]]:
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el archivo {ruta}")
    with ruta.open(encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames:
            raise ErrorContrato("Archivo vacío o sin cabecera")
        cabeceras = [c.strip() for c in lector.fieldnames]
        faltantes = [c for c in COLUMNAS_OBLIGATORIAS if c not in cabeceras]
        if faltantes:
            raise ErrorContrato(f"Faltan columnas obligatorias: {faltantes}")
        filas = []
        for i, fila in enumerate(lector, start=1):
            limpia = {k.strip(): (v or "").strip() for k, v in fila.items() if k}
            limpia["_fila"] = i
            filas.append(limpia)
    return filas
