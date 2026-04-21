# PASO 1
def factorial_recursivo(n):
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)

print(f"factorial_recursivo(6) = {factorial_recursivo(6)}")

# PASO 2
def factorial_iterativo(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

print(f"factorial_iterativo(6) = {factorial_iterativo(6)}")

# PASO 3
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

nums = " ".join(str(fibonacci(i)) for i in range(10))
print(f"fibonacci: {nums}")

# PASO 4
def fibonacci_iterativo(n):
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

nums = " ".join(str(fibonacci_iterativo(i)) for i in range(10))
print(f"fibonacci_iterativo: {nums}")
