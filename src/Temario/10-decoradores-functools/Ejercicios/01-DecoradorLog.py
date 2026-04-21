# =============================================================================
# EJERCICIO 1: Decorador de Logging
# =============================================================================
# Crea un decorador llamado "log" que imprima el nombre de la función,
# los argumentos recibidos y el resultado devuelto cada vez que se ejecute.
# Usa @wraps para preservar los metadatos.
#
# RESULTADO ESPERADO:
# [LOG] sumar(3, 5) -> 8
# 8
# [LOG] saludar('Ana', saludo='Buenos días') -> Buenos días, Ana
# Buenos días, Ana
# =============================================================================

from functools import wraps

# Tu código aquí


# Pruebas
@log
def sumar(a, b):
    return a + b

@log
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}"

print(sumar(3, 5))
print(saludar("Ana", saludo="Buenos días"))
