# =============================================================================
# EJERCICIO 3: Configurar un logger con handler y formatter explícitos
# =============================================================================
# Configura un logger llamado "miapp" con:
#   - nivel DEBUG
#   - un único StreamHandler que escriba a sys.stdout
#   - ese handler debe tener nivel INFO (descartar DEBUG)
#   - formatter: "[%(name)s] %(levelname)s: %(message)s"
#
# Al emitir DEBUG, INFO, WARNING y ERROR, solo deben aparecer los tres
# últimos (el DEBUG queda filtrado por el handler).
#
# Pista: para evitar handlers duplicados si el ejercicio se ejecuta varias
# veces en el mismo intérprete, usa:
#     logger.handlers.clear()
# antes de añadir el handler.
#
# RESULTADO ESPERADO:
# [miapp] INFO: operación iniciada
# [miapp] WARNING: recurso casi agotado
# [miapp] ERROR: operación fallida
# =============================================================================

import logging
import sys

# Tu código aquí: configura el logger


# Pruebas
logger.debug("detalle interno")
logger.info("operación iniciada")
logger.warning("recurso casi agotado")
logger.error("operación fallida")
