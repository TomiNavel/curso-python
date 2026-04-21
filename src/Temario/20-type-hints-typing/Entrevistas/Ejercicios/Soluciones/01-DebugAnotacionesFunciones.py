# =====================
# SOLUCIÓN
# =====================
# Error 1: En "filtrar", el parámetro "condicion" está anotado como
#   Callable[[int], int], pero la función lambda devuelve un bool (el
#   resultado de x % 2 == 0). La anotación correcta es Callable[[int], bool].
#
# Error 2: En "buscar_nombre", el tipo del diccionario es dict[str, int],
#   pero el valor por defecto del .get() es "No encontrado" (una cadena).
#   Además, los valores del diccionario en las pruebas son mixtos (int y str).
#   El tipo correcto del diccionario es dict[str, str | int], y el tipo de
#   retorno debe ser str | int porque .get() puede devolver un valor int
#   del diccionario o la cadena por defecto.
#
# Error 3: En "aplicar_operaciones", *args está anotado como list[int],
#   pero *args se anota con el tipo de cada elemento individual, no con el
#   tipo del contenedor. La anotación correcta es *args: int.
#
# ERRORES CORREGIDOS:
# 1. Callable[[int], int] → Callable[[int], bool]
# 2. dict[str, int] → dict[str, str | int], retorno → str | int
# 3. *args: list[int] → *args: int

from typing import Callable


def filtrar(numeros: list[int], condicion: Callable[[int], bool]) -> list[int]:
    return [n for n in numeros if condicion(n)]


def buscar_nombre(registros: dict[str, str | int], clave: str) -> str | int:
    return registros.get(clave, "No encontrado")


def aplicar_operaciones(*args: int) -> int:
    total = 0
    for n in args:
        total += n
    return total


# Pruebas
print(filtrar([1, 2, 3, 4, 5], lambda x: x % 2 == 0))
print(buscar_nombre({"edad": 30}, "nombre"))
print(buscar_nombre({"nombre": "Ana"}, "nombre"))
print(aplicar_operaciones(1, 2, 3))
