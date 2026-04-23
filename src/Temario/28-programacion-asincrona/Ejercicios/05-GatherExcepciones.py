# =============================================================================
# EJERCICIO 5: gather con return_exceptions
# =============================================================================
# La función "operacion(valor)" devuelve valor*2 si valor es positivo, y
# lanza ValueError si es negativo.
#
# Usa asyncio.gather con return_exceptions=True para ejecutar varias
# llamadas EN PARALELO sin que el fallo de una cancele las otras.
#
# Después, filtra los resultados: devuelve una lista solo con los valores
# numéricos (descarta las excepciones, no las conviertas a None).
#
# RESULTADO ESPERADO:
# [2, 4, 10]
# =============================================================================

import asyncio


async def operacion(valor):
    await asyncio.sleep(0.01)
    if valor < 0:
        raise ValueError(f"valor inválido: {valor}")
    return valor * 2


# Tu código aquí
# - Lanza operacion() para [1, 2, -1, 5, -3] con gather y
#   return_exceptions=True.
# - Filtra los resultados para quedarte solo con los números.
# - Imprime la lista filtrada.
