# =============================================================================
# EJERCICIO 5: Reintento de Operación
# =============================================================================
# Crea una función `reintentar` que reciba una función y un número máximo de
# intentos. Ejecuta la función hasta que tenga éxito o se agoten los intentos.
#
# Comportamiento:
# - Ejecutar la función en un bucle hasta max_intentos veces
# - Si tiene éxito, devolver el resultado
# - Si falla, imprimir "Intento {n}/{max}: {mensaje_error}"
# - Si se agotan los intentos, lanzar la última excepción recibida
#
# RESULTADO ESPERADO:
# Intento 1/3: fallo simulado
# Intento 2/3: fallo simulado
# Éxito en intento 3
# Resultado: ok
# ---
# Intento 1/2: siempre fallo
# Intento 2/2: siempre fallo
# Error final: siempre fallo
# =============================================================================

# Tu código aquí

# --- Código de prueba ---

# contador = 0
#
# def operacion_inestable():
#     global contador
#     contador += 1
#     if contador < 3:
#         raise RuntimeError("fallo simulado")
#     print(f"Éxito en intento {contador}")
#     return "ok"
#
# def operacion_imposible():
#     raise RuntimeError("siempre fallo")
#
# resultado = reintentar(operacion_inestable, max_intentos=3)
# print(f"Resultado: {resultado}")
#
# print("---")
#
# try:
#     reintentar(operacion_imposible, max_intentos=2)
# except RuntimeError as e:
#     print(f"Error final: {e}")
