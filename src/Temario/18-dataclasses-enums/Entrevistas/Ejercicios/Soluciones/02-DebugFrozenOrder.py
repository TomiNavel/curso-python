# =====================
# SOLUCIÓN
# =====================
# Error 1: Falta order=True. Sin él, la dataclass no genera __lt__ y sorted()
#   lanza TypeError al comparar instancias. Solución: añadir order=True al
#   decorador.
#
# Error 2: El orden de los campos es incorrecto para ordenar por fecha.
#   Con order=True, la comparación se hace campo por campo en el orden
#   declarado, así que con "nombre" antes de "fecha" el orden sería
#   alfabético por nombre. Solución: declarar "fecha" primero.
#
# Error 3: Falta frozen=True. Sin él, la línea "e1.nombre = ..." no lanza
#   error (y el requisito explícito del ejercicio es que no se pueda cambiar),
#   y además los eventos no son hashables, por lo que no se pueden usar como
#   claves de diccionario. Solución: añadir frozen=True al decorador.
#
# Con frozen=True, la línea e1.nombre = "..." ahora lanza FrozenInstanceError,
# por lo que hay que envolverla en try/except o eliminarla. En la solución la
# eliminamos para que el resultado coincida con el esperado.
#
# ERRORES CORREGIDOS:
# 1. Añadir order=True
# 2. Reordenar: fecha primero, nombre después
# 3. Añadir frozen=True (y eliminar la asignación inválida)


from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Evento:
    fecha: str
    nombre: str


e1 = Evento("2024-06-01", "Cierre")
e2 = Evento("2024-01-10", "Inicio")
e3 = Evento("2024-03-15", "Revisión")

eventos = [e1, e2, e3]
print(sorted(eventos))

agenda = {e2: "Reunión importante"}
print(agenda[Evento("2024-01-10", "Inicio")])
