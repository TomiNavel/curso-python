# Preguntas de entrevista: Diccionarios y Sets

1. ¿Por qué el acceso a un diccionario es O(1)? ¿Qué estructura interna lo permite?
2. ¿Qué tipos de datos pueden ser claves de un diccionario y cuáles no? ¿Por qué?
3. ¿Cuál es la diferencia entre acceder a una clave con `dict[clave]` y con `dict.get(clave)`?
4. ¿Qué devuelven `keys()`, `values()` e `items()`? ¿Son listas?
5. ¿Cuál es la diferencia entre `del dict[clave]` y `dict.pop(clave)`?
6. ¿Para qué sirve `setdefault()` y en qué se diferencia de `get()`?
7. ¿Qué ocurre si se usa `update()` con claves que ya existen en el diccionario?
8. ¿Qué es un `Counter` y para qué se usa?
9. ¿Qué es un set y qué garantía ofrece sobre sus elementos?
10. ¿Por qué `{}` crea un diccionario vacío y no un set vacío?
11. ¿Cuál es la diferencia entre `remove` y `discard` en un set?
12. ¿Qué operaciones de conjuntos soportan los sets y para qué sirve cada una?
13. ¿Qué es un `frozenset` y cuándo se necesita?
14. ¿Puede un diccionario contener otro diccionario como valor? ¿Y como clave?

---

### R1. ¿Por qué el acceso a un diccionario es O(1)? ¿Qué estructura interna lo permite?

Un diccionario usa internamente una **hash table**. Cuando se inserta un par clave-valor, Python calcula el hash de la clave (un número entero) y usa ese número para determinar en qué posición de memoria almacenar el par. Al acceder, calcula el hash de nuevo y va directamente a esa posición sin recorrer nada.

Esto hace que el acceso, inserción y eliminación sean O(1) en promedio, independientemente del tamaño del diccionario. En el peor caso (muchas colisiones de hash) puede degradarse a O(n), pero en la práctica es extremadamente raro.

### R2. ¿Qué tipos de datos pueden ser claves de un diccionario y cuáles no? ¿Por qué?

Solo los objetos **hashables** pueden ser claves. Un objeto es hashable si tiene un hash que no cambia durante su vida (implementa `__hash__`) y puede compararse con otros objetos (implementa `__eq__`).

Los tipos inmutables son hashables: `str`, `int`, `float`, `bool`, `tuple` (si todos sus elementos también son inmutables), `frozenset`. Los tipos mutables no lo son: `list`, `dict`, `set`. La razón es que si una clave pudiera cambiar después de insertarse, su hash cambiaría y el diccionario no podría encontrarla en la posición donde la almacenó.

```python
d = {}
d["texto"] = 1          # str — válido
d[42] = 2                # int — válido
d[(1, 2)] = 3            # tuple de inmutables — válido
# d[[1, 2]] = 4          # list — TypeError: unhashable type
# d[{1, 2}] = 5          # set — TypeError: unhashable type
d[frozenset({1, 2})] = 6 # frozenset — válido
```

### R3. ¿Cuál es la diferencia entre acceder a una clave con `dict[clave]` y con `dict.get(clave)`?

`dict[clave]` lanza `KeyError` si la clave no existe. `dict.get(clave)` devuelve `None` si no existe, o un valor por defecto si se le pasa como segundo argumento.

```python
usuario = {"nombre": "Ana"}

print(usuario["nombre"])          # "Ana"
# print(usuario["email"])         # KeyError: 'email'

print(usuario.get("nombre"))      # "Ana"
print(usuario.get("email"))       # None
print(usuario.get("email", "N/A")) # "N/A"
```

Se usa `[]` cuando la ausencia de la clave es un error lógico (debería existir). Se usa `get()` cuando la ausencia es un caso esperado.

### R4. ¿Qué devuelven `keys()`, `values()` e `items()`? ¿Son listas?

No son listas. Devuelven **vistas dinámicas** (`dict_keys`, `dict_values`, `dict_items`). La diferencia con una lista es que estas vistas no son copias estáticas: si el diccionario cambia después de obtener la vista, la vista refleja el cambio automáticamente.

```python
d = {"a": 1, "b": 2}
claves = d.keys()
print(claves)       # dict_keys(['a', 'b'])

d["c"] = 3
print(claves)       # dict_keys(['a', 'b', 'c']) — refleja el cambio
```

Si se necesita una lista real (por ejemplo, para indexar por posición), hay que convertir explícitamente con `list()`.

### R5. ¿Cuál es la diferencia entre `del dict[clave]` y `dict.pop(clave)`?

Ambos eliminan un par clave-valor. La diferencia es que `pop()` **devuelve el valor** eliminado, mientras que `del` no devuelve nada. Además, `pop()` acepta un valor por defecto para evitar `KeyError` si la clave no existe, mientras que `del` siempre lanza `KeyError` si no existe.

```python
d = {"a": 1, "b": 2, "c": 3}

del d["a"]                    # elimina, no devuelve nada
valor = d.pop("b")            # elimina y devuelve 2
seguro = d.pop("z", "default") # devuelve "default", sin error
# del d["z"]                  # KeyError
```

### R6. ¿Para qué sirve `setdefault()` y en qué se diferencia de `get()`?

Ambos devuelven el valor de una clave si existe, y un valor por defecto si no existe. La diferencia es que `setdefault()` **también inserta** la clave con el valor por defecto en el diccionario cuando no existe, mientras que `get()` no modifica el diccionario.

```python
d = {"a": 1}

# get: no modifica el diccionario
d.get("b", 0)
print(d)           # {"a": 1} — "b" no se añadió

# setdefault: inserta la clave si no existe
d.setdefault("b", 0)
print(d)           # {"a": 1, "b": 0} — "b" se añadió
```

### R7. ¿Qué ocurre si se usa `update()` con claves que ya existen en el diccionario?

Los valores existentes se **sobreescriben** con los valores del diccionario pasado a `update()`. Las claves que no existían se añaden. No se lanza ningún error.

```python
config = {"host": "localhost", "puerto": 5432}
config.update({"puerto": 3306, "db": "test"})
print(config)  # {'host': 'localhost', 'puerto': 3306, 'db': 'test'}
# "puerto" se sobreescribió, "db" se añadió, "host" no se tocó
```

El operador `|` (Python 3.9+) hace lo mismo pero crea un diccionario nuevo en lugar de modificar el existente.

### R8. ¿Qué es un `Counter` y para qué se usa?

`Counter` es una subclase de `dict` del módulo `collections` especializada en contar ocurrencias. Recibe un iterable y devuelve un diccionario donde las claves son los elementos y los valores sus conteos.

```python
from collections import Counter

letras = Counter("mississippi")
print(letras)              # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
print(letras.most_common(2))  # [('i', 4), ('s', 4)]
print(letras["s"])         # 4
print(letras["z"])         # 0 — no lanza KeyError
```

A diferencia de un `dict` normal, acceder a una clave inexistente en un `Counter` devuelve `0` en lugar de lanzar `KeyError`.

### R9. ¿Qué es un set y qué garantía ofrece sobre sus elementos?

Un set es una colección **no ordenada** de elementos **únicos**. Garantiza que no puede haber duplicados: añadir un elemento que ya existe no tiene efecto. Internamente usa una hash table, igual que los diccionarios, lo que le da búsqueda, inserción y eliminación en O(1).

Los elementos de un set deben ser hashables (misma restricción que las claves de un diccionario). No se puede acceder a un elemento por índice porque los sets no tienen orden.

### R10. ¿Por qué `{}` crea un diccionario vacío y no un set vacío?

Porque la sintaxis `{}` existía en Python antes que los sets. Históricamente `{}` siempre representó un diccionario vacío, y cuando se añadieron los sets al lenguaje se mantuvo esa convención por compatibilidad.

Para crear un set vacío es obligatorio usar `set()`. Sin embargo, `{1, 2, 3}` (con elementos) sí crea un set, porque Python distingue `{clave: valor}` (diccionario) de `{valor}` (set).

```python
print(type({}))        # <class 'dict'>
print(type(set()))     # <class 'set'>
print(type({1, 2}))    # <class 'set'>
print(type({"a": 1}))  # <class 'dict'>
```

### R11. ¿Cuál es la diferencia entre `remove` y `discard` en un set?

Ambos eliminan un elemento del set. La diferencia es el comportamiento cuando el elemento no existe: `remove` lanza `KeyError`, mientras que `discard` no hace nada (silencioso).

Se usa `remove` cuando la ausencia del elemento indica un error lógico en el programa. Se usa `discard` cuando la eliminación es opcional y no importa si el elemento ya no estaba.

```python
s = {1, 2, 3}
s.remove(2)       # elimina 2
# s.remove(99)    # KeyError

s.discard(3)      # elimina 3
s.discard(99)     # no hace nada, sin error
```

### R12. ¿Qué operaciones de conjuntos soportan los sets y para qué sirve cada una?

- **Unión** (`a | b` o `a.union(b)`): todos los elementos de ambos conjuntos.
- **Intersección** (`a & b` o `a.intersection(b)`): solo los elementos comunes.
- **Diferencia** (`a - b` o `a.difference(b)`): elementos en `a` que no están en `b`.
- **Diferencia simétrica** (`a ^ b` o `a.symmetric_difference(b)`): elementos que están en uno pero no en ambos.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # {1, 2, 3, 4, 5, 6}
print(a & b)   # {3, 4}
print(a - b)   # {1, 2}
print(a ^ b)   # {1, 2, 5, 6}
```

Además, `issubset`, `issuperset` e `isdisjoint` permiten comprobar relaciones entre conjuntos.

### R13. ¿Qué es un `frozenset` y cuándo se necesita?

`frozenset` es la versión **inmutable** de un set. No se puede añadir ni eliminar elementos después de crearlo. A cambio, es hashable, lo que permite usarlo como clave de un diccionario o como elemento de otro set — situaciones donde un set normal no funcionaría.

```python
fs = frozenset([1, 2, 3])

# Puede ser clave de diccionario
permisos = {
    frozenset(["lectura"]): "usuario",
    frozenset(["lectura", "escritura"]): "editor",
}

# Soporta operaciones de conjuntos
print(fs | frozenset({4}))  # frozenset({1, 2, 3, 4})

# No soporta modificación
# fs.add(4)  # AttributeError
```

### R14. ¿Puede un diccionario contener otro diccionario como valor? ¿Y como clave?

Como **valor**, sí. Los valores de un diccionario pueden ser cualquier objeto de Python, incluidos otros diccionarios. Esto permite crear estructuras anidadas.

Como **clave**, no. Los diccionarios son mutables y por lo tanto no son hashables. No pueden usarse como claves.

```python
# Como valor — válido
usuarios = {
    "ana": {"edad": 28, "ciudad": "Madrid"},
    "carlos": {"edad": 35, "ciudad": "Barcelona"},
}
print(usuarios["ana"]["ciudad"])  # "Madrid"

# Como clave — inválido
# d = {{"a": 1}: "valor"}  # TypeError: unhashable type: 'dict'
```
