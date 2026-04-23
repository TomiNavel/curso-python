# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Timeout y cancelación
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "consultar_con_timeout(duracion, timeout)":
#   - intenta ejecutar "operacion(duracion)" con el timeout dado.
#   - si acaba a tiempo, devuelve su resultado.
#   - si se pasa del timeout, devuelve "timeout" (sin propagar la
#     excepción al llamador).
#
# RESULTADO ESPERADO:
# ok
# timeout
# =============================================================================

import asyncio


async def operacion(duracion):
    await asyncio.sleep(duracion)
    return "ok"


async def consultar_con_timeout(duracion, timeout):
    try:
        return asyncio.wait_for(operacion(duracion), timeout)
    except TimeoutError:
        return "timeout"


print(await consultar_con_timeout(0.1, 0.5))
print(await consultar_con_timeout(0.5, 0.1))
