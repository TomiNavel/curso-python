# PASO 1
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}"

print(saludar("Ana"))
print(saludar("Ana", saludo="Buenos días"))

# PASO 2
def crear_titulo(texto, separador="---"):
    return f"{separador} {texto} {separador}"

print(crear_titulo("Sección 1"))
print(crear_titulo("Sección 1", separador="==="))
print(crear_titulo("Importante", separador="***"))

# PASO 3
def ficha_persona(nombre, edad="desconocida", ciudad="desconocida"):
    return f"Nombre: {nombre}, Edad: {edad}, Ciudad: {ciudad}"

print(ficha_persona("Ana", edad=28, ciudad="Madrid"))
print(ficha_persona("Pedro"))
