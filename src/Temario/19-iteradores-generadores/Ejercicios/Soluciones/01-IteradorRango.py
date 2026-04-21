# =====================
# SOLUCIÓN
# =====================
# La clase implementa el protocolo de iteración completo:
# - __iter__ devuelve self porque la propia instancia actúa como iterador
# - __next__ produce el siguiente valor y lanza StopIteration al llegar al fin
# El atributo "actual" guarda el estado entre llamadas a __next__, que es lo
# que permite al iterador recordar por dónde iba.


class RangoDescendente:
    def __init__(self, inicio, fin):
        self.actual = inicio
        self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual <= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual -= 1
        return valor


print(list(RangoDescendente(10, 5)))

for n in RangoDescendente(5, 2):
    print(n)
