# =============================================================================
# EJERCICIO 4: Historial con Properties
# =============================================================================
# Crea una clase `Historial` que registre los cambios de un valor usando
# properties.
#
# Atributos internos:
# - _valor (cualquier tipo)
# - _cambios (lista de tuplas (valor_anterior, valor_nuevo))
#
# Properties:
# - valor: getter y setter. El setter registra cada cambio en _cambios
#   antes de actualizar el valor. No registra si el nuevo valor es igual
#   al actual.
#
# Properties calculadas:
# - total_cambios: cantidad de cambios realizados
# - ultimo_cambio: última tupla (anterior, nuevo) o None si no hay cambios
#
# Métodos:
# - historial_completo(): devuelve lista de strings "anterior -> nuevo"
# - revertir(): vuelve al valor anterior (el último cambio se deshace).
#   Si no hay cambios, lanza ValueError("No hay cambios que revertir").
#
# __str__: "Historial: valor=100, cambios=3"
#
# RESULTADO ESPERADO:
# Historial: valor=10, cambios=0
# Historial: valor=20, cambios=1
# Historial: valor=50, cambios=2
# Historial: valor=50, cambios=2
# Último cambio: (20, 50)
# Historial completo:
#   10 -> 20
#   20 -> 50
# Después de revertir:
# Historial: valor=20, cambios=1
# =============================================================================

# Tu código aquí

# h = Historial(10)
# print(h)
# h.valor = 20
# print(h)
# h.valor = 50
# print(h)
# h.valor = 50  # mismo valor, no registra cambio
# print(h)
# print(f"Último cambio: {h.ultimo_cambio}")
# print("Historial completo:")
# for linea in h.historial_completo():
#     print(f"  {linea}")
# h.revertir()
# print("Después de revertir:")
# print(h)
