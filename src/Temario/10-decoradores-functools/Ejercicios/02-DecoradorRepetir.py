# =============================================================================
# EJERCICIO 2: Decorador con Argumentos — Repetir
# =============================================================================
# Crea un decorador "repetir(veces)" que ejecute la función decorada
# el número de veces indicado y devuelva una lista con todos los resultados.
#
# RESULTADO ESPERADO:
# [6, 6, 6]
# ['Hola, Ana', 'Hola, Ana']
# =============================================================================

from functools import wraps

# Tu código aquí

# Pruebas
@repetir(veces=3)
def sumar(a, b):
    return a + b

@repetir(veces=2)
def saludar(nombre):
    return f"Hola, {nombre}"

print(sumar(1, 5))
print(saludar("Ana"))
