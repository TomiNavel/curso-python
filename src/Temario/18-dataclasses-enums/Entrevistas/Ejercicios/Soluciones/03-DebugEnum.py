# =====================
# SOLUCIÓN
# =====================
# Error 1: La comparación "estado_actual == EstadoPedido.ENVIADO" siempre
#   devuelve False porque se compara una cadena ("ENVIADO") con un miembro
#   de Enum. Para convertir la cadena al miembro correspondiente se usa
#   acceso por nombre: EstadoPedido[estado_actual]. Alternativa: convertir
#   el miembro a cadena con .name. Solución elegida: usar EstadoPedido[...].
#
# Error 2: print muestra "EstadoPedido.ENVIADO" en lugar de solo "ENVIADO".
#   El resultado esperado indica que solo se quiere el nombre. Solución: usar
#   EstadoPedido.ENVIADO.name en lugar del miembro directamente.
#
# Error 3: "Valor numérico: {EstadoPedido.ENVIADO.name}" muestra "ENVIADO"
#   en lugar del valor numérico 2. Confunde .name con .value. Solución:
#   usar .value en lugar de .name.
#
# ERRORES CORREGIDOS:
# 1. Comparar usando EstadoPedido[estado_actual]
# 2. Usar .name al imprimir el estado
# 3. Usar .value en lugar de .name para el valor numérico


from enum import Enum


class EstadoPedido(Enum):
    PENDIENTE = 1
    ENVIADO = 2
    ENTREGADO = 3
    CANCELADO = 4


estado_actual = "ENVIADO"

if EstadoPedido[estado_actual] == EstadoPedido.ENVIADO:
    print(f"El pedido está en estado: {EstadoPedido.ENVIADO.name}")
    print(f"Valor numérico: {EstadoPedido.ENVIADO.value}")

estados = [e for e in EstadoPedido.__members__]
print(f"Estados disponibles: {estados}")
