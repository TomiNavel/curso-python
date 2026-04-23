# =============================================================================
# SOLUCIÓN
# =============================================================================

from concurrent.futures import ThreadPoolExecutor


def cuadrado(n):
    return n * n


def cuadrados_en_paralelo(numeros):
    # El context manager asegura que el pool se cierre correctamente al
    # terminar, esperando a que todas las tareas en curso acaben.
    # list() consume el iterador que devuelve map; sin él, map devolvería
    # un iterador perezoso.
    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(pool.map(cuadrado, numeros))


# Pruebas
print(cuadrados_en_paralelo([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
