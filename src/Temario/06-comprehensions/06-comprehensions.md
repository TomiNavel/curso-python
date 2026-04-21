# 6. Comprehensions

Las comprehensions son una de las características más distintivas y poderosas de Python. Permiten crear colecciones (listas, diccionarios, sets) de forma concisa y expresiva en una sola línea, a partir de un iterable existente. Son más legibles y generalmente más rápidas que el bucle `for` equivalente.

En el tema 3 se introdujeron brevemente las list comprehensions. Este tema las cubre en profundidad junto a dict comprehensions, set comprehensions y generator expressions.

---

## 6.1. List Comprehensions

### 6.1.1. Sintaxis básica

Una list comprehension construye una nueva lista aplicando una expresión a cada elemento de un iterable. Su sintaxis es:

```
[expresión for variable in iterable]
```

Esto equivale a un bucle `for` que acumula resultados en una lista:

```python
# Con bucle for
cuadrados = []
for n in range(1, 6):
    cuadrados.append(n ** 2)
print(cuadrados)  # [1, 4, 9, 16, 25]

# Con list comprehension — mismo resultado
cuadrados = [n ** 2 for n in range(1, 6)]
print(cuadrados)  # [1, 4, 9, 16, 25]
```

La comprehension se lee de izquierda a derecha: "para cada `n` en `range(1, 6)`, calcula `n ** 2` y ponlo en la lista".

Otro ejemplo con strings:

```python
nombres = ["ana", "pedro", "luis"]
mayusculas = [nombre.upper() for nombre in nombres]
print(mayusculas)  # ['ANA', 'PEDRO', 'LUIS']
```

### 6.1.2. Comprehension con condición (filtrado)

Se puede añadir una cláusula `if` al final para filtrar elementos. Solo los elementos que cumplan la condición se incluyen en la lista resultante:

```
[expresión for variable in iterable if condición]
```

```python
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Solo los pares
pares = [n for n in numeros if n % 2 == 0]
print(pares)  # [2, 4, 6, 8, 10]

# Solo strings con más de 4 caracteres
nombres = ["Ana", "Pedro", "Luis", "Alejandra", "Bo"]
largos = [nombre for nombre in nombres if len(nombre) > 4]
print(largos)  # ['Pedro', 'Alejandra']
```

El equivalente con bucle for sería:

```python
pares = []
for n in numeros:
    if n % 2 == 0:
        pares.append(n)
```

### 6.1.3. Comprehension con if/else (transformación condicional)

Cuando se necesita transformar un valor de forma diferente según una condición, el `if/else` va **antes** del `for`, no después. Esto es porque ya no se está filtrando (excluyendo elementos) sino decidiendo qué expresión aplicar a cada elemento:

```
[expresión_si_true if condición else expresión_si_false for variable in iterable]
```

```python
numeros = [1, 2, 3, 4, 5]

# Etiquetar cada número como "par" o "impar"
etiquetas = ["par" if n % 2 == 0 else "impar" for n in numeros]
print(etiquetas)  # ['impar', 'par', 'impar', 'par', 'impar']
```

La diferencia clave:
- `if` al final → **filtra** (puede producir menos elementos que el original)
- `if/else` al inicio → **transforma** (siempre produce la misma cantidad de elementos)

```python
notas = [85, 42, 91, 67, 38, 73]

# Filtrar: solo aprobados (>= 50)
aprobados = [nota for nota in notas if nota >= 50]
print(aprobados)  # [85, 91, 67, 73]

# Transformar: etiquetar todas
resultados = ["Aprobado" if nota >= 50 else "Suspendido" for nota in notas]
print(resultados)  # ['Aprobado', 'Suspendido', 'Aprobado', 'Aprobado', 'Suspendido', 'Aprobado']
```

### 6.1.4. Comprehensions anidadas

Una comprehension puede contener múltiples cláusulas `for`. Cada `for` adicional equivale a un bucle anidado dentro del anterior, y se leen de izquierda a derecha en el mismo orden que se escribirían los bucles.

El caso de uso más habitual es **aplanar** una lista de listas, es decir, convertir una estructura como `[[1, 2], [3, 4]]` en una lista plana `[1, 2, 3, 4]`. También son útiles para generar combinaciones de elementos de varios iterables.

```python
# Aplanar una lista de listas
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
plana = [num for fila in matriz for num in fila]
print(plana)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

El equivalente con bucles:

```python
plana = []
for fila in matriz:        # primer for de la comprehension
    for num in fila:       # segundo for de la comprehension
        plana.append(num)
```

Otro ejemplo — generar pares de coordenadas:

```python
coordenadas = [(x, y) for x in range(3) for y in range(3)]
print(coordenadas)
# [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
```

Se puede combinar con filtrado:

```python
# Solo pares donde x != y
pares = [(x, y) for x in range(3) for y in range(3) if x != y]
print(pares)  # [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
```

> **Regla práctica:** Si una comprehension anidada requiere más de dos `for` o se vuelve difícil de leer, es mejor usar bucles `for` tradicionales. La legibilidad siempre es prioritaria.

---

## 6.2. Dict Comprehensions

Las dict comprehensions permiten crear diccionarios de forma concisa a partir de cualquier iterable. Son especialmente útiles cuando se necesita construir un diccionario transformando datos existentes: convertir dos listas paralelas en un diccionario, filtrar entradas de un diccionario según una condición, o transformar las claves o valores de un diccionario existente.

En el tema 4 se vio que `dict(zip(claves, valores))` crea un diccionario a partir de dos listas. Las dict comprehensions hacen lo mismo, pero además permiten aplicar transformaciones y filtros en el mismo paso, sin necesidad de crear estructuras intermedias.

La sintaxis es igual que una list comprehension, pero con llaves `{}` y separando clave y valor con `:`:

```
{clave: valor for variable in iterable}
```

```python
nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34, 22]

# Crear diccionario desde dos listas
personas = {nombre: edad for nombre, edad in zip(nombres, edades)}
print(personas)  # {'Ana': 28, 'Pedro': 34, 'Luis': 22}
```

Al igual que en las list comprehensions, se puede añadir `if` para incluir solo los elementos que cumplan una condición. Esto es muy práctico para filtrar las entradas de un diccionario existente recorriéndolo con `.items()`:

```python
notas = {"Ana": 85, "Pedro": 42, "Luis": 91, "María": 67}

# Solo aprobados
aprobados = {nombre: nota for nombre, nota in notas.items() if nota >= 50}
print(aprobados)  # {'Ana': 85, 'Luis': 91, 'María': 67}
```

También se pueden intercambiar claves y valores, lo que permite invertir un diccionario. Esto solo funciona correctamente si los valores son únicos y hashables (strings, números, tuplas), ya que pasarán a ser las claves del nuevo diccionario:

```python
original = {"a": 1, "b": 2, "c": 3}
invertido = {valor: clave for clave, valor in original.items()}
print(invertido)  # {1: 'a', 2: 'b', 3: 'c'}
```

Otro caso de uso habitual es transformar los valores manteniendo las mismas claves. Por ejemplo, convertir precios de una moneda a otra:

```python
precios_usd = {"laptop": 999, "mouse": 25, "teclado": 75}
tasa = 0.92

# Convertir precios a euros
precios_eur = {producto: round(precio * tasa, 2) for producto, precio in precios_usd.items()}
print(precios_eur)  # {'laptop': 919.08, 'mouse': 23.0, 'teclado': 69.0}
```

---

## 6.3. Set Comprehensions

Las set comprehensions funcionan igual que las list comprehensions, pero producen un set en lugar de una lista. Se escriben con llaves `{}` sin `:` (la presencia o ausencia de `:` es lo que distingue una set comprehension de una dict comprehension).

La ventaja principal frente a una list comprehension es que los duplicados se eliminan automáticamente. Esto las hace ideales cuando se necesita extraer valores únicos de una colección, o cuando el resultado de la transformación puede producir repeticiones que no interesan.

```
{expresión for variable in iterable}
```

```python
numeros = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# Set de cuadrados — los duplicados del iterable original no generan
# entradas duplicadas en el resultado
cuadrados = {n ** 2 for n in numeros}
print(cuadrados)  # {1, 4, 9, 16, 25}
```

Se puede combinar con filtrado, igual que en cualquier otra comprehension:

```python
texto = "programacion"
vocales_en_texto = {letra for letra in texto if letra in "aeiou"}
print(vocales_en_texto)  # {'a', 'i', 'o'}
```

Un caso de uso muy habitual es normalizar datos para encontrar valores únicos. Por ejemplo, si se reciben emails con mayúsculas y minúsculas mezcladas, una set comprehension puede normalizarlos y eliminar duplicados en un solo paso:

```python
emails = ["Ana@mail.com", "ana@MAIL.com", "pedro@mail.com", "PEDRO@mail.com"]
unicos = {email.lower() for email in emails}
print(unicos)  # {'ana@mail.com', 'pedro@mail.com'}
```

---

## 6.4. Generator Expressions

Las generator expressions tienen la misma sintaxis que las list comprehensions pero con paréntesis `()` en lugar de corchetes `[]`. A primera vista parecen lo mismo, pero su comportamiento es fundamentalmente diferente.

Una list comprehension crea todos los elementos de golpe y los almacena en memoria. Una generator expression no crea nada: devuelve un objeto generador que calcula los elementos **uno a uno, bajo demanda**, solo cuando se le piden. Este concepto se llama **evaluación diferida** (lazy evaluation) y es clave para entender los generadores.

La ventaja práctica es el consumo de memoria. Si se necesitan los cuadrados de un millón de números, una lista almacena un millón de valores en memoria. Un generador almacena solo la "receta" para calcularlos y ocupa una cantidad constante de memoria, sin importar cuántos elementos represente.

```
(expresión for variable in iterable)
```

```python
# List comprehension — crea toda la lista en memoria (un millón de elementos)
cuadrados_lista = [n ** 2 for n in range(1000000)]

# Generator expression — no crea nada hasta que se consume
cuadrados_gen = (n ** 2 for n in range(1000000))
```

### 6.4.1. Cuándo usar generator expressions

Son ideales cuando solo se necesita **procesar los elementos una vez** sin guardarlos todos en memoria. El caso de uso más habitual es pasarlas como argumento a funciones que consumen iterables elemento a elemento. Las más comunes:

- `sum(iterable)` — suma todos los elementos
- `max(iterable)` / `min(iterable)` — encuentra el mayor / menor
- `any(iterable)` — devuelve `True` si **al menos un** elemento es truthy
- `all(iterable)` — devuelve `True` si **todos** los elementos son truthy

Estas funciones recorren el generador elemento a elemento y producen un único resultado, por lo que no necesitan tener todos los datos en memoria a la vez:

```python
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# sum() consume el generador elemento a elemento
total = sum(n ** 2 for n in numeros)
print(total)  # 385

# Cuando el generador es el único argumento de una función,
# se pueden omitir los paréntesis exteriores
mayor = max(len(palabra) for palabra in ["Python", "es", "genial"])
print(mayor)  # 6
```

`any()` y `all()` son especialmente útiles para comprobar condiciones sobre una colección sin escribir un bucle explícito. Además, `any()` deja de iterar en cuanto encuentra el primer `True`, y `all()` en cuanto encuentra el primer `False`, lo que las hace eficientes con generadores grandes:

```python
nombres = ["Ana", "Pedro", "Luis"]

# ¿Hay algún nombre con más de 4 caracteres?
hay_largo = any(len(nombre) > 4 for nombre in nombres)
print(hay_largo)  # True

# ¿Todos los nombres tienen 5 caracteres o menos?
todos_cortos = all(len(nombre) <= 5 for nombre in nombres)
print(todos_cortos)  # True
```

### 6.4.2. Limitaciones de los generadores

Un generador solo se puede consumir **una vez**. Una vez recorrido, queda vacío y no se puede volver a iterar sobre él. Esto es una consecuencia directa de la evaluación diferida: los valores no se almacenan, se calculan al vuelo y se descartan.

```python
gen = (n ** 2 for n in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]
print(list(gen))  # [] — ya está agotado
```

Si se necesita acceder a los datos más de una vez, se debe usar una list comprehension o convertir el generador a lista con `list()`.

---

## 6.5. Cuándo usar y cuándo no usar comprehensions

Las comprehensions son una herramienta poderosa, pero no siempre son la mejor opción. Su uso adecuado mejora la legibilidad; su abuso la destruye.

### Usar comprehensions cuando:

- La operación es una **transformación simple** o un **filtrado directo**
- El resultado cabe en **una línea legible** (o dos como máximo)
- Se quiere crear una nueva colección a partir de otra

```python
# Bien — claro y conciso
pares = [n for n in numeros if n % 2 == 0]
nombres_upper = [n.upper() for n in nombres]
conteo = {palabra: texto.count(palabra) for palabra in palabras}
```

### Usar bucles for cuando:

- La lógica requiere **múltiples pasos** o **efectos secundarios** (como `print()`)
- Se necesitan **más de dos for** anidados
- La comprehension supera las **~80 columnas** y pierde legibilidad
- Se necesita **acumular estado** que va cambiando (contadores, flags)

```python
# Mal — demasiado complejo para una comprehension
resultado = [x + y for x in range(10) for y in range(10) if x != y if (x + y) % 3 == 0]

# Mejor con bucle for
resultado = []
for x in range(10):
    for y in range(10):
        if x != y and (x + y) % 3 == 0:
            resultado.append(x + y)
```

### Error frecuente: comprehensions con efectos secundarios

Las comprehensions están diseñadas para **crear colecciones**, no para ejecutar acciones. Usar una comprehension solo por su efecto secundario (como `print()`) es un antipatrón:

```python
# MAL — crea una lista de None solo para imprimir
[print(n) for n in numeros]

# BIEN — usar un bucle for
for n in numeros:
    print(n)
```

### Resumen de sintaxis

| Tipo | Sintaxis | Resultado |
|------|----------|-----------|
| List comprehension | `[expr for x in iterable]` | `list` |
| Dict comprehension | `{key: val for x in iterable}` | `dict` |
| Set comprehension | `{expr for x in iterable}` | `set` |
| Generator expression | `(expr for x in iterable)` | `generator` |

Todas admiten `if` para filtrar y múltiples `for` para anidar.
