# =============================================================================
# EJERCICIO 4: Lanzar tareas en segundo plano con create_task
# =============================================================================
# La función "procesar_en_fondo(cola)" debe recoger elementos de la cola
# y añadirlos a una lista "salida". Debe parar al recibir None como
# elemento centinela.
#
# Completa el código para:
#   - crear una Task que ejecute procesar_en_fondo en segundo plano.
#   - poner tres elementos en la cola (1, 2, 3) y luego None.
#   - esperar a que la task termine con await.
#   - imprimir la lista salida.
#
# RESULTADO ESPERADO:
# [1, 2, 3]
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


# Tu código aquí: crear task, alimentar cola, esperar task, imprimir salida
