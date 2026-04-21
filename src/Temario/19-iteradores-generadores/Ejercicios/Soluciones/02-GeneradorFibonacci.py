# =====================
# SOLUCIÓN
# =====================
# El generador mantiene dos variables "a" y "b" que representan los dos últimos
# números de la sucesión. En cada iteración se produce "a" y se avanzan las
# variables mediante asignación múltiple: a toma el valor de b y b toma el
# valor de a+b. El bucle se repite "n" veces con ayuda de un contador.
# Si "n" es 0, el bucle no se ejecuta ni una sola vez y el generador termina
# sin producir ningún valor.


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


print(list(fibonacci(10)))
print(list(fibonacci(5)))
print(list(fibonacci(0)))
