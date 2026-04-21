# =============================================================================
# EJERCICIO 2: Rango Numérico
# =============================================================================
# Crea una clase `RangoNumerico` que represente un valor dentro de un rango
# permitido, usando properties para la validación.
#
# Atributos internos:
# - _valor (float)
# - _minimo (float)
# - _maximo (float)
#
# Properties:
# - valor: getter y setter. El setter clampea el valor al rango [minimo, maximo]
#   (si es menor que minimo, se asigna minimo; si es mayor que maximo, se asigna maximo).
# - minimo: solo getter
# - maximo: solo getter
# - porcentaje: property calculada. Devuelve qué porcentaje del rango
#   representa el valor actual (0.0 a 100.0), redondeado a 1 decimal.
#   Fórmula: (valor - minimo) / (maximo - minimo) * 100
#
# __str__: "50.0 [0 - 100] (50.0%)"
# __repr__: RangoNumerico(50.0, 0, 100)
#
# RESULTADO ESPERADO:
# 50.0 [0 - 100] (50.0%)
# 75.0 [0 - 100] (75.0%)
# 100 [0 - 100] (100.0%)
# 0 [0 - 100] (0.0%)
# 36.5 [-20 - 80] (56.5%)
# =============================================================================

# Tu código aquí

# r = RangoNumerico(50, 0, 100)
# print(r)
# r.valor = 75
# print(r)
# r.valor = 150  # clampea a 100
# print(r)
# r.valor = -10  # clampea a 0
# print(r)
#
# r2 = RangoNumerico(36.5, -20, 80)
# print(r2)
