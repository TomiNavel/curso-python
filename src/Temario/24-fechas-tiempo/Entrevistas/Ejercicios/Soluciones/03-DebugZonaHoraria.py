# =====================
# SOLUCIÓN
# =====================
# Error 1: strptime devuelve un datetime naive (sin zona horaria), y
#   astimezone sobre un naive lanza ValueError porque no sabe de qué
#   zona partir. Hay que marcar el datetime como UTC antes de convertir.
#   Solución: aplicar .replace(tzinfo=timezone.utc) tras el strptime,
#   o usar fromisoformat y asignar la zona explícitamente.
#
# Error 2: el formato de salida usa "%h:%M". "%h" no es un marcador válido
#   de strftime (en algunos locales coincide con %b, nombre abreviado del
#   mes). El marcador correcto para hora 24h con dos dígitos es "%H".
#   Solución: cambiar "%h" por "%H".
#
# Error 3 (menor): parsear con strptime funciona para este formato, pero
#   fromisoformat es la opción idiomática desde Python 3.7 para ISO 8601
#   y evita tener que recordar los marcadores. Ambos enfoques son válidos;
#   aquí adoptamos fromisoformat para que el código sea más limpio y el
#   fix del error 1 quede más claro asignando la zona al construir.
#
# ERRORES CORREGIDOS:
# 1. astimezone sobre naive → marcar como UTC antes
# 2. "%h:%M" → "%H:%M"
# 3. strptime para ISO → fromisoformat (mejora opcional de legibilidad)

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def hora_en_tokio(texto_utc):
    dt = datetime.fromisoformat(texto_utc).replace(tzinfo=timezone.utc)
    dt_tokio = dt.astimezone(ZoneInfo("Asia/Tokyo"))
    return dt_tokio.strftime("%H:%M")


# Pruebas
print(hora_en_tokio("2026-04-22T14:30:00"))
print(hora_en_tokio("2026-04-21T23:15:00"))
