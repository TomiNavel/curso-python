# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Configuración que no aplica
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es configurar el logging para que:
#   - se muestren mensajes desde INFO en adelante.
#   - el formato sea "[%(levelname)s] %(message)s".
#   - los logs salgan por sys.stdout (no stderr).
#
# Al emitir debug/info/warning/error, solo deben aparecer info, warning
# y error con el formato indicado.
#
# RESULTADO ESPERADO:
# [INFO] sistema arrancado
# [WARNING] configuración por defecto
# [ERROR] conexión rechazada
# =============================================================================

import logging
import sys

# Configuración previa de un import anterior (simulada). Esto deja el root
# logger con un handler ya colocado antes de nuestra llamada.
logging.basicConfig(level=logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format="[%(LEVELNAME)s] %(message)s",
    stream=sys.stderr,
)

logging.debug("detalle interno")
logging.info("sistema arrancado")
logging.warning("configuración por defecto")
logging.error("conexión rechazada")
