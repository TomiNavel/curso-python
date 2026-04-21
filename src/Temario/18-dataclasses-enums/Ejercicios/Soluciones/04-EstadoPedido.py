from enum import Enum


class EstadoPedido(Enum):
    PENDIENTE = 1
    ENVIADO = 2
    ENTREGADO = 3
    CANCELADO = 4


def describir(estado: EstadoPedido) -> str:
    return f"El pedido está {estado.name.lower()}"


# Pruebas
print(describir(EstadoPedido.PENDIENTE))
print(describir(EstadoPedido.ENTREGADO))

print("--- Todos los estados ---")
for estado in EstadoPedido:
    print(f"{estado.name} = {estado.value}")
