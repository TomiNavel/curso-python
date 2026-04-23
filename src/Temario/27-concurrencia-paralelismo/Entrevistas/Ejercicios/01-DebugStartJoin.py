# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Threads secuenciales
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es lanzar 3 threads que añaden su nombre a la lista
# "resultados". Deben ejecutarse concurrentemente (no secuencialmente)
# y al final la lista debe contener los 3 nombres.
#
# RESULTADO ESPERADO (orden puede variar):
# 3
# =============================================================================

import threading


def trabajar(nombre, resultados):
    resultados.append(nombre)


resultados = []
threads = []

for nombre in ["A", "B", "C"]:
    t = threading.Thread(target=trabajar(nombre, resultados))
    t.start()
    t.join()

print(len(resultados))
