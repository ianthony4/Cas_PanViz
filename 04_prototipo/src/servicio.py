"""Operaciones del prototipo: importar, corregir, resumir y publicar."""

import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from src import config, repositorio
from src.importador import importar_csv
from src.resumen import resumir
from src.seguridad import exigir_permiso
from src.validador import validar


def importar(ruta: Union[str, Path], usuario: str = "digitador01") -> dict:
    """Importa un CSV, valida y guarda el conjunto aceptado y los rechazados."""
    exigir_permiso(usuario, "importar")
    ruta = Path(ruta)
    if ruta.resolve() != config.ARCHIVO_TRABAJO.resolve():
        config.ESTADO_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ruta, config.ARCHIVO_TRABAJO)
    resultado = validar(importar_csv(config.ARCHIVO_TRABAJO))

    previos = {r["id"]: r for r in repositorio.leer_aceptados()}
    for reg in resultado.aceptados:
        previos[reg.id] = reg.a_dict()
    # H01: el lote más reciente manda; si un ID aceptado antes ahora llega inválido, sale del conjunto
    ids_lote = {reg.id for reg in resultado.aceptados}
    for rech in resultado.rechazados:
        if rech.id not in ids_lote:
            previos.pop(rech.id, None)
    aceptados = sorted(previos.values(), key=lambda r: r["id"])

    repositorio.guardar_aceptados(aceptados)
    repositorio.guardar_rechazados([r.a_dict() for r in resultado.rechazados])
    return {
        "procesados": resultado.total,
        "aceptados_en_archivo": len(resultado.aceptados),
        "rechazados": len(resultado.rechazados),
        "total_conjunto_aceptado": len(aceptados),
    }


def corregir(fila_datos: int, campo: str, valor: str, usuario: str = "digitador01") -> dict:
    """Corrige un campo de la fila indicada en la copia de trabajo y reimporta."""
    exigir_permiso(usuario, "corregir")
    with config.ARCHIVO_TRABAJO.open(encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        cabecera = lector.fieldnames
        filas = list(lector)
    if not 1 <= fila_datos <= len(filas) or campo not in cabecera:
        raise ValueError("Fila o campo inexistente")
    filas[fila_datos - 1][campo] = valor.strip()
    with config.ARCHIVO_TRABAJO.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecera)
        escritor.writeheader()
        escritor.writerows(filas)
    return importar(config.ARCHIVO_TRABAJO, usuario)


def estado(distrito: Optional[str] = None) -> dict:
    aceptados = repositorio.leer_aceptados()
    return {
        "aceptados": len(aceptados),
        "rechazados": repositorio.leer_rechazados(),
        "resumen": resumir(aceptados, distrito),
        "publicado": repositorio.leer_publicado(),
    }


def publicar(usuario: str) -> dict:
    """Publica el conjunto aceptado actual. Operación protegida."""
    exigir_permiso(usuario, "publicar")
    anterior = repositorio.leer_publicado()
    aceptados = repositorio.leer_aceptados()
    publicado = {
        "version": anterior["version"] + 1,
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "publicado_por": usuario,
        "registros": aceptados,
        "resumen": resumir(aceptados),
    }
    repositorio.guardar_publicado(publicado)
    return publicado


def reiniciar_estado() -> None:
    """Borra el estado persistido (solo para pruebas y demostración)."""
    if config.ESTADO_DIR.exists():
        shutil.rmtree(config.ESTADO_DIR)
