# =============================================================================
# EJERCICIO 3: Normalizar espacios en blanco
# =============================================================================
# Escribe una función "normalizar(texto)" que:
#   - reemplace cualquier secuencia de espacios, tabs o saltos de línea
#     por un único espacio.
#   - elimine los espacios iniciales y finales del resultado.
# Debe hacerlo usando re.sub en una sola expresión regular.
#
# RESULTADO ESPERADO:
# hola mundo y saludos
# =============================================================================


# Tu código aquí


# Pruebas
texto = "   hola   mundo\t\t y\n\n saludos  "
print(normalizar(texto))
