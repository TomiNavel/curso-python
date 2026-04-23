# =============================================================================
# SOLUCIÓN
# =============================================================================

from datetime import date


def dias_entre(fecha1: date, fecha2: date) -> int:
    # Restar dos date devuelve un timedelta; .days da la parte entera.
    return abs((fecha2 - fecha1).days)


# Pruebas
print(dias_entre(date(2026, 4, 22), date(2026, 4, 29)))
print(dias_entre(date(2026, 4, 29), date(2026, 4, 22)))
print(dias_entre(date(2026, 1, 1), date(2027, 1, 1)))
