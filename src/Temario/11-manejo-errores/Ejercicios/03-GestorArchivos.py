# =============================================================================
# EJERCICIO 3: Gestor de Archivos Seguro
# =============================================================================
# Crea una función `leer_archivo` que intente leer un archivo y maneje los
# posibles errores, usando try/except/else/finally.
#
# Comportamiento:
# - Intentar abrir y leer el archivo
# - Si no existe → imprimir "Error: el archivo '{ruta}' no existe"
# - Si hay error de permisos → imprimir "Error: sin permisos para '{ruta}'"
# - Si se lee con éxito → imprimir "Leídos {n} caracteres de '{ruta}'" (en else)
# - Siempre → imprimir "Operación de lectura finalizada" (en finally)
# - Devolver el contenido si se leyó, o None si falló
#
# RESULTADO ESPERADO (los archivos no existen, así que solo se verá el caso de error):
# Error: el archivo 'datos.txt' no existe
# Operación de lectura finalizada
# Resultado: None
# Error: el archivo 'config.json' no existe
# Operación de lectura finalizada
# Resultado: None
# =============================================================================

# Tu código aquí

# resultado = leer_archivo("datos.txt")
# print(f"Resultado: {resultado}")
# resultado = leer_archivo("config.json")
# print(f"Resultado: {resultado}")
