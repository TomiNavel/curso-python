# =====================
# SOLUCIÓN
# =====================
# Error 1: hay dos llamadas a basicConfig. Por defecto, la segunda se
#   ignora silenciosamente porque el root logger ya tiene handlers tras
#   la primera. El nivel INFO, el formato nuevo y el stream personalizado
#   no se aplican. Solución: pasar force=True a la segunda llamada para
#   que reemplace la configuración previa.
#
# Error 2: el formato usa "%(LEVELNAME)s" en mayúsculas. Los atributos
#   del log record son case-sensitive: el correcto es "%(levelname)s".
#   El marcador en mayúsculas simplemente no se sustituye y saldría
#   literal en el mensaje.
#   Solución: cambiar LEVELNAME por levelname.
#
# Error 3: el stream es sys.stderr, pero el enunciado pide sys.stdout.
#   Solución: cambiar a sys.stdout.
#
# ERRORES CORREGIDOS:
# 1. segundo basicConfig ignorado → añadir force=True
# 2. %(LEVELNAME)s → %(levelname)s
# 3. stream=sys.stderr → stream=sys.stdout

import logging
import sys

logging.basicConfig(level=logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stdout,
    force=True,
)

logging.debug("detalle interno")
logging.info("sistema arrancado")
logging.warning("configuración por defecto")
logging.error("conexión rechazada")
