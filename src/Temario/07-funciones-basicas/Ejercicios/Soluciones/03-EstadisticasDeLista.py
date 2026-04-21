# PASO 1
def mayor(numeros):
    resultado = numeros[0]
    for n in numeros:
        if n > resultado:
            resultado = n
    return resultado

def menor(numeros):
    resultado = numeros[0]
    for n in numeros:
        if n < resultado:
            resultado = n
    return resultado

def suma(numeros):
    total = 0
    for n in numeros:
        total += n
    return total

def promedio(numeros):
    return suma(numeros) / len(numeros)

numeros = [45, 23, 67, 15, 92, 61]
print(f"Mayor: {mayor(numeros)}")
print(f"Menor: {menor(numeros)}")
print(f"Suma: {suma(numeros)}")
print(f"Promedio: {promedio(numeros)}")

# PASO 2
def resumen(numeros):
    return mayor(numeros), menor(numeros), suma(numeros), promedio(numeros)

ma, me, su, pr = resumen(numeros)
print(f"Resumen: mayor={ma}, menor={me}, suma={su}, promedio={pr}")
