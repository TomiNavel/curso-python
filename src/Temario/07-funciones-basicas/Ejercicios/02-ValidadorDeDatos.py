# =============================================================================
# EJERCICIO 2: Validador de Datos
# =============================================================================
# Crea funciones que validen datos y devuelvan True o False.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# True
# False
# True
# True
# False
# False
# Ana: válido
# Pedro: válido
# : no válido
# 12: no válido
# =============================================================================

# PASO 1: Define una función "es_edad_valida" que reciba una edad (entero)
# y devuelva True si está entre 0 y 120 (inclusive), False en caso contrario.
# Imprime: es_edad_valida(25), es_edad_valida(-5), es_edad_valida(120).

# Tu código aquí

# PASO 2: Define una función "es_nombre_valido" que reciba un string y
# devuelva True si tiene al menos 1 carácter, no está vacío tras hacer
# strip(), y solo contiene letras y espacios (usa .replace(" ", "").isalpha()).
# Devuelve False en caso contrario.
# Imprime: es_nombre_valido("Ana María"), es_nombre_valido(""), es_nombre_valido("Pedro123").

# Tu código aquí

# PASO 3: Dada la lista nombres = ["Ana", "Pedro", "", "12"], recórrela
# con un for. Para cada nombre, si es_nombre_valido devuelve True,
# imprime "X: válido". Si no, imprime "X: no válido".

nombres = ["Ana", "Pedro", "", "12"]
# Tu código aquí
