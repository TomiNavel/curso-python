# Errores comunes: Diccionarios y Sets

## Error 1: Acceder a una clave inexistente con corchetes

Usar `dict[clave]` cuando la clave no existe lanza `KeyError`. Es uno de los errores más frecuentes, especialmente al trabajar con datos que provienen de fuentes externas donde no se garantiza la presencia de todas las claves.

```python
usuario = {"nombre": "Ana", "edad": 28}

# MAL — lanza KeyError si la clave no existe
print(usuario["email"])  # KeyError: 'email'

# BIEN — usar get() para acceso seguro
print(usuario.get("email"))          # None
print(usuario.get("email", "N/A"))   # "N/A"
```

## Error 2: Usar una lista como clave de diccionario

Las listas son mutables y por lo tanto no son hashables. Intentar usarlas como clave lanza `TypeError`. El mismo problema ocurre con sets y otros diccionarios.

```python
# MAL — las listas no son hashables
coordenadas = {}
coordenadas[[0, 0]] = "origen"  # TypeError: unhashable type: 'list'

# BIEN — usar una tupla (inmutable, hashable)
coordenadas = {}
coordenadas[(0, 0)] = "origen"  # correcto
```

## Error 3: Confundir `{}` con un set vacío

`{}` crea un diccionario vacío, no un set vacío. Es una trampa sintáctica que causa errores silenciosos: el código no falla, pero el tipo de dato es incorrecto.

```python
# MAL — esto es un dict, no un set
vacio = {}
print(type(vacio))  # <class 'dict'>

# BIEN — set vacío se crea con set()
vacio = set()
print(type(vacio))  # <class 'set'>
```

## Error 4: Asumir que `update()` conserva los valores originales

`update()` sobreescribe los valores de las claves que ya existen. No fusiona valores ni lanza error por colisión. Si se necesita conservar el valor original ante colisiones, hay que comprobarlo manualmente.

```python
config = {"puerto": 5432, "host": "localhost"}

# MAL — se pierde el valor original de "puerto" sin aviso
config.update({"puerto": 3306})
print(config["puerto"])  # 3306 — sobreescrito

# BIEN — comprobar antes si se quiere conservar el original
config = {"puerto": 5432, "host": "localhost"}
nuevos = {"puerto": 3306, "db": "test"}
for clave, valor in nuevos.items():
    config.setdefault(clave, valor)  # solo inserta si no existe
print(config["puerto"])  # 5432 — conservado
```

## Error 5: Asumir que `pop()` sin argumento funciona en diccionarios

En listas, `pop()` sin argumentos elimina el último elemento. En diccionarios, `pop()` **requiere obligatoriamente una clave** como argumento. Sin ella, lanza `TypeError`.

```python
d = {"a": 1, "b": 2}

# MAL — pop() sin argumento no funciona en dicts
# d.pop()  # TypeError: pop expected at least 1 argument, got 0

# BIEN — especificar la clave
valor = d.pop("a")       # devuelve 1, elimina "a"
valor = d.pop("z", None) # devuelve None si no existe
```

Nota: `popitem()` (sin argumentos) existe y elimina el último par insertado, pero es un método diferente.

## Error 6: Olvidar que las vistas de diccionario son dinámicas

`keys()`, `values()` e `items()` devuelven vistas que reflejan el estado actual del diccionario en todo momento. Si el diccionario cambia después de obtener la vista, la vista también cambia. Esto puede causar resultados inesperados si se asume que la vista es una copia estática.

```python
d = {"a": 1, "b": 2}
claves = d.keys()
print(claves)   # dict_keys(['a', 'b'])

d["c"] = 3
print(claves)   # dict_keys(['a', 'b', 'c']) — cambió sin reasignar

# Si se necesita una copia estática, convertir a lista
claves_fijas = list(d.keys())
d["d"] = 4
print(claves_fijas)  # ['a', 'b', 'c'] — no cambió
```

## Error 7: Añadir elementos no hashables a un set

Los sets usan hash table internamente, igual que las claves de un diccionario. Solo pueden contener elementos hashables. Intentar añadir una lista o un diccionario lanza `TypeError`.

```python
# MAL — las listas no son hashables
s = set()
s.add([1, 2, 3])  # TypeError: unhashable type: 'list'

# BIEN — usar tupla (inmutable, hashable)
s = set()
s.add((1, 2, 3))  # correcto

# BIEN — usar frozenset para conjuntos dentro de conjuntos
s = set()
s.add(frozenset({1, 2}))  # correcto
```

## Error 8: Esperar orden en un set

Los sets no tienen orden. No se puede acceder por índice, y el orden en que se imprimen los elementos puede variar entre ejecuciones. Asumir un orden concreto causa bugs sutiles.

```python
s = {3, 1, 4, 1, 5, 9}
print(s)     # {1, 3, 4, 5, 9} — el orden puede variar
# print(s[0])  # TypeError: 'set' object is not subscriptable

# Si se necesita orden, convertir a lista ordenada
ordenado = sorted(s)
print(ordenado)     # [1, 3, 4, 5, 9]
print(ordenado[0])  # 1
```

## Error 9: Confundir `remove` con `discard` en sets

`remove` lanza `KeyError` si el elemento no existe, mientras que `discard` no. Usar `remove` sin estar seguro de que el elemento existe causa errores en tiempo de ejecución.

```python
s = {1, 2, 3}

# MAL — lanza error si el elemento no existe
# s.remove(99)  # KeyError: 99

# BIEN — discard no lanza error
s.discard(99)  # silencioso

# BIEN — comprobar existencia antes de remove
if 99 in s:
    s.remove(99)
```

La regla: `remove` cuando la ausencia es un error lógico, `discard` cuando es un caso esperado.

## Error 10: Modificar un diccionario anidado creyendo que es una copia

Al igual que con las listas, asignar un diccionario a otra variable no crea una copia. Ambas variables apuntan al mismo objeto. Modificar a través de una afecta a la otra.

```python
original = {"config": {"puerto": 5432}}

# MAL — no es una copia, es la misma referencia
copia = original
copia["config"]["puerto"] = 3306
print(original["config"]["puerto"])  # 3306 — modificado

# BIEN — copia superficial con copy()
import copy
original = {"config": {"puerto": 5432}}
copia = original.copy()
copia["config"]["puerto"] = 3306
print(original["config"]["puerto"])  # 3306 — copy() es superficial, no copia los internos

# BIEN — copia profunda con deepcopy()
original = {"config": {"puerto": 5432}}
copia = copy.deepcopy(original)
copia["config"]["puerto"] = 3306
print(original["config"]["puerto"])  # 5432 — independiente
```
