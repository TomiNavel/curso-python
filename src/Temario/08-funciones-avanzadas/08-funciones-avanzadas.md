# 8. Funciones Avanzadas

Este tema amplía lo visto en el tema 7 con conceptos que permiten escribir código más conciso y expresivo. Se introducen las funciones anónimas (`lambda`), las funciones de orden superior que Python trae incorporadas (`map`, `filter`, `sorted`), la recursión y los mecanismos avanzados de control sobre cómo se pasan argumentos a una función.

---

## 8.1. Funciones lambda

### 8.1.1. Sintaxis y concepto

Una función `lambda` es una función anónima (sin nombre) definida en una sola línea. Mientras que `def` crea una función con nombre y un cuerpo que puede contener múltiples sentencias, `lambda` crea una función que consiste en una única expresión cuyo resultado se devuelve automáticamente.

La sintaxis es:

```
lambda parámetros: expresión
```

No lleva `return` ni dos puntos con bloque indentado. La expresión se evalúa y se devuelve implícitamente:

```python
# Función normal
def doble(n):
    return n * 2

# Equivalente con lambda
doble = lambda n: n * 2

print(doble(5))  # 10
```

Una lambda puede tener varios parámetros, separados por comas:

```python
sumar = lambda a, b: a + b
print(sumar(3, 5))  # 8
```

### 8.1.2. Cuándo usar lambda

Asignar una lambda a una variable (como en los ejemplos anteriores) es un antipatrón. Si la función necesita un nombre, se debe usar `def`. Las lambdas están pensadas para usarse **inline**, como argumento de otra función, cuando la operación es tan simple que definir una función con `def` sería excesivo:

```python
nombres = ["Ana", "Pedro", "Bo", "Alejandra"]

# Lambda como argumento de sorted — no necesita nombre propio
ordenados = sorted(nombres, key=lambda nombre: len(nombre))
print(ordenados)  # ['Bo', 'Ana', 'Pedro', 'Alejandra']
```

El equivalente con `def` sería:

```python
def longitud(nombre):
    return len(nombre)

ordenados = sorted(nombres, key=longitud)
```

Ambas formas son correctas. La lambda es más concisa cuando la operación es trivial; `def` es preferible cuando la lógica es más compleja o cuando la función se reutiliza en varios sitios.

### 8.1.3. Limitaciones de lambda

Una lambda solo puede contener **una expresión**. No puede incluir sentencias como `if/else` multilínea, bucles `for`, `while`, `return`, `raise` ni asignaciones. El operador ternario sí está permitido porque es una expresión:

```python
# Operador ternario — es una expresión, funciona en lambda
clasificar = lambda n: "par" if n % 2 == 0 else "impar"
print(clasificar(7))  # "impar"

# Bucle for — es una sentencia, NO funciona en lambda
# lambda nums: for n in nums: print(n)  → SyntaxError
```

Si la lógica necesita más de una expresión, hay que usar `def`.

---

## 8.2. Funciones de orden superior

Una función de orden superior es una función que recibe otra función como argumento o que devuelve una función como resultado. En el tema 7 se vio que las funciones son objetos de primera clase y se pueden pasar como argumento. Python incluye varias funciones built-in que explotan este concepto.

### 8.2.1. `map()`

`map(función, iterable)` aplica una función a cada elemento de un iterable y devuelve un iterador con los resultados. No modifica el iterable original:

```python
numeros = [1, 2, 3, 4, 5]

# Aplicar una función a cada elemento
cuadrados = list(map(lambda n: n ** 2, numeros))
print(cuadrados)  # [1, 4, 9, 16, 25]
```

`map()` devuelve un **iterador** (similar a un generador), no una lista. Por eso se envuelve en `list()` para ver los resultados. Esto es eficiente en memoria cuando se trabaja con grandes cantidades de datos.

El equivalente con una list comprehension es más idiomático en Python y generalmente preferido:

```python
cuadrados = [n ** 2 for n in numeros]
```

`map()` se usa más cuando ya se tiene una función definida que se quiere aplicar directamente, sin necesidad de crear una lambda:

```python
# Convertir lista de strings a enteros — map es más limpio que la comprehension
valores = ["1", "2", "3", "4"]
numeros = list(map(int, valores))
print(numeros)  # [1, 2, 3, 4]

# Equivalente con comprehension
numeros = [int(v) for v in valores]
```

`map()` también acepta múltiples iterables. En ese caso, la función debe aceptar tantos argumentos como iterables se pasen:

```python
a = [1, 2, 3]
b = [10, 20, 30]
sumas = list(map(lambda x, y: x + y, a, b))
print(sumas)  # [11, 22, 33]
```

### 8.2.2. `filter()`

`filter(función, iterable)` devuelve un iterador con los elementos del iterable para los que la función devuelve `True`. Es decir, filtra los elementos que no cumplen la condición:

```python
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

pares = list(filter(lambda n: n % 2 == 0, numeros))
print(pares)  # [2, 4, 6, 8, 10]
```

Al igual que `map()`, el equivalente con comprehension es generalmente preferido en Python:

```python
pares = [n for n in numeros if n % 2 == 0]
```

`filter()` es más útil cuando ya se tiene una función de validación definida:

```python
def es_positivo(n):
    return n > 0

numeros = [-3, -1, 0, 2, 5, -4, 8]
positivos = list(filter(es_positivo, numeros))
print(positivos)  # [2, 5, 8]
```

Si se pasa `None` como función, `filter()` elimina los elementos falsy:

```python
datos = [0, "", "hola", None, 42, [], "mundo", False]
sin_falsy = list(filter(None, datos))
print(sin_falsy)  # ['hola', 42, 'mundo']
```

### 8.2.3. `sorted()` con `key` y `reverse`

`sorted()` se vio brevemente en el tema 3, pero su verdadero potencial aparece cuando se combina con el parámetro `key`, que acepta una función. Esta función se aplica a cada elemento para determinar su valor de ordenamiento, sin modificar los elementos en sí:

```python
palabras = ["banana", "kiwi", "manzana", "uva"]

# Ordenar por longitud
por_longitud = sorted(palabras, key=len)
print(por_longitud)  # ['uva', 'kiwi', 'banana', 'manzana']

# Ordenar por última letra
por_ultima = sorted(palabras, key=lambda p: p[-1])
print(por_ultima)  # ['banana', 'manzana', 'uva', 'kiwi']
```

Con diccionarios, `key` permite ordenar por cualquier campo:

```python
personas = [
    {"nombre": "Ana", "edad": 28},
    {"nombre": "Pedro", "edad": 22},
    {"nombre": "Luis", "edad": 35},
]

por_edad = sorted(personas, key=lambda p: p["edad"])
print(por_edad)
# [{'nombre': 'Pedro', 'edad': 22}, {'nombre': 'Ana', 'edad': 28}, {'nombre': 'Luis', 'edad': 35}]
```

El parámetro `reverse=True` invierte el orden:

```python
por_edad_desc = sorted(personas, key=lambda p: p["edad"], reverse=True)
# Luis (35), Ana (28), Pedro (22)
```

`max()` y `min()` también aceptan `key`:

```python
mayor = max(personas, key=lambda p: p["edad"])
print(mayor)  # {'nombre': 'Luis', 'edad': 35}
```

### 8.2.4. `map` y `filter` vs comprehensions

Tanto `map()` como `filter()` tienen equivalentes directos con list comprehensions. En la comunidad Python se prefieren las comprehensions en la mayoría de casos porque son más legibles y no requieren convertir el resultado a lista:

| Operación | `map`/`filter` | Comprehension |
|-----------|---------------|---------------|
| Transformar | `list(map(f, iterable))` | `[f(x) for x in iterable]` |
| Filtrar | `list(filter(f, iterable))` | `[x for x in iterable if f(x)]` |
| Ambos | `list(map(f, filter(g, iterable)))` | `[f(x) for x in iterable if g(x)]` |

Situaciones donde `map()`/`filter()` son preferibles:
- Cuando ya se tiene una función con nombre y la comprehension no aporta claridad: `list(map(int, valores))` vs `[int(v) for v in valores]`
- Cuando se necesita evaluación diferida (sin `list()`) para procesar grandes volúmenes de datos

---

## 8.3. Recursión

### 8.3.1. Concepto y caso base

La recursión es una técnica donde una función se llama a sí misma para resolver un problema dividiéndolo en subproblemas más pequeños. Cada llamada recursiva trabaja con un caso más sencillo hasta llegar a un **caso base** que se resuelve directamente sin más llamadas.

El caso base es fundamental: sin él, la función se llamaría infinitamente hasta que Python lance un `RecursionError` (por defecto, el límite es 1000 llamadas).

El ejemplo clásico es el cálculo del factorial (n! = n × (n-1) × ... × 1):

```python
def factorial(n):
    # Caso base: el factorial de 0 y 1 es 1
    if n <= 1:
        return 1
    # Caso recursivo: n * factorial del anterior
    return n * factorial(n - 1)

print(factorial(5))  # 120 → 5 * 4 * 3 * 2 * 1
```

Para entender cómo funciona, se puede trazar la cadena de llamadas:

```
factorial(5)
→ 5 * factorial(4)
→ 5 * 4 * factorial(3)
→ 5 * 4 * 3 * factorial(2)
→ 5 * 4 * 3 * 2 * factorial(1)
→ 5 * 4 * 3 * 2 * 1  ← caso base alcanzado
→ 120
```

### 8.3.2. Recursión vs iteración

Todo problema que se resuelve con recursión también se puede resolver con un bucle (iteración). La recursión es más elegante para problemas que se descomponen naturalmente en subproblemas (árboles, fractales, divide y vencerás), pero la iteración suele ser más eficiente en Python porque cada llamada recursiva consume memoria en la pila de llamadas.

```python
# Factorial iterativo — más eficiente en Python
def factorial_iterativo(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

# Factorial recursivo — más expresivo pero menos eficiente
def factorial_recursivo(n):
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)
```

### 8.3.3. Recursión con estructuras de datos

La recursión es especialmente útil para recorrer estructuras anidadas cuya profundidad no se conoce de antemano:

```python
def aplanar(lista):
    """Aplana una lista anidada a cualquier profundidad."""
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado

datos = [1, [2, 3], [4, [5, 6, [7]]]]
print(aplanar(datos))  # [1, 2, 3, 4, 5, 6, 7]
```

Otro ejemplo clásico: la secuencia de Fibonacci, donde cada número es la suma de los dos anteriores:

```python
def fibonacci(n):
    """Devuelve el n-ésimo número de Fibonacci."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

# Los primeros 10 números de Fibonacci
for i in range(10):
    print(fibonacci(i), end=" ")
# 0 1 1 2 3 5 8 13 21 34
```

> **Nota:** Esta implementación de Fibonacci es muy ineficiente porque recalcula los mismos valores muchas veces. La versión iterativa o con memoización (que se verá en temas posteriores) es mucho más rápida.

---

## 8.4. Funciones built-in útiles

Python tiene varias funciones built-in que complementan el trabajo con funciones y datos. Algunas ya se han mencionado en temas anteriores, pero aquí se cubren en el contexto de su uso con funciones de orden superior.

### 8.4.1. `isinstance()`

Comprueba si un objeto es de un tipo determinado. Es la forma correcta de verificar tipos en Python (en lugar de `type(x) == int`):

```python
print(isinstance(42, int))        # True
print(isinstance("hola", str))    # True
print(isinstance(3.14, (int, float)))  # True — acepta tupla de tipos
```

### 8.4.2. `callable()`

Comprueba si un objeto se puede llamar como función:

```python
def saludar():
    return "Hola"

print(callable(saludar))  # True
print(callable(42))       # False
print(callable(len))      # True
```

### 8.4.3. `any()` y `all()`

`any()` devuelve `True` si **al menos un** elemento del iterable es truthy. `all()` devuelve `True` si **todos** los elementos son truthy. Ambas aplican cortocircuito: `any()` para de iterar en cuanto encuentra el primer `True`, y `all()` para en cuanto encuentra el primer `False`.

```python
numeros = [0, 1, 2, 3]

print(any(numeros))  # True — al menos uno es truthy (1, 2, 3)
print(all(numeros))  # False — 0 es falsy

# Con iterables vacíos
print(any([]))  # False — no hay ningún elemento truthy
print(all([]))  # True — no hay ningún elemento que sea falsy (verdad vacua)
```

Su uso más habitual es con generator expressions para evaluar condiciones sobre colecciones:

```python
edades = [22, 17, 30, 15]

# ¿Hay algún menor de edad?
print(any(edad < 18 for edad in edades))  # True

# ¿Son todos mayores de edad?
print(all(edad >= 18 for edad in edades))  # False

# Validar que todos los campos obligatorios tienen valor
campos = {"nombre": "Ana", "email": "ana@mail.com", "telefono": ""}
print(all(campos.values()))  # False — "telefono" es string vacío (falsy)
```

`any()` y `all()` son más legibles y eficientes que el equivalente con bucle, y aparecen con frecuencia en entrevistas como alternativa a `for` + `if` + `break`.

### 8.4.4. `zip()` y `enumerate()` con funciones

Ya se vieron en el tema 5, pero se mencionan aquí porque combinan muy bien con `map()` y lambdas para procesamiento de datos en paralelo:

```python
nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34, 22]

# Crear strings formateados combinando zip con map
perfiles = list(map(lambda t: f"{t[0]} ({t[1]})", zip(nombres, edades)))
print(perfiles)  # ['Ana (28)', 'Pedro (34)', 'Luis (22)']

# Equivalente con comprehension — más legible
perfiles = [f"{nombre} ({edad})" for nombre, edad in zip(nombres, edades)]
```
