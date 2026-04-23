# =============================================================================
# SOLUCIÓN
# =============================================================================

import threading


def incrementar_n_veces(contador, n, lock):
    # El "with lock:" adquiere el lock al entrar y lo libera al salir,
    # incluso si hay excepción. Es el patrón idiomático; llamar a
    # acquire() y release() manualmente es más frágil.
    for _ in range(n):
        with lock:
            contador[0] += 1


contador = [0]
lock = threading.Lock()
threads = []

for _ in range(5):
    t = threading.Thread(target=incrementar_n_veces, args=(contador, 100, lock))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(contador[0])
