# =====================
# SOLUCIÓN
# =====================
# Error 1: la función ignora el parámetro "hoy" y usa datetime.now(). Esto
#   hace imposibles los tests reproducibles y devuelve la edad respecto a
#   la hora de ejecución, no a la fecha que el llamador pidió. Además,
#   datetime.now() devuelve un datetime y fecha_nacimiento es un date, así
#   que la resta lanza TypeError.
#   Solución: usar el parámetro "hoy" en la resta.
#
# Error 2: dividir los días entre 365 da un resultado impreciso por los
#   años bisiestos. Para 30 años, el resultado puede ser 29 o 30 según
#   la cantidad exacta de bisiestos. El cálculo correcto de edad no se
#   basa en días, sino en comparar componentes año/mes/día.
#   Solución: calcular la edad como diferencia de años, ajustada si el
#   cumpleaños aún no ha llegado en el año actual.
#
# Error 3: no se considera el caso "todavía no cumplió este año". Incluso
#   con el cálculo correcto de años, hay que restar 1 si la fecha de hoy
#   es anterior al cumpleaños del año actual.
#   Solución: comparar (mes, día) para decidir si se resta 1.
#
# ERRORES CORREGIDOS:
# 1. datetime.now() en lugar del parámetro hoy → usar hoy
# 2. delta.days // 365 impreciso → diferencia de años
# 3. falta ajuste si el cumple no ha llegado → comparar (mes, día)

from datetime import date


def calcular_edad(fecha_nacimiento, hoy):
    edad = hoy.year - fecha_nacimiento.year
    # Si (mes, día) de hoy es anterior al (mes, día) de nacimiento en el
    # año actual, aún no ha cumplido años.
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


# Pruebas
print(calcular_edad(date(1996, 4, 22), date(2026, 4, 22)))
print(calcular_edad(date(1996, 4, 22), date(2026, 4, 21)))
print(calcular_edad(date(2026, 4, 22), date(2026, 4, 22)))
