# =============================================================================
# EJERCICIO 1: Cuenta Bancaria
# =============================================================================
# Crea una clase `CuentaBancaria` con las siguientes características:
#
# Atributos de instancia:
# - titular (string)
# - saldo (float, por defecto 0)
#
# Atributo de clase:
# - total_cuentas (int, cuenta cuántas instancias se han creado)
#
# Métodos:
# - depositar(monto): suma al saldo. Lanzar ValueError si monto <= 0.
# - retirar(monto): resta del saldo. Lanzar ValueError si monto > saldo o monto <= 0.
# - transferir(destino, monto): retira de esta cuenta y deposita en destino.
# - __repr__: CuentaBancaria('Ana', 1000.0)
# - __str__: "Cuenta de Ana: $1,000.00"
#
# RESULTADO ESPERADO:
# Cuenta de Ana: $1,000.00
# Cuenta de Ana: $1,300.00
# Cuenta de Bob: $700.00
# Cuenta de Ana: $800.00
# Total cuentas: 2
# CuentaBancaria('Ana', 800.0)
# =============================================================================

# Tu código aquí

# cuenta_ana = CuentaBancaria("Ana", 1000)
# cuenta_bob = CuentaBancaria("Bob", 500)
# print(cuenta_ana)
# cuenta_ana.depositar(300)
# print(cuenta_ana)
# cuenta_bob.depositar(200)
# print(cuenta_bob)
# cuenta_ana.transferir(cuenta_bob, 500)
# print(cuenta_ana)
# print(f"Total cuentas: {CuentaBancaria.total_cuentas}")
# print(repr(cuenta_ana))
