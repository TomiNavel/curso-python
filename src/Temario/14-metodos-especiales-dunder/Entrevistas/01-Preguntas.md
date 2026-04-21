# Preguntas de Entrevista: Métodos Especiales y Dunder Methods

1. ¿Qué son los dunder methods y por qué no se deben llamar directamente?
2. ¿Qué ocurre cuando se escribe `a + b` y la clase de `a` no define `__add__`?
3. ¿Por qué un operador aritmético debe devolver un nuevo objeto en lugar de modificar `self`?
4. ¿Qué es `NotImplemented` y en qué se diferencia de `NotImplementedError`?
5. ¿Por qué al definir `__eq__` Python automáticamente hace que el objeto sea no hashable?
6. ¿Qué es `@total_ordering` y qué requisitos tiene?
7. ¿Cuál es la diferencia entre `__iter__`/`__next__` y simplemente definir `__getitem__`?
8. ¿Qué hace `__call__` y cuándo es útil?
9. ¿Cuál es la relación entre `__bool__` y `__len__`?
10. ¿Qué métodos debe implementar un objeto para poder usarse con la sentencia `with`?
11. ¿Qué regla deben cumplir `__eq__` y `__hash__` entre sí?
12. ¿Cuál es el resultado de este código?
    ```python
    class Caja:
        def __init__(self, *items):
            self.items = list(items)

        def __len__(self):
            return len(self.items)

        def __getitem__(self, indice):
            return self.items[indice]

        def __contains__(self, item):
            return item.upper() in [i.upper() for i in self.items]

    c = Caja("Manzana", "Pera", "UVA")
    print(len(c))
    print(c[1])
    print("uva" in c)
    print("naranja" in c)
    print(list(c))
    ```

---

### R1. ¿Qué son los dunder methods y por qué no se deben llamar directamente?

Son métodos cuyo nombre empieza y termina con doble guion bajo (`__nombre__`). Python los invoca automáticamente en respuesta a operaciones específicas: `+` llama a `__add__`, `len()` llama a `__len__`, `for` llama a `__iter__`, etc.

No se deben llamar directamente por dos razones:
1. No es idiomático — se escribe `len(obj)`, no `obj.__len__()`.
2. Python puede optimizar la llamada vía operador/función built-in de formas que la llamada directa no aprovecha.

---

### R2. ¿Qué ocurre cuando `a + b` y la clase de `a` no define `__add__`?

Python sigue este orden:
1. Intenta `a.__add__(b)`. Si no existe o devuelve `NotImplemented`, pasa al paso 2.
2. Intenta `b.__radd__(a)` (el método "reflejado" del operando derecho). Si no existe o devuelve `NotImplemented`, pasa al paso 3.
3. Lanza `TypeError: unsupported operand type(s) for +`.

Este mecanismo de fallback permite que tipos diferentes cooperen: si la clase de `a` no sabe sumar con `b`, quizá la clase de `b` sí sabe hacerlo al revés.

---

### R3. ¿Por qué devolver un nuevo objeto en lugar de modificar `self`?

Porque los operadores aritméticos deben ser operaciones puras. `a + b` no debería modificar ni `a` ni `b` — debe devolver un resultado nuevo. Modificar `self` viola la expectativa del programador y genera bugs difíciles de rastrear:

```python
# Si __add__ modificara self:
a = Vector(1, 2)
b = Vector(3, 4)
c = a + b   # si modifica a, ahora a == c == Vector(4, 6) — incorrecto
```

Los operadores "in-place" (`+=`, `-=`) tienen sus propios métodos (`__iadd__`, `__isub__`) donde sí se puede modificar `self`.

---

### R4. `NotImplemented` vs `NotImplementedError`

`NotImplemented` es un **valor** (un singleton) que un dunder method devuelve para indicar que no sabe manejar esa operación con ese tipo de operando. Python lo interpreta como "prueba con el otro operando".

`NotImplementedError` es una **excepción** que se lanza en métodos abstractos o en código que aún no está implementado.

```python
# NotImplemented — devolver
def __add__(self, other):
    if not isinstance(other, MiClase):
        return NotImplemented  # "no sé sumar con ese tipo"

# NotImplementedError — lanzar
def metodo_abstracto(self):
    raise NotImplementedError("Las subclases deben implementar este método")
```

Confundirlos es un error frecuente. Si un `__add__` lanza `NotImplementedError`, Python no tiene oportunidad de probar con `__radd__` del otro operando.

---

### R5. ¿Por qué definir `__eq__` hace que el objeto sea no hashable?

Por defecto, `__hash__` se basa en `id()` (la dirección de memoria del objeto). Si se define `__eq__` para comparar por valor, dos objetos distintos en memoria pueden ser "iguales". Pero sus hashes (basados en `id()`) serían diferentes, violando la regla: **objetos iguales deben tener el mismo hash**.

Para evitar esta inconsistencia, Python establece `__hash__ = None` automáticamente cuando se define `__eq__` sin `__hash__`. Esto fuerza al programador a definir un `__hash__` coherente con su `__eq__`, o a aceptar que el objeto no es hashable.

---

### R6. ¿Qué es `@total_ordering` y qué requisitos tiene?

Es un decorador de `functools` que genera automáticamente los métodos de comparación faltantes. Requisitos:
1. La clase debe definir `__eq__`.
2. La clase debe definir al menos uno de: `__lt__`, `__le__`, `__gt__` o `__ge__`.

A partir de estos dos métodos, `@total_ordering` genera los restantes. Por ejemplo, si se definen `__eq__` y `__lt__`, genera `__le__`, `__gt__` y `__ge__`.

---

### R7. `__iter__`/`__next__` vs `__getitem__`

Si solo se define `__getitem__`, Python puede iterar sobre el objeto llamando a `__getitem__(0)`, `__getitem__(1)`, etc., hasta que se lance `IndexError`. Es un mecanismo de compatibilidad.

`__iter__`/`__next__` es el protocolo de iteración explícito. Es más flexible porque:
- No requiere acceso por índice (puede generar valores al vuelo).
- Permite iteradores infinitos.
- Es más eficiente para estructuras que no son secuencias indexadas (como árboles o grafos).

Si se definen ambos, `for` usa `__iter__`, no `__getitem__`.

---

### R8. ¿Qué hace `__call__` y cuándo es útil?

`__call__` permite invocar un objeto con paréntesis como si fuera una función. Es útil cuando se necesita un "callable con estado" — un objeto que recuerda información entre llamadas.

Casos de uso habituales:
- Objetos que actúan como funciones configurables (estrategias, transformadores).
- Acumuladores o contadores que mantienen estado.
- Implementación del patrón decorador basado en clases.

Se puede verificar si un objeto es llamable con `callable(obj)`.

---

### R9. Relación entre `__bool__` y `__len__`

Python evalúa el valor de verdad de un objeto en este orden:
1. Si tiene `__bool__`, lo usa.
2. Si no tiene `__bool__` pero tiene `__len__`, el objeto es falsy si `len()` devuelve 0, truthy en caso contrario.
3. Si no tiene ninguno de los dos, el objeto siempre es truthy.

`__bool__` tiene prioridad sobre `__len__`. Esto permite definir un valor de verdad independiente de la longitud, lo cual es útil para objetos que no son colecciones (como una conexión que puede estar activa o inactiva).

---

### R10. ¿Qué métodos necesita un objeto para usarse con `with`?

`__enter__` y `__exit__`. Al entrar en el bloque `with`, Python llama a `__enter__()` y asigna su valor de retorno a la variable `as`. Al salir (con o sin excepción), llama a `__exit__(exc_type, exc_val, exc_tb)`.

`__exit__` recibe información sobre la excepción (o `None` si no hubo ninguna). Si devuelve `True`, la excepción se suprime. Si devuelve `False` o `None`, la excepción se propaga.

---

### R11. Regla entre `__eq__` y `__hash__`

Si dos objetos son iguales según `__eq__`, **deben** tener el mismo hash. Lo contrario no se exige: dos objetos con el mismo hash pueden no ser iguales (colisión de hash).

Para implementar `__hash__`, la práctica estándar es crear una tupla con los mismos atributos que participan en `__eq__` y llamar a `hash()` sobre ella:

```python
def __hash__(self):
    return hash((self.atributo1, self.atributo2))
```

Además, los atributos que participan en el hash deben ser efectivamente inmutables. Modificarlos después de insertar el objeto en un set o diccionario corrompe la estructura.

---

### R12. ¿Cuál es el resultado del código?

```python
class Caja:
    def __init__(self, *items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, indice):
        return self.items[indice]

    def __contains__(self, item):
        return item.upper() in [i.upper() for i in self.items]

c = Caja("Manzana", "Pera", "UVA")
print(len(c))
print(c[1])
print("uva" in c)
print("naranja" in c)
print(list(c))
```

Salida:

```
3
Pera
True
False
['Manzana', 'Pera', 'UVA']
```

- `len(c)` → 3 (tres items).
- `c[1]` → `"Pera"` (índice 1).
- `"uva" in c` → `True` — `__contains__` compara en mayúsculas, y `"UVA"` está en la lista.
- `"naranja" in c` → `False` — no existe en ninguna forma.
- `list(c)` → `['Manzana', 'Pera', 'UVA']` — `list()` itera usando `__getitem__` con índices 0, 1, 2 hasta `IndexError`.
