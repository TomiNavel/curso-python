# =============================================================================
# SOLUCIÓN
# =============================================================================

import asyncio


async def operacion(duracion_real):
    await asyncio.sleep(duracion_real)
    return "ok"


async def consultar(timeout, duracion_real):
    # wait_for lanza asyncio.TimeoutError si la corrutina no termina en
    # el tiempo indicado. También cancela la corrutina en curso para que
    # no siga ejecutándose inútilmente.
    try:
        return await asyncio.wait_for(operacion(duracion_real), timeout=timeout)
    except asyncio.TimeoutError:
        return "timeout"


# Pruebas
print(await consultar(timeout=0.5, duracion_real=0.1))
print(await consultar(timeout=0.1, duracion_real=0.5))
