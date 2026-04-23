# =============================================================================
# EJERCICIO 5: Convertir entre zonas horarias
# =============================================================================
# Escribe una función "convertir_a_madrid(instante_utc)" que reciba un
# datetime aware en UTC y devuelva el mismo instante expresado en la zona
# "Europe/Madrid", como datetime aware.
#
# El parámetro siempre será un datetime aware (con tzinfo=timezone.utc).
#
# RESULTADO ESPERADO:
# 2026-04-22 16:30:00+02:00
# 2026-01-22 15:30:00+01:00
# =============================================================================

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# Tu código aquí


# Pruebas: el primero está en verano (UTC+2), el segundo en invierno (UTC+1).
print(convertir_a_madrid(datetime(2026, 4, 22, 14, 30, tzinfo=timezone.utc)))
print(convertir_a_madrid(datetime(2026, 1, 22, 14, 30, tzinfo=timezone.utc)))
