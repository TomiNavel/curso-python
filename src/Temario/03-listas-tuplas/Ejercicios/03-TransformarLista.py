"""
Ejercicio: Transformar lista

Dada una lista de números, realiza las siguientes operaciones e imprime
el resultado de cada una:

1. Crear una copia independiente de la lista con .copy()
2. Invertir la copia usando slicing [::-1] (sin modificar la original)
3. Mostrar la original para verificar que no cambió
4. Extraer los elementos del índice 2 al 5 (sin incluir el 5) usando slicing
5. Reemplazar los elementos del índice 1 al 3 por [99, 88] en la lista original
6. Mostrar los 3 primeros y los 3 últimos elementos de la original usando slicing
7. Mostrar la lista original con elementos tomados de 2 en 2 (paso 2)

Resultado esperado para numeros = [10, 20, 30, 40, 50, 60, 70, 80]:
    Copia invertida: [80, 70, 60, 50, 40, 30, 20, 10]
    Original intacta: [10, 20, 30, 40, 50, 60, 70, 80]
    Fragmento [2:5]: [30, 40, 50]
    Después de reemplazar [1:3]: [10, 99, 88, 40, 50, 60, 70, 80]
    Primeros 3: [10, 99, 88]
    Últimos 3: [60, 70, 80]
    Cada 2: [10, 88, 50, 70]
"""

numeros = [10, 20, 30, 40, 50, 60, 70, 80]

# Tu código aquí
