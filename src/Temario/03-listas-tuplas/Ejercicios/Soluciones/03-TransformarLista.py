"""
Solución: Transformar lista
"""

numeros = [10, 20, 30, 40, 50, 60, 70, 80]

copia = numeros.copy()

invertida = copia[::-1]
print(f"Copia invertida: {invertida}")

print(f"Original intacta: {numeros}")

fragmento = numeros[2:5]
print(f"Fragmento [2:5]: {fragmento}")

numeros[1:3] = [99, 88]
print(f"Después de reemplazar [1:3]: {numeros}")

print(f"Primeros 3: {numeros[:3]}")
print(f"Últimos 3: {numeros[-3:]}")

print(f"Cada 2: {numeros[::2]}")
