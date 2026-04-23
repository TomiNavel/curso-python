# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Conversión entre zonas horarias
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "hora_en_tokio(texto_utc)" recibe un texto en formato ISO
# "YYYY-MM-DDTHH:MM:SS" que representa un instante en UTC, y devuelve
# la hora equivalente en Tokio como string "HH:MM".
#
# RESULTADO ESPERADO:
# 23:30
# 08:15
# =============================================================================

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def hora_en_tokio(texto_utc):
    dt = datetime.strptime(texto_utc, "%Y-%m-%dT%H:%M:%S")
    dt_tokio = dt.astimezone(ZoneInfo("Asia/Tokyo"))
    return dt_tokio.strftime("%h:%M")


# Pruebas
print(hora_en_tokio("2026-04-22T14:30:00"))   # 14:30 UTC → 23:30 Tokio
print(hora_en_tokio("2026-04-21T23:15:00"))   # 23:15 UTC → 08:15 del día siguiente
