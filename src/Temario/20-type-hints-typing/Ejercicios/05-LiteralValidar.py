# =============================================================================
# EJERCICIO 5: Literal — validar nivel de log
# =============================================================================
# Implementa una función "registrar" que reciba un mensaje (str) y un nivel
# de log restringido a los valores "DEBUG", "INFO", "WARNING", "ERROR".
# Usa Literal para anotar el parámetro del nivel.
#
# La función debe devolver una cadena con el formato "[NIVEL] mensaje".
#
# Implementa también una función "es_critico" que reciba un nivel con la misma
# restricción y devuelva True solo si el nivel es "ERROR".
#
# RESULTADO ESPERADO:
# [INFO] Servidor iniciado
# [ERROR] Conexión perdida
# [DEBUG] Variable x = 42
# False
# True
# =============================================================================

# Tu código aquí


# Pruebas
print(registrar("Servidor iniciado", "INFO"))
print(registrar("Conexión perdida", "ERROR"))
print(registrar("Variable x = 42", "DEBUG"))
print(es_critico("WARNING"))
print(es_critico("ERROR"))
