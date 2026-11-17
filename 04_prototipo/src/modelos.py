"""Estructuras de datos del prototipo PANVIZ IRAS."""

from dataclasses import asdict, dataclass, field
from typing import List


@dataclass
class Registro:
    """Notificación de IRAS aceptada (cada fila es un caso)."""
    id: str
    fecha_notificacion: str
    establecimiento: str
    provincia: str
    distrito: str
    grupo_etario: str
    evento: str
    estado_validacion: str = "ACEPTADO"
    fila_datos: int = 0

    def a_dict(self) -> dict:
        return asdict(self)


@dataclass
class Rechazo:
    fila_datos: int
    id: str
    campo: str
    motivo: str
    valor: str

    def a_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResultadoValidacion:
    total: int
    aceptados: List[Registro] = field(default_factory=list)
    rechazados: List[Rechazo] = field(default_factory=list)
