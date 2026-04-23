# =====================
# SOLUCIÓN
# =====================
# Error 1: "operacion" está definida como función normal (def). Aunque
#   devuelve valores ejecutando código síncrono puro, gather espera
#   awaitables. Pasar funciones normales a gather produce un TypeError
#   al no poder "awaitar" un int. Debe ser async def.
#   Solución: cambiar def por async def. Añadimos un await asyncio.sleep
#   trivial para que sea efectivamente una corrutina.
#
# Error 2: falta await delante de asyncio.gather. gather devuelve un
#   awaitable; sin await, "resultados" es un objeto awaitable sin
#   ejecutar, no una lista de resultados. La iteración posterior
#   falla.
#   Solución: añadir await.
#
# Error 3: sin return_exceptions=True, la primera excepción cancela
#   todas las demás corrutinas y se propaga al llamador. Para que las
#   excepciones aparezcan como elementos de la lista (y poder
#   convertirlas a None), hace falta return_exceptions=True.
#   Solución: pasar return_exceptions=True a gather.
#
# ERRORES CORREGIDOS:
# 1. def operacion → async def operacion
# 2. asyncio.gather(...) sin await → await asyncio.gather(...)
# 3. falta return_exceptions=True para no cancelar el resto

import asyncio


async def operacion(valor):
    await asyncio.sleep(0.01)
    if valor < 0:
        raise ValueError("valor inválido")
    return valor * 10


async def lanzar(valores):
    resultados = await asyncio.gather(
        *[operacion(v) for v in valores],
        return_exceptions=True,
    )
    return [r if not isinstance(r, Exception) else None for r in resultados]


print(await lanzar([1, 2, -3, 4]))
