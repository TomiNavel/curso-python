# =============================================================================
# EJERCICIO 2: Ejecutar varias corrutinas en paralelo con gather
# =============================================================================
# La función "trabajo_lento(segundos, valor)" espera el tiempo indicado
# y devuelve el valor. Usa asyncio.gather para ejecutar tres instancias
# EN PARALELO y recoger los tres resultados.
#
# Si se hiciera await secuencial, tardaría 0.3s. Con gather, las tres
# tareas se solapan y el tiempo total es aproximadamente 0.1s.
#
# Imprime la lista de resultados.
#
# RESULTADO ESPERADO:
# ['A', 'B', 'C']
# =============================================================================

import asyncio


async def trabajo_lento(segundos, valor):
    await asyncio.sleep(segundos)
    return valor


# Tu código aquí: usa asyncio.gather para lanzar 3 llamadas a trabajo_lento
# con (0.1, "A"), (0.1, "B"), (0.1, "C") y recoge los resultados.
