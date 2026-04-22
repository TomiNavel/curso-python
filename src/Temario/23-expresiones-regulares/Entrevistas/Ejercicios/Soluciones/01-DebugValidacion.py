# =====================
# SOLUCIÓN
# =====================
# Error 1: el patrón no usa raw string. Sin el prefijo r, "\d" puede
#   interpretarse como escape de Python en algunas versiones (aunque hoy
#   en día funciona, emite DeprecationWarning y es frágil). La convención
#   en Python es usar r"..." para regex.
#   Solución: añadir el prefijo r.
#
# Error 2: usa re.match en lugar de re.fullmatch. match solo exige que
#   el patrón encaje desde el principio, no hasta el final. Por eso
#   "12345678AB" y "  12345678A  " dan True por accidente (el primero
#   porque "12345678A" encaja al principio, y el segundo no encajaría
#   aunque match tolera caracteres adicionales tras la coincidencia).
#   Para validación se debe usar fullmatch.
#   Solución: cambiar a re.fullmatch.
#
# Error 3: la clase de letras final es [A-Za-z], que permite minúsculas.
#   El enunciado pide solo letras mayúsculas. Por eso "12345678a" da True
#   incorrectamente.
#   Solución: restringir la clase a [A-Z].
#
# ERRORES CORREGIDOS:
# 1. patrón sin prefijo r → usar raw string
# 2. re.match → re.fullmatch
# 3. [A-Za-z] → [A-Z]

import re


def es_dni(texto):
    return re.fullmatch(r"\d{8}[A-Z]", texto) is not None


# Pruebas
print(es_dni("12345678A"))
print(es_dni("87654321Z"))
print(es_dni("12345678a"))
print(es_dni("1234567A"))
print(es_dni("12345678AB"))
print(es_dni("  12345678A  "))
