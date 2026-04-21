# Preguntas de Entrevista: Funciones Avanzadas

1. ¿Qué es una función `lambda` y en qué se diferencia de una función definida con `def`?
2. ¿Cuándo es apropiado usar una lambda y cuándo no?
3. ¿Qué hace `map()` y qué devuelve?
4. ¿Qué hace `filter()` y qué ocurre si se le pasa `None` como función?
5. ¿En qué situaciones se prefieren `map()`/`filter()` frente a list comprehensions?
6. ¿Cómo funciona el parámetro `key` en `sorted()`?
7. ¿Qué es la recursión y qué es un caso base? ¿Qué ocurre si no hay caso base?
8. ¿Cuáles son las ventajas e inconvenientes de la recursión frente a la iteración en Python?
9. ¿Qué diferencia hay entre `type(x) == int` e `isinstance(x, int)`?
10. ¿Qué devuelve `map()`: una lista o un iterador? ¿Por qué importa?
11. ¿Por qué `fibonacci(n)` recursivo sin memoización es ineficiente?
12. ¿Qué es una función de orden superior?
13. ¿Cómo ordenarías una lista de diccionarios por un campo específico?

---

### R1. ¿Qué es una función `lambda` y en qué se diferencia de una función definida con `def`?

Una lambda es una función anónima definida en una sola línea con la sintaxis `lambda parámetros: expresión`. A diferencia de `def`:

- No tiene nombre (es anónima)
- Solo puede contener una expresión, no sentencias
- Devuelve el resultado de la expresión implícitamente (sin `return`)
- No puede incluir bucles, asignaciones ni múltiples sentencias

```python
# def — función con nombre, cuerpo completo
def doble(n):
    return n * 2

# lambda — anónima, una expresión
lambda n: n * 2
```

### R2. ¿Cuándo es apropiado usar una lambda y cuándo no?

Es apropiado usarla **inline como argumento** de otra función cuando la operación es trivial y no se reutiliza:

```python
sorted(nombres, key=lambda n: len(n))
```

No es apropiado asignarla a una variable (`doble = lambda n: n * 2`). Si la función necesita un nombre, se debe usar `def`. Tampoco cuando la lógica es compleja: si la lambda no se entiende de un vistazo, usar `def`.

### R3. ¿Qué hace `map()` y qué devuelve?

`map(función, iterable)` aplica la función a cada elemento del iterable y devuelve un **iterador** (no una lista) con los resultados. Para obtener una lista hay que envolverlo en `list()`:

```python
numeros = [1, 2, 3]
cuadrados = list(map(lambda n: n ** 2, numeros))  # [1, 4, 9]
```

### R4. ¿Qué hace `filter()` y qué ocurre si se le pasa `None` como función?

`filter(función, iterable)` devuelve un iterador con los elementos para los que la función devuelve `True`.

Si se pasa `None` como función, filtra los elementos **falsy** (elimina `0`, `""`, `None`, `[]`, `False`, etc.):

```python
datos = [0, "hola", "", None, 42, False]
list(filter(None, datos))  # ['hola', 42]
```

### R5. ¿En qué situaciones se prefieren `map()`/`filter()` frente a list comprehensions?

En la comunidad Python se prefieren las comprehensions en la mayoría de casos. `map()`/`filter()` son preferibles cuando:

- Ya existe una función con nombre y la comprehension no aporta claridad: `list(map(int, valores))` es más limpio que `[int(v) for v in valores]`
- Se necesita evaluación diferida sin materializar la lista (sin `list()`), por ejemplo al procesar grandes volúmenes de datos

Para todo lo demás, las comprehensions son más idiomáticas y legibles.

### R6. ¿Cómo funciona el parámetro `key` en `sorted()`?

`key` recibe una función que se aplica a cada elemento para obtener el valor por el que se ordena. Los elementos se comparan según el resultado de `key`, pero no se modifican en la lista resultante:

```python
palabras = ["banana", "kiwi", "uva"]
sorted(palabras, key=len)  # ['uva', 'kiwi', 'banana']
```

`key` se aplica una vez por elemento, no en cada comparación. También funciona con `max()`, `min()` y `.sort()`.

### R7. ¿Qué es la recursión y qué es un caso base? ¿Qué ocurre si no hay caso base?

La recursión es cuando una función se llama a sí misma para resolver un problema dividiéndolo en subproblemas más pequeños. El **caso base** es la condición que detiene las llamadas recursivas y devuelve un resultado directamente.

Sin caso base, la función se llama infinitamente hasta que Python lanza un `RecursionError` al alcanzar el límite de profundidad de la pila (por defecto 1000 llamadas).

```python
def factorial(n):
    if n <= 1:      # Caso base
        return 1
    return n * factorial(n - 1)  # Caso recursivo
```

### R8. ¿Cuáles son las ventajas e inconvenientes de la recursión frente a la iteración en Python?

**Ventajas:**
- Código más expresivo y natural para problemas que se descomponen en subproblemas (árboles, estructuras anidadas, divide y vencerás)
- Más fácil de razonar en ciertos algoritmos

**Inconvenientes:**
- Cada llamada recursiva consume memoria en la pila de llamadas
- Python tiene un límite de profundidad (1000 por defecto)
- Python no optimiza la recursión de cola (tail call optimization), a diferencia de otros lenguajes
- Generalmente más lento que el bucle equivalente

En Python, la iteración es preferible para la mayoría de casos. La recursión se reserva para problemas donde aporta claridad significativa.

### R9. ¿Qué diferencia hay entre `type(x) == int` e `isinstance(x, int)`?

`type(x) == int` compara el tipo exacto. `isinstance(x, int)` comprueba si el objeto es de ese tipo **o de una subclase**. `isinstance` es la forma recomendada:

```python
# isinstance también acepta una tupla de tipos
isinstance(3.14, (int, float))  # True
```

Además, `isinstance` es más flexible y respeta la herencia, lo que es importante en código orientado a objetos.

### R10. ¿Qué devuelve `map()`: una lista o un iterador? ¿Por qué importa?

Devuelve un **iterador**. Esto importa porque:

- No se puede indexar (`resultado[0]` falla)
- Solo se puede recorrer una vez (se agota como un generador)
- Es eficiente en memoria: no crea todos los elementos de golpe

Si se necesita una lista, hay que envolverlo en `list()`. Si solo se va a iterar una vez (por ejemplo en un `for`), se puede usar directamente sin convertir.

### R11. ¿Por qué `fibonacci(n)` recursivo sin memoización es ineficiente?

Porque recalcula los mismos valores muchas veces. Para calcular `fibonacci(5)`, se calcula `fibonacci(3)` dos veces, `fibonacci(2)` tres veces, etc. La complejidad crece exponencialmente (O(2^n)).

```
fibonacci(5)
├── fibonacci(4)
│   ├── fibonacci(3)
│   │   ├── fibonacci(2) ← se calcula aquí
│   │   └── fibonacci(1)
│   └── fibonacci(2)     ← y otra vez aquí
└── fibonacci(3)          ← y fibonacci(3) entero otra vez
```

La solución es usar iteración o memoización (almacenar resultados ya calculados), lo que reduce la complejidad a O(n).

### R12. ¿Qué es una función de orden superior?

Una función que recibe otra función como argumento o que devuelve una función como resultado. Ejemplos built-in: `map()`, `filter()`, `sorted()` (con `key`), `max()`, `min()`.

```python
# sorted recibe len como argumento — es de orden superior
sorted(["banana", "kiwi", "uva"], key=len)
```

### R13. ¿Cómo ordenarías una lista de diccionarios por un campo específico?

Usando `sorted()` con una función `key` (lambda o `def`) que extraiga el campo:

```python
personas = [
    {"nombre": "Ana", "edad": 28},
    {"nombre": "Pedro", "edad": 22},
    {"nombre": "Luis", "edad": 35},
]

por_edad = sorted(personas, key=lambda p: p["edad"])
# Pedro (22), Ana (28), Luis (35)

# Descendente
por_edad_desc = sorted(personas, key=lambda p: p["edad"], reverse=True)
```