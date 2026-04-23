# =============================================================================
# EJERCICIO 1: Configurar logging básico con basicConfig
# =============================================================================
# Completa el código para:
#   - Configurar logging con basicConfig, nivel INFO y formato:
#     "%(levelname)s - %(message)s"
#   - Emitir un mensaje DEBUG, uno INFO y uno WARNING.
#
# Solo los mensajes INFO y WARNING deben aparecer en la salida; el DEBUG
# debe filtrarse por el nivel configurado.
#
# Pistas:
#   - logging.basicConfig(level=..., format=..., stream=sys.stdout, force=True)
#   - logging.debug(...), logging.info(...), logging.warning(...)
# El parámetro force=True fuerza reconfigurar si ya había logging activo.
#
# RESULTADO ESPERADO:
# INFO - arrancando sistema
# WARNING - configuración por defecto en uso
# =============================================================================

import logging
import sys

# Tu código aquí: configura basicConfig


# Tu código aquí: emite los tres mensajes
