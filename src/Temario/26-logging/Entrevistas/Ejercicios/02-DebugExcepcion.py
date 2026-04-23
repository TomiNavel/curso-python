# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Logging de excepciones
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "dividir_seguro" debe calcular a/b, y si falla debe:
#   - loggear el error como ERROR con traceback incluido.
#   - devolver None (no relanzar la excepción).
#   - registrar que la operación terminó con un INFO, haya salido bien o no.
#
# RESULTADO ESPERADO:
# INFO - operación completada
# 5.0
# ERROR - error al dividir 10 / 0
# Traceback (most recent call last):
#   ...
# ZeroDivisionError: division by zero
# INFO - operación completada
# None
# =============================================================================

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    stream=sys.stdout,
    force=True,
)

logger = logging.getLogger("calculo")


def dividir_seguro(a, b):
    try:
        resultado = a / b
    except ZeroDivisionError as e:
        logger.error(e)
        return None
    logging.info("operación completada")
    return resultado


# Pruebas
print(dividir_seguro(10, 2))
print(dividir_seguro(10, 0))
