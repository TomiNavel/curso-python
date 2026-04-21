def crear_contador(inicio):
    valor = inicio

    def incrementar():
        nonlocal valor
        valor += 1
        return valor

    return incrementar


# Pruebas
contador = crear_contador(0)
print(contador())  # 1
print(contador())  # 2
print(contador())  # 3

otro = crear_contador(9)
print(otro())  # 10
print(otro())  # 11
