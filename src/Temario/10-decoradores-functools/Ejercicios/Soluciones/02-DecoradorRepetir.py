from functools import wraps


def repetir(veces):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultados = []
            for _ in range(veces):
                resultados.append(func(*args, **kwargs))
            return resultados
        return wrapper
    return decorador


# Pruebas
@repetir(veces=3)
def sumar(a, b):
    return a + b

@repetir(veces=2)
def saludar(nombre):
    return f"Hola, {nombre}"

print(sumar(1, 5))
print(saludar("Ana"))
