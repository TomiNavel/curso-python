# =============================================================================
# EJERCICIO 2: Validador de Datos
# =============================================================================
# Crea una función `validar_edad` que reciba un valor y verifique que sea una
# edad válida. Debe lanzar excepciones con mensajes descriptivos.
#
# Reglas:
# - Si el valor no es int ni str convertible a int → raise TypeError
# - Si el valor es negativo → raise ValueError
# - Si el valor es mayor que 150 → raise ValueError
# - Si es válido, devolver el entero
#
# Luego, crea una función `registrar_usuario` que reciba nombre y edad,
# use validar_edad internamente y maneje los errores con try/except.
#
# RESULTADO ESPERADO:
# Usuario Ana registrado con edad 25
# Error de tipo: Se esperaba un entero, se recibió: 'veinticinco' (str)
# Error de valor: La edad no puede ser negativa, se recibió: -5
# Error de valor: La edad no puede superar 150, se recibió: 200
# Usuario Carlos registrado con edad 30
# =============================================================================

# Tu código aquí

# registrar_usuario("Ana", 25)
# registrar_usuario("Bob", "veinticinco")
# registrar_usuario("Clara", -5)
# registrar_usuario("Diana", 200)
# registrar_usuario("Carlos", "30")
