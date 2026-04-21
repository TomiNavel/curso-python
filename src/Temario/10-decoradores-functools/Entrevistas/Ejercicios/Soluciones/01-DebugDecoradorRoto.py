# =====================
# SOLUCIÓN
# =====================
# Error 1: el wrapper no devuelve el resultado de func(). La línea
#   func(*args, **kwargs) se ejecuta pero el resultado se descarta.
#   Corrección: return func(*args, **kwargs)
#
# Error 2: (consecuencia del error 1) sumar(3, 5) devuelve None en
#   lugar de 8.
#
# Error 3: el decorador no usa @wraps, por lo que __name__ devuelve
#   "wrapper" y __doc__ devuelve None.
#   Corrección: añadir @wraps(func) al wrapper.
#
# ERRORES CORREGIDOS:
# 1. Añadir "return func(*args, **kwargs)" en el wrapper
# 2. (resuelto con el error 1)
# 3. Añadir "from functools import wraps" y "@wraps(func)" antes de wrapper


from functools import wraps

def mi_decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

resultado = sumar(3, 5)
print(resultado)

print(sumar.__name__)
print(sumar.__doc__)
