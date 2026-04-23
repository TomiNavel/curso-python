# =============================================================================
# SOLUCIÓN
# =============================================================================

import asyncio

cola = asyncio.Queue()
salida = []


async def procesar_en_fondo(cola):
    while True:
        item = await cola.get()
        if item is None:
            break
        salida.append(item)


# create_task programa la corrutina en el loop y devuelve un objeto Task
# que ya está corriendo. A diferencia de "await corrutina()", no
# bloquea: el flujo principal sigue inmediatamente.
task = asyncio.create_task(procesar_en_fondo(cola))

for i in [1, 2, 3, None]:
    await cola.put(i)

# await sobre la task espera a que termine su ejecución.
await task

print(salida)
