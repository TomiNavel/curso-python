# =============================================================================
# EJERCICIO 1: Anotar funciones
# =============================================================================
# Añade type hints a las tres funciones siguientes. No modifiques la lógica,
# solo añade las anotaciones de tipo a los parámetros y al valor de retorno.
#
# RESULTADO ESPERADO:
# 15
# Hola, Ana
# Hola, invitado
# [2, 4, 6]
# =============================================================================


def area_rectangulo(base, altura):
    return base * altura


def saludar(nombre=None):
    if nombre is None:
        return "Hola, invitado"
    return f"Hola, {nombre}"


def filtrar_pares(numeros):
    return [n for n in numeros if n % 2 == 0]


# Pruebas
print(area_rectangulo(3, 5))
print(saludar("Ana"))
print(saludar())
print(filtrar_pares([1, 2, 3, 4, 5, 6]))
