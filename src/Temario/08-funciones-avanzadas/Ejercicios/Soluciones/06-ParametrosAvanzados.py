# PASO 1
def potencia(base, exponente, /):
    return base ** exponente

print(potencia(2, 10))
print(potencia(4, 5))

# PASO 2
def saludar(nombre, *, saludo="Hola"):
    return f"{saludo}, {nombre}!"

print(saludar("Ana"))
print(saludar("Pedro", saludo="Buenos días"))

# PASO 3
def conectar(host, /, puerto, *, timeout=30):
    return f"conectado a {host}:{puerto} (timeout={timeout})"

print(conectar("localhost", 5432))
print(conectar("miservidor", puerto=3306, timeout=10))
