# =============================================================================
# SOLUCIÓN
# =============================================================================

from datetime import datetime


def formatear_duracion(inicio: datetime, fin: datetime) -> str:
    total = int((fin - inicio).total_seconds())
    horas, resto = divmod(total, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas}h {minutos}m {segundos}s"


# Pruebas
print(formatear_duracion(datetime(2026, 4, 22, 9, 0), datetime(2026, 4, 22, 17, 30)))
print(formatear_duracion(datetime(2026, 4, 22, 9, 0), datetime(2026, 4, 22, 9, 5, 45)))
print(formatear_duracion(datetime(2026, 4, 22, 0, 0), datetime(2026, 4, 23, 1, 0)))
