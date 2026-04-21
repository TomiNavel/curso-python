# =====================
# SOLUCIÓN
# =====================
# Error 1: map() devuelve un iterador, no una lista. Al imprimir
#   directamente muestra "<map object at ...>". Falta envolver en list().
#   Corrección: cuadrados = list(map(lambda n: n ** 2, numeros))
#
# Error 2: una lambda no puede contener sentencias (if/else multilínea).
#   Hay que usar el operador ternario. Además, la intención es multiplicar
#   cada número por 2 (no filtrar pares).
#   Corrección: pares = list(map(lambda n: n * 2, numeros))
#
# Error 3: una lambda no lleva return — el resultado de la expresión
#   se devuelve implícitamente.
#   Corrección: longitudes = list(map(lambda n: len(n), nombres))
#   O mejor: longitudes = list(map(len, nombres))
#
# ERRORES CORREGIDOS:
# 1. map(...) → list(map(...))
# 2. lambda n: if n % 2 == 0: n * 2 → lambda n: n * 2
# 3. lambda n: return len(n) → lambda n: len(n)


numeros = [1, 2, 3, 4, 5]

cuadrados = list(map(lambda n: n ** 2, numeros))
print(f"Cuadrados: {cuadrados}")

pares = list(map(lambda n: n * 2, numeros))
print(f"Pares: {pares}")

nombres = ["Ana", "Pedro", "Luis"]
longitudes = list(map(lambda n: len(n), nombres))
print(f"Longitudes: {longitudes}")
