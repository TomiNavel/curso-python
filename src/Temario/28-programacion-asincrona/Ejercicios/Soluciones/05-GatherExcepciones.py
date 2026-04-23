# =============================================================================
# SOLUCIÓN
# =============================================================================

import asyncio


async def operacion(valor):
    await asyncio.sleep(0.01)
    if valor < 0:
        raise ValueError(f"valor inválido: {valor}")
    return valor * 2


# Con return_exceptions=True, las excepciones aparecen como ELEMENTOS de
# la lista en lugar de propagarse. Esto permite procesar las que salieron
# bien sin que una mala las cancele todas.
crudos = await asyncio.gather(
    *[operacion(v) for v in [1, 2, -1, 5, -3]],
    return_exceptions=True,
)

numericos = [r for r in crudos if not isinstance(r, Exception)]

print(numericos)
