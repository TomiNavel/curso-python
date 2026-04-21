# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Import y __main__
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Factorial de 5: 120
# Raíz de 144: 12.0
# PI redondeado: 3.14
# =============================================================================

from math import *

def calcular_factorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

def raiz_cuadrada(n):
    return sqrt(n)

def redondear_pi(decimales):
    return round(pi, decimales)

print(f"Factorial de 5: {calcular_factorial(5)}")
print(f"Raíz de 144: {raiz_cuadrada(144)}")
print(f"PI redondeado: {redondear_pi(2)}")

factorial = calcular_factorial(5)
print(f"Verificación: factorial(5) + 1 = {factorial(5) + 1}")
