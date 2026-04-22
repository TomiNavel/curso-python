# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Invertir formato de fecha
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "convertir_fechas(texto)" debe tomar un texto con fechas en
# formato DD/MM/YYYY (dos dígitos / dos dígitos / cuatro dígitos) y devolver
# el mismo texto con las fechas convertidas al formato YYYY-MM-DD.
# Por ejemplo: "nacido el 22/04/2026" debe convertirse en "nacido el 2026-04-22".
#
# Solo deben convertirse fechas con la estructura completa DD/MM/YYYY.
# No tocar "12/34" ni "1/2/3" porque no tienen los dígitos exigidos.
#
# RESULTADO ESPERADO:
# Ana nació el 2026-04-22 y Luis el 2025-01-03.
# No convertir: 12/34 ni 1/2/3.
# =============================================================================

import re


def convertir_fechas(texto):
    patron = "(\d+)/(\d+)/(\d+)"
    return re.sub(patron, "\1-\2-\3", texto)


# Pruebas
print(convertir_fechas("Ana nació el 22/04/2026 y Luis el 03/01/2025."))
print(convertir_fechas("No convertir: 12/34 ni 1/2/3."))
