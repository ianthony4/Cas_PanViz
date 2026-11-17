"""Configuración del microprototipo PANVIZ IRAS (Infecciones Respiratorias Agudas).

Alcance local: Red Arequipa y Caylloma, datos sintéticos únicamente.
"""

import csv
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "datos"
ESTADO_DIR = Path(os.environ.get("PANVIZ_ESTADO_DIR", BASE_DIR / "estado"))
LOGS_DIR = Path(os.environ.get("PANVIZ_LOGS_DIR", BASE_DIR / "logs"))

ARCHIVO_ENTRADA_DEFAULT = DATOS_DIR / "iras_sinteticos_30.csv"
ARCHIVO_ORACULO = DATOS_DIR / "oraculo_esperado.json"
ARCHIVO_CATALOGO = DATOS_DIR / "catalogo_distritos.csv"

ARCHIVO_ACEPTADOS = ESTADO_DIR / "conjunto_aceptado.json"
ARCHIVO_RECHAZADOS = ESTADO_DIR / "rechazados.json"
ARCHIVO_PUBLICADO = ESTADO_DIR / "publicado.json"
ARCHIVO_TRABAJO = ESTADO_DIR / "entrada_trabajo.csv"

LOG_ACCESO = LOGS_DIR / "acceso.log"
LOG_USABILIDAD = LOGS_DIR / "usabilidad.csv"

# Evento epidemiológico del piloto
EVENTO = "IRAS"

# Contrato de columnas (R1)
COLUMNAS_OBLIGATORIAS: List[str] = [
    "id",
    "fecha_notificacion",
    "establecimiento",
    "distrito",
    "grupo_etario",
    "evento",
]

# Catálogo MINSA de grupos etarios para la vigilancia de IRAS
GRUPOS_ETARIOS: List[str] = [
    "Menor de 1 año",
    "1 a 4 años",
    "5 a 9 años",
    "10 a 19 años",
    "20 a 59 años",
    "60 años a más",
]
GRUPOS_INFANTILES = ["Menor de 1 año", "1 a 4 años"]   # población infantil (< 5 años)
GRUPOS_ADULTO_MAYOR = ["60 años a más"]

FORMATO_FECHA = "%Y-%m-%d"
ANIO_MIN, ANIO_MAX = 2020, 2030

# Usuarios y permisos locales (alcance didáctico, sin autenticación real)
USUARIOS: Dict[str, str] = {
    "resp.vigilancia": "responsable",
    "digitador01": "digitador",
}
PERMISOS: Dict[str, Set[str]] = {
    "responsable": {"importar", "corregir", "publicar"},
    "digitador": {"importar", "corregir"},
}


def cargar_catalogo() -> Dict[str, Tuple[str, str]]:
    """Devuelve {DISTRITO en mayúsculas: (provincia, nombre canónico del distrito)}."""
    with ARCHIVO_CATALOGO.open(encoding="utf-8") as f:
        return {r["distrito"].upper(): (r["provincia"], r["distrito"]) for r in csv.DictReader(f)}
