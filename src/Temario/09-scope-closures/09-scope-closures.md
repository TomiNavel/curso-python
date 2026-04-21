# 9. Scope y Closures

Entender dónde vive una variable y quién puede acceder a ella es fundamental para escribir código predecible. Python tiene reglas claras sobre la visibilidad de las variables según dónde se definen, y dominar estas reglas evita una categoría entera de bugs difíciles de detectar. Los closures, que dependen directamente de estas reglas de scope, son además la base sobre la que se construyen los decoradores (tema 10).

---

## 9.1. Scope (ámbito de variables)

El scope de una variable es la zona del código donde esa variable es accesible. Fuera de su scope, la variable no existe — intentar usarla lanza `NameError`. Python determina el scope de una variable en tiempo de compilación, según dónde aparece la asignación, no dónde se ejecuta el código.

### 9.1.1. Scope local y global

Hay dos scopes fundamentales:

- **Scope global**: variables definidas al nivel superior del módulo (fuera de cualquier función). Son accesibles desde cualquier punto del archivo.
- **Scope local**: variables definidas dentro de una función. Solo existen mientras la función se ejecuta y desaparecen al terminar.

```python
x = 10  # global — accesible en todo el módulo

def funcion():
    y = 5  # local — solo existe dentro de funcion()
    print(x)  # puede LEER la variable global
    print(y)

funcion()    # 10, 5
print(x)     # 10
print(y)     # NameError: name 'y' is not defined
```

Un detalle crucial: Python decide si una variable es local o global **en tiempo de compilación**, analizando si hay una asignación a esa variable dentro de la función. No importa si la asignación está después del `print` — si existe en algún lugar de la función, Python la considera local en toda la función:

```python
x = 10

def funcion():
    print(x)  # UnboundLocalError — Python ya sabe que x es local
    x = 20    # esta asignación hace que x sea local en TODA la función

funcion()
```

Este error confunde a muchos programadores. Python no cambia de "global" a "local" al llegar a la asignación. Desde el momento en que el intérprete compila la función, ve la asignación `x = 20` y marca `x` como local. Cuando `print(x)` se ejecuta antes de la asignación, la variable local `x` existe pero no tiene valor asignado todavía.

### 9.1.2. La regla LEGB (Local, Enclosing, Global, Built-in)

Cuando Python encuentra un nombre en una expresión, lo busca en cuatro scopes, en este orden:

1. **Local** — dentro de la función actual
2. **Enclosing** — dentro de las funciones que contienen a la actual (funciones anidadas)
3. **Global** — al nivel superior del módulo
4. **Built-in** — nombres predefinidos de Python (`print`, `len`, `range`, etc.)

La búsqueda se detiene en el primer scope donde encuentra el nombre. Si no lo encuentra en ninguno, lanza `NameError`.

```python
x = "global"

def externa():
    x = "enclosing"

    def interna():
        x = "local"
        print(x)  # "local" — encontrado en el scope Local

    interna()

externa()
```

Si eliminamos `x = "local"` de `interna()`, Python sube al scope Enclosing y encuentra `"enclosing"`. Si también eliminamos esa, sube a Global y encuentra `"global"`. Y si eliminamos todas, busca en Built-in — como `x` no existe ahí, lanza `NameError`.

```python
# Ejemplo del scope Built-in
# print es un nombre del scope Built-in — disponible en todas partes
print("hola")

# Pero se puede "ocultar" asignándole un valor en otro scope
print = 42       # ahora print es una variable global, no la función
print("hola")    # TypeError: 'int' object is not callable

# Para restaurarlo habría que hacer: del print
```

Este último ejemplo muestra por qué no se deben usar nombres de built-ins como nombres de variables — `list`, `dict`, `str`, `type`, `id` son errores frecuentes.

### 9.1.3. La sentencia global

La sentencia `global` indica a Python que una variable dentro de una función hace referencia a la variable global, en lugar de crear una nueva variable local. Sin `global`, cualquier asignación dentro de una función crea una variable local nueva.

```python
contador = 0

def incrementar():
    global contador
    contador += 1  # modifica la variable global, no crea una local

incrementar()
incrementar()
print(contador)  # 2
```

Sin la sentencia `global`, la línea `contador += 1` fallaría con `UnboundLocalError` — Python vería la asignación, marcaría `contador` como local, e intentaría leer su valor antes de asignarlo.

El uso de `global` es casi siempre una señal de diseño mejorable. Las funciones que dependen de estado global son difíciles de testear, de razonar y de mantener. En la mayoría de los casos, es mejor pasar el valor como argumento y devolver el resultado:

```python
# En lugar de global — recibir y devolver
def incrementar(contador):
    return contador + 1

contador = 0
contador = incrementar(contador)  # más predecible, más testeable
```

### 9.1.4. La sentencia nonlocal

`nonlocal` hace lo mismo que `global`, pero para el scope Enclosing en lugar del Global. Permite que una función anidada modifique una variable de la función que la contiene.

```python
def crear_contador():
    cuenta = 0

    def incrementar():
        nonlocal cuenta
        cuenta += 1
        return cuenta

    return incrementar

contador = crear_contador()
print(contador())  # 1
print(contador())  # 2
print(contador())  # 3
```

Sin `nonlocal`, la línea `cuenta += 1` dentro de `incrementar()` crearía una variable local `cuenta`, provocando `UnboundLocalError` al intentar leer su valor antes de asignarle uno.

La diferencia con `global` es clara:

- `global` apunta al scope del módulo (nivel superior)
- `nonlocal` apunta al scope de la función que contiene a la función actual

```python
x = "global"

def externa():
    x = "enclosing"

    def interna_con_global():
        global x
        x = "modificado por global"

    def interna_con_nonlocal():
        nonlocal x
        x = "modificado por nonlocal"

    interna_con_nonlocal()
    print(x)  # "modificado por nonlocal" — cambió la x de externa()

externa()
print(x)  # "global" — la x global no fue tocada por nonlocal

# Si ahora ejecutamos la otra:
def externa2():
    x = "enclosing"

    def interna_con_global():
        global x
        x = "modificado por global"

    interna_con_global()
    print(x)  # "enclosing" — la x de externa2() no cambió

externa2()
print(x)  # "modificado por global" — global sí modificó la del módulo
```

---

## 9.2. Closures

### 9.2.1. Funciones anidadas

Python permite definir funciones dentro de otras funciones. La función interna solo existe dentro del scope de la externa — no es accesible desde fuera.

```python
def saludar(nombre):
    def formatear():
        return nombre.upper()

    return f"Hola, {formatear()}"

print(saludar("ana"))  # "Hola, ANA"
print(formatear())     # NameError — no existe fuera de saludar()
```

Las funciones anidadas se usan para:
- Encapsular lógica auxiliar que solo tiene sentido dentro de la función contenedora
- Crear closures (sección siguiente)
- Construir decoradores (tema 10)

### 9.2.2. Qué es un closure y cómo se forma

Un closure se produce cuando una función anidada referencia variables del scope de la función que la contiene, **y esa función interna se devuelve o se pasa a otro lugar donde sobrevive más allá de la ejecución de la función externa**.

Normalmente, cuando una función termina de ejecutarse, sus variables locales desaparecen. Pero si una función interna las referencia y esa función interna sigue existiendo (porque fue devuelta, por ejemplo), Python mantiene esas variables vivas en un objeto especial llamado *cell*. La función interna junto con esas variables capturadas forma el closure.

```python
def crear_multiplicador(factor):
    def multiplicar(n):
        return n * factor  # referencia a 'factor' del scope de crear_multiplicador
    return multiplicar     # devuelve la función interna

doble = crear_multiplicador(2)
triple = crear_multiplicador(3)

print(doble(5))   # 10 — factor=2 sigue vivo en el closure
print(triple(5))  # 15 — factor=3 sigue vivo en otro closure independiente
```

Cuando `crear_multiplicador(2)` termina, la variable `factor` debería desaparecer. Pero `multiplicar` la referencia, así que Python la preserva. Cada llamada a `crear_multiplicador` crea un closure independiente con su propia copia del entorno.

Se puede inspeccionar el closure a través del atributo `__closure__`:

```python
print(doble.__closure__)             # (<cell at 0x...>,)
print(doble.__closure__[0].cell_contents)  # 2
print(triple.__closure__[0].cell_contents) # 3
```

No toda función anidada es un closure. Para que lo sea, deben cumplirse dos condiciones:
1. La función interna referencia variables del scope de la externa
2. La función interna sobrevive más allá de la ejecución de la externa

```python
# Esto NO es un closure — la función interna no referencia variables de la externa
def externa():
    def interna():
        return 42
    return interna

f = externa()
print(f.__closure__)  # None — no captura nada

# Esto SÍ es un closure
def externa(x):
    def interna():
        return x
    return interna

f = externa(10)
print(f.__closure__[0].cell_contents)  # 10
```

### 9.2.3. Late binding en closures (la trampa del for + lambda)

Los closures capturan **referencias** a variables, no sus valores. Esto significa que el valor que ve el closure es el que tiene la variable **en el momento de la llamada**, no en el momento en que se definió la función. Esta diferencia entre capturar la referencia y capturar el valor es la fuente de uno de los bugs más comunes en Python.

El caso clásico ocurre al crear funciones dentro de un bucle:

```python
funciones = []
for i in range(3):
    funciones.append(lambda: i)

# Uno esperaría [0, 1, 2], pero:
print([f() for f in funciones])  # [2, 2, 2]
```

Las tres lambdas capturan una referencia a la **misma variable** `i`. Cuando el bucle termina, `i` vale 2, y las tres funciones devuelven ese valor al ser llamadas.

La solución estándar es capturar el valor actual como argumento por defecto. Los argumentos por defecto se evalúan en el momento de la definición de la función, no en el momento de la llamada:

```python
funciones = []
for i in range(3):
    funciones.append(lambda i=i: i)  # i=i captura el VALOR actual

print([f() for f in funciones])  # [0, 1, 2]
```

El parámetro `i=i` crea un nuevo ámbito local para cada lambda con el valor que `i` tenía en esa iteración. Es la misma mecánica de los argumentos por defecto vista en el tema 7 — se evalúan una sola vez, al definir la función.

Este problema no es exclusivo de `lambda` — ocurre con cualquier función definida dentro de un bucle:

```python
# El mismo problema con def
funciones = []
for i in range(3):
    def f():
        return i
    funciones.append(f)

print([f() for f in funciones])  # [2, 2, 2]

# La misma solución
funciones = []
for i in range(3):
    def f(i=i):
        return i
    funciones.append(f)

print([f() for f in funciones])  # [0, 1, 2]
```

### 9.2.4. Casos de uso de closures

Los closures son útiles en situaciones donde se necesita crear funciones con comportamiento personalizado basado en parámetros de configuración.

**Funciones fábrica** — crear variantes de una función con parámetros preconfigurados:

```python
def crear_saludo(idioma):
    saludos = {"es": "Hola", "en": "Hello", "fr": "Bonjour"}
    saludo = saludos.get(idioma, "Hi")

    def saludar(nombre):
        return f"{saludo}, {nombre}"

    return saludar

saludar_es = crear_saludo("es")
saludar_en = crear_saludo("en")

print(saludar_es("Ana"))    # "Hola, Ana"
print(saludar_en("Ana"))    # "Hello, Ana"
```

**Acumuladores y contadores** — mantener estado entre llamadas sin usar variables globales ni clases:

```python
def crear_acumulador(inicial=0):
    total = [inicial]  # lista para poder mutar sin nonlocal

    def agregar(valor):
        total[0] += valor
        return total[0]

    return agregar

acumulador = crear_acumulador()
print(acumulador(10))  # 10
print(acumulador(5))   # 15
print(acumulador(3))   # 18

# Alternativa más clara con nonlocal
def crear_acumulador(inicial=0):
    total = inicial

    def agregar(valor):
        nonlocal total
        total += valor
        return total

    return agregar
```

**Caché simple** — recordar resultados de operaciones previas:

```python
def con_cache(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

@con_cache  # esto es un decorador, se explica en el tema 10
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Este último ejemplo muestra la conexión directa entre closures y decoradores. El patrón de envolver una función dentro de otra, capturando la función original en el closure, es la base de los decoradores que se estudian en el siguiente tema.
