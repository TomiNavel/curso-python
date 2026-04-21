# Cheat Sheet: Fundamentos de Python (Temas 1-6)

## 1. Tipos de datos y variables

| Tipo | Ejemplo | Mutable | Hashable |
|---------|-----------------|---------|----------|
| int | `42` | No | Si |
| float | `3.14` | No | Si |
| complex | `2 + 3j` | No | Si |
| bool | `True` / `False`| No | Si |
| str | `"hola"` | No | Si |
| list | `[1, 2, 3]` | Si | No |
| tuple | `(1, 2, 3)` | No | Si |
| set | `{1, 2, 3}` | Si | No |
| frozenset| `frozenset({1})`| No | Si |
| dict | `{"a": 1}` | Si | No |
| None | `None` | - | Si |

```python
# Asignacion
x = 10
a, b, c = 1, 2, 3
a = b = c = 0

# Constantes (convencion, no son realmente constantes)
MAX_INTENTOS = 3

# Conversion de tipos
int("42")       # 42
float("3.14")   # 3.14
str(100)        # "100"
bool(0)         # False
bool("")        # False
bool([])        # False
```

**Valores falsy:** `False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`

## 2. Operadores

```python
# Aritmeticos
+  -  *  /       # suma, resta, multiplicacion, division (siempre float)
//               # division entera
%                # modulo (resto)
**               # potencia

# Asignacion compuesta
x += 1    # x = x + 1
x -= 2    # x = x - 2
x *= 3    # x = x * 3
x //= 2   # x = x // 2

# Comparacion (se pueden encadenar)
==  !=  <  >  <=  >=
18 <= edad < 65          # encadenamiento

# Logicos (cortocircuito)
and    or    not
x = a or "default"       # valor por defecto si a es falsy

# Identidad (comparar con None o singletons)
x is None
x is not None

# Pertenencia
"a" in "hola"            # True
5 in [1, 2, 3]           # False
"key" in diccionario     # busca en keys
```

## 3. Strings

```python
# Creacion
s = "texto"
s = 'texto'
s = """texto
multilinea"""
s = r"C:\ruta\sin\escape"   # raw string

# Indexing y slicing
s[0]          # primer caracter
s[-1]         # ultimo caracter
s[1:4]        # desde indice 1 hasta 3
s[::-1]       # invertir string

# Concatenacion
"hola" + " " + "mundo"
"ja" * 3                    # "jajaja"
```

### Metodos de strings

```python
# Transformacion (devuelven nuevo string)
s.upper()          s.lower()          s.capitalize()
s.title()          s.strip()          s.lstrip()
s.rstrip()         s.replace(old, new)

# Busqueda
s.find("x")        # indice o -1
s.index("x")       # indice o ValueError
s.count("x")       # cantidad de ocurrencias
s.startswith("ab")  s.endswith("yz")

# Validacion
s.isdigit()    s.isalpha()    s.isalnum()    s.isspace()

# Division y union
s.split(",")                 # divide por separador -> lista
",".join(["a", "b", "c"])   # une lista -> string
s.partition(",")             # (antes, sep, despues)
```

### f-strings

```python
nombre = "Ana"
precio = 49.5

f"Hola {nombre}"                 # interpolacion basica
f"Precio: {precio:.2f}"         # 2 decimales -> "49.50"
f"Total: {precio:>10.2f}"       # alineado derecha, 10 chars
f"Numero: {42:05d}"             # ceros a la izquierda -> "00042"
f"Debug: {nombre=}"             # "nombre='Ana'" (Python 3.8+)
f"{'texto':^20}"                # centrado en 20 chars
f"{'texto':<20}"                # alineado izquierda
f"{'texto':>20}"                # alineado derecha
```

## 4. Listas

```python
# Creacion
lista = [1, 2, 3]
lista = list(range(5))          # [0, 1, 2, 3, 4]

# Acceso y slicing (igual que strings)
lista[0]      lista[-1]      lista[1:3]      lista[::-1]
```

### Metodos de listas

```python
# Agregar
lista.append(x)          # agrega al final
lista.insert(i, x)       # agrega en posicion i
lista.extend([4, 5])     # agrega varios elementos

# Eliminar
lista.remove(x)          # elimina primera ocurrencia (ValueError si no existe)
lista.pop()              # elimina y devuelve el ultimo
lista.pop(i)             # elimina y devuelve el de posicion i
lista.clear()            # vacia la lista
del lista[i]             # elimina por indice

# Consulta
lista.index(x)           # indice de primera ocurrencia
lista.count(x)           # cantidad de ocurrencias

# Ordenar
lista.sort()                          # in-place, ascendente
lista.sort(reverse=True)              # in-place, descendente
lista.sort(key=len)                   # in-place, por criterio
nueva = sorted(lista)                 # nueva lista ordenada
lista.reverse()                       # invierte in-place

# Copia
copia = lista.copy()                  # shallow copy (o lista[:])
import copy
copia = copy.deepcopy(lista)          # deep copy (listas anidadas)
```

## 5. Tuplas

```python
# Creacion (parentesis opcionales, la coma define la tupla)
t = (1, 2, 3)
t = 1, 2, 3
t = (42,)                # tupla de un elemento (coma obligatoria)

# Inmutables: no se pueden modificar despues de crearse
# Hashables: pueden ser keys de dict o elementos de set

# Desempaquetado
x, y = (10, 20)
primero, *resto = (1, 2, 3, 4)       # primero=1, resto=[2, 3, 4]
a, *medio, b = (1, 2, 3, 4, 5)       # a=1, medio=[2, 3, 4], b=5
_, y = (10, 20)                       # ignorar valores con _

# Named tuples
from collections import namedtuple
Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 7)
p.x    # 3 (acceso por nombre)
p[0]   # 3 (acceso por indice)
```

## 6. Diccionarios

```python
# Creacion
d = {"nombre": "Ana", "edad": 25}
d = dict(nombre="Ana", edad=25)
d = dict(zip(claves, valores))

# Acceso
d["nombre"]              # "Ana" (KeyError si no existe)
d.get("nombre")          # "Ana" (None si no existe)
d.get("x", "default")   # "default" si no existe

# Modificar
d["edad"] = 26           # actualizar o crear
d.update({"a": 1})       # actualizar varios
d.setdefault("k", 0)    # asigna solo si la key no existe
d1 | d2                  # merge (Python 3.9+, d2 prevalece)

# Eliminar
d.pop("key")             # elimina y devuelve valor
d.pop("key", None)       # sin error si no existe
del d["key"]             # elimina (KeyError si no existe)

# Iterar
d.keys()       # vista de claves
d.values()     # vista de valores
d.items()      # vista de pares (clave, valor)

# Solo keys hashables: str, int, float, bool, tuple, frozenset
# "in" busca en keys: "nombre" in d  -> True
```

### Counter y defaultdict

```python
from collections import Counter
c = Counter(["a", "b", "a", "c", "a"])   # Counter({'a': 3, 'b': 1, 'c': 1})
c.most_common(2)                          # [('a', 3), ('b', 1)]

from collections import defaultdict
dd = defaultdict(list)
dd["grupo"].append("Ana")                 # no necesita inicializar la key
```

## 7. Sets

```python
# Creacion
s = {1, 2, 3}
s = set()                # vacio (no {}, eso es dict)

# Elementos unicos, no ordenados, O(1) para busqueda

# Metodos
s.add(x)                 # agregar
s.remove(x)              # eliminar (KeyError si no existe)
s.discard(x)             # eliminar (sin error si no existe)
s.pop()                  # eliminar y devolver uno arbitrario

# Operaciones de conjuntos
a | b     a.union(b)                # union
a & b     a.intersection(b)         # interseccion
a - b     a.difference(b)           # diferencia
a ^ b     a.symmetric_difference(b) # diferencia simetrica

# Comparacion
a.issubset(b)            # a es subconjunto de b
a.issuperset(b)          # a contiene a b
a.isdisjoint(b)          # no tienen elementos en comun

# frozenset: set inmutable, puede ser key de dict
fs = frozenset({1, 2, 3})
```

## 8. Control de flujo

```python
# if / elif / else
if condicion:
    ...
elif otra:
    ...
else:
    ...

# Operador ternario
resultado = "par" if x % 2 == 0 else "impar"

# Walrus operator (Python 3.8+)
if (n := len(datos)) > 10:
    print(f"Demasiados: {n}")

# match / case (Python 3.10+)
match comando:
    case "salir":
        ...
    case "ayuda":
        ...
    case _:
        ...
```

### Bucles

```python
# for (iterar directamente, NO por indice)
for elemento in lista:
    ...

# while
while condicion:
    ...

# break: sale del bucle
# continue: salta a la siguiente iteracion
# pass: no hace nada (placeholder)

# else en bucles: se ejecuta si NO hubo break
for x in lista:
    if x == objetivo:
        break
else:
    print("No encontrado")
```

### Funciones de iteracion

```python
# range(start, stop, step) - lazy, O(1) memoria
range(5)           # 0, 1, 2, 3, 4
range(2, 8)        # 2, 3, 4, 5, 6, 7
range(0, 10, 2)    # 0, 2, 4, 6, 8

# enumerate - indice + valor
for i, val in enumerate(lista):           # i desde 0
for i, val in enumerate(lista, start=1):  # i desde 1

# zip - combinar iterables en paralelo
for nombre, edad in zip(nombres, edades):
    ...
```

## 9. Comprehensions

```python
# List comprehension
[x ** 2 for x in range(10)]                      # transformar todos
[x for x in range(10) if x % 2 == 0]             # filtrar
[x if x > 0 else 0 for x in datos]               # if/else (transforma todos)

# Dict comprehension
{k: v for k, v in pares}
{v: k for k, v in diccionario.items()}            # invertir dict
{k: v for k, v in d.items() if v > 0}             # filtrar

# Set comprehension
{x.lower() for x in palabras}                     # auto-deduplica

# Generator expression (lazy, no carga en memoria)
gen = (x ** 2 for x in range(1_000_000))
sum(x ** 2 for x in range(10))                    # sin parentesis extra

# Funciones que consumen generadores
sum(...)     max(...)     min(...)     any(...)     all(...)
```

### Cuando usar cada uno

| Necesitas... | Usa |
|---|---|
| Lista con todos los resultados | List comprehension |
| Diccionario transformado | Dict comprehension |
| Elementos unicos | Set comprehension |
| Procesar uno a uno (memoria) | Generator expression |
| Logica compleja (>1 linea) | Bucle for normal |
