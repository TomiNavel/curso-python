# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Dataclass con valores por defecto
# =============================================================================
# El siguiente código intenta definir una dataclass "Usuario" con una lista
# de roles opcional. Tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Usuario(nombre='Ana', edad=30, roles=['admin'])
# Usuario(nombre='Luis', edad=25, roles=[])
# False
# =============================================================================

from dataclasses import dataclass


@dataclass
class Usuario:
    roles = []
    nombre: str
    edad: int = 0


u1 = Usuario("Ana", 30)
u1.roles.append("admin")

u2 = Usuario("Luis", 25)

print(u1)
print(u2)
print(u1.roles is u2.roles)
