# =============================================================================
# SOLUCIÓN
# =============================================================================

import asyncio


async def trabajo_lento(segundos, valor):
    await asyncio.sleep(segundos)
    return valor


# asyncio.gather recibe awaitables (corrutinas ya llamadas) y los ejecuta
# concurrentemente. Devuelve una lista con los resultados en el mismo
# orden que los argumentos, no en el orden en que acaben.
resultados = await asyncio.gather(
    trabajo_lento(0.1, "A"),
    trabajo_lento(0.1, "B"),
    trabajo_lento(0.1, "C"),
)

print(resultados)
