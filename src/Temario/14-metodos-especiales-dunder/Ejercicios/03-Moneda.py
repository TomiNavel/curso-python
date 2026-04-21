# =============================================================================
# EJERCICIO 3: Moneda
# =============================================================================
# Crea una clase `Moneda` que represente una cantidad monetaria con comparación
# y hashing.
#
# Atributos:
# - cantidad (float, redondeado a 2 decimales en __init__)
# - divisa (str, por defecto "EUR")
#
# Métodos especiales:
# - __eq__: dos monedas son iguales si tienen misma cantidad y divisa
# - __lt__: solo se puede comparar con la misma divisa.
#   Si las divisas son distintas → ValueError.
# - __hash__: basado en (cantidad, divisa) para poder usar en sets/dicts
# - __bool__: False si cantidad es 0, True en caso contrario
# - __repr__: Moneda(29.99, 'EUR')
# - __str__: "29.99 EUR"
#
# Usa @total_ordering de functools para generar __le__, __gt__, __ge__.
#
# RESULTADO ESPERADO:
# 29.99 EUR
# Moneda(29.99, 'EUR')
# Iguales: True
# Menor: True
# Mayor o igual: True
# Bool 0: False
# Bool 100: True
# Únicos en set: 3
# Lookup dict: 29.99 EUR
# =============================================================================

# Tu código aquí

# from functools import total_ordering
# a = Moneda(29.99, "EUR")
# b = Moneda(29.99, "EUR")
# c = Moneda(50.00, "EUR")
# d = Moneda(100, "USD")
#
# print(a)
# print(repr(a))
# print(f"Iguales: {a == b}")
# print(f"Menor: {a < c}")
# print(f"Mayor o igual: {c >= a}")
# print(f"Bool 0: {bool(Moneda(0))}")
# print(f"Bool 100: {bool(Moneda(100))}")
#
# monedas = {Moneda(10, "EUR"), Moneda(10, "EUR"), Moneda(20, "EUR"), Moneda(10, "USD")}
# print(f"Únicos en set: {len(monedas)}")
#
# precios = {Moneda(29.99, "EUR"): "Camiseta"}
# print(f"Lookup dict: {list(precios.keys())[0]}")
