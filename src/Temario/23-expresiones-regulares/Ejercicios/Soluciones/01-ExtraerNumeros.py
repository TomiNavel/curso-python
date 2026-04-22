# =============================================================================
# SOLUCIÓN
# =============================================================================

import re


def extraer_numeros(texto: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", texto)]


# El orden del resultado es el orden de aparición en el texto.
print(extraer_numeros("Tenía 42 años, nació en 2026, compró 17 manzanas y 3 peras."))
