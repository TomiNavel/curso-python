# =============================================================================
# EJERCICIO 1: Calcular días entre dos fechas
# =============================================================================
# Escribe una función "dias_entre(fecha1, fecha2)" que reciba dos objetos
# date y devuelva el número de días completos entre ambos (valor absoluto,
# siempre positivo).
#
# RESULTADO ESPERADO:
# 7
# 7
# 365
# =============================================================================

from datetime import date


# Tu código aquí


# Pruebas
print(dias_entre(date(2026, 4, 22), date(2026, 4, 29)))
print(dias_entre(date(2026, 4, 29), date(2026, 4, 22)))
print(dias_entre(date(2026, 1, 1), date(2027, 1, 1)))
