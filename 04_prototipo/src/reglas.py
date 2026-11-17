"""Reglas de validación de notificaciones de IRAS (R2).

Cada regla recibe la fila cruda y devuelve None si cumple, o (campo, motivo) si falla.
Para añadir una regla basta con escribir la función y agregarla a REGLAS;
la vista y el resto del flujo no cambian (requisito de mantenibilidad, T11).
"""

from datetime import date, datetime
from typing import Callable, Dict, List, Optional, Tuple

from src.config import ANIO_MAX, ANIO_MIN, COLUMNAS_OBLIGATORIAS, EVENTO, FORMATO_FECHA, GRUPOS_ETARIOS, cargar_catalogo

Falla = Optional[Tuple[str, str]]
Regla = Callable[[Dict[str, str]], Falla]

_CATALOGO = cargar_catalogo()


def regla_campos_obligatorios(fila: Dict[str, str]) -> Falla:
    for campo in COLUMNAS_OBLIGATORIAS:
        if not fila.get(campo, "").strip():
            return campo, f"Campo obligatorio vacío: {campo}"
    return None


def regla_fecha_valida(fila: Dict[str, str]) -> Falla:
    valor = fila.get("fecha_notificacion", "")
    try:
        fecha = datetime.strptime(valor, FORMATO_FECHA)
    except ValueError:
        return "fecha_notificacion", f"Fecha inválida o con formato distinto a AAAA-MM-DD: {valor}"
    if not (ANIO_MIN <= fecha.year <= ANIO_MAX):
        return "fecha_notificacion", f"Año fuera del rango de vigilancia: {valor}"
    return None


def regla_evento(fila: Dict[str, str]) -> Falla:
    if fila.get("evento", "").strip().upper() != EVENTO:
        return "evento", f"Evento distinto de {EVENTO}: {fila.get('evento')}"
    return None


def regla_grupo_etario(fila: Dict[str, str]) -> Falla:
    if fila.get("grupo_etario") not in GRUPOS_ETARIOS:
        return "grupo_etario", f"Grupo etario fuera del catálogo MINSA: {fila.get('grupo_etario')}"
    return None


def regla_distrito_catalogo(fila: Dict[str, str]) -> Falla:
    if fila.get("distrito", "").strip().upper() not in _CATALOGO:
        return "distrito", f"Distrito fuera del ámbito Arequipa/Caylloma: {fila.get('distrito')}"
    return None


def regla_fecha_no_futura(fila: Dict[str, str]) -> Falla:
    """RV6 (CR-01): la fecha de notificación no puede ser posterior a la fecha de corte (hoy)."""
    try:
        fecha = datetime.strptime(fila.get("fecha_notificacion", ""), FORMATO_FECHA).date()
    except ValueError:
        return None  # el formato lo controla regla_fecha_valida
    if fecha > date.today():
        return "fecha_notificacion", f"Fecha de notificación posterior a la fecha de corte: {fecha.isoformat()}"
    return None


REGLAS: List[Regla] = [
    regla_campos_obligatorios,
    regla_fecha_valida,
    regla_evento,
    regla_grupo_etario,
    regla_distrito_catalogo,
    regla_fecha_no_futura,
]


def ubicar_distrito(nombre: str) -> Tuple[str, str]:
    """(provincia, nombre canónico) de un distrito ya validado."""
    return _CATALOGO[nombre.strip().upper()]
