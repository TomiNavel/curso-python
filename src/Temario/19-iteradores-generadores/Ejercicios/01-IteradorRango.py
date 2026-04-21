# =============================================================================
# EJERCICIO 1: Iterador personalizado — Rango descendente
# =============================================================================
# Implementa una clase "RangoDescendente" que funcione como un iterador y
# produzca números desde "inicio" (incluido) hasta "fin" (excluido), decreciendo
# de uno en uno. La clase debe implementar el protocolo de iteración completo:
# __iter__ y __next__, lanzando StopIteration cuando se agota la secuencia.
#
# Requisitos:
# - "inicio" siempre es mayor que "fin"
# - No puedes usar range() ni reversed() para generar los valores
# - La clase debe poder usarse en un bucle for y en list()
#
# RESULTADO ESPERADO:
# [10, 9, 8, 7, 6]
# 5
# 4
# 3
# =============================================================================


# Tu código aquí


# Tests
print(list(RangoDescendente(10, 5)))

for n in RangoDescendente(5, 2):
    print(n)
