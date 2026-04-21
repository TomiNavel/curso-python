# Preguntas de entrevista: Control de Flujo

1. ¿Qué diferencia hay entre `if/elif/else` y usar varios `if` seguidos?
2. ¿Qué es el operador ternario en Python y cuándo conviene usarlo?
3. ¿Qué es la evaluación en cortocircuito (short-circuit) y cómo se aprovecha en condicionales?
4. ¿Qué valores son falsy en Python?
5. ¿Qué diferencia hay entre `for` y `while`? ¿Cuándo se usa cada uno?
6. ¿Qué hace `break` y qué hace `continue`?
7. ¿Para qué sirve el bloque `else` en un bucle `for` o `while`?
8. ¿Qué es `pass` y cuándo se usa?
9. ¿Qué es `range()` y por qué no es una lista?
10. ¿Para qué sirve `enumerate()` y qué ventaja tiene sobre `range(len(...))`?
11. ¿Qué hace `zip()` y qué ocurre si los iterables tienen distinta longitud?
12. ¿Qué es `match/case` y en qué se diferencia de un `switch/case` tradicional?
13. ¿Cómo se evita un bucle infinito con `while`?
14. ¿Por qué no se debe modificar una lista mientras se itera sobre ella con `for`?

---

### R1. ¿Qué diferencia hay entre `if/elif/else` y usar varios `if` seguidos?

Con `if/elif/else`, Python evalúa las condiciones en orden y **ejecuta solo el primer bloque cuya condición sea verdadera**. En cuanto uno se cumple, el resto se ignora. Con varios `if` seguidos, cada uno se evalúa de forma independiente — pueden ejecutarse varios bloques en la misma pasada.

```python
x = 15

# Solo imprime "mayor que 10" — el elif se salta porque ya se cumplió el if
if x > 10:
    print("mayor que 10")
elif x > 5:
    print("mayor que 5")

# Imprime ambos — cada if es independiente
if x > 10:
    print("mayor que 10")
if x > 5:
    print("mayor que 5")
```

### R2. ¿Qué es el operador ternario en Python y cuándo conviene usarlo?

Es una forma de escribir un `if/else` en una sola línea que devuelve un valor. La sintaxis es `valor_si_true if condicion else valor_si_false`.

Conviene usarlo cuando la condición y ambos valores son simples y caben de forma legible en una línea. Si la lógica es compleja o los valores son expresiones largas, el `if/else` tradicional es más claro.

```python
estado = "mayor" if edad >= 18 else "menor"
```

### R3. ¿Qué es la evaluación en cortocircuito (short-circuit) y cómo se aprovecha en condicionales?

Python deja de evaluar una expresión booleana en cuanto puede determinar el resultado. Con `and`, si el primer operando es falsy, no evalúa el segundo (porque el resultado ya es falso). Con `or`, si el primer operando es truthy, no evalúa el segundo (porque el resultado ya es verdadero).

Esto se aprovecha para escribir guardas seguras: primero se comprueba que un valor existe y luego se accede a él. Si la primera comprobación falla, la segunda nunca se ejecuta y no hay error.

```python
# Si usuario es None, Python no evalúa usuario.get("activo") — evita AttributeError
if usuario and usuario.get("activo"):
    print("usuario activo")
```

### R4. ¿Qué valores son falsy en Python?

Los valores que se evalúan como `False` en un contexto booleano son: `False`, `None`, `0` (y `0.0`, `0j`), cadenas vacías `""`, y colecciones vacías (`[]`, `()`, `{}`, `set()`). Todo lo demás es truthy.

Esto permite escribir condiciones directas sin comparaciones explícitas:

```python
# En lugar de: if len(lista) > 0
if lista:
    print("hay elementos")
```

### R5. ¿Qué diferencia hay entre `for` y `while`? ¿Cuándo se usa cada uno?

`for` itera sobre un iterable (lista, string, range, dict...) y se ejecuta una vez por cada elemento. El número de iteraciones está determinado por el iterable. `while` repite mientras una condición sea verdadera — el número de iteraciones no se conoce de antemano.

Se usa `for` cuando se recorre una colección o se necesita un número fijo de repeticiones. Se usa `while` cuando la condición de parada depende de algo que cambia durante la ejecución (entrada del usuario, un cálculo, un evento externo).

### R6. ¿Qué hace `break` y qué hace `continue`?

`break` termina el bucle completamente — la ejecución salta a la primera línea después del bucle. `continue` salta el resto de la iteración actual y pasa directamente a la siguiente iteración.

```python
for n in [1, 2, 3, 4, 5]:
    if n == 3:
        break       # sale del bucle — no procesa 3, 4, 5
    print(n)        # imprime 1, 2

for n in [1, 2, 3, 4, 5]:
    if n == 3:
        continue    # salta el 3, pero sigue con 4 y 5
    print(n)        # imprime 1, 2, 4, 5
```

### R7. ¿Para qué sirve el bloque `else` en un bucle `for` o `while`?

El bloque `else` de un bucle se ejecuta **solo si el bucle terminó de forma natural**, es decir, sin que se ejecutara un `break`. Si el bucle se interrumpió con `break`, el `else` se salta.

Es útil en búsquedas: se recorre una colección buscando un elemento, si se encuentra se usa `break`, y el `else` maneja el caso de "no encontrado".

```python
for usuario in ["ana", "pedro", "luis"]:
    if usuario == "maria":
        print("encontrada")
        break
else:
    print("no encontrada")  # se ejecuta porque no hubo break
```

### R8. ¿Qué es `pass` y cuándo se usa?

`pass` es una sentencia que no hace nada. Existe porque Python requiere sintácticamente que los bloques (`if`, `for`, `while`, etc.) tengan al menos una instrucción. Se usa como placeholder cuando se necesita un bloque vacío, ya sea temporalmente durante el desarrollo o porque la lógica requiere ignorar un caso explícitamente.

```python
for n in numeros:
    if n < 0:
        pass  # por ahora ignoramos los negativos
    else:
        print(n)
```

### R9. ¿Qué es `range()` y por qué no es una lista?

`range()` es un objeto que representa una secuencia de enteros. No genera todos los números a la vez — almacena solo el inicio, fin y paso, y calcula cada valor bajo demanda. Por eso `range(1_000_000)` ocupa la misma memoria que `range(5)`.

No es una lista porque no necesita serlo: al no materializar todos los valores, es más eficiente en memoria. Soporta `len()`, indexing e `in` (con comprobación en O(1)), pero no permite modificar sus elementos.

### R10. ¿Para qué sirve `enumerate()` y qué ventaja tiene sobre `range(len(...))`?

`enumerate()` devuelve pares `(índice, valor)` al iterar. La ventaja sobre `range(len(lista))` es que da acceso directo al elemento sin necesidad de indexar la lista manualmente, lo que produce código más limpio y menos propenso a errores.

```python
frutas = ["manzana", "pera", "uva"]

# Con range(len(...)) — redundante, accede por índice teniendo el elemento disponible
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

# Con enumerate — directo
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")
```

### R11. ¿Qué hace `zip()` y qué ocurre si los iterables tienen distinta longitud?

`zip()` combina varios iterables elemento a elemento, produciendo tuplas. Si los iterables tienen distinta longitud, `zip()` se detiene cuando el más corto se agota — los elementos sobrantes del más largo se ignoran silenciosamente.

```python
nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34]

for nombre, edad in zip(nombres, edades):
    print(f"{nombre}: {edad}")
# Ana: 28
# Pedro: 34
# "Luis" se ignora porque edades se agotó
```

Para continuar hasta el iterable más largo, se usa `itertools.zip_longest`.

### R12. ¿Qué es `match/case` y en qué se diferencia de un `switch/case` tradicional?

`match/case` (Python 3.10+) es structural pattern matching. A diferencia de un `switch/case` que solo compara valores, `match/case` puede comparar la **estructura** de los datos: descomponer tuplas, extraer valores de diccionarios y asignar partes del dato a variables.

```python
punto = (3, 0)

match punto:
    case (0, 0):
        print("origen")
    case (x, 0):
        print(f"eje X en {x}")   # se ejecuta, x=3
    case (x, y):
        print(f"punto en ({x}, {y})")
```

El `case (x, 0)` no pregunta "¿es igual a `(x, 0)`?", sino "¿es una tupla de dos elementos donde el segundo es 0? Si es así, extrae el primero en `x`".

### R13. ¿Cómo se evita un bucle infinito con `while`?

Un bucle `while` se convierte en infinito si la condición nunca llega a ser falsa. Para evitarlo hay que asegurarse de que algo dentro del bucle modifique el estado que evalúa la condición: un contador que se incrementa, una variable que se actualiza, o un `break` que interrumpe la ejecución.

```python
# Correcto: el contador se incrementa y eventualmente la condición es falsa
intentos = 0
while intentos < 5:
    print(intentos)
    intentos += 1

# Correcto: break garantiza la salida
while True:
    respuesta = input("¿Salir? (s/n): ")
    if respuesta == "s":
        break
```

Si se usa `while True`, el `break` es obligatorio — sin él, el bucle no termina nunca.

### R14. ¿Por qué no se debe modificar una lista mientras se itera sobre ella con `for`?

Cuando un `for` itera sobre una lista, Python usa un índice interno para recorrerla. Si se añaden o eliminan elementos durante la iteración, los índices se desplazan y el bucle puede saltarse elementos o procesarlos dos veces.

```python
numeros = [1, 2, 3, 4, 5]

# Mal — eliminar durante iteración salta elementos
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)
print(numeros)  # [1, 3, 5]? No — resultado: [1, 3, 5] solo por suerte, con otras listas falla

# Bien — iterar sobre una copia
for n in numeros[:]:
    if n % 2 == 0:
        numeros.remove(n)
```

La solución es iterar sobre una copia (`lista[:]`) o construir una nueva lista con los elementos deseados.
