# =============================================================================
# SOLUCIÓN
# =============================================================================

from datetime import date, timedelta


def sumar_laborables(fecha: date, n: int) -> date:
    actual = fecha
    restantes = n
    while restantes > 0:
        actual += timedelta(days=1)
        # weekday() devuelve 0..4 para lunes..viernes, 5..6 para fin de semana.
        if actual.weekday() < 5:
            restantes -= 1
    return actual


# Pruebas
print(sumar_laborables(date(2026, 4, 22), 5))
print(sumar_laborables(date(2026, 4, 27), 4))
print(sumar_laborables(date(2026, 4, 22), 2))
