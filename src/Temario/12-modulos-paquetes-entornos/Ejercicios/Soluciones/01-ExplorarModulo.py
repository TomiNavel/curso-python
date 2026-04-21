def explorar_modulo(nombre):
    try:
        modulo = __import__(nombre)
    except ModuleNotFoundError:
        return {"error": f"Módulo '{nombre}' no encontrado"}

    nombres_publicos = [n for n in dir(modulo) if not n.startswith("_")]

    funciones = [n for n in nombres_publicos if callable(getattr(modulo, n))]
    constantes = [
        n for n in nombres_publicos
        if not callable(getattr(modulo, n)) and n.isupper()
    ]

    return {
        "nombre": nombre,
        "funciones": funciones,
        "constantes": constantes,
        "total_publicos": len(nombres_publicos),
    }


info_math = explorar_modulo("math")
print(f"Nombre: {info_math['nombre']}")
print(f"Funciones (primeras 5): {info_math['funciones'][:5]}")
print(f"Constantes: {info_math['constantes']}")
print(f"Total públicos: {info_math['total_publicos']}")
print()

info_string = explorar_modulo("string")
print(f"Nombre: {info_string['nombre']}")
print(f"Constantes: {info_string['constantes']}")
print()

info_falso = explorar_modulo("modulo_falso")
print(info_falso)
