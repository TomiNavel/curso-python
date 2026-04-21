# =============================================================================
# EJERCICIO 4: Aplanar listas anidadas con yield from
# =============================================================================
# Escribe una función generadora recursiva "aplanar" que reciba una lista que
# puede contener elementos o sublistas (anidadas a cualquier profundidad) y
# produzca todos los elementos de forma plana, en el mismo orden.
#
# Requisitos:
# - Debe ser un generador (usar yield o yield from)
# - Debe funcionar con cualquier nivel de anidamiento
# - Usa yield from para delegar en la llamada recursiva
# - Considera como "lista" cualquier objeto de tipo list
#
# RESULTADO ESPERADO:
# [1, 2, 3, 4, 5]
# [1, 2, 3, 4, 5, 6]
# ['a', 'b', 'c', 'd']
# =============================================================================


# Tu código aquí


# Tests
print(list(aplanar([1, [2, 3], [4, [5]]])))
print(list(aplanar([[1, 2], [3, [4, [5, [6]]]]])))
print(list(aplanar(["a", ["b", ["c"], "d"]])))
