# =============================================================================
# EJERCICIO 3: Generador de Contraseñas
# =============================================================================
# Crea una función `generar_password` que genere contraseñas aleatorias usando
# los módulos `random` y `string`.
#
# Parámetros:
# - longitud: longitud de la contraseña (por defecto 12)
# - mayusculas: incluir mayúsculas (por defecto True)
# - digitos: incluir dígitos (por defecto True)
# - especiales: incluir caracteres especiales (por defecto False)
#
# Reglas:
# - Siempre incluye letras minúsculas
# - Si longitud < 4, lanzar ValueError("La longitud mínima es 4")
# - La contraseña debe contener al menos un carácter de cada tipo activado
# - Los caracteres restantes se eligen aleatoriamente del conjunto completo
# - Mezclar el resultado para que los caracteres obligatorios no queden al inicio
#
# Crea también una función `evaluar_fortaleza` que reciba una contraseña y
# devuelva "débil", "media" o "fuerte" según:
# - débil: solo tiene un tipo de carácter
# - media: tiene 2-3 tipos de caracteres
# - fuerte: tiene los 4 tipos (minúsculas, mayúsculas, dígitos, especiales)
#
# RESULTADO ESPERADO (los valores exactos varían por aleatoriedad):
# generar_password(): aK7mBx2nPq4j (12 chars, con mayúsculas y dígitos)
# generar_password(8, especiales=True): kM3!pBn@ (8 chars, con todo)
# generar_password(6, mayusculas=False, digitos=False): abcxyz (6 chars, solo minúsculas)
# evaluar_fortaleza("abc"): débil
# evaluar_fortaleza("aBc123"): media
# evaluar_fortaleza("aB3!xY9@"): fuerte
# =============================================================================

# Tu código aquí

# import random
# random.seed(42)
# print(generar_password())
# print(generar_password(8, especiales=True))
# print(generar_password(6, mayusculas=False, digitos=False))
# print()
# print(evaluar_fortaleza("abcdef"))
# print(evaluar_fortaleza("aBc123"))
# print(evaluar_fortaleza("aB3!xY9@"))
