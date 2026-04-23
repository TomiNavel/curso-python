# =====================
# SOLUCIÓN
# =====================
# Error 1: target=trabajar(nombre, resultados) LLAMA a la función en el
#   thread principal y le pasa su resultado (None) como target al Thread.
#   El Thread no tiene nada que ejecutar. La forma correcta es pasar la
#   función sin llamar y los argumentos con args=(...).
#   Solución: target=trabajar, args=(nombre, resultados).
#
# Error 2: start y join dentro del mismo bucle. Esto hace que cada thread
#   termine antes de arrancar el siguiente, perdiendo toda la concurrencia.
#   Secuencial vestido de threads. La forma correcta es arrancar todos
#   primero y luego hacer join a todos.
#   Solución: dos bucles: uno para start+append a lista, otro para join.
#
# Error 3: la lista "threads" se declara pero no se usa. Hay que guardar
#   cada thread creado para poder hacer join después. Sin esta lista, el
#   segundo bucle no tendría a qué iterar.
#   Solución: append de t a threads después de start.
#
# ERRORES CORREGIDOS:
# 1. target=trabajar(nombre, resultados) → target=trabajar, args=(nombre, resultados)
# 2. start+join en el mismo bucle → dos bucles separados
# 3. la lista threads no se rellena → añadir t con append

import threading


def trabajar(nombre, resultados):
    resultados.append(nombre)


resultados = []
threads = []

for nombre in ["A", "B", "C"]:
    t = threading.Thread(target=trabajar, args=(nombre, resultados))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(len(resultados))
