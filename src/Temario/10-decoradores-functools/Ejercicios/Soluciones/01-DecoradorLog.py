from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Formatear argumentos posicionales y keyword para el mensaje
        partes = [repr(a) for a in args]
        partes += [f"{k}={v!r}" for k, v in kwargs.items()]
        firma = ", ".join(partes)

        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__}({firma}) -> {resultado}")
        return resultado
    return wrapper


# Pruebas
@log
def sumar(a, b):
    return a + b

@log
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}"

print(sumar(3, 5))
print(saludar("Ana", saludo="Buenos días"))
