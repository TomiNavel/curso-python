# PASO 1
def doble(n):
    return n * 2

def cuadrado(n):
    return n ** 2

def es_par(n):
    return n % 2 == 0

# PASO 2
def aplicar(lista, operacion):
    resultado = []
    for elemento in lista:
        resultado.append(operacion(elemento))
    return resultado

# PASO 3
numeros = [1, 2, 3, 4, 5]
print(aplicar(numeros, doble))
print(aplicar(numeros, cuadrado))
print(aplicar(numeros, es_par))
print(aplicar(numeros, str))
