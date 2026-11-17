"""Validación de notificaciones: reglas de reglas.py + duplicados por ID (R2)."""

from typing import Dict, List, Optional

from src.modelos import Rechazo, Registro, ResultadoValidacion
from src.reglas import REGLAS, Regla, ubicar_distrito


def validar(filas: List[Dict[str, str]], reglas: Optional[List[Regla]] = None) -> ResultadoValidacion:
    reglas = REGLAS if reglas is None else reglas
    resultado = ResultadoValidacion(total=len(filas))
    vistos = set()
    for fila in filas:
        id_ = fila.get("id", "")
        if id_ and id_ in vistos:
            resultado.rechazados.append(
                Rechazo(fila["_fila"], id_, "id", f"ID duplicado: {id_} ya fue recibido", id_)
            )
            continue
        falla = None
        for regla in reglas:
            falla = regla(fila)
            if falla:
                break
        if falla:
            campo, motivo = falla
            resultado.rechazados.append(Rechazo(fila["_fila"], id_, campo, motivo, fila.get(campo, "")))
            continue
        vistos.add(id_)
        provincia, distrito = ubicar_distrito(fila["distrito"])
        resultado.aceptados.append(
            Registro(
                id=id_,
                fecha_notificacion=fila["fecha_notificacion"],
                establecimiento=fila["establecimiento"],
                provincia=provincia,
                distrito=distrito,
                grupo_etario=fila["grupo_etario"],
                evento=fila["evento"].upper(),
                fila_datos=fila["_fila"],
            )
        )
    return resultado
