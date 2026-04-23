# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — gather con errores
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función debe ejecutar varias operaciones en paralelo; si alguna
# falla, debe devolverse None para esa posición pero las otras deben
# completarse con su resultado.
#
# Entrada: [1, 2, -3, 4]
# "operacion" devuelve valor*10 o lanza ValueError si es negativo.
#
# RESULTADO ESPERADO:
# [10, 20, None, 40]
# =============================================================================

import asyncio


def operacion(valor):
    if valor < 0:
        raise ValueError("valor inválido")
    return valor * 10


async def lanzar(valores):
    resultados = asyncio.gather(*[operacion(v) for v in valores])
    return [r if not isinstance(r, ValueError) else None for r in resultados]


print(await lanzar([1, 2, -3, 4]))
