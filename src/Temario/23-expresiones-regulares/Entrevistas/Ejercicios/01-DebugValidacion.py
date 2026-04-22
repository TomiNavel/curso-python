# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Validación de DNI
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# Un DNI español válido tiene exactamente 8 dígitos seguidos de una letra
# mayúscula. Ejemplos válidos: "12345678A", "87654321Z".
# La función debe aceptar solo DNIs con el formato exacto y rechazar todo
# lo demás (letras minúsculas, espacios, longitud distinta, etc.).
#
# RESULTADO ESPERADO:
# True
# True
# False
# False
# False
# False
# =============================================================================

import re


def es_dni(texto):
    return re.match("\d{8}[A-Za-z]", texto) is not None


# Pruebas
print(es_dni("12345678A"))
print(es_dni("87654321Z"))
print(es_dni("12345678a"))
print(es_dni("1234567A"))
print(es_dni("12345678AB"))
print(es_dni("  12345678A  "))
