# =====================
# SOLUCIÓN
# =====================
# Error 1: pool.submit(procesar(n)) llama a procesar PRIMERO en el thread
#   principal y pasa su resultado a submit. Cuando n=-3, procesar lanza
#   ValueError antes incluso de submit, y todo el programa falla. El
#   patrón correcto es pool.submit(procesar, n), pasando la función sin
#   llamar y los argumentos aparte.
#   Solución: pool.submit(procesar, n).
#
# Error 2: f.result() relanza la excepción si la tarea falló. Sin try/except
#   alrededor, el ValueError del n=-3 rompe toda la función. El enunciado
#   pide que esas excepciones se conviertan en None y el flujo continúe.
#   Solución: envolver result() en try/except ValueError (o Exception).
#
# Error 3: el pool se crea con ThreadPoolExecutor() sin usar context
#   manager ni llamar a shutdown. Los workers quedan vivos indefinidamente.
#   En código corto no suele romper nada pero es una fuga de recursos.
#   Lo idiomático es el patrón "with ThreadPoolExecutor(...) as pool:".
#   Solución: usar "with" para cerrar el pool automáticamente.
#
# ERRORES CORREGIDOS:
# 1. submit(procesar(n)) → submit(procesar, n)
# 2. f.result() sin try/except → capturar excepción y poner None
# 3. pool sin context manager → with ThreadPoolExecutor(...) as pool

from concurrent.futures import ThreadPoolExecutor


def procesar(n):
    if n < 0:
        raise ValueError("no admite negativos")
    return n * 10


def lanzar(numeros):
    resultados = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(procesar, n) for n in numeros]
        for f in futures:
            try:
                resultados.append(f.result())
            except ValueError:
                resultados.append(None)
    return resultados


# Pruebas
print(lanzar([1, 2, -3, 4]))
