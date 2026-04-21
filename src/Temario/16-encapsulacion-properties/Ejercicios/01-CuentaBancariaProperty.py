# =============================================================================
# EJERCICIO 1: Cuenta Bancaria con Properties
# =============================================================================
# Crea una clase `CuentaBancaria` que use properties para proteger el saldo.
#
# Atributos internos:
# - _titular (str)
# - _saldo (float)
#
# Properties:
# - titular: getter y setter. El setter valida que no sea vacío (ValueError).
# - saldo: solo getter (lectura). No se puede asignar directamente.
#
# Métodos:
# - depositar(monto): suma al saldo. ValueError si monto <= 0.
# - retirar(monto): resta del saldo. ValueError si monto <= 0 o monto > saldo.
# - __str__: "Cuenta de Ana: $1,500.00"
# - __repr__: CuentaBancaria('Ana', 1500.0)
#
# RESULTADO ESPERADO:
# Cuenta de Ana: $1,000.00
# Cuenta de Ana: $1,500.00
# Cuenta de Ana: $1,200.00
# Error: El monto debe ser positivo
# Error: Saldo insuficiente
# Error: can't set attribute
# CuentaBancaria('Ana', 1200.0)
# =============================================================================

# Tu código aquí

# c = CuentaBancaria("Ana", 1000)
# print(c)
# c.depositar(500)
# print(c)
# c.retirar(300)
# print(c)
#
# try:
#     c.depositar(-100)
# except ValueError as e:
#     print(f"Error: {e}")
#
# try:
#     c.retirar(5000)
# except ValueError as e:
#     print(f"Error: {e}")
#
# try:
#     c.saldo = 999999
# except AttributeError as e:
#     print(f"Error: {e}")
#
# print(repr(c))
