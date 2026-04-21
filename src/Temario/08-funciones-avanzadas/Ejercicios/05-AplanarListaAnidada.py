# =============================================================================
# EJERCICIO 5: Aplanar Lista Anidada
# =============================================================================
# Crea una función recursiva que aplane listas con cualquier nivel de
# anidamiento.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# [1, 2, 3, 4, 5, 6]
# [1, 2, 3, 4, 5, 6, 7]
# ['a', 'b', 'c', 'd', 'e']
# [1, 2, 3]
# =============================================================================

# PASO 1: Define una función "aplanar" que reciba una lista. Recorre cada
# elemento: si es una lista (usa isinstance(elemento, list)), llama a
# "aplanar" recursivamente y extiende el resultado. Si no es una lista,
# lo añade directamente. Devuelve la lista aplanada.
# Prueba con: [1, [2, 3], [4, [5, 6]]]

# Tu código aquí

# PASO 2: Prueba con una lista más profunda: [1, [2, [3, [4, [5, [6, [7]]]]]]]

# Tu código aquí

# PASO 3: Prueba con strings y anidamiento mixto: ["a", ["b", "c"], [["d"], "e"]]

# Tu código aquí

# PASO 4: Prueba con una lista sin anidamiento: [1, 2, 3]
# (debe devolver la misma lista sin cambios)

# Tu código aquí
