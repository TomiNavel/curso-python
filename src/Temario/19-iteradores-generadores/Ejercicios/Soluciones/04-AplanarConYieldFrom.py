# =====================
# SOLUCIÓN
# =====================
# El generador recorre la lista recibida. Si el elemento actual es otra lista,
# delega la iteración mediante "yield from aplanar(elemento)", que produce
# todos los valores del sub-generador como si fuesen propios. Si no es una
# lista, simplemente lo emite con yield. La recursión se detiene cuando se
# llega a elementos que no son listas, que se producen directamente.
# Este patrón es el uso canónico de yield from: delegar en un sub-generador
# para aplanar estructuras arbitrariamente anidadas sin bucles explícitos.


def aplanar(lista):
    for elemento in lista:
        if isinstance(elemento, list):
            yield from aplanar(elemento)
        else:
            yield elemento


print(list(aplanar([1, [2, 3], [4, [5]]])))
print(list(aplanar([[1, 2], [3, [4, [5, [6]]]]])))
print(list(aplanar(["a", ["b", ["c"], "d"]])))
