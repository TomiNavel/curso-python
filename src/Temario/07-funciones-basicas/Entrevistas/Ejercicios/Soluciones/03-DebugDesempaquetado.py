# =====================
# SOLUCIÓN
# =====================
# Error 1: Código muerto después de return.
#   La línea print("División completada") nunca se ejecuta.
#   Solución: eliminar la línea o moverla antes del return.
#
# Error 2: Argumentos posicionales después de uno por nombre.
#   crear_perfil(nombre="Ana", 28, "Madrid") → SyntaxError.
#   Solución: crear_perfil("Ana", 28, "Madrid")
#
# Error 3: La función devuelve 2 valores pero se intentan desempaquetar en 3.
#   x, y, z = calcular(3, 5) → ValueError: not enough values to unpack.
#   Solución: x, y = calcular(3, 5)
#
# ERRORES CORREGIDOS:
# 1. Eliminar print("División completada") después de return
# 2. crear_perfil(nombre="Ana", 28, "Madrid") → crear_perfil("Ana", 28, "Madrid")
# 3. x, y, z = calcular(3, 5) → x, y = calcular(3, 5)


def dividir_con_resto(a, b):
    cociente = a // b
    resto = a % b
    return cociente, resto

c, r = dividir_con_resto(17, 5)
print(f"Cociente: {c}, Resto: {r}")

def crear_perfil(nombre, edad, ciudad):
    return f"{nombre}, {edad} años, {ciudad}"

perfil = crear_perfil("Ana", 28, "Madrid")
print(f"Perfil: {perfil}")

def calcular(a, b):
    return a * 2, b * 3

x, y = calcular(3, 5)
print(f"Números: {x}, {y}")
