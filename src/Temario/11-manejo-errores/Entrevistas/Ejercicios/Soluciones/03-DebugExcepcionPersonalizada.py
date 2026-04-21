# =====================
# SOLUCIÓN
# =====================
# Error 1: Las excepciones están intercambiadas en las validaciones. Cuando el
#   nombre es inválido se lanza EdadNoValidaError, y cuando la edad es inválida
#   se lanza NombreNoValidoError. Solución: intercambiar las excepciones para
#   que cada validación lance la excepción correcta.
#
# Error 2: Dentro de procesar_registro, "print(resultado)" se ejecuta fuera
#   del try/except. Cuando la función lanza una excepción, "resultado" nunca
#   se asigna, y esa línea falla con UnboundLocalError. Además, en los casos
#   de error no debería imprimirse resultado. Solución: mover el print al
#   bloque else del try/except.
#
# Error 3: Consecuencia del error 1. Como las excepciones están intercambiadas,
#   los except capturan la excepción equivocada y muestran el prefijo
#   incorrecto ("Error de edad" cuando es de nombre, y viceversa).
#
# ERRORES CORREGIDOS:
# 1. Lanzar NombreNoValidoError para nombre vacío
# 2. Lanzar EdadNoValidaError para edad negativa
# 3. Mover print(resultado) al bloque else


class EdadNoValidaError(Exception):
    pass

class NombreNoValidoError(Exception):
    pass


def registrar_persona(nombre, edad):
    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        raise NombreNoValidoError(f"Nombre no válido: (vacío)")

    if edad < 0:
        raise EdadNoValidaError(f"Edad no válida: {edad}")

    return f"Persona registrada: {nombre_limpio} ({edad} años)"


def procesar_registro(nombre, edad):
    try:
        resultado = registrar_persona(nombre, edad)
    except EdadNoValidaError as e:
        print(f"Error de edad: {e}")
    except NombreNoValidoError as e:
        print(f"Error de nombre: {e}")
    else:
        print(resultado)


procesar_registro("Ana", -5)
procesar_registro("Ana", 30)
procesar_registro("  ", 25)
