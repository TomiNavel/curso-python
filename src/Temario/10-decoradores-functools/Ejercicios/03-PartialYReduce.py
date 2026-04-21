# =============================================================================
# EJERCICIO 3: partial y reduce
# =============================================================================
# Resuelve cada paso usando functools.partial o functools.reduce.
#
# RESULTADO ESPERADO:
# 19.50 €
# 0.00045000 BTC
# 120
# abcde
# =============================================================================

from functools import partial, reduce

# PASO 1: Dada la función formatear_precio, crea dos funciones especializadas
# usando partial:
# - precio_eur: moneda="€", decimales=2
# - precio_btc: moneda="BTC", decimales=8

def formatear_precio(cantidad, moneda, decimales):
    return f"{cantidad:.{decimales}f} {moneda}"

# Tu código aquí

# print(precio_eur(19.5))
# print(precio_btc(0.00045))


# PASO 2: Usa reduce para calcular el factorial de 5 (5! = 120)
# partiendo de la lista [1, 2, 3, 4, 5]

# Tu código aquí

# print(factorial)


# PASO 3: Usa reduce para concatenar una lista de strings en uno solo
# sin usar "".join()

letras = ["a", "b", "c", "d", "e"]

# Tu código aquí

# print(concatenado)
