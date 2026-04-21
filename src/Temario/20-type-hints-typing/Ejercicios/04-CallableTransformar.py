# =============================================================================
# EJERCICIO 4: Callable — transformar lista
# =============================================================================
# Implementa una función "transformar_lista" que reciba una lista de enteros
# y una función de transformación (int -> int), y devuelva una nueva lista
# con la transformación aplicada a cada elemento.
#
# Anota el parámetro de la función de transformación usando Callable.
#
# RESULTADO ESPERADO:
# [1, 4, 9, 16, 25]
# [2, 4, 6, 8, 10]
# [0, 1, 2, 3, 4]
# =============================================================================

# Tu código aquí


# Pruebas
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x ** 2))
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x * 2))
print(transformar_lista([1, 2, 3, 4, 5], lambda x: x - 1))
