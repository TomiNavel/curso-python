# 14. Métodos Especiales y Dunder Methods

Cuando se crea una clase en Python, los operadores y funciones nativas del lenguaje no saben cómo trabajar con ella. El resultado por defecto es este:

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

p1 = Producto("Laptop", 999)
p2 = Producto("Laptop", 999)

print(p1)        # <__main__.Producto object at 0x000001A3> — dirección de memoria
print(p1 == p2)  # False — aunque tienen exactamente los mismos datos
```

Python no sabe qué significa imprimir un `Producto` ni comparar dos `Producto` porque nadie se lo ha dicho. Los **dunder methods** (de "double underscore") son el mecanismo para decírselo: métodos con nombre `__nombre__` que Python invoca automáticamente en respuesta a operaciones concretas. Definir `__str__` le dice a Python cómo imprimir el objeto. Definir `__eq__` le dice qué significa que dos objetos sean iguales. Definir `__add__` le dice cómo sumarlos.

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} — {self.precio}€"

    def __eq__(self, other):
        if not isinstance(other, Producto):
            return NotImplemented
        return self.nombre == other.nombre and self.precio == other.precio

p1 = Producto("Laptop", 999)
p2 = Producto("Laptop", 999)

print(p1)        # Laptop — 999€
print(p1 == p2)  # True
```

Cada operador y función built-in de Python tiene un dunder method asociado. Cuando se escribe `a + b`, Python llama a `a.__add__(b)`. Cuando se escribe `len(a)`, Python llama a `a.__len__()`. Si la clase define ese método, la operación funciona. Si no, Python lanza `TypeError` o devuelve un resultado por defecto (como comparar por identidad de memoria en el caso de `==`).

Esto significa que cualquier clase puede comportarse exactamente como los tipos nativos de Python — sumarse, compararse, iterarse, usarse con `len()`, e incluso usarse en bloques `with` — simplemente definiendo los métodos adecuados.

---

## 14.1. Qué son los dunder methods

Los dunder methods son métodos cuyo nombre empieza y termina con doble guion bajo (`__nombre__`). No se llaman directamente — Python los invoca en respuesta a operaciones específicas:

| Operación | Llamada interna |
|-----------|----------------|
| `a + b` | `a.__add__(b)` |
| `a == b` | `a.__eq__(b)` |
| `len(a)` | `a.__len__()` |
| `bool(a)` | `a.__bool__()` |
| `for x in a` | `a.__iter__()` → `__next__()` |
| `a[i]` | `a.__getitem__(i)` |
| `str(a)` | `a.__str__()` |
| `repr(a)` | `a.__repr__()` |

La convención de nombrado con dobles guiones bajos está reservada para Python. Nunca se deben inventar nombres propios con este formato (`__mi_metodo__`). Los métodos con un solo guion bajo (`_privado`) o dos sin cierre (`__privado`) tienen otros significados que se verán en el tema 16.

Un dunder method siempre se invoca a través de la operación correspondiente, no directamente. Es decir, se escribe `len(mi_objeto)`, no `mi_objeto.__len__()`. La llamada directa funciona, pero no es idiomático y puede comportarse diferente en ciertos casos (Python optimiza las llamadas vía operador/función built-in).

---

## 14.2. Operadores aritméticos

Los operadores `+`, `-`, `*` y `/` tienen cada uno un dunder method asociado. Cuando Python evalúa `a + b`, llama a `a.__add__(b)`. Si la clase no define ese método, Python lanza `TypeError`.

| Operador | Método |
|----------|--------|
| `+` | `__add__` |
| `-` | `__sub__` |
| `*` | `__mul__` |
| `/` | `__truediv__` |

Cada método recibe `self` (operando izquierdo) y `other` (operando derecho), y debe devolver un objeto nuevo con el resultado — sin modificar los originales.

Un vector matemático (par de coordenadas `x`, `y`) es un ejemplo natural: tiene operaciones aritméticas bien definidas (`(3,4) + (1,2) = (4,6)`), pero Python no las conoce porque `Vector` es una clase propia.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, escalar):
        return Vector(self.x * escalar, self.y * escalar)

    def __rmul__(self, escalar):
        # Se invoca cuando el operando izquierdo no sabe operar con Vector
        # Permite escribir tanto  vector * 3  como  3 * vector
        return self.__mul__(escalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


a = Vector(3, 4)
b = Vector(1, 2)

print(a + b)    # Vector(4, 6)
print(a - b)    # Vector(2, 2)
print(a * 3)    # Vector(9, 12)  — llama a __mul__
print(3 * a)    # Vector(9, 12)  — llama a __rmul__ porque int no sabe multiplicar por Vector
```

Cuando la operación no tiene sentido para el tipo recibido, el método debe devolver `NotImplemented` — no lanzar una excepción. Esto le indica a Python que pruebe con el método del otro operando. Si ambos devuelven `NotImplemented`, Python lanza `TypeError` automáticamente.

---

## 14.3. Operadores de comparación

Los operadores de comparación permiten usar `==`, `<`, `>`, `<=` y `>=` con objetos personalizados.

| Operador | Método |
|----------|--------|
| `==` | `__eq__` |
| `!=` | `__ne__` (Python lo genera automáticamente si se define `__eq__`) |
| `<` | `__lt__` |
| `<=` | `__le__` |
| `>` | `__gt__` |
| `>=` | `__ge__` |

`__eq__` es el más importante. Sin él, `==` compara por identidad (si son el mismo objeto en memoria), no por valor. Esto es lo que ocurre por defecto, como se vio en el tema 13.

```python
class Dinero:
    def __init__(self, cantidad, moneda="EUR"):
        self.cantidad = cantidad
        self.moneda = moneda

    def __eq__(self, other):
        if not isinstance(other, Dinero):
            return NotImplemented
        return self.cantidad == other.cantidad and self.moneda == other.moneda

    def __lt__(self, other):
        if not isinstance(other, Dinero):
            return NotImplemented
        if self.moneda != other.moneda:
            raise ValueError(f"No se pueden comparar {self.moneda} y {other.moneda}")
        return self.cantidad < other.cantidad

    def __le__(self, other):
        return self == other or self < other

    def __repr__(self):
        return f"Dinero({self.cantidad}, {self.moneda!r})"


a = Dinero(100, "EUR")
b = Dinero(200, "EUR")
c = Dinero(100, "EUR")

print(a == c)   # True — misma cantidad y moneda
print(a == b)   # False
print(a < b)    # True
print(a <= c)   # True
```

### 14.3.1. @total_ordering

Definir los seis métodos de comparación es tedioso. El decorador `@total_ordering` de `functools` permite definir solo `__eq__` y uno de los cuatro restantes (`__lt__`, `__le__`, `__gt__` o `__ge__`), y genera automáticamente los demás:

```python
from functools import total_ordering

@total_ordering
class Temperatura:
    def __init__(self, grados):
        self.grados = grados

    def __eq__(self, other):
        if not isinstance(other, Temperatura):
            return NotImplemented
        return self.grados == other.grados

    def __lt__(self, other):
        if not isinstance(other, Temperatura):
            return NotImplemented
        return self.grados < other.grados

    def __repr__(self):
        return f"Temperatura({self.grados})"


a = Temperatura(20)
b = Temperatura(30)

# Todos estos funcionan gracias a @total_ordering
print(a < b)    # True
print(a > b)    # False — generado automáticamente
print(a <= b)   # True — generado automáticamente
print(a >= b)   # False — generado automáticamente
```

`@total_ordering` tiene un coste de rendimiento mínimo porque genera los métodos faltantes a partir de combinaciones de `__eq__` y el método que se proporcionó. En la práctica, el impacto es insignificante para la mayoría de las aplicaciones.

---

## 14.4. Contenedores

Los dunder methods de contenedores permiten que un objeto se comporte como una lista, un diccionario o cualquier colección — soportando indexación (`obj[i]`), asignación (`obj[i] = valor`), eliminación (`del obj[i]`), longitud (`len(obj)`) y pertenencia (`x in obj`).

| Operación | Método |
|-----------|--------|
| `len(obj)` | `__len__` |
| `obj[key]` | `__getitem__` |
| `obj[key] = val` | `__setitem__` |
| `del obj[key]` | `__delitem__` |
| `x in obj` | `__contains__` |

```python
class ListaLimitada:
    """Lista que no permite más de N elementos."""

    def __init__(self, limite):
        self._datos = []
        self._limite = limite

    def agregar(self, elemento):
        if len(self._datos) >= self._limite:
            raise OverflowError(f"Límite de {self._limite} elementos alcanzado")
        self._datos.append(elemento)

    def __len__(self):
        return len(self._datos)

    def __getitem__(self, indice):
        return self._datos[indice]

    def __setitem__(self, indice, valor):
        self._datos[indice] = valor

    def __delitem__(self, indice):
        del self._datos[indice]

    def __contains__(self, elemento):
        return elemento in self._datos

    def __repr__(self):
        return f"ListaLimitada({self._datos})"


lista = ListaLimitada(3)
lista.agregar("a")
lista.agregar("b")
lista.agregar("c")

print(len(lista))       # 3
print(lista[0])          # a
print("b" in lista)      # True

lista[1] = "B"
print(lista)             # ListaLimitada(['a', 'B', 'c'])

del lista[2]
print(lista)             # ListaLimitada(['a', 'B'])
```

`__getitem__` es el más versátil de todos. Si se define `__getitem__`, Python automáticamente permite iterar sobre el objeto con `for` (iterando con índices 0, 1, 2... hasta que se lance `IndexError`). También habilita el slicing si el método maneja objetos `slice`:

```python
class Rango:
    def __init__(self, inicio, fin):
        self._datos = list(range(inicio, fin))

    def __getitem__(self, indice):
        # Funciona con índices simples y con slicing
        return self._datos[indice]

    def __len__(self):
        return len(self._datos)

r = Rango(10, 20)
print(r[0])        # 10
print(r[-1])       # 19
print(r[2:5])      # [12, 13, 14] — slicing funciona automáticamente

# for funciona gracias a __getitem__
for n in r:
    print(n, end=" ")  # 10 11 12 13 14 15 16 17 18 19
```

Si no se define `__contains__`, Python usa `__iter__` (o `__getitem__`) para buscar el elemento recorriendo la colección. Definir `__contains__` permite implementar una búsqueda más eficiente cuando sea posible.

---

## 14.5. Iteración

El protocolo de iteración en Python se basa en dos métodos: `__iter__` y `__next__`. Un objeto es **iterable** si define `__iter__`, y es un **iterador** si define tanto `__iter__` como `__next__`.

- `__iter__()` debe devolver un objeto iterador (puede ser `self` si el propio objeto es el iterador).
- `__next__()` devuelve el siguiente elemento. Cuando no quedan más, debe lanzar `StopIteration`.

```python
class Cuenta:
    """Cuenta regresiva desde un número hasta 1."""

    def __init__(self, inicio):
        self.actual = inicio

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual <= 0:
            raise StopIteration
        valor = self.actual
        self.actual -= 1
        return valor


for n in Cuenta(5):
    print(n, end=" ")  # 5 4 3 2 1
```

Un detalle importante: este iterador se agota después de un uso. Si se quiere iterar varias veces, el patrón correcto es separar el iterable del iterador — `__iter__` devuelve un nuevo objeto iterador cada vez:

```python
class Repetidor:
    """Repite un valor N veces. Se puede iterar múltiples veces."""

    def __init__(self, valor, veces):
        self.valor = valor
        self.veces = veces

    def __iter__(self):
        # Devuelve un nuevo iterador cada vez
        for _ in range(self.veces):
            yield self.valor


r = Repetidor("hola", 3)

# Primera iteración
for x in r:
    print(x, end=" ")  # hola hola hola

print()

# Segunda iteración — funciona porque __iter__ crea un nuevo generador
for x in r:
    print(x, end=" ")  # hola hola hola
```

El uso de `yield` dentro de `__iter__` convierte el método en un generador, que es la forma más sencilla de crear un iterador sin definir una clase separada con `__next__`. Los generadores se verán en profundidad en el tema 19.

---

## 14.6. Contexto

Los métodos `__enter__` y `__exit__` permiten usar un objeto con la sentencia `with`. Esto es útil para garantizar que un recurso se cierre o limpie correctamente, sin importar si ocurre una excepción.

- `__enter__()` se ejecuta al entrar en el bloque `with`. Su valor de retorno se asigna a la variable después de `as`.
- `__exit__(exc_type, exc_val, exc_tb)` se ejecuta al salir del bloque `with`, haya o no excepción. Los tres parámetros contienen información sobre la excepción (o `None` si no hubo ninguna). Si devuelve `True`, la excepción se suprime.

```python
class Temporizador:
    """Mide el tiempo de ejecución de un bloque de código."""

    def __enter__(self):
        import time
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.duracion = time.perf_counter() - self.inicio
        print(f"Tiempo: {self.duracion:.4f} segundos")
        return False  # no suprime excepciones


with Temporizador() as t:
    total = sum(range(1_000_000))

# Salida: Tiempo: 0.0234 segundos (varía según el equipo)
```

Otro ejemplo — un gestor que abre y cierra un archivo de log:

```python
class ArchivoLog:
    def __init__(self, ruta):
        self.ruta = ruta
        self.archivo = None

    def __enter__(self):
        self.archivo = open(self.ruta, "a", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.archivo:
            self.archivo.close()
        return False

    def escribir(self, mensaje):
        self.archivo.write(mensaje + "\n")


with ArchivoLog("app.log") as log:
    log.escribir("Inicio de operación")
    log.escribir("Operación completada")
# El archivo se cierra automáticamente al salir del with
```

Los context managers se verán con más detalle en el tema 21, incluyendo la forma simplificada con `@contextmanager`.

---

## 14.7. Llamabilidad

El método `__call__` permite que un objeto se comporte como una función — que se pueda invocar con paréntesis. Cualquier objeto que defina `__call__` es "llamable" (callable).

```python
class Multiplicador:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, valor):
        return valor * self.factor


doble = Multiplicador(2)
triple = Multiplicador(3)

print(doble(5))    # 10 — llama a doble.__call__(5)
print(triple(5))   # 15

# callable() confirma que el objeto es llamable
print(callable(doble))  # True
```

`__call__` es útil cuando un objeto necesita mantener estado entre llamadas, algo que una función normal no puede hacer fácilmente (sin closures):

```python
class Acumulador:
    def __init__(self):
        self.total = 0
        self.llamadas = 0

    def __call__(self, valor):
        self.total += valor
        self.llamadas += 1
        return self.total

    def __repr__(self):
        return f"Acumulador(total={self.total}, llamadas={self.llamadas})"


acc = Acumulador()
print(acc(10))   # 10
print(acc(20))   # 30
print(acc(5))    # 35
print(acc)       # Acumulador(total=35, llamadas=3)
```

---

## 14.8. Booleano y formato

### `__bool__`

`__bool__` define el valor de verdad de un objeto. Se invoca con `bool()`, en condiciones `if` y en expresiones booleanas.

Sin `__bool__`, Python usa `__len__` como fallback: un objeto con `__len__` es falsy si `len()` devuelve 0, y truthy en caso contrario. Si no hay ni `__bool__` ni `__len__`, el objeto siempre es truthy.

```python
class Cola:
    def __init__(self):
        self._elementos = []

    def agregar(self, elem):
        self._elementos.append(elem)

    def __len__(self):
        return len(self._elementos)

    def __bool__(self):
        return len(self._elementos) > 0


cola = Cola()
print(bool(cola))   # False — vacía

if not cola:
    print("Cola vacía")  # Se imprime

cola.agregar("tarea")
print(bool(cola))   # True

if cola:
    print("Cola con elementos")  # Se imprime
```

En este ejemplo, `__bool__` y `__len__` producirían el mismo resultado. Pero `__bool__` permite controlar el valor de verdad de forma independiente a la longitud, lo cual es útil cuando un objeto no es una colección pero necesita evaluarse como booleano:

```python
class Conexion:
    def __init__(self, host):
        self.host = host
        self.activa = False

    def conectar(self):
        self.activa = True

    def __bool__(self):
        return self.activa


conn = Conexion("localhost")
print(bool(conn))    # False

conn.conectar()
if conn:
    print("Conectado")  # Se imprime
```

### `__format__`

`__format__` controla cómo se muestra el objeto cuando se usa dentro de un f-string con formato o con la función `format()`. Recibe un string con la especificación de formato (lo que va después de `:` en un f-string).

```python
class Porcentaje:
    def __init__(self, valor):
        self.valor = valor

    def __format__(self, spec):
        if spec == "%":
            return f"{self.valor * 100:.1f}%"
        elif spec == "decimal":
            return f"{self.valor:.4f}"
        return str(self.valor)

    def __repr__(self):
        return f"Porcentaje({self.valor})"


p = Porcentaje(0.856)

print(f"{p}")           # 0.856 — sin formato, usa str()
print(f"{p:%}")         # 85.6% — formato personalizado
print(f"{p:decimal}")   # 0.8560 — otro formato personalizado
print(format(p, "%"))   # 85.6% — equivalente a f"{p:%}"
```

---

## 14.9. Hashing

`__hash__` devuelve un entero que identifica al objeto para su uso en sets y como clave de diccionarios. Python lo usa cuando se inserta un objeto en un `set` o se usa como clave en un `dict`.

La regla fundamental: **si dos objetos son iguales (`__eq__`), deben tener el mismo hash**. El incumplimiento de esta regla corrompe el comportamiento de sets y diccionarios.

Por defecto, si se define `__eq__` sin `__hash__`, Python establece `__hash__ = None`, haciendo el objeto no hashable. Esto es una medida de seguridad: si se cambia la definición de igualdad, el hash por defecto (basado en `id()`) ya no es coherente.

```python
class Coordenada:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        if not isinstance(other, Coordenada):
            return NotImplemented
        return self.lat == other.lat and self.lon == other.lon

    def __hash__(self):
        return hash((self.lat, self.lon))

    def __repr__(self):
        return f"Coordenada({self.lat}, {self.lon})"


# Se puede usar en sets
lugares = {Coordenada(40.4, -3.7), Coordenada(41.4, 2.2), Coordenada(40.4, -3.7)}
print(lugares)  # {Coordenada(40.4, -3.7), Coordenada(41.4, 2.2)} — sin duplicados

# Se puede usar como clave de diccionario
nombres = {Coordenada(40.4, -3.7): "Madrid", Coordenada(41.4, 2.2): "Barcelona"}
print(nombres[Coordenada(40.4, -3.7)])  # Madrid
```

Para generar un hash correcto, la forma más habitual es crear una tupla con los atributos que participan en `__eq__` y llamar a `hash()` sobre ella: `hash((self.attr1, self.attr2))`. Esto funciona porque las tuplas ya son hashables.

Un objeto hashable debe ser **efectivamente inmutable** en los atributos que definen su igualdad. Si se modifica un atributo que participa en el hash después de insertar el objeto en un set, el set se corrompe:

```python
c = Coordenada(40.4, -3.7)
lugares = {c}
print(c in lugares)    # True

c.lat = 0  # se modifica un atributo que participa en el hash
print(c in lugares)    # False — ¡el set ya no lo encuentra!
```

Por esto, las clases hashables suelen proteger sus atributos para evitar modificaciones accidentales. Las herramientas para hacerlo (properties, `__slots__`, frozen dataclasses) se verán en temas posteriores.
