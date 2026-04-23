# =============================================================================
# EJERCICIO 2: Elegir el nivel correcto para cada evento
# =============================================================================
# Completa la función "registrar_evento(tipo, mensaje)" para que emita
# el log con el nivel apropiado según el tipo recibido:
#   - "inicio" o "normal" → INFO
#   - "lento" o "reintento" → WARNING
#   - "fallo" → ERROR
#   - "caido" → CRITICAL
#
# Si el tipo no está en la lista, emite un WARNING indicando "tipo
# desconocido: {tipo}".
#
# Usa el logger devuelto por logging.getLogger("app"), NO logging.info
# directo.
#
# RESULTADO ESPERADO:
# INFO - sistema arrancado
# WARNING - respuesta tardando
# ERROR - conexión rechazada
# CRITICAL - base de datos inaccesible
# WARNING - tipo desconocido: extrano
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
    # Tu código aquí
    pass


# Pruebas
registrar_evento("inicio", "sistema arrancado")
registrar_evento("lento", "respuesta tardando")
registrar_evento("fallo", "conexión rechazada")
registrar_evento("caido", "base de datos inaccesible")
registrar_evento("extrano", "mensaje ignorado")
