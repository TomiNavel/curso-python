# =====================
# SOLUCIÓN
# =====================
# Error 1: "calcular" está definida como función síncrona (def) y usa
#   time.sleep (bloqueante). Desde una corrutina, time.sleep congela el
#   event loop durante toda la espera, anulando cualquier concurrencia.
#   Debe ser async def con asyncio.sleep.
#   Solución: convertir calcular a async def y usar asyncio.sleep.
#
# Error 2: "r1 = calcular(5)" y "r2 = calcular(10)" son llamadas a una
#   función normal. Si calcular se vuelve async, estas llamadas NO
#   ejecutan el cuerpo — solo crean objetos coroutine. Hay que usar
#   await (y hacerlo en paralelo con gather para aprovechar la
#   concurrencia).
#   Solución: usar asyncio.gather para lanzar las dos tareas en paralelo.
#
# Error 3: sin gather, aunque se pusiera "await calcular(...)", las dos
#   llamadas irían secuenciales (0.2s total en lugar de 0.1s). El
#   enunciado pide ejecución concurrente.
#   Solución: envolver las dos corrutinas en asyncio.gather.
#
# ERRORES CORREGIDOS:
# 1. def calcular + time.sleep → async def calcular + asyncio.sleep
# 2. calcular(5) sin await → await (o gather) sobre corrutinas async
# 3. ejecución secuencial → asyncio.gather para paralelismo

import asyncio


async def calcular(valor):
    await asyncio.sleep(0.1)
    return valor


async def main():
    r1, r2 = await asyncio.gather(calcular(5), calcular(10))
    return r1 + r2


print(await main())
