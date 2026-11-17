"""Control mínimo de permisos sobre operaciones protegidas (R5).

Alcance local: no hay autenticación; el usuario se identifica por nombre y su rol
se resuelve en el servidor. La comprobación está en la lógica, no en la vista.
"""

from datetime import datetime

from src import config


class PermisoDenegado(Exception):
    pass


def registrar_acceso(usuario: str, accion: str, resultado: str) -> None:
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with config.LOG_ACCESO.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')}\t{usuario}\t{accion}\t{resultado}\n")


def exigir_permiso(usuario: str, accion: str) -> None:
    rol = config.USUARIOS.get(usuario)
    if rol is None or accion not in config.PERMISOS.get(rol, set()):
        registrar_acceso(usuario, accion, "DENEGADO")
        raise PermisoDenegado(f"El usuario '{usuario}' no tiene permiso para '{accion}'")
    registrar_acceso(usuario, accion, "PERMITIDO")
