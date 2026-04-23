# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — await olvidado y sleep bloqueante
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función debe ejecutar dos tareas concurrentes que tardan 0.1s cada
# una (en total ≈0.1s, NO 0.2s) y devolver sus resultados sumados.
#
# RESULTADO ESPERADO:
# 15
# =============================================================================

import asyncio
import time


def calcular(valor):
    time.sleep(0.1)
    return valor


async def main():
    r1 = calcular(5)
    r2 = calcular(10)
    return r1 + r2


print(await main())
