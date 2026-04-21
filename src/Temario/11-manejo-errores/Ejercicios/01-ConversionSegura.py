# =============================================================================
# EJERCICIO 1: Conversión Segura
# =============================================================================
# Crea una función `convertir_a_entero` que reciba un valor y lo convierta a
# entero. Si no es posible, debe devolver un valor por defecto.
#
# - Si la conversión falla (ValueError, TypeError), devolver el valor por defecto
# - El valor por defecto es 0 si no se especifica
# - Si la conversión es exitosa, imprimir "Convertido: {resultado}"
# - Si falla, imprimir "No se pudo convertir '{valor}': {mensaje_error}"
#
# RESULTADO ESPERADO:
# Convertido: 42
# 42
# Convertido: 3
# 3
# No se pudo convertir 'abc': invalid literal for int() with base 10: 'abc'
# 0
# No se pudo convertir 'None': int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
# -1
# =============================================================================

# Tu código aquí

# print(convertir_a_entero("42"))
# print(convertir_a_entero("3.7"))
# print(convertir_a_entero("abc"))
# print(convertir_a_entero(None, -1))
