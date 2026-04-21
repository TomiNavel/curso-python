# =============================================================================
# EJERCICIO 2: Generador Fibonacci
# =============================================================================
# Escribe una función generadora "fibonacci" que produzca los primeros "n"
# números de la sucesión de Fibonacci, en la que cada número es la suma de los
# dos anteriores, comenzando por 0 y 1.
#
# Requisitos:
# - Debe ser una función generadora (usar yield)
# - No puedes construir una lista intermedia
# - Si "n" es 0, no debe producir ningún valor
#
# RESULTADO ESPERADO:
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
# [0, 1, 1, 2, 3]
# []
# =============================================================================


# Tu código aquí


# Tests
print(list(fibonacci(10)))
print(list(fibonacci(5)))
print(list(fibonacci(0)))
