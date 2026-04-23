# =============================================================================
# EJERCICIO 1: Crear y arrancar threads
# =============================================================================
# Completa la función "lanzar_tareas(tareas)" que reciba una lista de
# tuplas (nombre, resultado) y lance un thread por cada una. Cada thread
# debe ejecutar "trabajar(nombre, resultado, salida)", que añade
# (nombre, resultado) a la lista "salida".
#
# La función debe esperar a que todos los threads terminen (join) antes
# de devolver la lista "salida".
#
# Nota: en este entorno los threads no corren realmente en paralelo, pero
# la API y el orden de start/join son los mismos que en Python nativo.
#
# RESULTADO ESPERADO (orden puede variar entre ejecuciones):
# 3
# =============================================================================

import threading


def trabajar(nombre, resultado, salida):
    salida.append((nombre, resultado))


def lanzar_tareas(tareas):
    salida = []
    # Tu código aquí
    return salida


# Pruebas
resultados = lanzar_tareas([("A", 1), ("B", 2), ("C", 3)])
print(len(resultados))
