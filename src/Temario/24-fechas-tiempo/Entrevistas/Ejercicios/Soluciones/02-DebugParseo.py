# =====================
# SOLUCIÓN
# =====================
# Error 1: el formato de entrada de strptime es incorrecto. El texto viene
#   como "YYYY-MM-DD" pero el patrón dice "%d-%m-%Y" (DD-MM-YYYY). Con el
#   texto "2026-04-22", el intento de interpretar 2026 como día lanza
#   ValueError.
#   Solución: usar "%Y-%m-%d".
#
# Error 2: el formato de salida usa "%y" (año de 2 dígitos) en lugar de
#   "%Y" (año de 4 dígitos). Para 2026 produciría "26" en lugar de "2026".
#   Solución: usar "%Y" mayúscula.
#
# Error 3: la función no protege strptime contra inputs que no encajan.
#   "22/04/2026" y "no es fecha" lanzan ValueError y hacen fallar todo el
#   script. El enunciado pide devolver None en esos casos.
#   Solución: envolver en try/except ValueError.
#
# ERRORES CORREGIDOS:
# 1. formato entrada "%d-%m-%Y" → "%Y-%m-%d"
# 2. formato salida "%y" → "%Y"
# 3. falta try/except para inputs inválidos → devolver None

from datetime import datetime


def reformatear(texto):
    try:
        fecha = datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        return None
    return fecha.strftime("%d/%m/%Y")


# Pruebas
print(reformatear("2026-04-22"))
print(reformatear("2025-12-31"))
print(reformatear("22/04/2026"))
print(reformatear("no es fecha"))
