# =============================================================================
# EJERCICIO 1: Fracción
# =============================================================================
# Crea una clase `Fraccion` que represente fracciones matemáticas.
#
# Atributos:
# - numerador (int)
# - denominador (int, no puede ser 0 → ValueError)
# - La fracción debe almacenarse simplificada (dividir ambos por el MCD)
#   Usa math.gcd para calcular el máximo común divisor.
#   Si el denominador es negativo, mover el signo al numerador.
#
# Métodos especiales:
# - __add__(self, other): suma de fracciones → nueva Fraccion simplificada
# - __sub__(self, other): resta de fracciones → nueva Fraccion simplificada
# - __mul__(self, other): multiplicación → nueva Fraccion simplificada
# - __truediv__(self, other): división → nueva Fraccion simplificada
#   (dividir entre fracción con numerador 0 → ZeroDivisionError)
# - __eq__(self, other): dos fracciones son iguales si tienen mismo
#   numerador y denominador (ya simplificadas)
# - __repr__: Fraccion(1, 2)
# - __str__: "1/2"
#
# Fórmulas:
# - Suma: a/b + c/d = (a*d + c*b) / (b*d)
# - Resta: a/b - c/d = (a*d - c*b) / (b*d)
# - Multiplicación: a/b * c/d = (a*c) / (b*d)
# - División: a/b / c/d = (a*d) / (b*c)
#
# RESULTADO ESPERADO:
# 1/2 + 1/3 = 5/6
# 3/4 - 1/4 = 1/2
# 2/3 * 3/5 = 2/5
# 1/2 / 1/4 = 2/1
# Fraccion(2, 3) == Fraccion(4, 6): True
# Fraccion(1, 2)
# =============================================================================

# Tu código aquí

# import math
# a = Fraccion(1, 2)
# b = Fraccion(1, 3)
# print(f"{a} + {b} = {a + b}")
# print(f"{Fraccion(3, 4)} - {Fraccion(1, 4)} = {Fraccion(3, 4) - Fraccion(1, 4)}")
# print(f"{Fraccion(2, 3)} * {Fraccion(3, 5)} = {Fraccion(2, 3) * Fraccion(3, 5)}")
# print(f"{Fraccion(1, 2)} / {Fraccion(1, 4)} = {Fraccion(1, 2) / Fraccion(1, 4)}")
# print(f"Fraccion(2, 3) == Fraccion(4, 6): {Fraccion(2, 3) == Fraccion(4, 6)}")
# print(repr(a))
