# 4. Diccionarios y Sets

Diccionarios y sets comparten la misma estructura interna — una hash table — lo que les da operaciones de búsqueda, inserción y eliminación en O(1). La diferencia es su propósito: los diccionarios almacenan pares clave-valor, los sets almacenan elementos únicos sin valor asociado.

## 4.1. Diccionarios

Un diccionario es una colección de pares **clave-valor** mutable y ordenada por inserción (garantizado desde Python 3.7). Es la estructura de datos más importante de Python después de las listas.

### 4.1.1. Características y hash tables

Internamente, un diccionario es una **hash table**. Cuando se añade una clave, Python calcula su hash — un número entero derivado del valor de la clave — y usa ese número para determinar en qué posición de memoria almacenar el par. Cuando se accede a una clave, Python calcula su hash de nuevo y va directamente a esa posición, sin recorrer nada.

Esto hace que el acceso, inserción y eliminación en un diccionario sean O(1) en promedio, independientemente del tamaño.

La consecuencia directa de usar hashing: **solo los objetos hashables pueden ser keys**. Los tipos inmutables (strings, números, tuplas de inmutables) son hashables. Las listas, dicts y sets no lo son.

```python
# Keys válidas
d = {
    "nombre": "Ana",    # string
    42: "respuesta",    # int
    (0, 0): "origen",   # tupla
}

# Key inválida
d[[1, 2]] = "valor"  # TypeError: unhashable type: 'list'
```

### 4.1.2. Creación y acceso

Hay varias formas de crear un diccionario. La más común es con llaves `{}` y pares `clave: valor`. También se puede usar el constructor `dict()` con argumentos con nombre, lo cual es más legible cuando las claves son strings simples.

Para acceder a un valor se usa la clave entre corchetes. Si la clave no existe, Python lanza `KeyError`. Para comprobar si una clave existe antes de acceder, se usa el operador `in`, que funciona en O(1) gracias a la hash table.

Añadir un par nuevo y modificar uno existente usan la misma sintaxis: `dict[clave] = valor`. Si la clave ya existe, se sobreescribe el valor; si no existe, se crea.

```python
# Creación con llaves
usuario = {"nombre": "Ana", "edad": 28, "activo": True}

# Creación con dict()
config = dict(host="localhost", puerto=5432)

# Diccionario vacío
vacio = {}

# Acceso por clave
print(usuario["nombre"])   # "Ana"
print(usuario["edad"])     # 28

# Acceso a clave inexistente — lanza KeyError
print(usuario["email"])    # KeyError: 'email'

# Añadir o modificar
usuario["email"] = "ana@ejemplo.com"   # añade nueva clave
usuario["edad"] = 29                   # modifica existente

# Eliminar
del usuario["activo"]

# Comprobar existencia de clave — O(1)
print("nombre" in usuario)   # True
print("activo" in usuario)   # False
```

### 4.1.3. Métodos de diccionarios (get, keys, values, items, update, pop, setdefault, fromkeys)

Los diccionarios tienen métodos especializados para acceder y modificar su contenido de forma segura. El más importante es `get()`, que permite acceder a una clave sin riesgo de `KeyError`: si la clave no existe, devuelve `None` o un valor por defecto que se le indique.

`keys()`, `values()` e `items()` devuelven **vistas dinámicas** del diccionario. No son listas estáticas: si el diccionario cambia después de obtener la vista, la vista refleja el cambio automáticamente.

`update()` fusiona otro diccionario (o iterable de pares) en el actual. Si hay claves en común, los valores del diccionario pasado sobreescriben los existentes. Desde Python 3.9, también se puede usar el operador `|` para fusionar dos diccionarios en uno nuevo, sin modificar ninguno de los originales.

`pop()` elimina una clave y devuelve su valor, similar al `pop()` de listas pero con clave en lugar de índice. Acepta un valor por defecto para evitar `KeyError`.

`setdefault()` es útil cuando se quiere obtener un valor pero también asegurar que la clave exista: si la clave ya existe devuelve su valor sin tocar nada, y si no existe la crea con el valor indicado.

`fromkeys()` es un método de clase (se llama sobre `dict`, no sobre una instancia) que crea un diccionario nuevo a partir de un iterable de claves, asignando a todas el mismo valor por defecto. Es la forma más directa de inicializar un diccionario cuando se conocen las claves de antemano y se quiere arrancar con un valor común. Atención con valores mutables: como el valor se comparte entre todas las claves, modificar uno modifica todos.

```python
usuario = {"nombre": "Ana", "edad": 28}

# get: acceso seguro — devuelve None (o valor por defecto) si la clave no existe
print(usuario.get("nombre"))         # "Ana"
print(usuario.get("email"))          # None — no lanza KeyError
print(usuario.get("email", "N/A"))   # "N/A" — valor por defecto explícito

# keys, values, items: vistas dinámicas del diccionario
print(usuario.keys())    # dict_keys(['nombre', 'edad'])
print(usuario.values())  # dict_values(['Ana', 28])
print(usuario.items())   # dict_items([('nombre', 'Ana'), ('edad', 28)])
# Son vistas, no listas — reflejan cambios en el dict en tiempo real

# update: fusiona otro dict (o iterable de pares) — sobreescribe claves existentes
usuario.update({"edad": 29, "ciudad": "Madrid"})
print(usuario)  # {'nombre': 'Ana', 'edad': 29, 'ciudad': 'Madrid'}

# Fusionar diccionarios con | (Python 3.9+) — crea un dict nuevo
defaults = {"timeout": 30, "puerto": 5432}
custom = {"puerto": 3306, "db": "test"}
merged = defaults | custom   # {'timeout': 30, 'puerto': 3306, 'db': 'test'}
# custom sobreescribe defaults en caso de colisión

# pop: elimina y devuelve el valor — lanza KeyError si no existe (salvo default)
edad = usuario.pop("edad")           # devuelve 29
rol = usuario.pop("rol", "usuario")  # devuelve "usuario" sin lanzar error

# setdefault: devuelve el valor si la clave existe, si no la crea con el valor dado
usuario.setdefault("activo", True)   # crea "activo": True
usuario.setdefault("nombre", "Bob")  # no modifica "nombre", devuelve "Ana"

# fromkeys: crea un dict nuevo con las claves dadas y un valor común por defecto
campos = dict.fromkeys(["nombre", "email", "telefono"], "")
# {'nombre': '', 'email': '', 'telefono': ''}

# Sin valor, todas las claves apuntan a None
permisos = dict.fromkeys(["lectura", "escritura", "admin"])
# {'lectura': None, 'escritura': None, 'admin': None}

# CUIDADO con valores mutables — el mismo objeto se comparte entre claves
grupos = dict.fromkeys(["a", "b", "c"], [])
grupos["a"].append(1)
print(grupos)  # {'a': [1], 'b': [1], 'c': [1]} — los tres apuntan a la MISMA lista
```

### 4.1.4. Counter

`Counter` es una subclase de `dict` del módulo `collections` especializada en contar elementos. Recibe un iterable y devuelve un dict donde las keys son los elementos y los values sus conteos. Es la forma más directa de contar ocurrencias sin escribir lógica manual.

El método `most_common(n)` devuelve los `n` elementos más frecuentes como lista de tuplas, ordenados de mayor a menor frecuencia.

```python
from collections import Counter

# Contar caracteres
letras = Counter("mississippi")
print(letras)  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# Contar palabras
palabras = Counter(["gato", "perro", "gato", "pez", "gato"])
print(palabras)  # Counter({'gato': 3, 'perro': 1, 'pez': 1})

# most_common: los N elementos más frecuentes
print(palabras.most_common(2))  # [('gato', 3), ('perro', 1)]

# Acceso directo al conteo de un elemento
print(palabras["gato"])   # 3
print(palabras["león"])   # 0 — no lanza KeyError, devuelve 0

# Operaciones aritméticas entre Counters
a = Counter(["a", "b", "a", "c"])
b = Counter(["a", "b", "b"])
print(a + b)  # Counter({'a': 3, 'b': 3, 'c': 1}) — suma conteos
print(a - b)  # Counter({'a': 1, 'c': 1})           — resta (descarta negativos)
print(a & b)  # Counter({'a': 1, 'b': 1})            — mínimo
print(a | b)  # Counter({'a': 2, 'b': 2, 'c': 1})   — máximo
```

## 4.2. Sets

Un set es una colección **no ordenada** de elementos **únicos**. Internamente usa la misma estructura de hash table que los diccionarios, lo que le da búsqueda, inserción y eliminación en O(1). Su propósito principal es eliminar duplicados y hacer operaciones de teoría de conjuntos.

### 4.2.1. Características y unicidad

La unicidad es automática — añadir un elemento que ya existe no hace nada, no lanza error. Esta propiedad convierte a los sets en la herramienta ideal para eliminar duplicados de cualquier iterable.

Al igual que las keys de un dict, los elementos de un set deben ser **hashables**. No se pueden crear sets de listas ni de otros sets (para eso existe `frozenset`, que se verá más adelante).

Los sets no tienen orden — no se puede acceder a un elemento por índice (`set[0]` lanza `TypeError`). Si se necesita orden, hay que convertir a lista.

```python
numeros = {1, 2, 3, 2, 1}
print(numeros)  # {1, 2, 3} — duplicados eliminados automáticamente

# Caso de uso más común: eliminar duplicados de una lista
lista = [1, 2, 2, 3, 3, 3, 4]
sin_duplicados = list(set(lista))
print(sin_duplicados)  # [1, 2, 3, 4] — orden no garantizado
```

### 4.2.2. Creación de sets

Hay un detalle importante en la creación de sets: las llaves `{}` sin pares clave-valor crean un set, **pero `{}` vacío crea un diccionario**, no un set. Para crear un set vacío es obligatorio usar `set()`.

Se puede crear un set a partir de cualquier iterable (lista, string, tupla) usando `set()`. Los duplicados se eliminan automáticamente.

```python
# Con llaves — atención: {} crea un dict vacío, no un set
colores = {"rojo", "verde", "azul"}

# Set vacío — obligatoriamente con set()
vacio = set()     # correcto
no_vacio = {}     # esto es un dict vacío, no un set

# Desde un iterable
desde_lista = set([1, 2, 3, 2, 1])   # {1, 2, 3}
desde_string = set("abracadabra")     # {'a', 'b', 'r', 'c', 'd'}
```

### 4.2.3. Operaciones de conjuntos (union, intersection, difference, symmetric_difference)

Las operaciones de conjuntos son el punto fuerte de los sets. Replican las operaciones matemáticas de la teoría de conjuntos y funcionan en O(n), mucho más eficiente que hacer búsquedas manuales en listas.

Cada operación tiene dos formas equivalentes: un método (`a.union(b)`) y un operador simbólico (`a | b`). El resultado es siempre un set nuevo; los originales no se modifican.

También existen métodos para comprobar relaciones entre conjuntos: `issubset` (¿todos los elementos de A están en B?), `issuperset` (¿A contiene todos los elementos de B?) e `isdisjoint` (¿A y B no tienen elementos en común?).

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Unión: todos los elementos de ambos
print(a | b)           # {1, 2, 3, 4, 5, 6}
print(a.union(b))      # equivalente

# Intersección: solo los elementos comunes
print(a & b)                  # {3, 4}
print(a.intersection(b))      # equivalente

# Diferencia: elementos en a que no están en b
print(a - b)                  # {1, 2}
print(a.difference(b))        # equivalente

# Diferencia simétrica: elementos que están en uno pero no en ambos
print(a ^ b)                              # {1, 2, 5, 6}
print(a.symmetric_difference(b))          # equivalente

# Subconjunto y superconjunto
c = {1, 2}
print(c.issubset(a))    # True  — c ⊆ a
print(a.issuperset(c))  # True  — a ⊇ c
print(a.isdisjoint(b))  # False — tienen elementos comunes
```

### 4.2.4. Métodos de sets (add, remove, discard, pop, update)

Los métodos de modificación de sets son similares a los de listas, con una diferencia clave: no hay concepto de posición. `add` añade un elemento (si ya existe, no hace nada). `remove` y `discard` eliminan un elemento, pero `remove` lanza `KeyError` si no existe mientras que `discard` no lanza error. La regla es: usar `remove` cuando la ausencia del elemento indica un error lógico en el programa, y `discard` cuando es una operación opcional.

`pop()` en sets elimina y devuelve un elemento **arbitrario** (no el último como en listas, porque los sets no tienen orden). `update` añade múltiples elementos desde un iterable.

```python
colores = {"rojo", "verde", "azul"}

# add: añade un elemento — O(1)
colores.add("amarillo")
colores.add("rojo")    # no hace nada, ya existe

# remove: elimina un elemento — lanza KeyError si no existe
colores.remove("verde")
# colores.remove("negro")  # KeyError

# discard: elimina un elemento — NO lanza error si no existe
colores.discard("azul")
colores.discard("negro")  # silencioso, sin error

# pop: elimina y devuelve un elemento arbitrario — lanza KeyError si el set está vacío
elemento = colores.pop()

# update: añade múltiples elementos desde un iterable
colores.update(["rosa", "morado"])
colores |= {"naranja"}  # equivalente con operador
```

### 4.2.5. frozenset

`frozenset` es la versión inmutable de un set. Una vez creado, no se puede añadir ni eliminar elementos. A cambio, es hashable — puede usarse como key de un diccionario o como elemento de otro set.

El caso de uso más habitual es cuando se necesita un conjunto como key de un dict o elemento de otro set — situación que con un set normal no sería posible por no ser hashable.

```python
fs = frozenset([1, 2, 3, 2, 1])
print(fs)  # frozenset({1, 2, 3})

# Es hashable — puede ser key de dict o elemento de set
permisos = {
    frozenset(["lectura"]): "usuario",
    frozenset(["lectura", "escritura"]): "editor",
    frozenset(["lectura", "escritura", "admin"]): "admin",
}

# Soporta todas las operaciones de conjuntos (pero no las de modificación)
a = frozenset({1, 2, 3})
b = frozenset({2, 3, 4})
print(a | b)   # frozenset({1, 2, 3, 4})
print(a & b)   # frozenset({2, 3})

# No soporta add, remove, discard, update
# a.add(4)  # AttributeError: 'frozenset' object has no attribute 'add'
```

---

## Contenido que requiere temas posteriores

Las siguientes secciones cubren aspectos importantes de diccionarios y sets, pero necesitan conceptos que se enseñan en temas posteriores. Se incluyen aquí como referencia para consultar una vez vistos esos temas.

### 4.3. Iteración sobre diccionarios *(requiere tema 5: Control de Flujo)*

Iterar sobre un diccionario recorre sus claves por defecto. Para acceder a los valores o a los pares clave-valor, se usan los métodos `values()` e `items()` respectivamente. La forma más habitual es `items()`, que permite desempaquetar clave y valor directamente.

```python
config = {"host": "localhost", "puerto": 5432, "db": "myapp"}

# Iterar sobre keys (comportamiento por defecto)
for clave in config:
    print(clave)

# Iterar sobre values
for valor in config.values():
    print(valor)

# Iterar sobre pares clave-valor — el más común
for clave, valor in config.items():
    print(f"{clave}: {valor}")

# Fusionar diccionarios (Python 3.9+)
defaults = {"timeout": 30, "puerto": 5432}
custom = {"puerto": 3306, "db": "test"}
merged = defaults | custom   # {'timeout': 30, 'puerto': 3306, 'db': 'test'}
# custom sobreescribe defaults en caso de colisión
```

### 4.4. Ordenamiento de diccionarios *(requiere tema 5: Control de Flujo y tema 8: Funciones Avanzadas)*

Desde Python 3.7 los dicts mantienen el orden de inserción. Para ordenar por clave o valor se usa `sorted()` combinado con `lambda` para definir el criterio de ordenamiento.

```python
precios = {"banana": 0.5, "manzana": 1.2, "kiwi": 0.8}

# Ordenar por clave
por_clave = dict(sorted(precios.items()))
print(por_clave)  # {'banana': 0.5, 'kiwi': 0.8, 'manzana': 1.2}

# Ordenar por valor
por_valor = dict(sorted(precios.items(), key=lambda item: item[1]))
print(por_valor)  # {'banana': 0.5, 'kiwi': 0.8, 'manzana': 1.2}

# Ordenar por valor descendente
por_valor_desc = dict(sorted(precios.items(), key=lambda item: item[1], reverse=True))
print(por_valor_desc)  # {'manzana': 1.2, 'kiwi': 0.8, 'banana': 0.5}
```

### 4.5. defaultdict *(requiere tema 5: Control de Flujo)*

`defaultdict` es una subclase de `dict` del módulo `collections` que, en lugar de lanzar `KeyError` al acceder a una clave inexistente, crea automáticamente esa clave con un valor por defecto generado por una función que se le pasa al crear el dict.

Resuelve un patrón muy común: acumular valores en un dict sin tener que comprobar si la clave ya existe.

```python
from collections import defaultdict

# Sin defaultdict: hay que inicializar la clave antes de usarla
palabras = ["gato", "perro", "gato", "pez", "perro", "gato"]
conteo = {}
for palabra in palabras:
    if palabra not in conteo:
        conteo[palabra] = 0
    conteo[palabra] += 1

# Con defaultdict(int): int() devuelve 0, valor por defecto para enteros
conteo = defaultdict(int)
for palabra in palabras:
    conteo[palabra] += 1  # si no existe, se crea con 0 automáticamente
print(dict(conteo))  # {'gato': 3, 'perro': 2, 'pez': 1}

# defaultdict(list): agrupar elementos por categoría
grupos = defaultdict(list)
datos = [("fruta", "manzana"), ("verdura", "zanahoria"), ("fruta", "pera")]
for categoria, item in datos:
    grupos[categoria].append(item)  # si no existe, se crea con [] automáticamente
print(dict(grupos))  # {'fruta': ['manzana', 'pera'], 'verdura': ['zanahoria']}
```

La función que se pasa (`int`, `list`, `set`, o cualquier callable) se llama sin argumentos cada vez que se accede a una clave nueva.

### 4.6. deque y OrderedDict *(requiere tema 5: Control de Flujo)*

#### deque

`deque` (double-ended queue, pronunciado "deck") es una estructura del módulo `collections` optimizada para añadir y eliminar elementos en **ambos extremos** en O(1). Una lista normal es O(1) para `append` y `pop` al final, pero O(n) para `insert(0, x)` y `pop(0)` al principio, porque tiene que desplazar todos los elementos. `deque` resuelve eso.

Es la estructura ideal para implementar colas (FIFO), pilas (LIFO), y buffers circulares. En entrevistas técnicas aparece frecuentemente cuando se pregunta sobre la complejidad de inserción al principio de una lista.

`deque` también acepta un parámetro `maxlen` al crearse. Si se establece, el deque descarta automáticamente elementos del extremo opuesto cuando se añaden nuevos y se supera el límite. Esto lo convierte en un buffer circular sin lógica adicional.

```python
from collections import deque

# Creación
d = deque([1, 2, 3])

# Añadir elementos — O(1) en ambos extremos
d.append(4)       # al final:     deque([1, 2, 3, 4])
d.appendleft(0)   # al principio: deque([0, 1, 2, 3, 4])

# Eliminar elementos — O(1) en ambos extremos
d.pop()       # elimina del final:     devuelve 4
d.popleft()   # elimina del principio: devuelve 0

# Extender en ambos extremos
d.extend([4, 5])        # al final:     deque([1, 2, 3, 4, 5])
d.extendleft([0, -1])   # al principio: deque([-1, 0, 1, 2, 3, 4, 5])
# Nota: extendleft invierte el orden de los elementos añadidos

# Rotar elementos
d = deque([1, 2, 3, 4, 5])
d.rotate(2)    # rota 2 posiciones a la derecha: deque([4, 5, 1, 2, 3])
d.rotate(-2)   # rota 2 posiciones a la izquierda: deque([1, 2, 3, 4, 5])

# maxlen: buffer circular — descarta automáticamente del extremo opuesto
ultimos_3 = deque(maxlen=3)
ultimos_3.append(1)   # deque([1])
ultimos_3.append(2)   # deque([1, 2])
ultimos_3.append(3)   # deque([1, 2, 3])
ultimos_3.append(4)   # deque([2, 3, 4]) — el 1 se descarta automáticamente
```

**Cuándo usar deque en lugar de list:**

| Operación | list | deque |
|---|---|---|
| Añadir/eliminar al final | O(1) | O(1) |
| Añadir/eliminar al principio | O(n) | O(1) |
| Acceso por índice | O(1) | O(n) |

Si se necesita acceso frecuente por índice (`d[3]`), la lista es mejor. Si se necesita inserción/eliminación frecuente en ambos extremos, `deque` es la opción correcta.

#### OrderedDict

`OrderedDict` es una subclase de `dict` que en versiones anteriores a Python 3.7 era la única forma de tener un diccionario que mantuviera el orden de inserción. Desde Python 3.7, los `dict` normales ya garantizan ese orden, por lo que `OrderedDict` ha perdido la mayor parte de su utilidad.

Sin embargo, `OrderedDict` conserva dos diferencias que un dict normal no tiene:

1. **La comparación entre OrderedDicts considera el orden**, mientras que entre dicts normales no:

```python
from collections import OrderedDict

# Dicts normales: el orden no afecta la igualdad
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True — mismo contenido, orden irrelevante

# OrderedDicts: el orden sí afecta la igualdad
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False — mismo contenido, distinto orden
```

2. **`move_to_end(key)`** permite mover una clave existente al final o al principio:

```python
od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")             # mueve "a" al final
print(od)  # OrderedDict([('b', 2), ('c', 3), ('a', 1)])

od.move_to_end("c", last=False)  # mueve "c" al principio
print(od)  # OrderedDict([('c', 3), ('b', 2), ('a', 1)])
```

En la práctica, se encuentra `OrderedDict` en código anterior a Python 3.7 y en casos donde la comparación por orden es importante. Para código nuevo, usar `dict` normal es suficiente en la gran mayoría de casos.
