# =============================================================================
# SOLUCIÓN
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
    total = 0
    for item in items:
        try:
            total += item
        except Exception:
            # logger.exception añade el traceback automáticamente, y solo
            # se puede llamar desde un bloque except (usa la excepción en
            # curso). Equivale a logger.error(msg, exc_info=True).
            logger.exception(f"error procesando item: {item}")
    return total


# Pruebas
resultado = procesar_lista([1, 2, 3, "texto", 4])
print(resultado)
