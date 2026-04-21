# 5. Control de Flujo

El control de flujo determina el orden en que se ejecutan las instrucciones de un programa. Sin él, el código se ejecutaría siempre de arriba a abajo de forma lineal. Python ofrece dos mecanismos: **condicionales** para ejecutar código solo cuando se cumple una condición, y **bucles** para repetir código un número determinado de veces o mientras se cumpla una condición.

## 5.1. Condicionales

### 5.1.1. if, elif, else

`if` evalúa una condición y ejecuta el bloque si es verdadera. `elif` añade condiciones alternativas. `else` captura todos los casos restantes. Solo se ejecuta el primer bloque cuya condición sea verdadera.

```python
temperatura = 22

if temperatura > 30:
    print("hace calor")
elif temperatura > 20:
    print("temperatura agradable")  # se ejecuta este
elif temperatura > 10:
    print("hace fresco")
else:
    print("hace frío")
```

Los condicionales anidados son válidos pero deben usarse con moderación — más de dos niveles de anidamiento suele ser señal de que el código puede simplificarse.

```python
edad = 25
tiene_carnet = True

if edad >= 18:
    if tiene_carnet:
        print("puede conducir")
    else:
        print("mayor de edad, pero sin carnet")
else:
    print("menor de edad")
```

### 5.1.2. Operador ternario

Python tiene una forma concisa de escribir un `if/else` en una sola línea cuando el resultado es un valor. La sintaxis es `valor_si_true if condicion else valor_si_false`.

```python
edad = 20
estado = "mayor" if edad >= 18 else "menor"

# Equivale a:
if edad >= 18:
    estado = "mayor"
else:
    estado = "menor"

# Uso común: valores por defecto
nombre = input("Nombre: ")
saludo = f"Hola, {nombre}" if nombre else "Hola, desconocido"
```

Usar solo cuando la condición y ambos valores son simples. Si la lógica es compleja, el `if/else` normal es más legible.

### 5.1.3. Expresiones booleanas, short-circuit y truthiness

Estos conceptos se explican en detalle en las secciones 1.3.3 y 1.4.3. Aquí se muestra cómo se aplican en condicionales.

**Truthiness en condicionales** — cualquier valor puede usarse directamente como condición sin comparar explícitamente:

```python
lista = [1, 2, 3]
nombre = "Ana"
conexion = None

if lista:           # equivale a: if len(lista) > 0
    print("hay elementos")

if nombre:          # equivale a: if nombre != ""
    print(f"Hola, {nombre}")

if not conexion:    # equivale a: if conexion is None
    print("sin conexión")
```

**Short-circuit en condicionales** — `and` deja de evaluar si el primero es falsy; `or` deja de evaluar si el primero es truthy. Esto permite escribir guardas seguras:

```python
# Sin short-circuit, acceder a .get() de None lanzaría AttributeError
usuario = None
if usuario and usuario.get("activo"):
    print("usuario activo")

# or como valor por defecto
config = configuracion_custom or configuracion_por_defecto
```

### 5.1.4. Walrus operator (:=, Python 3.8+)

El operador de asignación con nombre (`:=`), conocido como *walrus operator* por su parecido con los ojos y colmillos de una morsa, permite asignar un valor a una variable **dentro de una expresión**. Resuelve un problema concreto: cuando necesitas usar el resultado de una operación tanto en la condición como en el cuerpo de un `if` o `while`, sin tener que calcularlo dos veces ni sacarlo a una línea aparte.

Sin walrus, hay que elegir entre calcular el valor antes (una línea extra) o calcularlo dos veces (una en la condición y otra en el cuerpo):

```python
# Sin walrus — variable auxiliar antes del if
longitud = len(datos)
if longitud > 10:
    print(f"Demasiados elementos: {longitud}")

# Sin walrus — calcular dos veces
if len(datos) > 10:
    print(f"Demasiados elementos: {len(datos)}")  # len() se ejecuta dos veces
```

Con walrus, la asignación y la condición se combinan en una sola expresión:

```python
# Con walrus — asigna y evalúa en un solo paso
if (n := len(datos)) > 10:
    print(f"Demasiados elementos: {n}")
```

Donde más brilla es en bucles `while` que leen datos hasta que se agota la fuente:

```python
# Leer líneas de un archivo hasta que se acaben
while (linea := archivo.readline()) != "":
    procesar(linea)

# Leer input del usuario hasta que escriba "salir"
while (comando := input("> ")) != "salir":
    print(f"Ejecutando: {comando}")
```

También es útil para evitar cálculos repetidos en comprehensions con filtro, donde el valor calculado se necesita tanto en la condición como en el resultado:

```python
# Sin walrus — calcular dos veces
resultados = [calcular(x) for x in datos if calcular(x) > umbral]

# Con walrus — calcular una sola vez
resultados = [y for x in datos if (y := calcular(x)) > umbral]
```

No hay que abusar del walrus. Si la expresión ya es legible sin él, no añade nada. Su uso ideal es en los tres patrones anteriores: condiciones que reutilizan un valor, bucles `while` con lectura, y comprehensions con filtro costoso.

### 5.1.5. match/case (Python 3.10+)

`match/case` es el structural pattern matching de Python, introducido en Python 3.10. La diferencia con un `switch/case` tradicional es que no solo compara valores — puede comparar la estructura y forma de los datos. Un `case (x, 0)` no pregunta "¿es igual a `(x, 0)`?", sino "¿es una tupla de dos elementos donde el segundo es 0? Si es así, extrae el primero en `x`".

Esto lo hace especialmente potente para trabajar con estructuras complejas como respuestas de APIs, eventos o comandos, donde el tipo y forma del dato determina qué acción tomar.

```python
# Comparación de valores — equivale a un switch/case
comando = "salir"

match comando:
    case "iniciar":
        print("Iniciando...")
    case "parar":
        print("Parando...")
    case "salir":
        print("Saliendo...")   # se ejecuta este
    case _:                    # _ es el caso por defecto (equivale a else)
        print(f"Comando desconocido: {comando}")

# Comparación de estructura — aquí es donde match supera a if/elif
punto = (1, 0)

match punto:
    case (0, 0):
        print("origen")
    case (x, 0):
        print(f"sobre el eje X en {x}")   # se ejecuta este, x=1
    case (0, y):
        print(f"sobre el eje Y en {y}")
    case (x, y):
        print(f"punto en ({x}, {y})")

# Matching de estructura de dicts — solo requiere que las claves indicadas existan
evento = {"tipo": "click", "boton": "izquierdo"}

match evento:
    case {"tipo": "click", "boton": boton}:
        print(f"Click con botón {boton}")
    case {"tipo": "teclado", "tecla": tecla}:
        print(f"Tecla presionada: {tecla}")
    case _:
        print("Evento desconocido")
```

## 5.2. Bucles

### 5.2.1. for loop

El `for` de Python itera sobre cualquier objeto iterable — listas, strings, dicts, sets, rangos, ficheros, generadores. No usa índices numéricos por defecto como en C o Java.

```python
# Iterar sobre una lista
frutas = ["manzana", "pera", "uva"]
for fruta in frutas:
    print(fruta)

# Iterar sobre un string
for letra in "Python":
    print(letra)

# Iterar sobre las keys de un dict (comportamiento por defecto)
config = {"host": "localhost", "puerto": 5432}
for clave in config:
    print(clave)

# Iterar sobre pares clave-valor
for clave, valor in config.items():
    print(f"{clave}: {valor}")
```

### 5.2.2. while loop

`while` ejecuta el bloque mientras la condición sea verdadera. Se usa cuando el número de iteraciones no se conoce de antemano.

```python
intentos = 0
max_intentos = 3

while intentos < max_intentos:
    password = input("Introduce tu contraseña: ")
    if password == "secreta":
        print("Acceso concedido")
        break
    intentos += 1
    print(f"Incorrecto. Intentos restantes: {max_intentos - intentos}")
else:
    print("Cuenta bloqueada")

# Bucle infinito controlado
while True:
    comando = input("> ")
    if comando == "salir":
        break
    print(f"Ejecutando: {comando}")
```

### 5.2.3. break, continue, pass

Las tres palabras clave alteran el flujo de un bucle de formas distintas.

**`break`** termina el bucle completamente y salta a la primera línea después de él.

**`continue`** salta el resto de la iteración actual y pasa a la siguiente.

**`pass`** no hace nada — es un placeholder sintáctico para cuando Python requiere un bloque pero no hay código que ejecutar.

```python
numeros = [1, 3, 7, 2, 8, 4, 9]

# break: para al encontrar el primer par
for n in numeros:
    if n % 2 == 0:
        print(f"Primer par: {n}")
        break

# continue: procesa solo los impares
for n in numeros:
    if n % 2 == 0:
        continue
    print(f"Impar: {n}")

# pass: bloque vacío — útil en desarrollo o en clases/funciones pendientes
for n in numeros:
    if n > 5:
        pass  # TODO: manejar números grandes
    else:
        print(n)
```

### 5.2.4. else en bucles

Python permite añadir un bloque `else` a los bucles `for` y `while`. El bloque `else` se ejecuta **solo si el bucle terminó de forma natural** — sin que se ejecutara un `break`.

Es un patrón poco conocido pero útil para búsquedas: si recorres una colección buscando algo y usas `break` al encontrarlo, el `else` solo se ejecuta si no lo encontraste.

```python
usuarios = ["ana", "pedro", "luis"]

for usuario in usuarios:
    if usuario == "maria":
        print("María encontrada")
        break
else:
    print("María no está en la lista")  # se ejecuta este

# Ejemplo clásico: buscar si un número es primo
n = 17
for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        print(f"{n} no es primo, divisible por {i}")
        break  # encontró un divisor — no es primo
else:
    print(f"{n} es primo")  # el bucle terminó sin break — es primo
```

## 5.3. Funciones de iteración

Python incluye varias funciones built-in diseñadas para trabajar con iterables dentro de bucles. No son construcciones de control de flujo por sí mismas, pero aparecen constantemente en combinación con `for` y determinan cómo se recorre una colección.

### 5.3.1. range()

`range()` representa una secuencia de enteros. No es una lista — es un objeto que almacena únicamente el inicio, el fin y el paso, y calcula cada número solo cuando se le pide. Por eso `range(1_000_000)` ocupa la misma memoria que `range(5)`: nunca materializa todos los valores a la vez.

La sintaxis tiene tres formas: `range(fin)`, `range(inicio, fin)` y `range(inicio, fin, paso)`. Como en slicing, el `fin` nunca está incluido.

```python
range(5)          # 0, 1, 2, 3, 4       — empieza en 0 por defecto
range(2, 8)       # 2, 3, 4, 5, 6, 7   — fin excluido
range(0, 10, 2)   # 0, 2, 4, 6, 8      — paso de 2
range(10, 0, -1)  # 10, 9, 8, ..., 1   — paso negativo para contar hacia atrás

for i in range(3):
    print(i)  # 0, 1, 2

# range se comporta como una secuencia: soporta len(), indexing e in
r = range(10)
print(len(r))    # 10
print(r[3])      # 3
print(r[-1])     # 9
print(5 in r)    # True — O(1), no recorre todos los elementos
```

### 5.3.2. enumerate()

Cuando necesitas tanto el índice como el valor de cada elemento al iterar, el patrón `range(len(lista))` funciona pero es torpe: acceder por índice dentro del bucle es redundante cuando ya tienes el elemento. `enumerate()` resuelve esto devolviendo pares `(índice, valor)` directamente, manteniendo el bucle limpio y legible.

```python
frutas = ["manzana", "pera", "uva"]

# Antipatrón — acceder por índice cuando ya tienes el elemento es redundante
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

# Con enumerate — más directo y pythónico
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")

# enumerate acepta un inicio distinto de 0
for i, fruta in enumerate(frutas, start=1):
    print(f"{i}. {fruta}")  # 1. manzana, 2. pera, 3. uva
```

### 5.3.3. zip()

`zip()` toma varios iterables y los combina elemento a elemento, produciendo tuplas. En lugar de iterar una lista y acceder a otras por índice, `zip` permite recorrer varias colecciones en paralelo de forma directa.

Se detiene cuando el iterable más corto se agota. Si necesitas continuar hasta el más largo, `itertools.zip_longest` rellena los huecos con un valor por defecto.

```python
nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34, 22]

# Iterar dos listas en paralelo
for nombre, edad in zip(nombres, edades):
    print(f"{nombre}: {edad} años")

# Crear un dict desde dos listas — patrón muy común
claves = ["host", "puerto", "db"]
valores = ["localhost", 5432, "myapp"]
config = dict(zip(claves, valores))
print(config)  # {'host': 'localhost', 'puerto': 5432, 'db': 'myapp'}

# zip se detiene al más corto
a = [1, 2, 3, 4, 5]
b = ["a", "b", "c"]
print(list(zip(a, b)))  # [(1, 'a'), (2, 'b'), (3, 'c')]

# Para continuar hasta el más largo
from itertools import zip_longest
print(list(zip_longest(a, b, fillvalue="-")))
# [(1, 'a'), (2, 'b'), (3, 'c'), (4, '-'), (5, '-')]
```
