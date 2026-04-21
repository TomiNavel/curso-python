# =====================
# SOLUCIÓN
# =====================
# Error 1: El atributo self._elementos no tiene anotación de tipo. Está
#   declarado como una lista vacía sin indicar que contiene elementos de
#   tipo T. mypy no puede inferir la relación con el TypeVar.
#   Solución: anotar como self._elementos: list[T] = [].
#
# Error 2: El método "apilar" no anota el parámetro "elemento" con el tipo T.
#   Sin esta anotación, mypy trata el parámetro como Any y no verifica que
#   el tipo coincida con el parámetro genérico de la clase.
#   Solución: anotar como elemento: T.
#
# Error 3: El método "desapilar" usa pop(0), que extrae el primer elemento
#   (comportamiento de cola/FIFO), no el último (comportamiento de pila/LIFO).
#   Una pila extrae el último elemento añadido. Solución: usar pop() sin
#   argumento, que extrae el último elemento.
#
# ERRORES CORREGIDOS:
# 1. self._elementos = [] → self._elementos: list[T] = []
# 2. elemento → elemento: T
# 3. pop(0) → pop()

from typing import TypeVar, Generic

T = TypeVar("T")


class Pila(Generic[T]):
    def __init__(self) -> None:
        self._elementos: list[T] = []

    def apilar(self, elemento: T) -> None:
        self._elementos.append(elemento)

    def desapilar(self) -> T:
        return self._elementos.pop()

    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0


# Pruebas
pila_numeros: Pila[int] = Pila()
pila_numeros.apilar(1)
pila_numeros.apilar(2)
pila_numeros.apilar(3)
print(pila_numeros.desapilar())
print(pila_numeros.desapilar())
print(pila_numeros.esta_vacia())

pila_textos: Pila[str] = Pila()
pila_textos.apilar("hola")
pila_textos.apilar("mundo")
print(pila_textos.desapilar())
print(pila_textos.desapilar())
print(pila_textos.esta_vacia())
