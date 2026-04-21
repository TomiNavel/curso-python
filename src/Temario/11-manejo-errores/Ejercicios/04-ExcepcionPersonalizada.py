# =============================================================================
# EJERCICIO 4: Excepción Personalizada
# =============================================================================
# Crea un sistema de validación de contraseñas con excepciones personalizadas.
#
# PASO 1: Crea dos excepciones personalizadas:
# - `LongitudError` — contraseña demasiado corta
# - `ComplejidadError` — no cumple requisitos de complejidad
# Cada una debe heredar directamente de Exception (basta con "pass" en el
# cuerpo de la clase).
#
# PASO 2: Crea la función `validar_contrasena(contrasena)` que:
# - Si tiene menos de 8 caracteres → raise LongitudError con el mensaje
#   "Mínimo 8 caracteres, tiene {n}"
# - Si no tiene al menos un dígito → raise ComplejidadError con el mensaje
#   "Debe contener al menos un dígito"
# - Si es válida → devolver True
#
# PASO 3: Crea la función `registrar_contrasena(contrasena)` que use
# validar_contrasena y maneje los errores:
# - Capturar LongitudError → imprimir "Longitud: {mensaje}"
# - Capturar ComplejidadError → imprimir "Complejidad: {mensaje}"
# - Si es válida → imprimir "Contraseña registrada correctamente"
#
# RESULTADO ESPERADO:
# Longitud: Mínimo 8 caracteres, tiene 3
# Complejidad: Debe contener al menos un dígito
# Contraseña registrada correctamente
# =============================================================================

# Tu código aquí

# registrar_contrasena("abc")
# registrar_contrasena("abcdefgh")
# registrar_contrasena("abcdef1g")
