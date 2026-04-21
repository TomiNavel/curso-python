# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Clase genérica Pila
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# 3
# 2
# False
# mundo
# hola
# True
# =============================================================================

from typing import TypeVar, Generic

T = TypeVar("T")


class Pila(Generic[T]):
    def __init__(self) -> None:
        self._elementos = []

    def apilar(self, elemento) -> None:
        self._elementos.append(elemento)

    def desapilar(self) -> T:
        return self._elementos.pop(0)

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
