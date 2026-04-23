# =============================================================================
# EJERCICIO 3: Añadir días laborables
# =============================================================================
# Escribe una función "sumar_laborables(fecha, n)" que, partiendo de una
# fecha dada, avance n días laborables (lunes a viernes) y devuelva la
# fecha resultante. Ignora sábados y domingos durante el recorrido.
# Los festivos no se tienen en cuenta.
#
# Pista: weekday() devuelve 0=lunes ... 6=domingo.
#
# RESULTADO ESPERADO:
# 2026-04-29
# 2026-05-01
# 2026-04-24
# =============================================================================

from datetime import date, timedelta


# Tu código aquí


# Pruebas: el 2026-04-22 es miércoles
print(sumar_laborables(date(2026, 4, 22), 5))   # 5 laborables → miércoles siguiente
print(sumar_laborables(date(2026, 4, 27), 4))   # 4 laborables desde lunes → viernes
print(sumar_laborables(date(2026, 4, 22), 2))   # 2 laborables desde miércoles → viernes
