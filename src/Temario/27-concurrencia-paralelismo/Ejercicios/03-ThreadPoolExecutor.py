# =============================================================================
# EJERCICIO 3: Usar ThreadPoolExecutor.map
# =============================================================================
# La función "cuadrado(n)" devuelve n*n. Usa ThreadPoolExecutor con
# max_workers=4 para aplicar "cuadrado" a una lista de números usando
# el método map del pool.
#
# pool.map devuelve los resultados en el mismo orden que la entrada,
# incluso si los threads terminan en distinto orden.
#
# Devuelve la lista de resultados.
#
# RESULTADO ESPERADO:
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# =============================================================================

from concurrent.futures import ThreadPoolExecutor


def cuadrado(n):
    return n * n


def cuadrados_en_paralelo(numeros):
    # Tu código aquí
    pass


# Pruebas
print(cuadrados_en_paralelo([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
