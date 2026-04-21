class LongitudError(Exception):
    pass

class ComplejidadError(Exception):
    pass


def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        raise LongitudError(f"Mínimo 8 caracteres, tiene {len(contrasena)}")

    if not any(c.isdigit() for c in contrasena):
        raise ComplejidadError("Debe contener al menos un dígito")

    return True


def registrar_contrasena(contrasena):
    try:
        validar_contrasena(contrasena)
    except LongitudError as e:
        print(f"Longitud: {e}")
    except ComplejidadError as e:
        print(f"Complejidad: {e}")
    else:
        print("Contraseña registrada correctamente")


registrar_contrasena("abc")
registrar_contrasena("abcdefgh")
registrar_contrasena("abcdef1g")
