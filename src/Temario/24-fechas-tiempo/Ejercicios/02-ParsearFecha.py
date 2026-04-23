# =============================================================================
# EJERCICIO 2: Parsear fecha desde formato español
# =============================================================================
# Escribe una función "parsear_fecha(texto)" que reciba un string en formato
# "DD/MM/YYYY" y devuelva un objeto date correspondiente.
# Si el texto no tiene el formato correcto, la función debe devolver None.
#
# No hace falta validar rangos del calendario: basta con confiar en lo que
# strptime acepte.
#
# RESULTADO ESPERADO:
# 2026-04-22
# 2025-12-31
# None
# None
# =============================================================================

from datetime import datetime


# Tu código aquí


# Pruebas
print(parsear_fecha("22/04/2026"))
print(parsear_fecha("31/12/2025"))
print(parsear_fecha("2026-04-22"))
print(parsear_fecha("hola"))
