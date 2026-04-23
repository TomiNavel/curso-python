# =============================================================================
# EJERCICIO 2: Proteger un contador compartido con Lock
# =============================================================================
# La función "incrementar_n_veces(contador, n, lock)" debe incrementar
# "contador[0]" n veces de forma protegida por el lock.
#
# Usa "contador" como lista de un único elemento para que sea mutable
# entre threads (una variable int no se comparte si se reasigna).
#
# Lanza 5 threads, cada uno haciendo 100 incrementos. Al final el
# contador debe valer 500 exactamente.
#
# RESULTADO ESPERADO:
# 500
# =============================================================================

import threading


def incrementar_n_veces(contador, n, lock):
    # Tu código aquí
    pass


contador = [0]
lock = threading.Lock()
threads = []

# Tu código aquí: lanza 5 threads de 100 incrementos cada uno y espera


print(contador[0])
