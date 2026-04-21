# PASO 1
a = 10
b = 5

def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    return a / b

print(sumar(a, b))
print(restar(a, b))
print(multiplicar(a, b))
print(dividir(a, b))

# PASO 2
operaciones = {
    "+": sumar,
    "-": restar,
    "*": multiplicar,
    "/": dividir,
}

for operacion in ["+", "-", "*", "/", "%"]:
    if operacion in operaciones:
        resultado = operaciones[operacion](a, b)
        print(f"Resultado: {resultado}")
    else:
        print("Operación no válida")
