# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Parseo y formateo
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "reformatear(texto)" recibe una fecha en formato "YYYY-MM-DD"
# y devuelve la misma fecha en formato "DD/MM/YYYY". Si el texto no encaja
# con el formato de entrada, debe devolver None.
#
# RESULTADO ESPERADO:
# 22/04/2026
# 31/12/2025
# None
# None
# =============================================================================

from datetime import datetime


def reformatear(texto):
    fecha = datetime.strptime(texto, "%d-%m-%Y")
    return fecha.strftime("%d/%m/%y")


# Pruebas
print(reformatear("2026-04-22"))
print(reformatear("2025-12-31"))
print(reformatear("22/04/2026"))
print(reformatear("no es fecha"))
