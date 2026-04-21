# =====================
# SOLUCIÓN
# =====================
# Error 1: __len__ devuelve self.colores (la lista) en lugar de su longitud.
#   __len__ debe devolver un entero, no una lista.
#   Solución: return len(self.colores)
#
# Error 2: __iter__ devuelve self.colores (la lista) directamente.
#   Debería devolver un iterador. Una lista no es un iterador, es un iterable.
#   Solución: return iter(self.colores)
#
# Error 3: (Consecuencia del Error 1) len(p) lanza TypeError porque Python
#   espera un entero de __len__, no una lista.
#   Se resuelve al corregir Error 1.
#
# ERRORES CORREGIDOS:
# 1. return self.colores → return len(self.colores) en __len__
# 2. return self.colores → return iter(self.colores) en __iter__


class Paleta:
    def __init__(self, *colores):
        self.colores = list(colores)

    def __len__(self):
        return len(self.colores)

    def __getitem__(self, indice):
        return self.colores[indice]

    def __iter__(self):
        return iter(self.colores)

    def __contains__(self, color):
        return color in self.colores

    def __repr__(self):
        return f"Paleta({self.colores})"


p = Paleta("rojo", "verde", "azul")
print(f"Longitud: {len(p)}")
print(f"Elemento 0: {p[0]}")
print(" ".join(c for c in p))
print(f"verde está: {'verde' in p}")
