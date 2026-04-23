# =============================================================================
# SOLUCIÓN
# =============================================================================

import threading


def trabajar(nombre, resultado, salida):
    salida.append((nombre, resultado))


def lanzar_tareas(tareas):
    salida = []
    threads = []
    # Primero se crean y arrancan todos los threads, luego se espera a
    # todos con join. Arrancarlos y esperarlos en el mismo bucle haría
    # que cada thread terminara antes de arrancar el siguiente, perdiendo
    # la concurrencia.
    for nombre, resultado in tareas:
        t = threading.Thread(target=trabajar, args=(nombre, resultado, salida))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return salida


# Pruebas
resultados = lanzar_tareas([("A", 1), ("B", 2), ("C", 3)])
print(len(resultados))
