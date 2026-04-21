# =============================================================================
# EJERCICIO 1: Ordenar Diccionarios
# =============================================================================
# Ordena listas de diccionarios por distintos campos usando sorted() con key.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# Por edad: Pedro (22), Ana (28), Luis (35)
# Por nombre: Ana (28), Luis (35), Pedro (22)
# Por edad desc: Luis (35), Ana (28), Pedro (22)
# Más joven: Pedro (22)
# Mayor: Luis (35)
# =============================================================================

personas = [
    {"nombre": "Ana", "edad": 28},
    {"nombre": "Pedro", "edad": 22},
    {"nombre": "Luis", "edad": 35},
]

# PASO 1: Ordena la lista por edad (ascendente) usando sorted() con una
# lambda como key. Recorre el resultado con for e imprime cada persona
# con formato "nombre (edad)", todo en una línea precedido de "Por edad: ".

# Tu código aquí

# PASO 2: Ordena la lista por nombre (alfabéticamente) e imprime con el
# mismo formato, precedido de "Por nombre: ".

# Tu código aquí

# PASO 3: Ordena la lista por edad descendente usando reverse=True.
# Imprime con el mismo formato, precedido de "Por edad desc: ".

# Tu código aquí

# PASO 4: Usa max() y min() con key para obtener la persona más joven
# y la mayor. Imprime "Más joven: nombre (edad)" y "Mayor: nombre (edad)".

# Tu código aquí
