# =============================================================================
# SOLUCIÓN
# =============================================================================

import logging
import sys

# force=True garantiza que basicConfig se aplique aunque ya hubiera otra
# configuración previa (basicConfig se ignora silenciosamente si ya hay
# handlers). stream=sys.stdout dirige los logs al stdout capturado por el
# entorno.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    stream=sys.stdout,
    force=True,
)

logging.debug("detalle interno")             # filtrado por nivel INFO
logging.info("arrancando sistema")
logging.warning("configuración por defecto en uso")
