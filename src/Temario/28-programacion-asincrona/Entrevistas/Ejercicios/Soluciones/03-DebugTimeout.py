# =====================
# SOLUCIÓN
# =====================
# Error 1: falta await delante de asyncio.wait_for. Sin await, la
#   función devuelve un objeto awaitable sin ejecutar — el print mostraría
#   "<coroutine object wait_for...>" en lugar del resultado. Además, la
#   excepción TimeoutError solo puede lanzarse al esperar el awaitable,
#   así que el except nunca se dispara sin await.
#   Solución: añadir await.
#
# Error 2: la excepción capturada es TimeoutError (builtin de Python).
#   asyncio.wait_for lanza asyncio.TimeoutError, que en Python <3.11 NO
#   es el mismo que el TimeoutError builtin. En Python 3.11+ sí se
#   unificaron, pero por compatibilidad y claridad se captura siempre
#   asyncio.TimeoutError.
#   Solución: capturar asyncio.TimeoutError.
#
# Error 3: el argumento de wait_for se pasa posicional como "timeout",
#   pero la firma es wait_for(aw, timeout=...). Funciona por posición,
#   pero ser explícito con timeout=timeout mejora la legibilidad y
#   evita errores si la firma cambia. Este es el error más leve de los
#   tres.
#   Solución: usar timeout=timeout como kwarg.
#
# ERRORES CORREGIDOS:
# 1. asyncio.wait_for sin await → añadir await
# 2. except TimeoutError → except asyncio.TimeoutError
# 3. timeout posicional → timeout=timeout por legibilidad

import asyncio


async def operacion(duracion):
    await asyncio.sleep(duracion)
    return "ok"


async def consultar_con_timeout(duracion, timeout):
    try:
        return await asyncio.wait_for(operacion(duracion), timeout=timeout)
    except asyncio.TimeoutError:
        return "timeout"


print(await consultar_con_timeout(0.1, 0.5))
print(await consultar_con_timeout(0.5, 0.1))
