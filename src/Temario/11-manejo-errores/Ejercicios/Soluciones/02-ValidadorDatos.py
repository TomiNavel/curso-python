def validar_edad(valor):
    # Intentar convertir a entero si es string
    if isinstance(valor, str):
        try:
            valor = int(valor)
        except ValueError:
            raise TypeError(
                f"Se esperaba un entero, se recibió: {valor!r} ({type(valor).__name__})"
            )

    if not isinstance(valor, int):
        raise TypeError(
            f"Se esperaba un entero, se recibió: {valor!r} ({type(valor).__name__})"
        )

    if valor < 0:
        raise ValueError(f"La edad no puede ser negativa, se recibió: {valor}")

    if valor > 150:
        raise ValueError(f"La edad no puede superar 150, se recibió: {valor}")

    return valor


def registrar_usuario(nombre, edad):
    try:
        edad_validada = validar_edad(edad)
    except TypeError as e:
        print(f"Error de tipo: {e}")
    except ValueError as e:
        print(f"Error de valor: {e}")
    else:
        print(f"Usuario {nombre} registrado con edad {edad_validada}")


registrar_usuario("Ana", 25)
registrar_usuario("Bob", "veinticinco")
registrar_usuario("Clara", -5)
registrar_usuario("Diana", 200)
registrar_usuario("Carlos", "30")
