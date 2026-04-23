# =====================
# SOLUCIÓN
# =====================
# Error 1: "saldo[0] += 1" no está protegido por el lock, pese a que el
#   lock está definido. En Python puro bajo CPython, el GIL no garantiza
#   atomicidad de "+=" sobre elementos de listas, así que varios threads
#   pueden solapar lectura/escritura y perder incrementos. El código debe
#   usar "with lock:" en la sección crítica.
#   Solución: envolver saldo[0] += 1 en un with lock.
#
# Error 2: args=250 pasa un int donde Thread espera un iterable de
#   argumentos. Lanza TypeError al intentar desempaquetar. El patrón
#   correcto es args=(250,) con la coma para hacerla tupla.
#   Solución: args=(250,).
#
# Error 3: el bucle final con "pass" no hace join, deja los threads
#   corriendo. El print puede ejecutarse antes de que terminen y mostrar
#   un valor intermedio.
#   Solución: t.join() dentro del bucle.
#
# ERRORES CORREGIDOS:
# 1. saldo[0] += 1 sin lock → envolver en with lock
# 2. args=250 → args=(250,) para formar tupla
# 3. bucle final con pass → t.join()

import threading

saldo = [0]
lock = threading.Lock()


def incrementar(n):
    for _ in range(n):
        with lock:
            saldo[0] += 1


threads = []
for _ in range(4):
    t = threading.Thread(target=incrementar, args=(250,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(saldo[0])
