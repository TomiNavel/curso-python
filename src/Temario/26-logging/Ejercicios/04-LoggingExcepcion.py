# =============================================================================
# EJERCICIO 4: Loggear excepciones con traceback
# =============================================================================
# La función "procesar_lista(items)" suma los valores numéricos de una
# lista. Si al procesar un elemento ocurre una excepción, debe:
#   - loggear el error usando logger.exception(...) con un mensaje que
#     incluya el item problemático. Este método añade automáticamente
#     el traceback al log.
#   - continuar con los demás elementos (no relanzar).
#
# Al final devuelve la suma de los elementos procesados correctamente.
#
# RESULTADO ESPERADO (el traceback varía; lo importante es que aparezca):
# ERROR - error procesando item: texto
# Traceback (most recent call last):
#   ...
# TypeError: unsupported operand type(s) for +=: 'int' and 'str'
# 10
# =============================================================================

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    stream=sys.stdout,
    force=True,
)

logger = logging.getLogger("app")


def procesar_lista(items):
    # Tu código aquí
    pass


# Pruebas: "texto" provoca TypeError al sumarlo a un int
resultado = procesar_lista([1, 2, 3, "texto", 4])
print(resultado)
