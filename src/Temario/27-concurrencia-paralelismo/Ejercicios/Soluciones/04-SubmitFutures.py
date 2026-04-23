# =============================================================================
# SOLUCIÓN
# =============================================================================

from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


def dividir_parejas(parejas):
    resultados = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        # submit devuelve un Future por cada tarea. Al recorrer los futures
        # en el mismo orden que las entradas, la lista de resultados
        # preserva el orden original.
        futures = [pool.submit(dividir, a, b) for a, b in parejas]
        for f in futures:
            try:
                resultados.append(f.result())
            except Exception:
                resultados.append(None)
    return resultados


# Pruebas
print(dividir_parejas([(10, 2), (8, 4), (5, 0), (7, 7)]))
