# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — ThreadPoolExecutor mal utilizado
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es lanzar varias tareas con submit, recoger los resultados
# manejando excepciones (convirtiéndolas en None), y devolver la lista
# en el mismo orden que la entrada.
#
# La función "procesar(n)" devuelve n*10 si n es positivo, y lanza
# ValueError si es negativo.
#
# RESULTADO ESPERADO:
# [10, 20, None, 40]
# =============================================================================

from concurrent.futures import ThreadPoolExecutor


def procesar(n):
    if n < 0:
        raise ValueError("no admite negativos")
    return n * 10


def lanzar(numeros):
    pool = ThreadPoolExecutor(max_workers=4)
    futures = [pool.submit(procesar(n)) for n in numeros]
    resultados = []
    for f in futures:
        resultados.append(f.result())
    return resultados


# Pruebas
print(lanzar([1, 2, -3, 4]))
