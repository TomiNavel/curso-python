# =============================================================================
# SOLUCIÓN
# =============================================================================

import re


def censurar_telefonos(texto: str) -> str:
    # \b\d{9}\b: exactamente 9 dígitos aislados (no parte de un número más
    # largo). El prefijo +34 es opcional, con espacio opcional después.
    patron = r"(?:\+34\s?)?\b\d{9}\b"
    return re.sub(patron, "[TELÉFONO]", texto)


texto = "Llámame al 600123456 o al +34 655998877. El código 12345 no es teléfono."
print(censurar_telefonos(texto))
