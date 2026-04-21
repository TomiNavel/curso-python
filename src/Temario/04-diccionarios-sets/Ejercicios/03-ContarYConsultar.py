# =============================================================================
# EJERCICIO 3: Contar y Consultar con Counter
# =============================================================================
# Practica el uso de Counter para contar ocurrencias en strings y listas,
# consultar conteos y usar operaciones aritméticas entre Counters.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# Counter({'a': 3, 'n': 2, 'b': 1})
# [('a', 3), ('n', 2)]
# 3
# 0
# Counter({'manzana': 3, 'pera': 2, 'uva': 1})
# [('manzana', 3)]
# Counter({'manzana': 5, 'pera': 3, 'uva': 1, 'kiwi': 1})
# Counter({'manzana': 1, 'pera': 1, 'uva': 1})
# =============================================================================

from collections import Counter

# PASO 1: Crea un Counter a partir del string "banana" y guárdalo en "letras"
# Imprime el Counter

# Tu código aquí
letras = Counter("banana")
print (letras)

# PASO 2: Usa most_common(2) para obtener las 2 letras más frecuentes
# Imprime el resultado

# Tu código aquí

# PASO 3: Imprime cuántas veces aparece la letra "a"
# Imprime cuántas veces aparece la letra "z" (no existe en el Counter)

# Tu código aquí

# PASO 4: Crea un Counter "frutas" a partir de la lista:
# ["manzana", "pera", "manzana", "uva", "manzana", "pera"]
# Imprime el Counter
# Usa most_common(1) para obtener la fruta más frecuente e imprímelo

# Tu código aquí

# PASO 5: Crea un segundo Counter "mas_frutas" a partir de:
# ["manzana", "pera", "kiwi", "manzana"]
# Suma ambos Counters (frutas + mas_frutas) e imprime el resultado

# Tu código aquí

# PASO 6: Resta mas_frutas de frutas (frutas - mas_frutas) e imprime el resultado

# Tu código aquí
