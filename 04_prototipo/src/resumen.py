"""Resumen de casos aceptados por distrito y grupo etario (R3)."""

from typing import Dict, List, Optional

from src.config import GRUPOS_ADULTO_MAYOR, GRUPOS_ETARIOS, GRUPOS_INFANTILES


def resumir(aceptados: List[dict], distrito: Optional[str] = None) -> List[dict]:
    """Una fila por distrito: casos totales, casos por grupo etario, infantil (<5) y adulto mayor (60+)."""
    tabla: Dict[str, dict] = {}
    for r in aceptados:
        if distrito and r["distrito"].upper() != distrito.upper():
            continue
        fila = tabla.setdefault(
            r["distrito"],
            {"provincia": r["provincia"], "distrito": r["distrito"], "casos": 0, **{g: 0 for g in GRUPOS_ETARIOS}},
        )
        fila["casos"] += 1
        fila[r["grupo_etario"]] += 1
    for fila in tabla.values():
        fila["infantil_menor_5"] = sum(fila[g] for g in GRUPOS_INFANTILES)
        fila["adulto_mayor_60"] = sum(fila[g] for g in GRUPOS_ADULTO_MAYOR)
    return [tabla[k] for k in sorted(tabla)]
