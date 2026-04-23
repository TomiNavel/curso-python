# =============================================================================
# EJERCICIO 1: Tu primera corrutina
# =============================================================================
# Define una función asíncrona "saludar(nombre)" que:
#   - espere 0.1 segundos con asyncio.sleep.
#   - devuelva el string f"Hola, {nombre}".
#
# Después ejecútala dos veces (con "Ana" y "Luis") y muestra los
# resultados con print.
#
# Nota: en este entorno ya hay un event loop activo, así que usamos
# "await" directamente al nivel superior. En CPython normal el patrón
# sería:
#     async def main():
#         ...
#     asyncio.run(main())
#
# RESULTADO ESPERADO:
# Hola, Ana
# Hola, Luis
# =============================================================================

import asyncio


# Tu código aquí: define saludar


# Ejecutar y mostrar resultados
# Tu código aquí: dos await y dos print
