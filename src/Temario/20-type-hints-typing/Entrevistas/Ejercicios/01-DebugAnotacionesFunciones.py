# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Anotaciones de funciones
# =============================================================================
# El siguiente código tiene 3 errores en las anotaciones de tipo. Los errores
# no impiden la ejecución, pero hacen que las anotaciones sean incorrectas
# (mypy las señalaría). Encuéntralos y corrígelos.
#
# NOTA: los errores están en las anotaciones, no en la lógica del código.
# El código produce el resultado correcto, pero los tipos declarados no
# coinciden con lo que realmente ocurre.
#
# RESULTADO ESPERADO (no cambia, el código ya funciona):
# [2, 4]
# No encontrado
# Ana
# 6
# =============================================================================

from typing import Callable


def filtrar(numeros: list[int], condicion: Callable[[int], int]) -> list[int]:
    return [n for n in numeros if condicion(n)]


def buscar_nombre(registros: dict[str, int], clave: str) -> str:
    return registros.get(clave, "No encontrado")


def aplicar_operaciones(*args: list[int]) -> int:
    total = 0
    for n in args:
        total += n
    return total


# Pruebas
print(filtrar([1, 2, 3, 4, 5], lambda x: x % 2 == 0))
print(buscar_nombre({"edad": 30}, "nombre"))
print(buscar_nombre({"nombre": "Ana"}, "nombre"))
print(aplicar_operaciones(1, 2, 3))
