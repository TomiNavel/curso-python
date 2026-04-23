# =============================================================================
# EJERCICIO 4: submit y Future
# =============================================================================
# La función "dividir(a, b)" devuelve a/b, o lanza ZeroDivisionError si
# b es 0. Usa ThreadPoolExecutor.submit para lanzar varias tareas y
# recupera los resultados con .result().
#
# Escribe la función "dividir_parejas(parejas)" que recibe una lista de
# tuplas (a, b) y devuelve una lista con los resultados. Si alguna tarea
# lanza excepción, captúrala y pon None en su lugar.
#
# Pista: .result() de un Future relanza la excepción si la tarea falló.
#
# RESULTADO ESPERADO:
# [5.0, 2.0, None, 1.0]
# =============================================================================

from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


def dividir_parejas(parejas):
    # Tu código aquí
    pass


# Pruebas
print(dividir_parejas([(10, 2), (8, 4), (5, 0), (7, 7)]))
