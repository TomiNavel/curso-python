# Errores Comunes: Métodos Especiales y Dunder Methods

## Error 1: Modificar `self` en un operador aritmético

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # MAL — modifica el objeto original
        self.x += other.x
        self.y += other.y
        return self

a = Punto(1, 2)
b = Punto(3, 4)
c = a + b

print(c)  # Punto con x=4, y=6 — correcto
print(a)  # Punto con x=4, y=6 — ¡a fue modificado!
print(a is c)  # True — a y c son el mismo objeto
```

Los operadores aritméticos deben devolver un **nuevo** objeto sin modificar los operandos. La solución es `return Punto(self.x + other.x, self.y + other.y)`.

---

## Error 2: Lanzar `NotImplementedError` en lugar de devolver `NotImplemented`

```python
class Peso:
    def __init__(self, kg):
        self.kg = kg

    def __eq__(self, other):
        if not isinstance(other, Peso):
            # MAL — lanza excepción en lugar de devolver el valor especial
            raise NotImplementedError
        return self.kg == other.kg

p = Peso(70)
print(p == 42)  # NotImplementedError — debería ser False
```

`NotImplemented` es un **valor** que se devuelve para que Python intente con el otro operando. `NotImplementedError` es una **excepción** que interrumpe la ejecución. La solución es `return NotImplemented`.

---

## Error 3: Definir `__eq__` sin `__hash__`

```python
class Producto:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def __eq__(self, other):
        if not isinstance(other, Producto):
            return NotImplemented
        return self.codigo == other.codigo

p = Producto("A1", "Laptop")
productos = {p}  # TypeError: unhashable type: 'Producto'
```

Al definir `__eq__`, Python establece `__hash__ = None` automáticamente. Si el objeto necesita usarse en sets o como clave de diccionario, se debe definir `__hash__` con los mismos atributos que participan en `__eq__`:

```python
def __hash__(self):
    return hash(self.codigo)
```

---

## Error 4: Olvidar lanzar `StopIteration` en `__next__`

```python
class Rango:
    def __init__(self, fin):
        self.actual = 0
        self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        # MAL — nunca lanza StopIteration
        valor = self.actual
        self.actual += 1
        return valor

# Esto nunca termina
for n in Rango(3):
    print(n)  # 0 1 2 3 4 5 6 ... ¡bucle infinito!
```

`__next__` debe lanzar `StopIteration` cuando se agotan los elementos. Sin esa señal, `for` sigue llamando indefinidamente. La solución:

```python
def __next__(self):
    if self.actual >= self.fin:
        raise StopIteration
    valor = self.actual
    self.actual += 1
    return valor
```

---

## Error 5: `__enter__` no devuelve `self`

```python
class Conexion:
    def __init__(self, host):
        self.host = host

    def __enter__(self):
        print(f"Conectando a {self.host}")
        # MAL — no devuelve nada (devuelve None implícitamente)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Desconectando")
        return False

with Conexion("localhost") as conn:
    print(conn.host)  # AttributeError: 'NoneType' object has no attribute 'host'
```

La variable `as conn` recibe el valor de retorno de `__enter__`. Si no se devuelve nada, `conn` es `None`. La solución es añadir `return self` al final de `__enter__`.

---

## Error 6: Confundir `__bool__` con `__eq__`

```python
class Semaforo:
    def __init__(self, color):
        self.color = color

    def __bool__(self):
        # MAL — devuelve string en lugar de bool
        return self.color

s = Semaforo("verde")
if s:
    print("Adelante")
# TypeError: __bool__ should return bool, returned str
```

`__bool__` debe devolver estrictamente `True` o `False`, no un valor truthy/falsy. La solución es `return self.color == "verde"` o cualquier expresión que devuelva un booleano.

---

## Error 7: Llamar dunder methods directamente en lugar de usar la operación

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):
        return 2

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

a = Vector(1, 2)
b = Vector(3, 4)

# MAL — llamadas directas a dunder methods
c = a.__add__(b)
longitud = a.__len__()
texto = a.__repr__()

# BIEN — usar operadores y funciones built-in
c = a + b
longitud = len(a)
texto = repr(a)
```

Aunque las llamadas directas funcionan, no son idiomáticas y pueden comportarse diferente en ciertos casos (Python optimiza las llamadas vía operador/función). Además, dificultan la lectura del código.

---

## Error 8: Olvidar `return False` en `__exit__` y suprimir excepciones por accidente

```python
class Gestor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Limpiando recursos")
        return True  # ¡suprime TODAS las excepciones!

with Gestor():
    raise ValueError("Error grave")
    # No se propaga — return True lo silenció

print("Continúa como si nada")  # Se ejecuta sin error
```

`__exit__` que devuelve `True` suprime cualquier excepción, lo que puede ocultar errores graves. Solo devolver `True` cuando se quiera suprimir intencionalmente una excepción específica. La práctica segura es devolver `False` (o no devolver nada, que equivale a `None` → falsy).

---

## Error 9: Mutar atributos de un objeto hashable después de insertarlo en un set

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Punto):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

p = Punto(1, 2)
puntos = {p}
print(p in puntos)   # True

p.x = 99  # se modifica un atributo que participa en el hash
print(p in puntos)   # False — ¡el set ya no lo encuentra!
print(list(puntos))  # [Punto(99, 2)] — el objeto sigue ahí, pero con hash incorrecto
```

Modificar atributos que participan en el hash corrompe sets y diccionarios. Los objetos hashables deben ser efectivamente inmutables en esos atributos.

---

## Error 10: Definir `__contains__` que no devuelve booleano

```python
class Catalogo:
    def __init__(self, items):
        self.items = items

    def __contains__(self, item):
        # MAL — devuelve el índice en lugar de True/False
        for i, elem in enumerate(self.items):
            if elem == item:
                return i  # devuelve 0 para el primer elemento
        return -1  # -1 es truthy

c = Catalogo(["a", "b", "c"])
print("a" in c)   # 0 — Python lo convierte a bool, pero 0 es False → ¡dice que "a" NO está!
print("z" in c)   # -1 — -1 es truthy → ¡dice que "z" SÍ está!
```

`__contains__` debe devolver `True` o `False`. Aunque Python convierte el resultado a booleano, valores como `0` (falsy) o `-1` (truthy) producen resultados invertidos. La solución es `return item in self.items`.
