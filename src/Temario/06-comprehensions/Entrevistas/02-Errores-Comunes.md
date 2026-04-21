# Errores Comunes: Comprehensions

## Error 1: Poner `if/else` después del `for`

```python
# MAL — SyntaxError
resultado = [x for x in range(10) if x > 5 else x + 10]

# BIEN — if/else va ANTES del for (es una expresión condicional)
resultado = [x if x > 5 else x + 10 for x in range(10)]
```

El `if` después del `for` es para filtrar y no admite `else`. Si se necesita `else`, es una transformación condicional y va antes del `for`. Es probablemente el error de sintaxis más frecuente con comprehensions.

---

## Error 2: Usar comprehensions para efectos secundarios

```python
# MAL — crea una lista de None sin propósito
[print(nombre) for nombre in nombres]

# BIEN — usar un bucle for
for nombre in nombres:
    print(nombre)
```

Las comprehensions existen para **crear colecciones**. Usarlas solo por su efecto secundario (`print()`, modificar otra variable, escribir en un archivo) es un antipatrón: crea una lista innecesaria en memoria y oscurece la intención del código.

---

## Error 3: Comprehensions ilegibles por exceso de complejidad

```python
# MAL — imposible de entender de un vistazo
resultado = [x + y for x in range(10) for y in range(10) if x != y if (x + y) % 3 == 0 if x > 2]

# BIEN — bucle for cuando la lógica es compleja
resultado = []
for x in range(10):
    for y in range(10):
        if x != y and (x + y) % 3 == 0 and x > 2:
            resultado.append(x + y)
```

Si una comprehension necesita más de dos `for` o múltiples condiciones, pierde su ventaja de legibilidad. La regla es simple: si no se entiende de un vistazo, usar un bucle.

---

## Error 4: Orden incorrecto de los `for` en comprehensions anidadas

```python
matriz = [[1, 2], [3, 4], [5, 6]]

# MAL — NameError: 'fila' is not defined
plana = [num for num in fila for fila in matriz]

# BIEN — el for externo va primero (igual que en bucles anidados)
plana = [num for fila in matriz for num in fila]
```

Los `for` en una comprehension se leen de izquierda a derecha, en el mismo orden que se escribirían como bucles anidados. El `for` externo (que define la variable usada por el interno) siempre va primero.

---

## Error 5: Confundir `{}` vacío con un set vacío

```python
# Esto NO es un set vacío, es un diccionario vacío
vacio = {}
print(type(vacio))  # <class 'dict'>

# Para crear un set vacío hay que usar set()
vacio = set()
print(type(vacio))  # <class 'set'>
```

Python usa `{}` tanto para diccionarios como para sets. Sin contenido, la ambigüedad se resuelve a favor del diccionario por razones históricas (los diccionarios existieron antes que los sets en Python). Sin embargo, `{1, 2, 3}` sí crea un set porque no tiene `:`.

---

## Error 6: Intentar consumir un generador más de una vez

```python
gen = (n ** 2 for n in range(5))

# Primera vez — funciona
total = sum(gen)
print(total)  # 30

# Segunda vez — el generador ya está agotado
maximo = max(gen)  # ValueError: max() arg is an empty sequence
```

Un generador se agota tras ser recorrido una vez. Si se necesitan múltiples operaciones sobre los mismos datos, hay que usar una list comprehension o guardar el resultado en una variable antes de consumirlo:

```python
cuadrados = [n ** 2 for n in range(5)]
total = sum(cuadrados)    # 30
maximo = max(cuadrados)   # 16
```

---

## Error 7: Modificar la lista que se está iterando con una comprehension

```python
numeros = [1, 2, 3, 4, 5]

# MAL — comportamiento impredecible
numeros = [n * 2 for n in numeros]  # Funciona, pero solo porque se reasigna

# PELIGROSO — modificar durante la iteración con un bucle
for i in range(len(numeros)):
    numeros[i] = numeros[i] * 2  # Modifica in-place durante la iteración
```

La comprehension en este caso funciona correctamente porque crea una lista **nueva** y luego la reasigna al mismo nombre. Pero es importante entender que no modifica la lista original: la reemplaza. Si otra variable apunta a la lista original, no verá los cambios:

```python
numeros = [1, 2, 3]
referencia = numeros
numeros = [n * 2 for n in numeros]

print(numeros)     # [2, 4, 6] — lista nueva
print(referencia)  # [1, 2, 3] — la original no cambió
```

---

## Error 8: Olvidar que dict comprehensions sobrescriben claves duplicadas

```python
palabras = ["hola", "casa", "hilo", "capa"]

# Si varias palabras empiezan por la misma letra, solo se guarda la última
por_letra = {palabra[0]: palabra for palabra in palabras}
print(por_letra)  # {'h': 'hilo', 'c': 'capa'}
```

Las claves de un diccionario son únicas. Si la comprehension genera claves repetidas, cada nueva entrada sobrescribe la anterior sin aviso. Si se necesitan múltiples valores por clave, hay que acumularlos en una lista con un bucle:

```python
por_letra = {}
for palabra in palabras:
    letra = palabra[0]
    if letra not in por_letra:
        por_letra[letra] = []
    por_letra[letra].append(palabra)

print(por_letra)  # {'h': ['hola', 'hilo'], 'c': ['casa', 'capa']}
```

---

## Error 9: Usar list comprehension donde basta un generador

```python
# MAL — crea una lista intermedia innecesaria
total = sum([n ** 2 for n in range(1000000)])

# BIEN — el generador pasa los valores directamente a sum()
total = sum(n ** 2 for n in range(1000000))
```

Cuando el resultado de la comprehension solo se usa como argumento de una función que consume iterables (`sum()`, `max()`, `min()`, `any()`, `all()`, `"".join()`), usar un generador evita crear la lista intermedia en memoria. La diferencia es especialmente relevante con volúmenes de datos grandes.

---

## Error 10: Confundir comprehension anidada con lista de listas

```python
# Esto APLANA la matriz (una sola lista)
matriz = [[1, 2], [3, 4], [5, 6]]
plana = [num for fila in matriz for num in fila]
print(plana)  # [1, 2, 3, 4, 5, 6]

# Esto CREA una lista de listas (comprehension dentro de comprehension)
doble = [[num * 2 for num in fila] for fila in matriz]
print(doble)  # [[2, 4], [6, 8], [10, 12]]
```

Son dos patrones distintos. El primero tiene dos `for` en la **misma** comprehension y produce una lista plana. El segundo tiene una comprehension **dentro** de otra (la interna genera cada sublista) y mantiene la estructura de lista de listas. La diferencia visual es sutil pero el resultado es completamente distinto.
