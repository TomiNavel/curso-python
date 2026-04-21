# =====================
# SOLUCIÓN
# =====================
# Error 1: Falta el método __iter__. Sin él, la clase no es iterable y list()
#   lanza "TypeError: 'Pares' object is not iterable". Solución: añadir
#   "def __iter__(self): return self" para declarar que la instancia es su
#   propio iterador.
#
# Error 2: Cuando se agota la secuencia, el método usa "return" en lugar de
#   lanzar StopIteration. Un iterador señala el fin de la iteración lanzando
#   StopIteration, no con un return. Solución: sustituir "return" por
#   "raise StopIteration".
#
# Error 3: El incremento es "self.actual += 1", que produce todos los números
#   (pares e impares), no solo los pares. Solución: usar "self.actual += 2"
#   para avanzar únicamente por los pares.
#
# ERRORES CORREGIDOS:
# 1. Añadir __iter__ que devuelva self
# 2. Lanzar StopIteration en lugar de usar return
# 3. Incrementar de 2 en 2 para producir solo números pares


class Pares:
    def __init__(self, limite):
        self.limite = limite
        self.actual = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual >= self.limite:
            raise StopIteration
        valor = self.actual
        self.actual += 2
        return valor


print(list(Pares(10)))
print(list(Pares(6)))
