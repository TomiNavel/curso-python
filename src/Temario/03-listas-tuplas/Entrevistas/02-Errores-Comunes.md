# Errores comunes: Listas y Tuplas

## Error 1: Asignar el resultado de un método in-place

Los métodos que modifican la lista (`sort`, `append`, `extend`, `reverse`, `insert`, `remove`, `clear`) actúan sobre la lista original y devuelven `None`. Asignar su resultado a una variable es uno de los errores más frecuentes en Python: la variable queda con `None` y se pierde la referencia a la lista.

```python
# MAL — lista queda como None
lista = [3, 1, 2]
lista = lista.sort()
print(lista)  # None

# BIEN — sort modifica la lista original directamente
lista = [3, 1, 2]
lista.sort()
print(lista)  # [1, 2, 3]

# Si se necesita una nueva lista sin modificar la original, usar sorted
original = [3, 1, 2]
nueva = sorted(original)
print(original)  # [3, 1, 2] — sin cambios
print(nueva)     # [1, 2, 3]
```

## Error 2: Modificar una lista mientras se itera sobre ella

Eliminar o añadir elementos durante un `for` desplaza los índices internos del iterador, provocando que se salten elementos o que el resultado sea incorrecto.

```python
numeros = [1, 2, 3, 4, 5, 6]

# MAL — al eliminar un elemento, los índices se desplazan
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)
print(numeros)  # [1, 3, 5, 6] — el 6 no se eliminó

# BIEN — crear una nueva lista con los elementos deseados
numeros = [1, 2, 3, 4, 5, 6]
numeros = [n for n in numeros if n % 2 != 0]
print(numeros)  # [1, 3, 5]

# BIEN — iterar sobre una copia
numeros = [1, 2, 3, 4, 5, 6]
for n in numeros[:]:
    if n % 2 == 0:
        numeros.remove(n)
print(numeros)  # [1, 3, 5]
```

## Error 3: Confundir append con extend

`append` añade su argumento como un único elemento. Si se le pasa una lista, la lista entera queda anidada como un solo elemento. `extend` desempaqueta el iterable y añade cada elemento por separado.

```python
lista = [1, 2, 3]
lista.append([4, 5])
print(lista)  # [1, 2, 3, [4, 5]] — lista anidada, probablemente no es lo que se quería

lista = [1, 2, 3]
lista.extend([4, 5])
print(lista)  # [1, 2, 3, 4, 5]
```

## Error 4: Crear listas con referencias compartidas usando *

Al multiplicar una lista que contiene objetos mutables, todas las copias son referencias al mismo objeto. Modificar uno los modifica todos.

```python
# MAL — las 3 sublistas son el MISMO objeto en memoria
matriz = [[0] * 3] * 3
matriz[0][0] = 1
print(matriz)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

# BIEN — cada sublista es un objeto independiente
matriz = [[0] * 3 for _ in range(3)]
matriz[0][0] = 1
print(matriz)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Con primitivos (`[0] * 3`) no ocurre este problema porque los enteros son inmutables: al reasignar se crea un nuevo objeto.

## Error 5: Confundir asignación con copia

Asignar una lista a otra variable no crea una copia — ambas apuntan al mismo objeto en memoria.

```python
# MAL — a y b son el mismo objeto
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4] — a también cambió

# BIEN — copia explícita
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)  # [1, 2, 3] — a no se vio afectada
```

Para listas con objetos mutables anidados, `copy()` no es suficiente — se necesita `copy.deepcopy()`.

## Error 6: Objetos mutables dentro de tuplas

Las tuplas son inmutables, pero si contienen objetos mutables (como listas), esos objetos internos sí pueden modificarse. Esto sorprende a muchos programadores y es una pregunta habitual en entrevistas.

```python
t = ([1, 2], [3, 4])

# La tupla no permite reasignar sus elementos
# t[0] = [99]  # TypeError

# Pero el contenido mutable de un elemento SÍ puede cambiar
t[0].append(99)
print(t)  # ([1, 2, 99], [3, 4])
```

La inmutabilidad de la tupla se refiere a las **referencias**: no se puede hacer que `t[0]` apunte a otro objeto. Pero el objeto al que apunta puede cambiar internamente si es mutable.

## Error 7: Olvidar la coma en tuplas de un elemento

Lo que define una tupla es la coma, no los paréntesis. Sin coma, los paréntesis se interpretan como agrupación.

```python
# MAL — esto es un int, no una tupla
t = (42)
print(type(t))  # <class 'int'>

# BIEN
t = (42,)
print(type(t))  # <class 'tuple'>

# También sin paréntesis
t = 42,
print(type(t))  # <class 'tuple'>
```

## Error 8: Usar remove con índice en lugar de valor

`remove` busca por **valor** y elimina la primera ocurrencia. Para eliminar por posición, se usa `pop` o `del`.

```python
frutas = ["manzana", "pera", "uva"]

# MAL — remove busca el valor 1, no la posición 1
# frutas.remove(1)  # ValueError: list.index(x): x not in list

# BIEN — eliminar por posición
eliminado = frutas.pop(1)       # "pera"

# BIEN — eliminar por valor
frutas = ["manzana", "pera", "uva"]
frutas.remove("pera")           # elimina la primera ocurrencia de "pera"
```

## Error 9: No verificar existencia antes de index o remove

Ambos métodos lanzan `ValueError` si el elemento no existe en la lista. En código de producción y en entrevistas, no manejar este caso es un error evidente.

```python
frutas = ["manzana", "pera"]

# MAL — falla si no existe
# frutas.remove("kiwi")  # ValueError
# frutas.index("kiwi")   # ValueError

# BIEN — comprobar primero
if "kiwi" in frutas:
    frutas.remove("kiwi")
```
