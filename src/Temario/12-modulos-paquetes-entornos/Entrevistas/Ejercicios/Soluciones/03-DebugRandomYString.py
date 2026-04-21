# =====================
# SOLUCIÓN
# =====================
# Error 1: random.choices(caracteres, longitud) usa "longitud" como segundo
#   argumento posicional, que corresponde al parámetro "weights" (pesos), no
#   a la cantidad de elementos. El parámetro de cantidad es "k".
#   Solución: random.choices(caracteres, k=longitud)
#
# Error 2: random.choice[frutas] usa corchetes en lugar de paréntesis.
#   Los corchetes son para indexación, no para llamar funciones.
#   Solución: random.choice(frutas)
#
# Error 3: random.shuffle(frutas) mezcla la lista in-place y devuelve None.
#   Al asignar el resultado a "mezclada", se guarda None.
#   Solución: llamar random.shuffle(frutas) sin asignar, luego usar frutas.
#
# ERRORES CORREGIDOS:
# 1. random.choices(caracteres, longitud) → random.choices(caracteres, k=longitud)
# 2. random.choice[frutas] → random.choice(frutas)
# 3. mezclada = random.shuffle(frutas) → random.shuffle(frutas), usar frutas


import random
import string

random.seed(42)


def generar_codigo(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    codigo = random.choices(caracteres, k=longitud)
    return "".join(codigo)


print(f"Código generado: {generar_codigo()}")

frutas = ["apple", "banana", "cherry", "date"]
elegida = random.choice(frutas)
print(f"Elemento elegido: {elegida}")

random.shuffle(frutas)
print(f"Lista mezclada: {frutas}")
