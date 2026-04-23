# =============================================================================
# SOLUCIÓN
# =============================================================================

import asyncio


async def saludar(nombre):
    # asyncio.sleep es la versión asíncrona de time.sleep: no bloquea el
    # event loop, solo suspende esta corrutina durante el tiempo indicado.
    await asyncio.sleep(0.1)
    return f"Hola, {nombre}"


# En CPython normal esto iría dentro de una main() + asyncio.run(main()).
# Aquí aprovechamos que el entorno ya expone un event loop activo.
print(await saludar("Ana"))
print(await saludar("Luis"))
