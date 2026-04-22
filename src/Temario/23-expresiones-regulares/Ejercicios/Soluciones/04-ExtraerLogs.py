# =============================================================================
# SOLUCIÓN
# =============================================================================

import re

LOG_PATTERN = re.compile(
    r"^\[(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"(?P<nivel>\w+): "
    r"(?P<mensaje>.+)$"
)


def parsear_log(linea: str) -> dict | None:
    m = LOG_PATTERN.match(linea)
    return m.groupdict() if m else None


# Precompilar el patrón es buena práctica cuando se aplica a muchas líneas
# en un bucle: se evita que el motor lo parsee cada vez.
print(parsear_log("[2026-04-22 10:15:32] ERROR: conexión rechazada"))
print(parsear_log("[2026-04-22 10:16:04] INFO: reintento satisfactorio"))
print(parsear_log("formato libre sin corchetes"))
