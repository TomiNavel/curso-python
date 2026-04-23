# =============================================================================
# SOLUCIÓN
# =============================================================================

import logging
import sys

logger = logging.getLogger("miapp")
logger.setLevel(logging.DEBUG)

# Limpiamos handlers previos para evitar duplicados si el mismo intérprete
# ejecuta este código varias veces.
logger.handlers.clear()
# También desactivamos la propagación al root para que los mensajes no
# salgan duplicados por la configuración por defecto del root logger.
logger.propagate = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))

logger.addHandler(handler)


# Pruebas
logger.debug("detalle interno")
logger.info("operación iniciada")
logger.warning("recurso casi agotado")
logger.error("operación fallida")
