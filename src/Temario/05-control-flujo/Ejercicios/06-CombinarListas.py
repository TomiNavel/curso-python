# =============================================================================
# EJERCICIO 6: Combinar Listas
# =============================================================================
# Combina listas paralelas usando zip y enumerate.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# 1. Ana - 28 años
# 2. Pedro - 34 años
# 3. Luis - 22 años
# ---
# Ana estudia Medicina
# Pedro estudia Derecho
# Luis estudia Ingeniería
# ---
# {'Ana': 28, 'Pedro': 34, 'Luis': 22}
# =============================================================================

nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34, 22]
carreras = ["Medicina", "Derecho", "Ingeniería"]

# PASO 1: Usa zip() y enumerate() para recorrer "nombres" y "edades" juntos,
# imprimiendo una lista numerada desde 1.
# Formato: "1. Ana - 28 años"

# Tu código aquí

for i, (nombre, edad) in enumerate(zip(nombres, edades), start=1):
    print(f"{i}. {nombre} - {edad} años")

# PASO 2: Imprime "---" como separador.
# Usa zip() para recorrer "nombres" y "carreras" juntos.
# Formato: "Ana estudia Medicina"

# Tu código aquí

# PASO 3: Imprime "---" como separador.
# Usa zip() y dict() para crear un diccionario que asocie cada nombre
# con su edad. Imprímelo.

# Tu código aquí
