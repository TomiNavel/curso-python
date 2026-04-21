# Preguntas de Entrevista: Decoradores y functools

1. ¿Qué es un decorador en Python y a qué equivale la sintaxis `@decorador`?
2. ¿Por qué el wrapper de un decorador usa `*args, **kwargs`?
3. ¿Qué problema resuelve `@functools.wraps` y por qué es importante usarlo?
4. ¿Cómo se crea un decorador que acepte argumentos (como `@repetir(veces=3)`)?
5. Si se apilan dos decoradores `@A` y `@B` sobre una función, ¿cuál se aplica primero?
6. ¿Qué hace `functools.partial` y en qué se diferencia de usar una lambda?
7. ¿Qué hace `functools.reduce` y por qué se usa poco en Python moderno?
8. ¿Qué hace `@lru_cache` y qué significa LRU?
9. ¿Cuál es la diferencia entre `@lru_cache(maxsize=128)` y `@cache`?
10. ¿Qué restricción tienen los argumentos de una función decorada con `@lru_cache`?
11. ¿Cuál es la relación entre decoradores y closures?
12. ¿Cómo verificarías que un decorador no rompe los metadatos de la función original?

---

### R1. ¿Qué es un decorador en Python y a qué equivale la sintaxis `@decorador`?

Un decorador es una función que recibe otra función como argumento y devuelve una nueva función (o la misma, modificada). La sintaxis `@decorador` es una notación abreviada que el intérprete traduce internamente a la asignación manual equivalente:

```python
@mi_decorador
def funcion():
    pass

# Equivale a:
def funcion():
    pass
funcion = mi_decorador(funcion)
```

Después de la decoración, el nombre `funcion` apunta a lo que devolvió el decorador, no a la función original.

### R2. ¿Por qué el wrapper de un decorador usa `*args, **kwargs`?

Para que el decorador sea genérico y funcione con cualquier función, independientemente de cuántos argumentos reciba o de qué tipo sean. Sin `*args, **kwargs`, el decorador solo serviría para funciones con una firma específica:

```python
def decorador(func):
    def wrapper(*args, **kwargs):  # acepta cualquier combinación de argumentos
        return func(*args, **kwargs)  # los pasa tal cual a la función original
    return wrapper
```

### R3. ¿Qué problema resuelve `@functools.wraps` y por qué es importante usarlo?

Cuando un decorador devuelve un wrapper, los metadatos de la función original (`__name__`, `__doc__`, `__module__`) se reemplazan por los del wrapper. `@wraps(func)` copia esos metadatos al wrapper:

```python
from functools import wraps

def decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

print(sumar.__name__)  # "sumar" — sin @wraps sería "wrapper"
print(sumar.__doc__)   # "Suma dos números." — sin @wraps sería None
```

Sin `@wraps`, las herramientas de depuración, documentación automática e introspección dejan de funcionar correctamente.

### R4. ¿Cómo se crea un decorador que acepte argumentos (como `@repetir(veces=3)`)?

Se añade un nivel más de anidamiento. La función externa recibe los argumentos de configuración y devuelve el decorador real:

```python
def repetir(veces):           # recibe la configuración
    def decorador(func):      # recibe la función
        def wrapper(*args, **kwargs):  # ejecuta la lógica
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador
```

`@repetir(veces=3)` se ejecuta en dos pasos: primero `repetir(veces=3)` devuelve `decorador`, y después `decorador(funcion)` devuelve `wrapper`.

### R5. Si se apilan dos decoradores `@A` y `@B` sobre una función, ¿cuál se aplica primero?

El más cercano a la función (`@B`) se aplica primero:

```python
@A
@B
def funcion():
    pass

# Equivale a:
funcion = A(B(funcion))
```

`B` envuelve la función original y `A` envuelve el resultado de `B`.

### R6. ¿Qué hace `functools.partial` y en qué se diferencia de usar una lambda?

`partial` crea una nueva función fijando algunos argumentos de otra función existente:

```python
from functools import partial

cuadrado = partial(pow, exp=2)  # fija exp=2
cuadrado(5)  # 25
```

Es similar a `lambda base: pow(base, exp=2)`, pero `partial` es más legible cuando solo se fijan argumentos, tiene un `repr` útil para depuración, y expone los argumentos fijados en `func`, `args` y `keywords`.

### R7. ¿Qué hace `functools.reduce` y por qué se usa poco en Python moderno?

`reduce` aplica una función de dos argumentos de forma acumulativa a un iterable, reduciéndolo a un solo valor:

```python
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])  # ((1+2)+3)+4 = 10
```

Se usa poco porque la mayoría de sus casos comunes tienen built-ins más legibles: `sum()`, `max()`, `min()`, `math.prod()`. Guido van Rossum lo movió de las built-ins a `functools` por esta razón.

### R8. ¿Qué hace `@lru_cache` y qué significa LRU?

`@lru_cache` es un decorador que almacena en caché los resultados de la función. Si se llama con los mismos argumentos, devuelve el resultado almacenado sin ejecutar la función de nuevo.

LRU significa *Least Recently Used*: cuando la caché alcanza su tamaño máximo (`maxsize`), descarta el resultado que lleva más tiempo sin ser consultado.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### R9. ¿Cuál es la diferencia entre `@lru_cache(maxsize=128)` y `@cache`?

`@cache` (Python 3.9+) es equivalente a `@lru_cache(maxsize=None)` — una caché sin límite de tamaño. `@lru_cache` con un `maxsize` limita la cantidad de resultados almacenados y descarta los menos usados.

`@cache` es más simple pero puede consumir memoria indefinidamente. `@lru_cache` con un `maxsize` es más seguro para funciones con un rango amplio de inputs.

### R10. ¿Qué restricción tienen los argumentos de una función decorada con `@lru_cache`?

Los argumentos deben ser **hashables** (inmutables), porque se usan como claves del diccionario interno de la caché. Listas, diccionarios y sets no son hashables, por lo que no se pueden pasar como argumentos a funciones decoradas con `@lru_cache`:

```python
@lru_cache
def procesar(datos):  # si datos es una lista, lanza TypeError
    return sum(datos)

procesar([1, 2, 3])  # TypeError: unhashable type: 'list'
procesar((1, 2, 3))  # funciona — las tuplas son hashables
```

### R11. ¿Cuál es la relación entre decoradores y closures?

Un decorador es un caso específico de closure. La función wrapper captura la función original (`func`) en su closure, manteniendo acceso a ella después de que el decorador termine de ejecutarse:

```python
def decorador(func):       # func queda capturada en el closure de wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)  # accede a func gracias al closure
    return wrapper
```

Sin closures, el wrapper no tendría forma de acceder a la función original.

### R12. ¿Cómo verificarías que un decorador no rompe los metadatos de la función original?

Comprobando `__name__` y `__doc__` de la función decorada:

```python
@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

assert sumar.__name__ == "sumar", "El decorador pierde el nombre"
assert sumar.__doc__ == "Suma dos números.", "El decorador pierde el docstring"
```

Si falla, el decorador no está usando `@functools.wraps`.
