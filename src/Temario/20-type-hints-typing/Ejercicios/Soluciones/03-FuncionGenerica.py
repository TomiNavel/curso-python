from typing import TypeVar

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


def ultimo(elementos: list[T]) -> T:
    return elementos[-1]


def invertir_par(par: tuple[A, B]) -> tuple[B, A]:
    return (par[1], par[0])


# Pruebas
print(ultimo([1, 2, 3]))
print(ultimo(["hola"]))
print(ultimo([False, True]))

print(invertir_par(("a", 2)))
print(invertir_par((42, False)))
