# Preguntas de entrevista: Listas y Tuplas

1. ¿Cuál es la diferencia fundamental entre una lista y una tupla?
2. ¿Qué devuelve `lista.append(4)`? ¿Y `sorted(lista)`? ¿Por qué son diferentes?
3. ¿Cuál es la diferencia entre `append` y `extend`?
4. ¿Qué ocurre si se modifica una lista mientras se itera sobre ella con un bucle `for`?
5. ¿Qué diferencia hay entre `sort()` y `sorted()`?
6. ¿Qué es una shallow copy y en qué se diferencia de una deep copy?
7. ¿Por qué `b = a` no crea una copia independiente de la lista?
8. ¿Qué pasa si se ejecuta `[[0]] * 3` y se modifica uno de los elementos internos?
9. ¿Cómo se crea una tupla de un solo elemento? ¿Por qué `(42)` no es una tupla?
10. ¿Puede una tupla contener objetos mutables? Si es así, ¿se pueden modificar?
11. ¿Qué es el unpacking y para qué se usa?
12. ¿Cuándo conviene usar una tupla en lugar de una lista?
13. ¿Qué es una named tuple y qué ventajas tiene sobre una tupla normal?
14. ¿Qué diferencia hay entre `remove`, `pop` y `del` para eliminar elementos de una lista?

---

### R1. ¿Cuál es la diferencia fundamental entre una lista y una tupla?

Las listas son **mutables** (se pueden modificar después de crearlas) y las tuplas son **inmutables** (no se pueden modificar). Esto tiene consecuencias prácticas: las listas tienen métodos de modificación (`append`, `sort`, `remove`...) que las tuplas no tienen, y las tuplas pueden usarse como claves de diccionarios o elementos de sets porque son hashables.

A nivel semántico, las listas representan colecciones homogéneas que pueden crecer o cambiar, mientras que las tuplas representan agrupaciones fijas de datos relacionados (como coordenadas o registros).

### R2. ¿Qué devuelve `lista.append(4)`? ¿Y `sorted(lista)`? ¿Por qué son diferentes?

`lista.append(4)` devuelve `None` porque modifica la lista original directamente (in-place). `sorted(lista)` devuelve una **nueva lista** ordenada sin modificar la original.

La diferencia es que los métodos in-place de las listas (`append`, `sort`, `reverse`, etc.) alteran el objeto existente y no necesitan devolver nada. Las funciones como `sorted` crean un objeto nuevo, así que lo devuelven para que pueda asignarse a una variable.

El error más común es escribir `lista = lista.append(4)`, que asigna `None` a `lista` y se pierde la referencia original.

### R3. ¿Cuál es la diferencia entre `append` y `extend`?

`append` añade su argumento como un único elemento al final de la lista. Si se le pasa una lista, la añade como elemento anidado. `extend` recibe un iterable y añade cada uno de sus elementos individualmente.

```python
a = [1, 2]
a.append([3, 4])   # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])   # [1, 2, 3, 4]
```

`extend` es equivalente a `+=` con listas.

### R4. ¿Qué ocurre si se modifica una lista mientras se itera sobre ella con un bucle `for`?

El iterador interno del `for` usa índices para recorrer la lista. Si se eliminan elementos durante la iteración, los índices se desplazan y el iterador salta elementos. Si se añaden elementos, puede causar iteraciones extra o un bucle infinito.

La solución es iterar sobre una copia (`lista[:]`) o construir una nueva lista con una list comprehension.

### R5. ¿Qué diferencia hay entre `sort()` y `sorted()`?

`sort()` es un método de lista que ordena **in-place** (modifica la lista original y devuelve `None`). `sorted()` es una función built-in que devuelve una **nueva lista** ordenada sin modificar la original.

Se usa `sort()` cuando no se necesita conservar el orden original. Se usa `sorted()` cuando se necesita el original intacto o cuando se quiere ordenar un iterable que no es lista (como una tupla o un generador).

Ambos aceptan los parámetros `key` (criterio de ordenamiento) y `reverse` (orden descendente).

### R6. ¿Qué es una shallow copy y en qué se diferencia de una deep copy?

Una **shallow copy** (copia superficial) crea un nuevo objeto lista, pero los elementos internos siguen siendo referencias a los mismos objetos. Si los elementos son inmutables (números, strings), no hay problema. Pero si contiene objetos mutables (como sublistas), modificar uno a través de la copia afecta también al original.

Una **deep copy** (copia profunda) crea un nuevo objeto y copia recursivamente todos los objetos internos. Las dos copias son completamente independientes.

```python
import copy
original = [[1, 2], [3, 4]]

shallow = original.copy()
deep = copy.deepcopy(original)

original[0].append(99)
print(shallow[0])  # [1, 2, 99] — afectada
print(deep[0])     # [1, 2]     — independiente
```

### R7. ¿Por qué `b = a` no crea una copia independiente de la lista?

En Python, las variables son **referencias** a objetos, no contenedores de valores. Cuando se escribe `b = a`, ambas variables apuntan al mismo objeto lista en memoria. No se crea un objeto nuevo. Cualquier modificación a través de `a` o `b` afecta al mismo objeto.

Para crear una copia independiente se necesita hacerlo explícitamente con `a.copy()`, `a[:]`, `list(a)` o `copy.deepcopy(a)` según el caso.

### R8. ¿Qué pasa si se ejecuta `[[0]] * 3` y se modifica uno de los elementos internos?

Las tres sublistas son el mismo objeto en memoria. Modificar una modifica todas.

```python
matriz = [[0]] * 3
matriz[0][0] = 1
print(matriz)  # [[1], [1], [1]]
```

El operador `*` copia las **referencias**, no los objetos. Las tres posiciones de la lista exterior apuntan a la misma sublista. La solución es usar una comprehension para crear objetos independientes: `[[0] for _ in range(3)]`.

### R9. ¿Cómo se crea una tupla de un solo elemento? ¿Por qué `(42)` no es una tupla?

Se crea con una coma después del valor: `(42,)` o simplemente `42,`. Lo que define una tupla es la **coma**, no los paréntesis. `(42)` es el número 42 entre paréntesis de agrupación, igual que en una expresión matemática como `(2 + 3)`.

```python
print(type((42)))   # <class 'int'>
print(type((42,)))  # <class 'tuple'>
```

### R10. ¿Puede una tupla contener objetos mutables? Si es así, ¿se pueden modificar?

Sí, una tupla puede contener objetos mutables como listas o diccionarios. Y sí, esos objetos internos pueden modificarse. La inmutabilidad de la tupla se refiere a las **referencias** que contiene: no se puede hacer que una posición apunte a otro objeto, pero el objeto al que apunta puede cambiar internamente si es mutable.

```python
t = ([1, 2], "hola")
t[0].append(3)     # válido — modifica la lista interna
print(t)           # ([1, 2, 3], "hola")
# t[0] = [4, 5]   # TypeError — no se puede cambiar la referencia
```

### R11. ¿Qué es el unpacking y para qué se usa?

El unpacking permite asignar los elementos de una secuencia (tupla, lista, etc.) a variables individuales en una sola línea.

```python
punto = (3, 7)
x, y = punto    # x=3, y=7
```

Se usa para: intercambiar variables (`a, b = b, a`), descomponer valores de retorno de funciones, iterar sobre listas de tuplas (`for x, y in coordenadas`), y capturar partes de una secuencia con `*` (`primero, *resto = lista`).

El número de variables debe coincidir con el número de elementos, a menos que se use `*` para capturar el resto en una lista.

### R12. ¿Cuándo conviene usar una tupla en lugar de una lista?

Se usa una tupla cuando los datos no deben cambiar después de crearse. Casos típicos:

- **Coordenadas y puntos fijos**: `(40.41, -3.70)` — no tiene sentido que cambien.
- **Claves de diccionarios**: las tuplas son hashables, las listas no.
- **Valores de retorno de funciones**: `divmod(10, 3)` devuelve `(3, 1)`.
- **Datos de configuración**: valores que deben permanecer constantes.

Además, las tuplas son más rápidas y ocupan menos memoria que las listas. Si los datos no necesitan modificarse, una tupla es la opción más adecuada.

### R13. ¿Qué es una named tuple y qué ventajas tiene sobre una tupla normal?

Una named tuple es una tupla cuyos elementos tienen nombre además de posición. Se accede por nombre (`punto.x`) o por índice (`punto[0]`).

```python
from collections import namedtuple
Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 7)
print(p.x)    # 3
print(p[0])   # 3
```

Ventajas sobre una tupla normal:
- **Legibilidad**: `p.x` es más claro que `p[0]`.
- **Autodocumentación**: los nombres de los campos describen qué representa cada posición.
- **Compatible con tuplas**: soporta unpacking, iteración e indexación.
- **Métodos útiles**: `_asdict()` para convertir a diccionario, `_replace()` para crear copias con campos modificados.

### R14. ¿Qué diferencia hay entre `remove`, `pop` y `del` para eliminar elementos de una lista?

- `remove(valor)`: busca por **valor** y elimina la primera ocurrencia. Lanza `ValueError` si no existe.
- `pop(indice)`: elimina por **posición** y **devuelve** el elemento eliminado. Sin argumento, elimina el último. Lanza `IndexError` si el índice no existe.
- `del lista[indice]`: elimina por **posición** sin devolver el valor. También puede eliminar slices (`del lista[1:3]`).

```python
frutas = ["manzana", "pera", "uva", "pera"]

frutas.remove("pera")   # elimina la primera "pera" → ["manzana", "uva", "pera"]

frutas = ["manzana", "pera", "uva"]
eliminada = frutas.pop(1)  # "pera", lista queda ["manzana", "uva"]

frutas = ["manzana", "pera", "uva"]
del frutas[1]              # lista queda ["manzana", "uva"]
```
