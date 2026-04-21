# =============================================================================
# EJERCICIO 4: Enum EstadoPedido
# =============================================================================
# Crea un Enum "EstadoPedido" con los siguientes miembros:
#   PENDIENTE = 1
#   ENVIADO = 2
#   ENTREGADO = 3
#   CANCELADO = 4
#
# Implementa una función "describir(estado)" que reciba un EstadoPedido y
# devuelva una cadena con el formato "El pedido está {nombre en minúsculas}".
#
# Además, muestra por pantalla todos los estados iterando sobre el enum.
#
# RESULTADO ESPERADO:
# El pedido está pendiente
# El pedido está entregado
# --- Todos los estados ---
# PENDIENTE = 1
# ENVIADO = 2
# ENTREGADO = 3
# CANCELADO = 4
# =============================================================================

# Tu código aquí


# Pruebas
print(describir(EstadoPedido.PENDIENTE))
print(describir(EstadoPedido.ENTREGADO))

print("--- Todos los estados ---")
for estado in EstadoPedido:
    print(f"{estado.name} = {estado.value}")
