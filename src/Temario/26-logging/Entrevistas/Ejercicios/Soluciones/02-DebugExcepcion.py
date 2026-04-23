# =====================
# SOLUCIÓN
# =====================
# Error 1: logger.error(e) solo registra el mensaje de la excepción, sin
#   traceback. Para incluir el traceback hay que usar logger.exception,
#   que equivale a error(msg, exc_info=True) pero es el patrón idiomático.
#   Además, el mensaje solo ponía la excepción; conviene dar más contexto
#   con los valores involucrados, como pide el enunciado ("error al
#   dividir 10 / 0").
#   Solución: usar logger.exception con un mensaje descriptivo.
#
# Error 2: el INFO se emite con logging.info(...) (logger raíz) en lugar
#   del logger configurado "calculo". Hace que el mensaje salga con name
#   "root" y pierde la trazabilidad del módulo. Además, debería emitirse
#   SIEMPRE (haya excepción o no), pero al estar después del try/except
#   solo se ejecuta en el camino feliz; cuando hay error, la función
#   retorna None antes.
#   Solución: usar logger.info (no logging.info) y moverlo a un bloque
#   finally para que se ejecute siempre.
#
# Error 3: aunque funcionalmente no rompe nada, el print del resultado
#   None en el camino de error no es un bug real; pero la combinación
#   anterior hacía que el "INFO operación completada" no apareciera en
#   el caso de error. Al mover el info a finally, el resultado esperado
#   se cumple.
#
# ERRORES CORREGIDOS:
# 1. logger.error(e) sin traceback → logger.exception(mensaje descriptivo)
# 2. logging.info() en root → logger.info() del logger "calculo"
# 3. info solo en camino feliz → moverlo a finally

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
    except ZeroDivisionError:
        logger.exception(f"error al dividir {a} / {b}")
        resultado = None
    finally:
        logger.info("operación completada")
    return resultado


# Pruebas
print(dividir_seguro(10, 2))
print(dividir_seguro(10, 0))
