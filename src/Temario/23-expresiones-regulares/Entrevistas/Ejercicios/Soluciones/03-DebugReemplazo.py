# =====================
# SOLUCIÓN
# =====================
# Error 1: ni el patrón ni el reemplazo usan raw string. Sin r, "\1", "\2"
#   y "\3" se interpretan como escapes de Python (caracteres de control),
#   no como referencias a grupos capturados. Lo mismo ocurre con "\d" del
#   patrón.
#   Solución: añadir el prefijo r a ambos strings.
#
# Error 2: el patrón usa \d+, que encaja con 1 o más dígitos. Esto convierte
#   incorrectamente "1/2/3" porque cumple el patrón aunque no sea una fecha
#   DD/MM/YYYY válida.
#   Solución: usar cuantificadores exactos: \d{2}/\d{2}/\d{4}.
#
# Error 3: el reemplazo es "\1-\2-\3", que produce DD-MM-YYYY. El formato
#   deseado es YYYY-MM-DD, así que el orden debe invertirse a \3-\2-\1.
#   Solución: cambiar el reemplazo a r"\3-\2-\1".
#
# ERRORES CORREGIDOS:
# 1. strings sin prefijo r → usar raw strings
# 2. \d+ permisivo → \d{2}/\d{2}/\d{4} exacto
# 3. reemplazo \1-\2-\3 → \3-\2-\1

import re


def convertir_fechas(texto):
    patron = r"(\d{2})/(\d{2})/(\d{4})"
    return re.sub(patron, r"\3-\2-\1", texto)


# Pruebas
print(convertir_fechas("Ana nació el 22/04/2026 y Luis el 03/01/2025."))
print(convertir_fechas("No convertir: 12/34 ni 1/2/3."))
