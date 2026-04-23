# =============================================================================
# SOLUCIÓN
# =============================================================================

from datetime import datetime, date


def parsear_fecha(texto: str) -> date | None:
    # strptime lanza ValueError si el formato no encaja. Capturarlo es la
    # forma idiomática de validar; también evita construir un regex.
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return None


# Pruebas
print(parsear_fecha("22/04/2026"))
print(parsear_fecha("31/12/2025"))
print(parsear_fecha("2026-04-22"))
print(parsear_fecha("hola"))
