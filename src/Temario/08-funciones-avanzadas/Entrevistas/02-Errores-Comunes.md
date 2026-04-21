# Errores Comunes: Funciones Avanzadas

## Error 1: Asignar una lambda a una variable

```python
# MAL — si necesita nombre, usar def
doble = lambda n: n * 2

# BIEN
def doble(n):
    return n * 2
```

Asignar una lambda a una variable anula su única ventaja (ser anónima). Además, dificulta la depuración porque el traceback mostrará `<lambda>` en lugar del nombre de la función. PEP 8 desaconseja esta práctica explícitamente.

---

## Error 2: Olvidar que `map()` y `filter()` devuelven iteradores

```python
numeros = [1, 2, 3, 4, 5]

# MAL — intentar usar como lista
resultado = map(lambda n: n * 2, numeros)
print(resultado)     # <map object at 0x...> — no es una lista
print(resultado[0])  # TypeError: 'map' object is not subscriptable

# BIEN — convertir a lista si se necesita indexar o imprimir
resultado = list(map(lambda n: n * 2, numeros))
print(resultado)     # [2, 4, 6, 8, 10]
```

`map()` y `filter()` devuelven iteradores por eficiencia. Si se necesita una lista, hay que envolverlos en `list()`.

---

## Error 3: Lambda con sentencias en lugar de expresiones

```python
# MAL — SyntaxError: una lambda no puede contener sentencias
procesar = lambda x: if x > 0: return x

# MAL — SyntaxError: no se puede asignar dentro de una lambda
guardar = lambda x: resultado = x * 2

# BIEN — usar operador ternario (es una expresión)
procesar = lambda x: x if x > 0 else 0

# BIEN — si necesita lógica compleja, usar def
def procesar(x):
    if x > 0:
        return x
    return 0
```

Las lambdas solo aceptan una expresión. Sentencias como `if/else` multilínea, `for`, `return`, `raise` o asignaciones no son válidas.

---

## Error 4: Recursión sin caso base

```python
# MAL — RecursionError: maximum recursion depth exceeded
def cuenta_atras(n):
    print(n)
    cuenta_atras(n - 1)

# BIEN — con caso base
def cuenta_atras(n):
    if n < 0:
        return
    print(n)
    cuenta_atras(n - 1)
```

Sin caso base, la función se llama infinitamente hasta que Python la detiene con un `RecursionError`. Toda función recursiva debe tener al menos una condición que devuelva un resultado sin hacer más llamadas recursivas.

---

## Error 5: Caso base que nunca se alcanza

```python
# MAL — si n es negativo, nunca llega a 0
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

factorial(-3)  # RecursionError — pasa por -1, -2, -3... sin parar

# BIEN — caso base que cubre todos los casos de parada
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Es tan importante definir un caso base como asegurarse de que la recursión avanza hacia él. Si los argumentos no convergen al caso base, el resultado es el mismo que no tener caso base.

---

## Error 6: Usar `map()` con lambda cuando una comprehension es más clara

```python
# MAL — lambda innecesaria, la comprehension es más directa
resultado = list(map(lambda x: x ** 2 + 1, filter(lambda x: x > 0, numeros)))

# BIEN — comprehension equivalente, mucho más legible
resultado = [x ** 2 + 1 for x in numeros if x > 0]
```

Encadenar `map()` y `filter()` con lambdas produce código denso y difícil de leer. Si la operación requiere transformación y filtrado, la comprehension es casi siempre más clara.

---

## Error 7: Confundir `key` con la transformación del resultado en `sorted()`

```python
palabras = ["banana", "kiwi", "uva"]

# MAL — creer que key transforma los elementos
resultado = sorted(palabras, key=len)
print(resultado)  # ['uva', 'kiwi', 'banana'] — sigue siendo strings, NO longitudes

# key solo determina el CRITERIO de ordenación, no modifica los elementos
```

`key` se usa para **comparar**, no para transformar. Los elementos en la lista resultante son los originales, no el resultado de aplicar `key`.

---

## Error 8: No convertir el resultado de `map()` antes de consumirlo dos veces

```python
numeros = [1, 2, 3, 4, 5]
dobles = map(lambda n: n * 2, numeros)

# Primera vez — funciona
print(list(dobles))  # [2, 4, 6, 8, 10]

# Segunda vez — vacío, el iterador se agotó
print(list(dobles))  # []

# BIEN — convertir a lista una vez y reutilizar
dobles = list(map(lambda n: n * 2, numeros))
print(dobles)  # [2, 4, 6, 8, 10]
print(dobles)  # [2, 4, 6, 8, 10]
```

Los iteradores de `map()` y `filter()` se agotan después de una pasada, igual que los generadores. Si se necesitan los datos más de una vez, convertir a lista primero.

---

## Error 9: Usar recursión donde un bucle es más apropiado

```python
# MAL — recursión para algo trivialmente iterativo
def sumar_lista(numeros, i=0, total=0):
    if i >= len(numeros):
        return total
    return sumar_lista(numeros, i + 1, total + numeros[i])

# BIEN — bucle simple
def sumar_lista(numeros):
    total = 0
    for n in numeros:
        total += n
    return total
```

La recursión es útil para problemas que se descomponen naturalmente en subproblemas (árboles, estructuras anidadas). Para recorrer una lista secuencialmente, un bucle es más claro, más eficiente y no tiene riesgo de `RecursionError`.
