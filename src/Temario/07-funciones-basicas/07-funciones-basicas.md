# 7. Funciones Básicas

Las funciones son bloques de código reutilizables que realizan una tarea concreta. En lugar de repetir el mismo código cada vez que se necesita, se define una función una vez y se la llama cuantas veces haga falta, pudiendo pasarle datos distintos en cada llamada.

Las funciones son fundamentales en cualquier programa que supere unas pocas líneas. Permiten organizar el código en piezas pequeñas y manejables, cada una con una responsabilidad clara. Esto hace que el código sea más fácil de leer, de mantener y de depurar: si algo falla, se sabe exactamente dónde buscar.

Hasta ahora, todo el código de los temas anteriores ha sido secuencial (se ejecuta de arriba a abajo). Las funciones introducen un cambio importante: permiten **definir** código que no se ejecuta inmediatamente, sino solo cuando se **llama** a la función.

---

## 7.1. Definición y llamada

### 7.1.1. Sintaxis básica

Una función se define con la palabra clave `def`, seguida del nombre de la función, paréntesis (que pueden contener parámetros) y dos puntos. El cuerpo de la función va indentado:

```python
def saludar():
    print("Hola, mundo")
```

Este código **define** la función pero no la ejecuta. Para ejecutarla, hay que **llamarla** usando su nombre seguido de paréntesis:

```python
saludar()   # Hola, mundo
saludar()   # Hola, mundo — se puede llamar cuantas veces se quiera
```

Sin los paréntesis, `saludar` es solo una referencia al objeto función, no una llamada. Es un error frecuente de principiantes olvidar los paréntesis y no entender por qué no se ejecuta nada.

### 7.1.2. Pasar datos a una función

Los parámetros son variables que se declaran en la definición de la función. Los argumentos son los valores concretos que se pasan al llamarla. En la práctica, muchas veces se usan ambos términos de forma intercambiable, pero la distinción es útil para entender la documentación de Python.

```python
def saludar(nombre):        # "nombre" es el parámetro
    print(f"Hola, {nombre}")

saludar("Ana")              # "Ana" es el argumento
saludar("Pedro")            # "Pedro" es el argumento
```

Una función puede tener múltiples parámetros, separados por comas:

```python
def presentar(nombre, edad, ciudad):
    print(f"{nombre} tiene {edad} años y vive en {ciudad}")

presentar("Ana", 28, "Madrid")
```

### 7.1.3. La sentencia `return`

`return` hace dos cosas: devuelve un valor al código que llamó a la función y termina la ejecución de la función inmediatamente. Cualquier código después de un `return` no se ejecuta.

```python
def sumar(a, b):
    return a + b

resultado = sumar(3, 5)
print(resultado)  # 8
```

La diferencia entre `print()` y `return` es fundamental y una fuente constante de confusión para principiantes. `print()` muestra un valor en la consola pero no lo devuelve; `return` devuelve el valor al código que llamó a la función, donde se puede almacenar en una variable, usar en una expresión o pasar a otra función:

```python
def doble(n):
    return n * 2

# El valor retornado se puede usar directamente
print(doble(5))           # 10
total = doble(3) + doble(4)  # 6 + 8 = 14
```

Si una función no tiene `return` (o tiene `return` sin valor), devuelve `None` implícitamente:

```python
def saludar(nombre):
    print(f"Hola, {nombre}")

resultado = saludar("Ana")  # Imprime "Hola, Ana"
print(resultado)             # None
```

### 7.1.4. Retorno múltiple

Una función puede devolver varios valores separándolos con comas. Python los empaqueta automáticamente en una tupla:

```python
def dividir(a, b):
    cociente = a // b
    resto = a % b
    return cociente, resto

resultado = dividir(17, 5)
print(resultado)       # (3, 2) — es una tupla
print(type(resultado)) # <class 'tuple'>
```

Lo habitual es desempaquetar los valores directamente al recibirlos, usando el desempaquetado de tuplas visto en el tema 3:

```python
cociente, resto = dividir(17, 5)
print(cociente)  # 3
print(resto)     # 2
```

---

## 7.2. Parámetros y argumentos

### 7.2.1. Argumentos posicionales y por nombre (keyword)

Al llamar a una función, los argumentos se pueden pasar de dos formas:

- **Posicionales**: se asignan según su posición (el primero al primer parámetro, el segundo al segundo, etc.)
- **Por nombre (keyword)**: se especifica explícitamente a qué parámetro corresponde cada valor

```python
def crear_perfil(nombre, edad, ciudad):
    print(f"{nombre}, {edad} años, {ciudad}")

# Posicionales — el orden importa
crear_perfil("Ana", 28, "Madrid")

# Por nombre — el orden no importa
crear_perfil(ciudad="Madrid", nombre="Ana", edad=28)

# Mixto — los posicionales van primero, los de nombre después
crear_perfil("Ana", ciudad="Madrid", edad=28)
```

Los argumentos por nombre hacen el código más legible, especialmente cuando una función tiene varios parámetros o cuando el significado de un argumento no es obvio por su valor:

```python
# Sin nombres — ¿qué significan True y False?
configurar_conexion("servidor.com", 8080, True, False)

# Con nombres — queda claro
configurar_conexion("servidor.com", 8080, ssl=True, verbose=False)
```

### 7.2.2. Valores por defecto

Los parámetros pueden tener valores por defecto, que se usan cuando no se pasa un argumento para ese parámetro. Se definen con `=` en la firma de la función:

```python
def saludar(nombre, saludo="Hola"):
    print(f"{saludo}, {nombre}")

saludar("Ana")              # Hola, Ana — usa el valor por defecto
saludar("Ana", "Buenos días")  # Buenos días, Ana — sobrescribe el valor por defecto
```

Los parámetros con valor por defecto deben ir **después** de los que no lo tienen. De lo contrario, Python no sabría cómo asignar los argumentos posicionales:

```python
# MAL — SyntaxError
def saludar(saludo="Hola", nombre):
    print(f"{saludo}, {nombre}")

# BIEN — parámetros sin defecto primero
def saludar(nombre, saludo="Hola"):
    print(f"{saludo}, {nombre}")
```

> **Advertencia importante:** nunca usar objetos mutables (listas, diccionarios, sets) como valores por defecto. El objeto se crea una sola vez cuando se define la función y se comparte entre todas las llamadas, lo que produce efectos inesperados:

```python
# MAL — la lista se comparte entre llamadas
def agregar_item(item, lista=[]):
    lista.append(item)
    return lista

print(agregar_item("a"))  # ['a']
print(agregar_item("b"))  # ['a', 'b'] — ¡no es ['b']!

# BIEN — usar None y crear la lista dentro
def agregar_item(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

### 7.2.3. `*args`: argumentos posicionales variables

A veces una función necesita aceptar un número variable de argumentos posicionales. El parámetro `*args` recoge todos los argumentos posicionales adicionales en una **tupla**:

```python
def sumar_todos(*args):
    total = 0
    for numero in args:
        total += numero
    return total

print(sumar_todos(1, 2, 3))       # 6
print(sumar_todos(10, 20, 30, 40)) # 100
print(sumar_todos())               # 0
```

El nombre `args` es una convención, no un requisito. Lo que importa es el `*`. Pero usar `args` hace el código reconocible para otros programadores.

`*args` se puede combinar con parámetros normales. Los parámetros normales se asignan primero y `*args` recoge el resto:

```python
def mostrar_info(titulo, *valores):
    print(f"{titulo}:")
    for valor in valores:
        print(f"  - {valor}")

mostrar_info("Frutas", "manzana", "pera", "naranja")
# Frutas:
#   - manzana
#   - pera
#   - naranja
```

### 7.2.4. `**kwargs`: argumentos por nombre variables

De la misma forma que `*args` recoge posicionales adicionales, `**kwargs` recoge argumentos por nombre adicionales en un **diccionario**:

```python
def mostrar_datos(**kwargs):
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar_datos(nombre="Ana", edad=28, ciudad="Madrid")
# nombre: Ana
# edad: 28
# ciudad: Madrid
```

Al igual que con `args`, el nombre `kwargs` es una convención. Lo que importa es el `**`.

Se pueden combinar parámetros normales, `*args` y `**kwargs` en la misma función. El orden obligatorio es:

1. Parámetros normales
2. `*args`
3. `**kwargs`

```python
def funcion_completa(obligatorio, *args, **kwargs):
    print(f"Obligatorio: {obligatorio}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

funcion_completa("hola", 1, 2, 3, color="rojo", tamano=5)
# Obligatorio: hola
# Args: (1, 2, 3)
# Kwargs: {'color': 'rojo', 'tamano': 5}
```

### 7.2.5. Desempaquetado de argumentos con `*` y `**`

Los operadores `*` y `**` también se pueden usar al **llamar** a una función para desempaquetar una lista/tupla o un diccionario como argumentos:

```python
def sumar(a, b, c):
    return a + b + c

numeros = [1, 2, 3]
print(sumar(*numeros))  # 6 — equivale a sumar(1, 2, 3)

datos = {"a": 10, "b": 20, "c": 30}
print(sumar(**datos))   # 60 — equivale a sumar(a=10, b=20, c=30)
```

Esto es útil cuando los datos ya están en una lista o diccionario y se quieren pasar como argumentos individuales sin extraerlos manualmente.

### 7.2.6. Parámetros solo posicionales y solo keyword

Hasta ahora, todos los parámetros vistos se pueden pasar indistintamente por posición o por nombre. Python permite restringir esto mediante dos símbolos especiales en la firma de la función: `/` para forzar que ciertos parámetros se pasen **solo por posición**, y `*` para forzar que se pasen **solo por nombre**. Estas restricciones existen para mejorar la legibilidad de las llamadas y para dar libertad al autor de la función a la hora de renombrar parámetros sin romper código existente.

**Parámetros solo keyword (después de `*`)**

Todo parámetro que vaya después de un `*` solo en la lista de parámetros debe pasarse obligatoriamente por nombre. Esto es útil cuando los argumentos no tienen un orden obvio y se quiere forzar legibilidad en las llamadas, evitando que alguien escriba `crear_usuario("Ana", 28, False)` sin saber qué significa cada valor.

```python
def crear_usuario(nombre, *, edad, activo=True):
    print(f"{nombre}, {edad} años, activo={activo}")

# BIEN — edad y activo deben pasarse por nombre
crear_usuario("Ana", edad=28)
crear_usuario("Ana", edad=28, activo=False)

# MAL — TypeError: edad es solo keyword
# crear_usuario("Ana", 28)
```

**Parámetros solo posicionales (antes de `/`)**

Disponibles desde Python 3.8. Todo parámetro que vaya antes de `/` solo se puede pasar por posición, nunca por nombre. Esto es útil cuando los nombres de los parámetros son irrelevantes para quien llama, o cuando el autor quiere poder renombrarlos en el futuro sin romper código que los esté pasando por nombre.

```python
def potencia(base, exponente, /):
    return base ** exponente

# BIEN — solo por posición
print(potencia(2, 10))  # 1024

# MAL — TypeError: no se pueden pasar por nombre
# print(potencia(base=2, exponente=10))
```

**Combinación de los tres tipos**

Se pueden combinar parámetros solo posicionales, parámetros normales y parámetros solo keyword en la misma función. El orden obligatorio es: primero los solo posicionales, luego `/`, luego los normales (que aceptan ambas formas), luego `*`, y finalmente los solo keyword.

```python
def funcion(pos_only, /, normal, *, kw_only):
    print(f"{pos_only}, {normal}, {kw_only}")

# BIEN
funcion(1, 2, kw_only=3)
funcion(1, normal=2, kw_only=3)

# MAL
# funcion(pos_only=1, normal=2, kw_only=3)  → TypeError
# funcion(1, 2, 3)                          → TypeError
```

Este patrón aparece en muchas funciones de la biblioteca estándar de Python. Por ejemplo, `len(obj, /)` obliga a pasar el argumento por posición — no se puede llamar como `len(obj=[1, 2, 3])`.

---

## 7.3. Docstrings

Un docstring es un string literal que se coloca como primera sentencia del cuerpo de una función. Sirve para documentar qué hace la función, qué parámetros recibe y qué devuelve. No es un comentario: Python lo almacena como atributo `__doc__` de la función y lo usan herramientas como `help()` y los IDEs para mostrar información contextual.

```python
def calcular_area(base, altura):
    """Calcula el área de un triángulo.

    Args:
        base: La base del triángulo.
        altura: La altura del triángulo.

    Returns:
        El área del triángulo.
    """
    return (base * altura) / 2
```

Para funciones simples, basta un docstring de una línea:

```python
def doble(n):
    """Devuelve el doble del número recibido."""
    return n * 2
```

El docstring se puede consultar con `help()` o accediendo al atributo `__doc__`:

```python
help(doble)         # Muestra la documentación de la función
print(doble.__doc__) # "Devuelve el doble del número recibido."
```

Las convenciones más usadas para docstrings son:
- **Google style**: usa `Args:`, `Returns:`, `Raises:` (la que se muestra arriba)
- **NumPy style**: usa secciones con guiones como `Parameters`, `Returns`
- **reStructuredText**: usa directivas como `:param nombre:`, `:return:`

Lo importante es elegir un estilo y mantenerlo consistente en todo el proyecto.

---

## 7.4. Funciones como objetos

En Python, las funciones son **objetos de primera clase**. Esto significa que se pueden tratar como cualquier otro valor: asignarlas a variables, guardarlas en listas o diccionarios, y pasarlas como argumento a otras funciones. Este concepto es la base de técnicas avanzadas que se verán en temas posteriores (funciones de orden superior, decoradores, callbacks).

### 7.4.1. Asignar funciones a variables

Como una función es un objeto, su nombre es simplemente una variable que apunta a ese objeto. Se puede asignar a otra variable sin llamarla (sin paréntesis):

```python
def saludar(nombre):
    return f"Hola, {nombre}"

# "mi_funcion" ahora apunta al mismo objeto función que "saludar"
mi_funcion = saludar
print(mi_funcion("Ana"))  # Hola, Ana
```

### 7.4.2. Funciones en estructuras de datos

Las funciones se pueden almacenar en listas, diccionarios o cualquier otra estructura:

```python
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

operaciones = {
    "+": sumar,
    "-": restar,
    "*": multiplicar,
}

operacion = "+"
resultado = operaciones[operacion](10, 3)
print(resultado)  # 13
```

Este patrón es una alternativa a largas cadenas de `if/elif` para seleccionar comportamiento según un valor. Es más limpio y más fácil de extender.

### 7.4.3. Funciones como argumento

Una función se puede pasar como argumento a otra función. Esto es útil cuando se quiere que una función aplique una operación que no conoce de antemano:

```python
def aplicar_a_lista(lista, operacion):
    resultado = []
    for elemento in lista:
        resultado.append(operacion(elemento))
    return resultado

def doble(n):
    return n * 2

def cuadrado(n):
    return n ** 2

numeros = [1, 2, 3, 4, 5]
print(aplicar_a_lista(numeros, doble))     # [2, 4, 6, 8, 10]
print(aplicar_a_lista(numeros, cuadrado))  # [1, 4, 9, 16, 25]
```

Las funciones built-in `sorted()`, `max()` y `min()` usan este patrón con su parámetro `key`:

```python
nombres = ["Ana", "Pedro", "Bo", "Alejandra"]

# Ordenar por longitud del nombre
ordenados = sorted(nombres, key=len)
print(ordenados)  # ['Bo', 'Ana', 'Pedro', 'Alejandra']
```

---

## 7.5. Buenas prácticas

### 7.5.1. Una función, una tarea

Cada función debe hacer **una sola cosa** y hacerla bien. Si una función hace demasiadas cosas, es difícil de entender, de probar y de reutilizar. Una buena señal de que una función hace demasiado es que necesita un `and` en su descripción ("esta función valida los datos **y** los guarda **y** envía un email").

```python
# MAL — hace tres cosas
def procesar_pedido(pedido):
    # Valida
    if pedido["total"] <= 0:
        print("Error: total inválido")
        return
    # Aplica descuento
    if pedido["total"] > 100:
        pedido["total"] *= 0.9
    # Imprime resumen
    print(f"Pedido procesado: {pedido['total']}")

# BIEN — cada función hace una cosa
def es_pedido_valido(pedido):
    return pedido["total"] > 0

def aplicar_descuento(total, umbral=100, porcentaje=0.1):
    if total > umbral:
        return total * (1 - porcentaje)
    return total

def imprimir_resumen(total):
    print(f"Pedido procesado: {total}")
```

### 7.5.2. Nombres descriptivos

El nombre de una función debe describir lo que hace. Los verbos son la convención: `calcular_total()`, `validar_email()`, `obtener_usuario()`. Para funciones que devuelven booleanos, se suelen usar prefijos como `es_`, `tiene_`, `puede_`:

```python
def es_par(n):
    return n % 2 == 0

def tiene_permiso(usuario, accion):
    return accion in usuario["permisos"]
```

### 7.5.3. Evitar efectos secundarios inesperados

Una función es más predecible cuando su resultado depende solo de sus argumentos y no modifica estado externo. Si una función necesita modificar algo, debe ser evidente por su nombre y su documentación:

```python
# MAL — modifica la lista original sin que el nombre lo sugiera
def obtener_ordenados(lista):
    lista.sort()  # Modifica la lista original
    return lista

# BIEN — no modifica la original
def obtener_ordenados(lista):
    return sorted(lista)  # Crea una lista nueva
```
