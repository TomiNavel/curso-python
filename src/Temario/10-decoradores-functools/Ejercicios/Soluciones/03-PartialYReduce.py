from functools import partial, reduce

# PASO 1
def formatear_precio(cantidad, moneda, decimales):
    return f"{cantidad:.{decimales}f} {moneda}"

precio_eur = partial(formatear_precio, moneda="€", decimales=2)
precio_btc = partial(formatear_precio, moneda="BTC", decimales=8)

print(precio_eur(19.5))
print(precio_btc(0.00045))

# PASO 2
factorial = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])
print(factorial)

# PASO 3
letras = ["a", "b", "c", "d", "e"]
concatenado = reduce(lambda a, b: a + b, letras)
print(concatenado)
