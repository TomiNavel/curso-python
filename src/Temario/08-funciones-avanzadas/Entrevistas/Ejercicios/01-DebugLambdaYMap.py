# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Lambda y map()
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Cuadrados: [1, 4, 9, 16, 25]
# Pares: [2, 4, 6, 8, 10]
# Longitudes: [3, 5, 4]
# =============================================================================

numeros = [1, 2, 3, 4, 5]

# Error 1: algo va mal con el resultado de map()
cuadrados = map(lambda n: n ** 2, numeros)
print(f"Cuadrados: {cuadrados}")

# Error 2: la lambda tiene un problema de sintaxis
pares = list(map(lambda n: if n % 2 == 0: n * 2, numeros))
print(f"Pares: {pares}")

# Error 3: algo va mal con la lambda
nombres = ["Ana", "Pedro", "Luis"]
longitudes = list(map(lambda n: return len(n), nombres))
print(f"Longitudes: {longitudes}")
