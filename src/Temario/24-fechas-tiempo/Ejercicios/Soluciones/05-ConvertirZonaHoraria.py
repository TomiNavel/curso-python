# =============================================================================
# SOLUCIÓN
# =============================================================================

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def convertir_a_madrid(instante_utc: datetime) -> datetime:
    # astimezone preserva el instante absoluto y cambia la representación
    # a la zona indicada. El desfase lo gestiona ZoneInfo según las reglas
    # de DST de IANA, así que invierno y verano dan offsets distintos.
    return instante_utc.astimezone(ZoneInfo("Europe/Madrid"))


# Pruebas
print(convertir_a_madrid(datetime(2026, 4, 22, 14, 30, tzinfo=timezone.utc)))
print(convertir_a_madrid(datetime(2026, 1, 22, 14, 30, tzinfo=timezone.utc)))
