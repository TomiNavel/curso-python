# =============================================================================
# SOLUCIÓN
# =============================================================================

import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
    stream=sys.stdout,
    force=True,
)

logger = logging.getLogger("app")


def registrar_evento(tipo, mensaje):
    # Diccionario tipo → método del logger. Es más legible que un if/elif
    # largo y añadir nuevos tipos es añadir entradas al mapa.
    mapa = {
        "inicio": logger.info,
        "normal": logger.info,
        "lento": logger.warning,
        "reintento": logger.warning,
        "fallo": logger.error,
        "caido": logger.critical,
    }
    metodo = mapa.get(tipo)
    if metodo is None:
        logger.warning(f"tipo desconocido: {tipo}")
    else:
        metodo(mensaje)


# Pruebas
registrar_evento("inicio", "sistema arrancado")
registrar_evento("lento", "respuesta tardando")
registrar_evento("fallo", "conexión rechazada")
registrar_evento("caido", "base de datos inaccesible")
registrar_evento("extrano", "mensaje ignorado")
