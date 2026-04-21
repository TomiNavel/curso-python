# PASO 1
def sumar_todos(*args):
    total = 0
    for n in args:
        total += n
    return total

print(f"Total: {sumar_todos(10, 20, 30, 40, 50)}")
print(f"Total: {sumar_todos()}")

# PASO 2
def mostrar_datos(**kwargs):
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar_datos(nombre="Ana", edad=28, ciudad="Madrid", profesion="Ingeniera")

# PASO 3
def crear_perfil(nombre, edad, **kwargs):
    base = f"{nombre} ({edad})"
    if kwargs:
        extras = ", ".join(str(v) for v in kwargs.values())
        return f"{base} - {extras}"
    return base

print(crear_perfil("Ana", 28, ciudad="Madrid", profesion="Ingeniera"))
print(crear_perfil("Pedro", 35))
