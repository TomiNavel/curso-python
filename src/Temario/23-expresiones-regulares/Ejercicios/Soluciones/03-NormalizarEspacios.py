# =============================================================================
# SOLUCIÓN
# =============================================================================

import re


def normalizar(texto: str) -> str:
    # \s+ captura cualquier whitespace contiguo: espacios, tabs y saltos.
    # strip() al final quita el espacio inicial/final que sobreviva.
    return re.sub(r"\s+", " ", texto).strip()


texto = "   hola   mundo\t\t y\n\n saludos  "
print(normalizar(texto))
