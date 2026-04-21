from dataclasses import dataclass
from enum import IntEnum


class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


@dataclass
class Tarea:
    titulo: str
    prioridad: Prioridad = Prioridad.MEDIA


# Pruebas
tareas = [
    Tarea("Limpiar logs", Prioridad.BAJA),
    Tarea("Deploy", Prioridad.ALTA),
    Tarea("Documentar"),
]

for tarea in sorted(tareas, key=lambda t: t.prioridad, reverse=True):
    print(tarea)
