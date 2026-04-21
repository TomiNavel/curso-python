# 3. Listas y Tuplas

Listas y tuplas son secuencias ordenadas que permiten acceso por índice y slicing. La diferencia fundamental es la mutabilidad: las listas pueden modificarse después de crearse, las tuplas no. Esto determina cuándo usar cada una — listas para colecciones que cambian, tuplas para datos que deben permanecer fijos.

## 3.1. Listas

Una lista es una colección ordenada y mutable de elementos. Es la estructura de datos más versátil de Python: puede contener cualquier tipo de dato, mezclar tipos distintos y cambiar de tamaño dinámicamente.

### 3.1.1. Creación y acceso

Las listas se crean con corchetes `[]` o con la función `list()`. Pueden contener elementos de cualquier tipo, incluso mezclados, aunque en la práctica lo habitual es que todos los elementos sean del mismo tipo.

Cada elemento ocupa una posición numérica llamada **índice**. El primer elemento tiene índice `0`, el segundo `1`, y así sucesivamente. Python también permite índices negativos: `-1` es el último elemento, `-2` el penúltimo, etc. Esto es útil cuando se necesita acceder al final de la lista sin conocer su longitud.

Como las listas son mutables, se puede cambiar el valor de cualquier posición asignándole directamente con `=`.

```python
# Creación
numeros = [1, 2, 3, 4, 5]
mixta = [1, "hola", True, 3.14]   # puede mezclar tipos
vacia = []
desde_rango = list(range(5))      # [0, 1, 2, 3, 4]

# Acceso por índice — igual que strings
print(numeros[0])   # 1  — primer elemento
print(numeros[-1])  # 5  — último elemento
print(numeros[-2])  # 4  — segundo desde el final

# Modificación — a diferencia de los strings, las listas son mutables
numeros[0] = 99
print(numeros)  # [99, 2, 3, 4, 5]
```

### 3.1.2. Slicing

El slicing permite extraer una porción de la lista usando la sintaxis `[inicio:fin:paso]`. Funciona igual que en strings (sección 2.1.2):

- `inicio` es el índice donde empieza la porción (incluido). Si se omite, empieza desde el principio.
- `fin` es el índice donde termina (excluido). Si se omite, llega hasta el final.
- `paso` indica cada cuántos elementos se toma uno. Si se omite, es 1. Un paso negativo recorre la lista en sentido inverso.

El slicing siempre devuelve una **nueva lista**, no modifica la original. Sin embargo, si se usa slicing en el lado izquierdo de una asignación, permite reemplazar un fragmento de la lista original.

```python
letras = ["a", "b", "c", "d", "e"]

print(letras[1:3])   # ["b", "c"]
print(letras[:2])    # ["a", "b"]
print(letras[2:])    # ["c", "d", "e"]
print(letras[::2])   # ["a", "c", "e"] — cada 2 elementos
print(letras[::-1])  # ["e", "d", "c", "b", "a"] — lista invertida

# El slicing también permite reemplazar fragmentos
letras[1:3] = ["X", "Y"]
print(letras)  # ["a", "X", "Y", "d", "e"]
```

### 3.1.3. Métodos de modificación (append, insert, extend, remove, pop, clear)

Estos métodos modifican la lista original directamente, sin crear una nueva. A esto se le llama operar **in-place**. Es una consecuencia lógica de que las listas son mutables: en lugar de generar una copia modificada, alteran el objeto que ya existe en memoria.

Por esta razón, todos devuelven `None` — no hay lista nueva que devolver. Es un error frecuente escribir `lista = lista.append(4)`, porque `append` devuelve `None` y se pierde la referencia a la lista original. La excepción es `pop`, que sí devuelve un valor: el elemento que acaba de eliminar, ya que normalmente se necesita usar ese elemento.

```python
lista = [1, 2, 3]

# append: añade un elemento al final — O(1)
lista.append(4)           # [1, 2, 3, 4]

# insert: añade en una posición específica — O(n)
lista.insert(1, 99)       # [1, 99, 2, 3, 4]

# extend: añade todos los elementos de un iterable — equivale a +=
lista.extend([5, 6])      # [1, 99, 2, 3, 4, 5, 6]
lista += [7, 8]           # equivalente a extend

# remove: elimina la primera ocurrencia del valor — lanza ValueError si no existe
lista.remove(99)          # [1, 2, 3, 4, 5, 6, 7, 8]

# pop: elimina y devuelve el elemento en la posición dada (por defecto el último) — O(1) al final, O(n) en medio
ultimo = lista.pop()      # devuelve 8, lista queda [1, 2, 3, 4, 5, 6, 7]
primero = lista.pop(0)    # devuelve 1, lista queda [2, 3, 4, 5, 6, 7]

# clear: vacía la lista
lista.clear()             # []
```

**Diferencia entre `append` y `extend`:**

```python
lista = [1, 2, 3]

lista.append([4, 5])   # [1, 2, 3, [4, 5]] — añade la lista como un único elemento
lista = [1, 2, 3]
lista.extend([4, 5])   # [1, 2, 3, 4, 5]  — añade cada elemento por separado
```

### 3.1.4. Eliminar elementos (del por índice)

La sentencia `del` elimina elementos de una lista por su índice o por slicing. A diferencia de `remove` (que busca por valor) y `pop` (que elimina y devuelve), `del` trabaja directamente con posiciones y no devuelve nada.

```python
letras = ["a", "b", "c", "d", "e"]

# Eliminar un elemento por índice
del letras[1]
print(letras)  # ["a", "c", "d", "e"]

# Eliminar un rango con slicing
del letras[1:3]
print(letras)  # ["a", "e"]

# Eliminar la lista entera (la variable deja de existir)
del letras
# print(letras)  # NameError: name 'letras' is not defined
```

Comparación rápida de las tres formas de eliminar:

| Método | Busca por | Devuelve | Ejemplo |
|---|---|---|---|
| `del lista[i]` | Índice | Nada | `del lista[0]` |
| `lista.pop(i)` | Índice | El elemento eliminado | `lista.pop(0)` |
| `lista.remove(x)` | Valor | Nada (`None`) | `lista.remove("a")` |

### 3.1.5. Métodos de consulta (index, count)

Los métodos de consulta permiten buscar información dentro de una lista sin modificarla. `index` busca un valor y devuelve su posición (lanza `ValueError` si no existe), y `count` cuenta cuántas veces aparece un valor. Ambos recorren la lista completa, por lo que su coste es proporcional al tamaño de la lista.



```python
frutas = ["manzana", "pera", "manzana", "uva"]

# index: devuelve el índice de la primera ocurrencia — lanza ValueError si no existe
print(frutas.index("pera"))     # 1
print(frutas.index("manzana"))  # 0 — "manzana" está en 0 y en 2, pero index devuelve solo la primera

# count: cuenta cuántas veces aparece un valor
print(frutas.count("manzana"))  # 2
print(frutas.count("kiwi"))     # 0

# len: número de elementos (función built-in, no método)
print(len(frutas))  # 4
```

Para comprobar si un elemento existe sin necesitar su posición, el operador `in` es más directo y legible.

```python
# in: comprobar existencia — O(n)
print("uva" in frutas)   # True
print("kiwi" in frutas)  # False
```

### 3.1.6. Built-ins con iterables (len, max, min, sum)

Python ofrece varias funciones predefinidas que operan sobre iterables (listas, tuplas, sets, strings, etc.). No son métodos de la lista, sino **built-ins** del lenguaje: se llaman pasando la lista como argumento. Funcionan con cualquier iterable, no solo con listas, lo que las hace muy versátiles.

**`len(iterable)`** devuelve el número de elementos. Es una operación O(1) en listas, tuplas, strings, sets y dicts porque Python guarda el tamaño internamente — no recorre los elementos para contarlos.

```python
numeros = [10, 20, 30, 40]
print(len(numeros))     # 4
print(len("hola"))      # 4 — también funciona con strings
print(len([]))          # 0 — lista vacía
```

**`max(iterable)`** y **`min(iterable)`** devuelven el elemento mayor o menor. Por defecto comparan los elementos directamente con los operadores `>` y `<`, por lo que todos deben ser comparables entre sí (no se pueden mezclar números y strings, por ejemplo).

```python
numeros = [3, 1, 4, 1, 5, 9, 2, 6]
print(max(numeros))     # 9
print(min(numeros))     # 1

# También aceptan varios argumentos sueltos en lugar de un iterable
print(max(10, 20, 5))   # 20
print(min(10, 20, 5))   # 5

# Con strings, comparan alfabéticamente (orden Unicode)
palabras = ["pera", "manzana", "uva"]
print(max(palabras))    # "uva" — la "u" viene después en el alfabeto
print(min(palabras))    # "manzana"
```

Si el iterable está vacío, `max` y `min` lanzan `ValueError`. Para evitar el error, ambos aceptan un argumento `default` que se devuelve cuando no hay elementos.

```python
print(max([], default=0))   # 0 — no lanza error
```

**`sum(iterable)`** suma todos los elementos numéricos del iterable. Acepta un segundo argumento opcional que se usa como valor inicial (por defecto es `0`). No funciona con strings — para concatenar strings hay que usar `"".join()`.

```python
numeros = [1, 2, 3, 4, 5]
print(sum(numeros))         # 15
print(sum(numeros, 100))    # 115 — empieza a sumar desde 100

# Con tuplas también funciona
print(sum((10, 20, 30)))    # 60

# Truco: como bool es subtipo de int, sum cuenta valores True
votos = [True, False, True, True]
print(sum(votos))           # 3
```

### 3.1.7. Ordenamiento (sort, sorted, reverse, reversed)

Python ofrece dos formas de ordenar: el método `sort()` y la función `sorted()`. La diferencia clave es que `sort()` modifica la lista original (in-place, devuelve `None`), mientras que `sorted()` crea y devuelve una nueva lista ordenada sin tocar la original. Elegir entre uno u otro depende de si se necesita conservar el orden original.

Ambos aceptan el parámetro `reverse=True` para ordenar de mayor a menor, y el parámetro `key` para definir un criterio de ordenamiento personalizado. `key` recibe una función que se aplica a cada elemento antes de comparar — por ejemplo, `key=len` ordena los elementos por su longitud en lugar de por orden alfabético.

El método `reverse()` es diferente: no ordena, simplemente invierte el orden actual de la lista. Y la built-in `reversed()` invierte sin modificar el original: devuelve un iterador con los elementos en orden inverso, que normalmente se convierte a lista con `list()` o se recorre con un `for`.

```python
numeros = [3, 1, 4, 1, 5, 9, 2]

# sort: ordena in-place, devuelve None
numeros.sort()
print(numeros)  # [1, 1, 2, 3, 4, 5, 9]

numeros.sort(reverse=True)
print(numeros)  # [9, 5, 4, 3, 2, 1, 1]

# sorted: devuelve una nueva lista, el original no cambia
original = [3, 1, 4]
nueva = sorted(original)
print(original)  # [3, 1, 4] — sin cambios
print(nueva)     # [1, 3, 4]

# Ordenar por criterio personalizado con key
# key=len aplica len() a cada elemento y ordena por ese valor
palabras = ["banana", "kiwi", "manzana", "uva"]
palabras.sort(key=len)
print(palabras)  # ["uva", "kiwi", "banana", "manzana"]

# reverse: invierte el orden in-place (no ordena, solo invierte)
lista = [1, 2, 3]
lista.reverse()
print(lista)  # [3, 2, 1]

# reversed: devuelve un iterador con el orden invertido, sin modificar el original
original = [1, 2, 3]
invertida = list(reversed(original))
print(original)   # [1, 2, 3] — sin cambios
print(invertida)  # [3, 2, 1]

# También se puede recorrer directamente con for
for n in reversed([1, 2, 3]):
    print(n)      # 3, 2, 1
```

### 3.1.8. Constructores de colecciones (list, tuple, set, dict)

Los nombres de los tipos `list`, `tuple`, `set` y `dict` se pueden usar también como **funciones built-in** para crear colecciones a partir de otros iterables. Esta es la forma idiomática de convertir entre tipos de colección, eliminar duplicados o crear una colección vacía.

**`list(iterable)`** crea una nueva lista a partir de cualquier iterable. Es la forma habitual de "materializar" iteradores perezosos como `range()`, `reversed()`, `map()` o `filter()`, que no son listas pero sí se pueden recorrer.

```python
print(list("hola"))           # ['h', 'o', 'l', 'a'] — string a lista de caracteres
print(list(range(5)))         # [0, 1, 2, 3, 4]
print(list((1, 2, 3)))        # [1, 2, 3] — tupla a lista
print(list())                 # [] — lista vacía
```

**`tuple(iterable)`** crea una tupla a partir de cualquier iterable. Útil para "congelar" una lista en una versión inmutable que se pueda usar como key de diccionario o elemento de set.

```python
print(tuple([1, 2, 3]))       # (1, 2, 3) — lista a tupla
print(tuple("abc"))           # ('a', 'b', 'c')
print(tuple())                # () — tupla vacía
```

**`set(iterable)`** crea un set a partir de un iterable, eliminando automáticamente los elementos duplicados. Es el patrón estándar para deduplicar una lista en una sola línea.

```python
numeros = [1, 2, 2, 3, 3, 3, 4]
print(set(numeros))           # {1, 2, 3, 4} — duplicados eliminados

# Deduplicar manteniendo el resultado como lista
sin_duplicados = list(set(numeros))
print(sin_duplicados)         # [1, 2, 3, 4] — el orden no está garantizado

print(set())                  # set() — set vacío (no {}, eso es un dict)
```

**`dict(iterable)`** crea un diccionario. Acepta varias formas: una secuencia de pares `(clave, valor)`, otro diccionario, o argumentos por nombre directamente.

```python
# Desde una lista de pares
print(dict([("a", 1), ("b", 2)]))     # {'a': 1, 'b': 2}

# Desde argumentos por nombre
print(dict(nombre="Ana", edad=28))    # {'nombre': 'Ana', 'edad': 28}

# Combinando dos listas con zip()
claves = ["a", "b", "c"]
valores = [1, 2, 3]
print(dict(zip(claves, valores)))     # {'a': 1, 'b': 2, 'c': 3}

print(dict())                         # {} — dict vacío
```

Llamar a estos constructores sin argumentos crea siempre la colección vacía correspondiente. Es una alternativa equivalente a usar los literales `[]`, `()`, `{}`, salvo en el caso del set vacío, donde **hay que usar `set()` obligatoriamente** porque `{}` significa "diccionario vacío", no "set vacío".

### 3.1.9. Copia (shallow vs deep copy)

Asignar una lista a otra variable no crea una copia — ambas variables apuntan al mismo objeto. Modificar una modifica la otra.

```python
a = [1, 2, 3]
b = a           # b apunta al mismo objeto que a
b.append(4)
print(a)        # [1, 2, 3, 4] — a también cambió
```

Para crear una copia independiente se necesita hacerlo explícitamente. La diferencia entre shallow y deep copy aparece con listas anidadas.

**Shallow copy** (copia superficial) — crea un nuevo objeto lista, pero los elementos internos siguen siendo referencias al mismo objeto. Si los elementos son objetos mutables (listas, dicts), una modificación interna se refleja en ambas copias.

```python
import copy

original = [[1, 2], [3, 4]]

# Tres formas de hacer shallow copy
copia1 = original.copy()
copia2 = original[:]
copia3 = list(original)

copia1.append([5, 6])     # no afecta a original — el objeto lista es distinto
original[0].append(99)    # SÍ afecta a copia1 — comparten la sublista [1, 2]

print(original)  # [[1, 2, 99], [3, 4]]
print(copia1)    # [[1, 2, 99], [3, 4], [5, 6]]
```

**Deep copy** (copia profunda) — crea un nuevo objeto y copia recursivamente todos los objetos internos. Las dos copias son completamente independientes.

```python
original = [[1, 2], [3, 4]]
copia_profunda = copy.deepcopy(original)

original[0].append(99)
print(original)       # [[1, 2, 99], [3, 4]]
print(copia_profunda) # [[1, 2], [3, 4]] — no se vio afectada
```

**Regla práctica:** para listas de tipos primitivos (ints, strings, floats), shallow copy es suficiente porque los primitivos son inmutables. Para listas que contienen objetos mutables, usar `deepcopy`.

### 3.1.10. Listas anidadas (matrices)

Una lista puede contener otras listas como elementos. Esto permite representar estructuras bidimensionales como tablas, cuadrículas o matrices. Se accede a los elementos con doble indexación: el primer índice selecciona la fila (la sublista), el segundo selecciona la columna (el elemento dentro de esa sublista).

```python
# Matriz 3x3
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Acceso: matriz[fila][columna]
print(matriz[0])      # [1, 2, 3] — primera fila
print(matriz[0][1])   # 2 — fila 0, columna 1
print(matriz[2][2])   # 9 — fila 2, columna 2

# Modificar un elemento
matriz[1][1] = 99
print(matriz[1])  # [4, 99, 6]

# Recorrer una matriz
for fila in matriz:
    for elemento in fila:
        print(elemento, end=" ")
    print()
```

Un error muy común al crear matrices es usar multiplicación de listas. El problema es que `*` copia las **referencias**, no los objetos, por lo que todas las filas apuntan a la misma lista en memoria:

```python
# MAL: todas las filas son el mismo objeto
matriz = [[0] * 3] * 3
matriz[0][0] = 1
print(matriz)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — las tres filas cambiaron

# BIEN: cada fila es un objeto independiente
matriz = [[0] * 3 for _ in range(3)]
matriz[0][0] = 1
print(matriz)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] — solo cambió la primera fila
```

La multiplicación `[0] * 3` es segura porque `0` es inmutable — no hay referencia compartida que pueda causar problemas. El problema aparece solo cuando se multiplican listas (objetos mutables).

### 3.1.11. List comprehensions (introducción)

Una list comprehension es una forma concisa de crear listas aplicando una expresión a cada elemento de un iterable, con un filtro opcional. Es uno de los patrones más idiomáticos de Python y aparece constantemente en entrevistas.

La sintaxis es: `[expresión for elemento in iterable if condición]`

```python
# Sin comprehension
cuadrados = []
for n in range(1, 6):
    cuadrados.append(n ** 2)

# Con comprehension — equivalente, más conciso
cuadrados = [n ** 2 for n in range(1, 6)]
print(cuadrados)  # [1, 4, 9, 16, 25]

# Con filtro: solo pares
pares = [n for n in range(10) if n % 2 == 0]
print(pares)  # [0, 2, 4, 6, 8]

# Transformar strings
nombres = ["ana", "pedro", "luis"]
mayusculas = [nombre.upper() for nombre in nombres]
print(mayusculas)  # ["ANA", "PEDRO", "LUIS"]
```

Las comprehensions son más legibles y generalmente más rápidas que el bucle equivalente. El tema 6 las cubre en profundidad junto a dict, set y generator comprehensions.

## 3.2. Tuplas

Una tupla es una colección ordenada e **inmutable** de elementos. Sintácticamente es como una lista pero con paréntesis. La inmutabilidad es su característica definitoria: una vez creada, no puede modificarse.

### 3.2.1. Características e inmutabilidad

La inmutabilidad de las tuplas no es solo una restricción — tiene ventajas concretas:

- **Seguridad**: garantiza que los datos no se modifican accidentalmente
- **Rendimiento**: las tuplas son más rápidas que las listas para iterar y acceder
- **Hashables**: al ser inmutables, las tuplas pueden usarse como keys de diccionarios o elementos de sets (las listas no pueden)
- **Semántica**: comunican intención — una tupla indica que esos datos van juntos y no deben cambiar

```python
coordenada = (40.4168, -3.7038)  # latitud y longitud de Madrid

# Intentar modificar lanza TypeError
coordenada[0] = 0  # TypeError: 'tuple' object does not support item assignment

# Las tuplas pueden usarse como keys de dict (las listas no)
ubicaciones = {
    (40.4168, -3.7038): "Madrid",
    (41.3851, 2.1734): "Barcelona"
}
```

### 3.2.2. Creación y acceso

Las tuplas se crean con paréntesis `()` o con la función `tuple()`. Un detalle importante: lo que realmente define una tupla es la **coma**, no los paréntesis. Los paréntesis son opcionales en la mayoría de contextos; la expresión `3, 7` ya es una tupla. Esto tiene una consecuencia que genera muchos errores: para crear una tupla de un solo elemento es obligatorio añadir una coma después del valor — `(42,)` es una tupla, pero `(42)` es simplemente el número 42 entre paréntesis.

El acceso por índice y el slicing funcionan igual que en listas. La diferencia es que no se puede asignar a un índice porque las tuplas son inmutables.

```python
# Creación con paréntesis
punto = (3, 7)
rgb = (255, 128, 0)
vacia = ()

# Los paréntesis son opcionales — la coma es lo que define la tupla
punto = 3, 7        # válido, equivale a (3, 7)

# Tupla de un solo elemento — la coma es obligatoria
solo_uno = (42,)    # tupla con un elemento
no_es_tupla = (42)  # esto es simplemente el entero 42 entre paréntesis

# Desde un iterable
desde_lista = tuple([1, 2, 3])  # (1, 2, 3)
desde_string = tuple("abc")     # ('a', 'b', 'c')

# Acceso — igual que listas
print(rgb[0])   # 255
print(rgb[-1])  # 0
print(rgb[1:])  # (128, 0) — slicing devuelve otra tupla
```

### 3.2.3. Operaciones con tuplas

Las tuplas soportan todas las operaciones que no implican modificación: concatenación (`+`), repetición (`*`), pertenencia (`in`), longitud (`len`) y los métodos `count` e `index`. Estas son las mismas operaciones disponibles en strings y listas, ya que las tres son secuencias.

Las operaciones que generan un resultado nuevo (como concatenar dos tuplas con `+`) devuelven una **nueva tupla** — no modifican las originales, porque no pueden hacerlo.

También es posible convertir entre listas y tuplas con `list()` y `tuple()`. Esto es útil cuando se necesita modificar datos que llegaron como tupla: se convierte a lista, se modifica y se vuelve a convertir.

```python
a = (1, 2, 3)
b = (4, 5, 6)

# Concatenación — crea una nueva tupla
print(a + b)     # (1, 2, 3, 4, 5, 6)

# Repetición
print(a * 2)     # (1, 2, 3, 1, 2, 3)

# Pertenencia
print(2 in a)    # True

# Longitud
print(len(a))    # 3

# Métodos disponibles (solo los que no modifican)
print(a.count(2))   # 1
print(a.index(3))   # 2

# Conversión entre lista y tupla
lista = list(a)     # [1, 2, 3] — para poder modificar
tupla = tuple(lista)  # (1, 2, 3) — para volver a inmutable
```

### 3.2.4. Desempaquetado (unpacking)

El unpacking es una de las características más útiles de las tuplas y uno de los patrones más idiomáticos de Python. Permite asignar los elementos de una tupla a variables individuales en una sola línea.

```python
punto = (3, 7)
x, y = punto
print(x)  # 3
print(y)  # 7

# Funciona con cualquier iterable, no solo tuplas
nombre, apellido, edad = ["Ana", "García", 28]

# Intercambio de variables sin temporal — usa unpacking internamente
a, b = 1, 2
a, b = b, a
print(a, b)  # 2 1

# Unpacking con * para capturar el resto
primero, *resto = (1, 2, 3, 4, 5)
print(primero)  # 1
print(resto)    # [2, 3, 4, 5] — siempre devuelve lista

*inicio, ultimo = (1, 2, 3, 4, 5)
print(inicio)   # [1, 2, 3, 4]
print(ultimo)   # 5

primero, *medio, ultimo = (1, 2, 3, 4, 5)
print(medio)    # [2, 3, 4]

# Unpacking en bucles — muy común con listas de tuplas
coordenadas = [(0, 0), (1, 2), (3, 4)]
for x, y in coordenadas:
    print(f"x={x}, y={y}")
```

### 3.2.5. Named tuples

Una named tuple es una tupla cuyos elementos tienen nombre además de posición. Permite acceder a los valores por nombre (`punto.x`) o por índice (`punto[0]`), combinando la legibilidad de un objeto con la eficiencia y la inmutabilidad de una tupla.

```python
from collections import namedtuple

# Definición: nombre de la clase y nombres de los campos
Punto = namedtuple("Punto", ["x", "y"])
Color = namedtuple("Color", ["rojo", "verde", "azul"])

# Creación de instancias
p = Punto(3, 7)
rojo = Color(255, 0, 0)

# Acceso por nombre (más legible) o por índice (compatible con tuplas)
print(p.x)      # 3
print(p[0])     # 3 — mismo valor, acceso por índice
print(rojo.verde)  # 0

# Son tuplas reales — soportan unpacking, iteración, etc.
x, y = p
print(x, y)  # 3 7

# _asdict: convierte a diccionario
print(p._asdict())  # {'x': 3, 'y': 7}

# _replace: crea una nueva instancia con algún campo modificado (no modifica la original)
p2 = p._replace(x=10)
print(p)   # Punto(x=3, y=7)  — sin cambios
print(p2)  # Punto(x=10, y=7)
```

Las named tuples son útiles para representar registros simples de datos cuando no se necesita lógica adicional. Para casos más complejos con validación o métodos, se usan dataclasses (tema 16).
