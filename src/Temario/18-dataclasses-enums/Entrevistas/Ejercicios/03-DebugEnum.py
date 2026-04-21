# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Enum mal usado
# =============================================================================
# El siguiente código intenta modelar los estados de un pedido con un Enum
# y procesar el estado actual. Tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# El pedido está en estado: ENVIADO
# Valor numérico: 2
# Estados disponibles: ['PENDIENTE', 'ENVIADO', 'ENTREGADO', 'CANCELADO']
# =============================================================================

from enum import Enum


class EstadoPedido(Enum):
    PENDIENTE = 1
    ENVIADO = 2
    ENTREGADO = 3
    CANCELADO = 4


estado_actual = "ENVIADO"

if estado_actual == EstadoPedido.ENVIADO:
    print(f"El pedido está en estado: {EstadoPedido.ENVIADO}")
    print(f"Valor numérico: {EstadoPedido.ENVIADO.name}")

estados = [e for e in EstadoPedido.__members__]
print(f"Estados disponibles: {estados}")
