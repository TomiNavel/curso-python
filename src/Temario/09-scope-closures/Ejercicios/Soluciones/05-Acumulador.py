def crear_acumulador():
    total = 0

    def agregar(valor):
        nonlocal total
        total += valor
        return total

    def obtener_total():
        return total

    return agregar, obtener_total


# Pruebas
agregar, obtener_total = crear_acumulador()

print(agregar(10))        # 10
print(agregar(15))        # 25
print(obtener_total())    # 25
print(agregar(5))         # 30
print(obtener_total())    # 30
