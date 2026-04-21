# Errores Comunes: Decoradores y functools

## Error 1: Olvidar devolver el wrapper

```python
# MAL — el decorador no devuelve nada, la función se convierte en None
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Ejecutando...")
        return func(*args, **kwargs)
    # falta return wrapper

@mi_decorador
def sumar(a, b):
    return a + b

print(sumar(2, 3))  # TypeError: 'NoneType' object is not callable

# BIEN
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Ejecutando...")
        return func(*args, **kwargs)
    return wrapper  # devolver el wrapper
```

Si el decorador no devuelve el wrapper, devuelve `None` implícitamente. `sumar` pasa a valer `None` y al llamarla se obtiene `TypeError`.

---

## Error 2: Olvidar devolver el resultado dentro del wrapper

```python
# MAL — el wrapper no devuelve el resultado de func()
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes")
        func(*args, **kwargs)  # se ejecuta pero se descarta el resultado
        print("Después")
    return wrapper

@mi_decorador
def sumar(a, b):
    return a + b

resultado = sumar(2, 3)
print(resultado)  # None — se perdió el return

# BIEN
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes")
        resultado = func(*args, **kwargs)
        print("Después")
        return resultado  # devolver el resultado
    return wrapper
```

El wrapper debe capturar y devolver el resultado de `func()`. Sin el `return`, la función decorada siempre devuelve `None`.

---

## Error 3: No usar @wraps y perder metadatos

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

print(sumar.__name__)  # "wrapper" — debería ser "sumar"
print(sumar.__doc__)   # None — debería ser "Suma dos números."
```

Esto causa problemas con herramientas de documentación, depuración y logging. La solución es siempre usar `@wraps`:

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## Error 4: Llamar a la función al decorar en lugar de pasarla

```python
# MAL — los paréntesis ejecutan la función inmediatamente
@mi_decorador(sumar)  # TypeError o comportamiento inesperado
def sumar(a, b):
    return a + b

# BIEN — sin paréntesis, se pasa la referencia
@mi_decorador
def sumar(a, b):
    return a + b
```

`@mi_decorador` pasa la función al decorador. `@mi_decorador()` ejecuta `mi_decorador()` sin argumentos y aplica el resultado como decorador. Solo se usan paréntesis cuando el decorador acepta argumentos de configuración (como `@repetir(veces=3)`).

---

## Error 5: Confundir el orden de apilamiento de decoradores

```python
from functools import wraps

def mayusculas(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def exclamacion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!"
    return wrapper

# El orden importa
@mayusculas
@exclamacion
def saludar():
    return "hola"

print(saludar())  # "HOLA!" — exclamacion primero, luego mayusculas

@exclamacion
@mayusculas
def saludar2():
    return "hola"

print(saludar2())  # "HOLA!" — parece igual, pero...
# mayusculas convierte a "HOLA", exclamacion añade "!" → "HOLA!"
# vs. exclamacion añade "!" → "hola!", mayusculas convierte → "HOLA!"
# En este caso coincide, pero con otros decoradores el resultado puede diferir
```

El decorador más cercano a la función se aplica primero. Hay que leer de abajo hacia arriba.

---

## Error 6: Usar lru_cache con argumentos mutables

```python
from functools import lru_cache

@lru_cache
def procesar(datos):
    return sum(datos)

procesar([1, 2, 3])  # TypeError: unhashable type: 'list'
```

`lru_cache` necesita que los argumentos sean hashables para usarlos como claves de la caché. Listas, diccionarios y sets no son hashables.

```python
# BIEN — usar tuplas en lugar de listas
procesar((1, 2, 3))  # funciona

# O no usar caché para funciones con argumentos mutables
```

---

## Error 7: No poner paréntesis en @lru_cache cuando se requieren

```python
from functools import lru_cache

# Desde Python 3.8, ambas formas son válidas para lru_cache sin argumentos:
@lru_cache      # funciona (desde 3.8)
@lru_cache()    # también funciona

# PERO si se quiere especificar maxsize, los paréntesis son obligatorios:
@lru_cache(maxsize=256)
def funcion(n):
    return n * 2
```

Antes de Python 3.8, `@lru_cache` sin paréntesis no funcionaba — había que usar siempre `@lru_cache()`. Desde 3.8, `lru_cache` detecta si recibe una función directamente o un argumento de configuración.

---

## Error 8: Creer que reduce() es la forma idiomática de acumular

```python
from functools import reduce

# MAL — reduce para operaciones que tienen built-ins
total = reduce(lambda a, b: a + b, numeros)        # usar sum()
maximo = reduce(lambda a, b: a if a > b else b, numeros)  # usar max()

# BIEN — usar las built-ins
total = sum(numeros)
maximo = max(numeros)
```

`reduce` es apropiado solo cuando la operación acumulativa no tiene una built-in equivalente. Para `sum`, `max`, `min`, `math.prod` y la mayoría de acumulaciones, las alternativas son más legibles.

---

## Error 9: No usar *args y **kwargs en el wrapper

```python
# MAL — el wrapper solo acepta funciones sin argumentos
def mi_decorador(func):
    def wrapper():
        print("Antes")
        return func()
    return wrapper

@mi_decorador
def saludar(nombre):
    return f"Hola, {nombre}"

saludar("Ana")  # TypeError: wrapper() takes 0 positional arguments but 1 was given

# BIEN — wrapper genérico
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes")
        return func(*args, **kwargs)
    return wrapper
```

Un decorador que no pasa `*args, **kwargs` solo funciona con funciones que coincidan exactamente con la firma del wrapper.

---

## Error 10: Usar partial cuando la lambda es más clara

```python
from functools import partial

# partial es más legible cuando solo se fijan argumentos
formato_eur = partial(formatear, moneda="€")  # claro

# Pero para transformaciones, la lambda puede ser más directa
# MAL — partial forzado
transformar = partial(map, lambda x: x * 2)

# BIEN — expresión directa
resultado = [x * 2 for x in datos]
```

`partial` brilla cuando se fijan argumentos de una función existente con nombre. Para transformaciones o lógica más compleja, las comprehensions o lambdas son más apropiadas.
