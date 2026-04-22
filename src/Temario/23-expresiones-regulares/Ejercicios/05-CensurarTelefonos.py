# =============================================================================
# EJERCICIO 5: Censurar números de teléfono en un texto
# =============================================================================
# Escribe una función "censurar_telefonos(texto)" que sustituya cualquier
# número de teléfono español (9 dígitos juntos, opcionalmente precedidos
# por "+34 " o "+34") por la cadena "[TELÉFONO]".
#
# Ejemplos válidos que deben censurarse:
#   600123456
#   +34600123456
#   +34 600123456
#
# No censures números que no tengan exactamente 9 dígitos (p. ej. 8 o 10).
#
# RESULTADO ESPERADO:
# Llámame al [TELÉFONO] o al [TELÉFONO]. El código 12345 no es teléfono.
# =============================================================================


# Tu código aquí


# Pruebas
texto = "Llámame al 600123456 o al +34 655998877. El código 12345 no es teléfono."
print(censurar_telefonos(texto))
