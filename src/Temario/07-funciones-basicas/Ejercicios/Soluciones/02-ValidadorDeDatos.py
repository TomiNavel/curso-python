# PASO 1
def es_edad_valida(edad):
    return 0 <= edad <= 120

print(es_edad_valida(25))
print(es_edad_valida(-5))
print(es_edad_valida(120))

# PASO 2
def es_nombre_valido(nombre):
    nombre = nombre.strip()
    if len(nombre) == 0:
        return False
    return nombre.replace(" ", "").isalpha()

print(es_nombre_valido("Ana María"))
print(es_nombre_valido(""))
print(es_nombre_valido("Pedro123"))

# PASO 3
nombres = ["Ana", "Pedro", "", "12"]
for nombre in nombres:
    if es_nombre_valido(nombre):
        print(f"{nombre}: válido")
    else:
        print(f"{nombre}: no válido")
