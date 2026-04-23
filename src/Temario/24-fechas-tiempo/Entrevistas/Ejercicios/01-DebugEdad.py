# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Calcular edad
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "calcular_edad(fecha_nacimiento, hoy)" debe devolver la edad
# en años cumplidos a la fecha dada. Si el cumpleaños todavía no ha llegado
# en el año actual, la edad es un año menos.
#
# Ambas entradas son objetos date.
#
# RESULTADO ESPERADO:
# 30
# 29
# 0
# =============================================================================

from datetime import date, datetime


def calcular_edad(fecha_nacimiento, hoy):
    delta = datetime.now() - fecha_nacimiento
    return delta.days // 365


# Pruebas
# Nacimiento 22/04/1996, hoy 22/04/2026 → 30 años exactos
print(calcular_edad(date(1996, 4, 22), date(2026, 4, 22)))
# Nacimiento 22/04/1996, hoy 21/04/2026 → aún no cumplió, 29
print(calcular_edad(date(1996, 4, 22), date(2026, 4, 21)))
# Nacimiento 22/04/2026, hoy 22/04/2026 → 0
print(calcular_edad(date(2026, 4, 22), date(2026, 4, 22)))
