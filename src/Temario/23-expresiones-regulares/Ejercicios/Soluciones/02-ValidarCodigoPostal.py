# =============================================================================
# SOLUCIÓN
# =============================================================================

import re


def es_codigo_postal(texto: str) -> bool:
    return re.fullmatch(r"\d{5}", texto) is not None


# fullmatch exige que el patrón cubra todo el texto. Con search o match,
# "280130" o " 28013" darían falso positivo al encontrar 5 dígitos dentro
# de un texto más largo.
print(es_codigo_postal("28013"))
print(es_codigo_postal("08080"))
print(es_codigo_postal("280130"))
print(es_codigo_postal(" 28013"))
print(es_codigo_postal("28a13"))
