# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Excepción Personalizada
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Error de edad: Edad no válida: -5
# Persona registrada: Ana (30 años)
# Error de nombre: Nombre no válido: (vacío)
# =============================================================================

class EdadNoValidaError(Exception):
    pass

class NombreNoValidoError(Exception):
    pass


def registrar_persona(nombre, edad):
    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        raise EdadNoValidaError(f"Nombre no válido: (vacío)")

    if edad < 0:
        raise NombreNoValidoError(f"Edad no válida: {edad}")

    return f"Persona registrada: {nombre_limpio} ({edad} años)"


def procesar_registro(nombre, edad):
    try:
        resultado = registrar_persona(nombre, edad)
    except EdadNoValidaError as e:
        print(f"Error de edad: {e}")
    except NombreNoValidoError as e:
        print(f"Error de nombre: {e}")
    print(resultado)


procesar_registro("Ana", -5)
procesar_registro("Ana", 30)
procesar_registro("  ", 25)
