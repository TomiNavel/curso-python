# =============================================================================
# EJERCICIO 4: Formatear duración en texto legible
# =============================================================================
# Escribe una función "formatear_duracion(inicio, fin)" que reciba dos
# objetos datetime y devuelva un string con la diferencia expresada como
# "Xh Ym Zs" (horas, minutos y segundos, sin ceros de relleno).
#
# Asume que fin >= inicio. No hace falta gestionar días completos: si pasan
# más de 24 horas, las horas se expresan como total (p. ej. "30h 0m 0s").
#
# RESULTADO ESPERADO:
# 8h 30m 0s
# 0h 5m 45s
# 25h 0m 0s
# =============================================================================

from datetime import datetime


# Tu código aquí


# Pruebas
print(formatear_duracion(datetime(2026, 4, 22, 9, 0), datetime(2026, 4, 22, 17, 30)))
print(formatear_duracion(datetime(2026, 4, 22, 9, 0), datetime(2026, 4, 22, 9, 5, 45)))
print(formatear_duracion(datetime(2026, 4, 22, 0, 0), datetime(2026, 4, 23, 1, 0)))
