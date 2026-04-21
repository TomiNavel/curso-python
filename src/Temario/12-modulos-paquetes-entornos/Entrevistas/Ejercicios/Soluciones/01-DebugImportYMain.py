# =====================
# SOLUCIÓN
# =====================
# Error 1: from math import * importa la función "factorial" de math al espacio
#   de nombres. La variable local "factorial = calcular_factorial(5)" sobrescribe
#   esa función, pero el verdadero problema es que "factorial" pasa a ser un
#   entero (120) y luego se intenta llamar como función: factorial(5) → TypeError.
#   Además, from math import * es mala práctica. Solo importar lo necesario.
#   Solución: import math (o from math import sqrt, pi) y renombrar la variable.
#
# Error 2: La última línea usa factorial(5) pero "factorial" es un entero (120),
#   no una función. Se intenta llamar a un entero.
#   Solución: usar la variable directamente (factorial + 1) o renombrarla.
#
# Error 3: No hay guard __main__. Los prints se ejecutarían si otro archivo
#   importara este módulo. El código de ejecución debe estar protegido.
#   Solución: poner el código de ejecución dentro de if __name__ == "__main__"
#
# ERRORES CORREGIDOS:
# 1. from math import * → from math import sqrt, pi
# 2. factorial(5) + 1 → resultado_factorial + 1 (renombrar variable)
# 3. Código de ejecución envuelto en if __name__ == "__main__"


from math import sqrt, pi


def calcular_factorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado


def raiz_cuadrada(n):
    return sqrt(n)


def redondear_pi(decimales):
    return round(pi, decimales)


if __name__ == "__main__":
    print(f"Factorial de 5: {calcular_factorial(5)}")
    print(f"Raíz de 144: {raiz_cuadrada(144)}")
    print(f"PI redondeado: {redondear_pi(2)}")

    resultado_factorial = calcular_factorial(5)
    print(f"Verificación: factorial(5) + 1 = {resultado_factorial + 1}")
