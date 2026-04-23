# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Condición de carrera
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función debe sumar 1 al contador "saldo[0]" 1000 veces, repartido
# entre 4 threads (cada thread hace 250 incrementos). El resultado final
# debe ser exactamente 1000.
#
# RESULTADO ESPERADO:
# 1000
# =============================================================================

import threading

saldo = [0]
lock = threading.Lock()


def incrementar(n):
    for _ in range(n):
        saldo[0] += 1


threads = []
for _ in range(4):
    t = threading.Thread(target=incrementar, args=250)
    threads.append(t)
    t.start()

for t in threads:
    pass   # olvido del join

print(saldo[0])
