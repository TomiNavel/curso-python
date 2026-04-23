# =============================================================================
# EJERCICIO 3: Timeout en una operación asíncrona
# =============================================================================
# Escribe una función "consultar(timeout, duracion_real)" que llame a
# "operacion(duracion_real)" usando asyncio.wait_for con el timeout dado.
#   - Si la operación termina a tiempo, devuelve "ok".
#   - Si supera el timeout, captura asyncio.TimeoutError y devuelve
#     "timeout".
#
# La función "operacion" espera "duracion_real" segundos y devuelve "ok".
#
# RESULTADO ESPERADO:
# ok
# timeout
# =============================================================================

import asyncio


async def operacion(duracion_real):
    await asyncio.sleep(duracion_real)
    return "ok"


async def consultar(timeout, duracion_real):
    # Tu código aquí
    pass


# Pruebas
print(await consultar(timeout=0.5, duracion_real=0.1))   # termina en 0.1s → "ok"
print(await consultar(timeout=0.1, duracion_real=0.5))   # supera el timeout → "timeout"
