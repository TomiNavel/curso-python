# PASO 1
numeros = [-5, 3, -2, 7, 0, 1, -8, 9]
print(list(filter(lambda n: n > 0, numeros)))

# PASO 2
textos = ["hola", "", "mundo", "", ""]
print(list(filter(lambda t: t != "", textos)))

# PASO 3
datos = [0, "", 42, None, "hola", False, True, 3.14, []]
print(list(filter(None, datos)))

# PASO 4
notas = [85, 42, 91, 67, 38, 73]

def es_aprobado(nota):
    return nota >= 50

print(list(filter(es_aprobado, notas)))
