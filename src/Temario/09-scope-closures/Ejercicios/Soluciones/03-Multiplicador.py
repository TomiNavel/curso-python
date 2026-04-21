def crear_operacion(operador, valor):
    operaciones = {
        "+": lambda n: n + valor,
        "-": lambda n: n - valor,
        "*": lambda n: n * valor,
        "/": lambda n: n / valor,
    }

    operacion = operaciones.get(operador)

    def aplicar(n):
        if operacion is None:
            return None
        return operacion(n)

    return aplicar


# Pruebas
sumar5 = crear_operacion("+", 5)
restar7 = crear_operacion("-", 7)
por10 = crear_operacion("*", 10)
entre5 = crear_operacion("/", 5)
invalida = crear_operacion("%", 3)

print(sumar5(10))     # 15
print(restar7(10))    # 3
print(por10(5))       # 50
print(entre5(10))     # 2.0
print(invalida(10))   # None
