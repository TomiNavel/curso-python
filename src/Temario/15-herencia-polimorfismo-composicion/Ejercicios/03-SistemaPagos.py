# =============================================================================
# EJERCICIO 3: Sistema de Pagos (Duck Typing)
# =============================================================================
# Crea varias clases de procesadores de pago que compartan la misma interfaz
# SIN usar herencia (duck typing puro).
#
# Cada clase debe tener:
# - __init__: recibe los datos necesarios para el procesador
# - procesar(monto): devuelve un string con el resultado del pago
# - nombre_metodo(): devuelve el nombre del método de pago
#
# Clases:
# - TarjetaCredito: recibe numero (str, últimos 4 dígitos)
#   procesar: "Pago de $50.00 con tarjeta *1234"
#   nombre_metodo: "Tarjeta de crédito"
#
# - PayPal: recibe email (str)
#   procesar: "Pago de $50.00 vía PayPal (ana@mail.com)"
#   nombre_metodo: "PayPal"
#
# - Transferencia: recibe banco (str)
#   procesar: "Transferencia de $50.00 desde BBVA"
#   nombre_metodo: "Transferencia bancaria"
#
# Función libre ejecutar_pagos(procesadores, monto): recibe una lista de
# procesadores y un monto, imprime cada pago usando polimorfismo.
#
# RESULTADO ESPERADO:
# [Tarjeta de crédito] Pago de $50.00 con tarjeta *1234
# [PayPal] Pago de $50.00 vía PayPal (ana@mail.com)
# [Transferencia bancaria] Transferencia de $50.00 desde BBVA
# =============================================================================

# Tu código aquí

# procesadores = [
#     TarjetaCredito("1234"),
#     PayPal("ana@mail.com"),
#     Transferencia("BBVA"),
# ]
# ejecutar_pagos(procesadores, 50)
