# =============================================================================
# EJERCICIO 6: Parámetros Avanzados
# =============================================================================
# Practica parámetros solo posicionales (/) y solo keyword (*).
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# 1024
# 1024
# Hola, Ana!
# Buenos días, Pedro!
# conectado a localhost:5432 (timeout=30)
# conectado a miservidor:3306 (timeout=10)
# =============================================================================

# PASO 1: Define una función "potencia" con parámetros (base, exponente, /)
# que sean solo posicionales. Devuelve base ** exponente.
# Imprime: potencia(2, 10) y potencia(4, 5)

# Tu código aquí

# PASO 2: Define una función "saludar" con parámetros (nombre, *, saludo)
# donde saludo sea solo keyword con valor por defecto "Hola".
# Devuelve "saludo, nombre!".
# Imprime: saludar("Ana") y saludar("Pedro", saludo="Buenos días")

# Tu código aquí

# PASO 3: Define una función "conectar" con parámetros
# (host, /, puerto, *, timeout) donde timeout tenga valor por defecto 30.
# host es solo posicional, puerto es normal, timeout es solo keyword.
# Devuelve "conectado a host:puerto (timeout=X)".
# Imprime: conectar("localhost", 5432)
# y conectar("miservidor", puerto=3306, timeout=10)

# Tu código aquí
