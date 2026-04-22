# =============================================================================
# EJERCICIO 2: Validar códigos postales españoles
# =============================================================================
# Un código postal español válido es una secuencia de EXACTAMENTE 5 dígitos.
# No se permiten letras, espacios ni caracteres extra antes o después.
#
# Escribe una función "es_codigo_postal(texto)" que devuelva True si el
# texto es un código postal válido y False en caso contrario.
# Usa re.fullmatch.
#
# RESULTADO ESPERADO:
# True
# True
# False
# False
# False
# =============================================================================


# Tu código aquí


# Pruebas
print(es_codigo_postal("28013"))
print(es_codigo_postal("08080"))
print(es_codigo_postal("280130"))
print(es_codigo_postal(" 28013"))
print(es_codigo_postal("28a13"))
