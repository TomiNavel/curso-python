from typing import Callable


def transformar_lista(numeros: list[int], funcion: Callable[[int], int]) -> list[int]:
    return [funcion(n) for n in numeros]


# Pruebas
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x ** 2))
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x * 2))
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x - 1))
