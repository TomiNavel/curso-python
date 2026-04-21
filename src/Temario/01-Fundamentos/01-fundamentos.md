# 1. Fundamentos de Python

## 1.1. Instalación y Primer Programa

### 1.1.1. Qué es Python

Python es un lenguaje de programación interpretado, de propósito general y tipado dinámico. Fue creado por Guido van Rossum y publicado en 1991, con el objetivo de priorizar la legibilidad del código sobre la concisión sintáctica.

Su filosofía central está recogida en el documento **PEP 20** ("The Zen of Python"), cuyo principio más conocido es: *"Explicit is better than implicit"*. Python fuerza al programador a escribir código claro y estructurado, lo que reduce los errores y facilita el mantenimiento.

Es especialmente relevante hoy por tres razones:

- **Domina en Data Science e IA**: NumPy, Pandas, TensorFlow, PyTorch y scikit-learn están escritos para Python. No hay alternativa real en ese ecosistema.
- **Versátil**: sirve para scripting, automatización, APIs backend (Django, FastAPI), análisis de datos y CLIs.
- **Alta demanda laboral**: es consistentemente el lenguaje más solicitado en ofertas de trabajo según encuestas de Stack Overflow y GitHub.

**Python 2 vs Python 3** — Python 2 llegó a su fin de vida en enero de 2020. No hay razón para usarlo en proyectos nuevos. Las diferencias clave: en Python 3, `print` es una función (`print("hola")`), la división `/` devuelve float (`5 / 2 → 2.5`), los strings son Unicode por defecto, y `range()` devuelve un iterador en lugar de una lista.

### 1.1.2. Instalación de Python

Python se instala desde [python.org](https://python.org). Al instalar, es importante marcar la opción **"Add Python to PATH"** para poder ejecutarlo desde la terminal.

```bash
# Verificar la instalación
python --version   # Python 3.x.x
python3 --version  # en macOS/Linux
```

El ecosistema de Python gira en torno a dos herramientas base:

- **`python`** (o `python3`): el intérprete que ejecuta código
- **`pip`**: el gestor de paquetes que instala librerías de terceros desde [PyPI](https://pypi.org)

### 1.1.3. El intérprete y ejecutar scripts

Python puede ejecutarse de dos formas: en modo interactivo (el intérprete) o ejecutando un archivo `.py`.

```bash
# Modo interactivo — abre un prompt donde escribir código línea a línea
python
>>> print("Hola mundo")
Hola mundo
>>> 2 + 3
5
>>> exit()

# Ejecutar un script — crea un archivo .py y ejecútalo
python mi_script.py
```

El modo interactivo es útil para probar cosas rápidas. Para código real, siempre se trabaja con archivos `.py`.

### 1.1.4. Entorno de trabajo y gestión de paquetes

Cuando se instala una librería con `pip install`, se instala de forma global en el sistema. Esto genera conflictos cuando distintos proyectos necesitan versiones diferentes de la misma librería.

La solución son los **entornos virtuales**: instalaciones de Python aisladas por proyecto. Cada entorno tiene sus propios paquetes y no interfiere con otros proyectos.

```bash
# Crear un entorno virtual con venv (incluido en Python 3)
python -m venv .venv

# Activar el entorno
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instalar paquetes dentro del entorno
pip install requests

# Guardar las dependencias del proyecto
pip freeze > requirements.txt

# Instalar dependencias en otro entorno
pip install -r requirements.txt

# Desactivar el entorno
deactivate
```

En proyectos profesionales **siempre** se trabaja dentro de un entorno virtual. La carpeta `.venv` no se sube al repositorio — se añade al `.gitignore`.

Existen herramientas más avanzadas como **Poetry** (gestión moderna de dependencias) o **conda** (orientado a Data Science), pero `venv` + `pip` es suficiente para empezar y se usa en la mayoría de proyectos.

## 1.2. Sintaxis Básica

### 1.2.1. Indentación y estructura

En la mayoría de lenguajes, los bloques de código se delimitan con llaves `{}` o palabras clave como `begin`/`end`. Python usa la **indentación** como parte de la sintaxis. No es una convención estética — es obligatoria y el intérprete la enforza.

Un bloque de código comienza después de los dos puntos `:` y todo lo que pertenece a ese bloque debe tener el mismo nivel de indentación. El bloque termina cuando la indentación vuelve al nivel anterior.

```python
# Los dos puntos abren un bloque
if temperatura > 30:
    print("hace calor")   # este código pertenece al if
    print("lleva agua")   # este también
print("siempre se ejecuta")  # fuera del if, nivel base

# Bloques anidados: cada nivel añade 4 espacios
if usuario_activo:
    if precio > 100:
        print("descuento aplicado")
    print("usuario procesado")
print("fin")
```

El estándar (PEP 8) es usar **4 espacios** por nivel. No mezclar espacios y tabulaciones — Python 3 lanza un error si lo haces.

### 1.2.2. Comentarios y docstrings

Python tiene dos mecanismos distintos para documentar código, con propósitos diferentes.

Los **comentarios** (`#`) son para el programador que lee el código. El intérprete los ignora completamente. Se usan para explicar el razonamiento detrás de una decisión no obvia.

```python
# Calcular el IVA sobre el precio base
precio_final = precio_base * 1.21

resultado = valor ** 0.5  # raíz cuadrada usando exponente fraccionario
```

Los **docstrings** son cadenas de texto que documentan módulos, clases y funciones. Se escriben como primer elemento del cuerpo usando comillas triples `"""`. A diferencia de los comentarios, los docstrings son accesibles en tiempo de ejecución a través del atributo `__doc__`, y son los que usan herramientas como `help()`, IDEs y generadores de documentación automática.

```python
"""
Este es un docstring de módulo.
Describe el propósito del archivo.
"""

# Los docstrings se verán en detalle cuando se estudien funciones y clases.
# Por ahora, basta con saber que existen y que usan comillas triples.
```

### 1.2.3. Variables y constantes

En Python las variables no se declaran — simplemente se asignan. El intérprete infiere el tipo en el momento de la asignación y puede cambiar en cualquier momento (tipado dinámico).

```python
# Asignación simple — no hace falta declarar el tipo
nombre = "Ana"
edad = 28
activo = True

# La misma variable puede cambiar de tipo (aunque raramente es buena idea)
x = 10
x = "ahora soy un string"  # válido en Python, confuso en la práctica

# Asignación múltiple en una línea
a, b, c = 1, 2, 3

# Intercambio de valores sin variable temporal (idioma Python)
a, b = b, a
```

Python no tiene constantes reales — no hay una palabra clave `const` que impida la reasignación. Por convención, las constantes se escriben en `MAYÚSCULAS_CON_GUIONES`. Es una señal para otros programadores de que ese valor no debe modificarse, pero el lenguaje no lo enforza.

```python
# Constantes por convención
MAX_CONEXIONES = 100
TIMEOUT_SEGUNDOS = 30
BASE_URL = "https://api.ejemplo.com"
```

### 1.2.4. Convenciones de nombres (PEP 8)

PEP 8 es la guía de estilo oficial de Python. Define cómo nombrar variables, funciones, clases y módulos para que el código sea consistente y legible. En entrevistas se asume que conoces y aplicas PEP 8.

| Elemento | Convención | Ejemplo |
|---|---|---|
| Variables y funciones | `snake_case` | `nombre_usuario`, `calcular_total()` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_INTENTOS`, `BASE_URL` |
| Clases | `PascalCase` | `UsuarioPremium`, `ConexionDB` |
| Módulos y paquetes | `snake_case` minúsculo | `mi_modulo.py`, `utils/` |
| Métodos privados | `_nombre` (un guion bajo) | `_validar_email()` |
| Nombres reservados (evitar colisión) | `nombre_` (guion al final) | `type_`, `list_` |

Los guiones bajos en `_nombre` no impiden el acceso externo — es solo una convención que comunica "este atributo es un detalle de implementación, no parte de la API pública".

## 1.3. Tipos de Datos Primitivos

Python tiene cuatro tipos primitivos: números (en tres variantes), strings, booleanos y `None`. Son los bloques básicos con los que se construye cualquier programa.

### 1.3.1. Números (int, float, complex)

Python distingue tres tipos numéricos con comportamientos distintos.

**`int`** representa enteros de precisión arbitraria. A diferencia de Java o C, en Python un `int` no tiene límite de tamaño — puede representar números tan grandes como la memoria lo permita. No hay desbordamiento.

```python
edad = 28
poblacion_mundial = 8_100_000_000  # los guiones bajos mejoran la legibilidad
resultado = 2 ** 100               # número enorme, Python lo maneja sin problema

print(type(edad))  # <class 'int'>
```

**`float`** representa números decimales usando punto flotante de doble precisión (64 bits, estándar IEEE 754). Esto implica que algunos decimales no pueden representarse de forma exacta en binario — un detalle que aparece frecuentemente en entrevistas.

```python
precio = 9.99
pi = 3.14159

# Trampa clásica de entrevista: imprecisión de punto flotante
print(0.1 + 0.2)         # 0.30000000000000004, no 0.3
print(0.1 + 0.2 == 0.3)  # False

# Solución para comparar floats: usar round() o math.isclose()
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# Para dinero y precisión exacta, usar el módulo decimal
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))  # 0.3, exacto
```

**`complex`** representa números complejos con parte real e imaginaria. Se usa en cálculos matemáticos y de ingeniería. En la mayoría de aplicaciones web o de datos no se necesita, pero es parte del lenguaje.

```python
z = 3 + 4j      # j es la unidad imaginaria en Python (no i)
print(z.real)   # 3.0
print(z.imag)   # 4.0
print(abs(z))   # 5.0 — módulo del número complejo
```

**Conversión entre tipos numéricos:**

```python
x = int(3.9)    # 3 — trunca, no redondea
y = float(5)    # 5.0
z = round(3.9)  # 4 — redondeo estándar
```

### 1.3.2. Built-ins numéricas (abs, round, pow, divmod, bin, hex, oct)

Python incluye varias funciones predefinidas para trabajar con números. Son **built-ins**: están siempre disponibles, no hay que importar nada. Aquí se presentan como herramientas que el lenguaje ofrece. El concepto de qué es una función y cómo definir las propias se cubre en el tema 7.

**`abs(x)`** devuelve el valor absoluto de un número (su distancia al cero, siempre positivo). Funciona con `int`, `float` y `complex` (en este último devuelve el módulo).

```python
print(abs(-7))      # 7
print(abs(3.14))    # 3.14
print(abs(-2.5))    # 2.5
```

**`round(x, n)`** redondea un número al entero más cercano, o a `n` decimales si se especifica el segundo argumento. Usa redondeo bancario (banker's rounding): cuando el dígito a redondear es exactamente 5, redondea al par más cercano.

```python
print(round(3.7))       # 4
print(round(3.4))       # 3
print(round(3.14159, 2)) # 3.14
print(round(2.5))       # 2 — no 3, redondea al par más cercano
print(round(3.5))       # 4 — también al par
```

**`pow(base, exponente)`** calcula `base` elevada a `exponente`. Equivale al operador `**`, pero acepta un tercer argumento opcional para calcular el módulo de forma eficiente (útil en criptografía).

```python
print(pow(2, 10))       # 1024 — equivale a 2 ** 10
print(pow(2, 10, 1000)) # 24 — (2 ** 10) % 1000, calculado eficientemente
```

**`divmod(a, b)`** devuelve una tupla `(cociente, resto)` con el resultado de la división entera y el módulo en una sola operación. Es más eficiente que calcular `a // b` y `a % b` por separado.

```python
print(divmod(17, 5))    # (3, 2) — 17 dividido entre 5 es 3 con resto 2

# Útil para convertir segundos a minutos y segundos
segundos = 125
minutos, segs = divmod(segundos, 60)
print(f"{minutos}m {segs}s")  # 2m 5s
```

**`bin(x)`**, **`hex(x)`** y **`oct(x)`** convierten un entero a su representación en binario, hexadecimal u octal, respectivamente. Devuelven un `str` con un prefijo que indica la base: `0b` para binario, `0x` para hexadecimal y `0o` para octal. Estas funciones aparecen con frecuencia en problemas de manipulación de bits, criptografía y entrevistas técnicas.

```python
print(bin(10))      # '0b1010'
print(hex(255))     # '0xff'
print(oct(8))       # '0o10'

# Solo aceptan enteros — pasar un float lanza TypeError
# print(bin(3.14))  # TypeError

# Para obtener el resultado sin el prefijo, usar slicing
print(bin(10)[2:]) # '1010'
print(hex(255)[2:]) # 'ff'
```

Python también permite escribir literales numéricos directamente en estas bases con los mismos prefijos. El intérprete los almacena internamente como `int` normales — la base solo afecta a la forma de escribirlos, no a su representación en memoria.

```python
binario = 0b1010    # 10 en decimal
hexa = 0xff         # 255 en decimal
octal = 0o10        # 8 en decimal

print(binario, hexa, octal)  # 10 255 8
```

### 1.3.3. Strings (creación y características básicas) 

Un string en Python es una secuencia inmutable de caracteres Unicode. Se puede definir con comillas simples, dobles o triples — no hay diferencia funcional entre `'texto'` y `"texto"`.

```python
nombre = "Ana"
mensaje = 'Hola mundo'
multilinea = """Este string
ocupa varias
líneas"""
```

**f-strings** son la forma moderna y recomendada de interpolar valores en strings. Introducidos en Python 3.6, son más legibles y eficientes que `%` o `.format()`.

```python
nombre = "Ana"
edad = 28

# f-string — prefijo f antes de las comillas
saludo = f"Hola, {nombre}. Tienes {edad} años."

# Permite expresiones dentro de {}
precio = 9.99
print(f"Total con IVA: {precio * 1.21:.2f}€")  # formatea a 2 decimales
```

La **inmutabilidad** de los strings significa que ningún método modifica el string original — siempre devuelven uno nuevo. Este concepto es fundamental y se profundiza en el tema 2 junto con todos los métodos de strings, slicing y operaciones.

```python
saludo = "hola"
saludo.upper()       # no modifica saludo, devuelve un nuevo string "HOLA"
print(saludo)        # "hola" — sin cambios

saludo = saludo.upper()  # hay que reasignar para conservar el resultado
```

### 1.3.4. Booleanos y truthiness

`bool` es un subtipo de `int` en Python. `True` vale `1` y `False` vale `0`. Esto no es un detalle menor — tiene consecuencias prácticas.

```python
print(True + True)   # 2
print(True * 5)      # 5
print(False + 1)     # 1

# Se puede usar en contextos numéricos
votos = [True, False, True, True, False]
print(sum(votos))    # 3 — cuenta los True
```

**Truthy y Falsy** — en Python, cualquier valor puede evaluarse en un contexto booleano. Esto permite escribir condiciones más concisas pero puede ser fuente de bugs si no se entiende bien.

Los valores que se evalúan como `False` (valores **falsy**):
- `False`, `None`
- `0`, `0.0`
- Colecciones vacías: `""`, `[]`, `{}`, `set()`, `()`

Todo lo demás es `True` (valor **truthy**).

```python
nombre = ""
if nombre:                    # equivale a: if nombre != ""
    print(f"Hola, {nombre}")
else:
    print("Nombre vacío")     # se ejecuta este

lista = []
if not lista:                 # si la lista está vacía
    print("No hay elementos")
```

### 1.3.5. None

`None` es el valor que representa la **ausencia de valor**. Es el equivalente Python de `null` en otros lenguajes. Existe como un único objeto singleton — solo hay un `None` en todo el proceso de Python.

```python
# Inicialización de una variable cuyo valor se asignará más adelante
conexion = None

# Comprobar si una variable es None — siempre con 'is', nunca con '=='
if conexion is None:
    print("No hay conexión")
```

**`is None` vs `== None`** — para comparar con `None` siempre se usa `is`, nunca `==`. La razón: `is` compara identidad de objeto (si son el mismo objeto en memoria), mientras que `==` compara valor y puede ser sobreescrito. Como `None` es un singleton, `is None` siempre funciona correctamente. PEP 8 lo exige explícitamente.

### 1.3.6. Conversión de tipos (int, float, str, bool)

Python es de tipado dinámico, pero no convierte tipos automáticamente en la mayoría de operaciones. Si se intenta concatenar un string con un número, Python lanza un `TypeError` en lugar de convertir de forma implícita como haría JavaScript. Esto obliga al programador a convertir de forma explícita, lo que evita bugs silenciosos.

Las cuatro funciones de conversión básicas son `int()`, `float()`, `str()` y `bool()`. Cada una acepta distintos tipos de entrada y tiene sus propias reglas.

```python
# str → int: el string debe contener un número entero válido
int("42")       # 42
int("3.14")     # ValueError — no acepta decimales en string
int("hola")     # ValueError — no es un número

# str → float: acepta enteros y decimales
float("3.14")   # 3.14
float("42")     # 42.0
float("inf")    # inf — Python reconoce infinito

# float → int: trunca la parte decimal, no redondea
int(3.9)        # 3
int(-3.9)       # -3 — trunca hacia cero, no hacia abajo

# Cualquier tipo → str: siempre funciona
str(42)         # "42"
str(3.14)       # "3.14"
str(True)       # "True"
str(None)       # "None"

# Cualquier tipo → bool: aplica las reglas de truthiness
bool(0)         # False
bool(42)        # True
bool("")        # False
bool("hola")    # True
bool([])        # False
bool([1, 2])    # True
bool(None)      # False
```

La conversión `int()` también acepta una base como segundo argumento, útil para trabajar con sistemas numéricos:

```python
int("1010", 2)   # 10 — binario a decimal
int("ff", 16)    # 255 — hexadecimal a decimal
int("77", 8)     # 63 — octal a decimal
```

Un error común en entrevistas es intentar convertir directamente la entrada del usuario sin validar:

```python
# input() siempre devuelve str
edad = input("Edad: ")       # "28" — es un string
print(edad + 1)              # TypeError: no se puede sumar str + int

edad = int(input("Edad: "))  # convierte a int
print(edad + 1)              # 29 — funciona
```

## 1.4. Operadores

### 1.4.1. Aritméticos

Los operadores aritméticos de Python son los estándar con dos adiciones relevantes: la división entera `//` y el operador de exponente `**`.

```python
a, b = 17, 5

print(a + b)   # 22  — suma
print(a - b)   # 12  — resta
print(a * b)   # 85  — multiplicación
print(a / b)   # 3.4 — división real (siempre devuelve float)
print(a // b)  # 3   — división entera (floor division, trunca hacia abajo)
print(a % b)   # 2   — módulo (resto de la división entera)
print(a ** b)  # 1419857 — exponente (equivale a 17^5)
```

El operador `//` siempre redondea hacia abajo (floor), no hacia cero. Esto tiene efecto con números negativos:

```python
print(7 // 2)    #  3
print(-7 // 2)   # -4  — redondea hacia abajo, no hacia cero
```

El módulo `%` es muy útil para determinar si un número es par/impar (`n % 2 == 0`), trabajar con índices circulares, o implementar ciclos periódicos.

### 1.4.2. Comparación

Los operadores de comparación devuelven siempre un `bool`. Son los mismos que en la mayoría de lenguajes, con la adición de que Python permite **encadenarlos** de forma natural.

```python
x = 5

print(x == 5)   # True  — igualdad
print(x != 3)   # True  — desigualdad
print(x > 3)    # True  — mayor que
print(x < 10)   # True  — menor que
print(x >= 5)   # True  — mayor o igual
print(x <= 4)   # False — menor o igual

# Encadenamiento de comparaciones — idioma Python muy común
edad = 25
print(18 <= edad < 65)  # True — equivale a: 18 <= edad and edad < 65
```

El encadenamiento es más legible y evita repetir la variable. Es habitual en validaciones de rangos.

### 1.4.3. Lógicos y cortocircuito

Los operadores lógicos en Python son palabras clave (`and`, `or`, `not`), no símbolos como `&&`, `||`, `!` de otros lenguajes.

```python
tiene_dni = True
es_mayor = True

# and — True si ambos son True
puede_votar = tiene_dni and es_mayor

# or — True si al menos uno es True
tiene_acceso = es_admin or es_moderador

# not — invierte el valor booleano
bloqueado = not usuario_activo
```

**Cortocircuito** — `and` y `or` no evalúan el segundo operando si el primero ya determina el resultado. `and` para si el primero es falsy; `or` para si el primero es truthy. Esto se usa para escribir guardas y valores por defecto de forma concisa.

```python
# or como valor por defecto
nombre = input("Nombre: ") or "Anónimo"  # si input devuelve "", usa "Anónimo"

# and como guarda — solo accede a .nombre si usuario no es None
nombre = usuario and usuario.nombre
```

`and` y `or` no devuelven necesariamente `True` o `False` — devuelven **el valor que determinó el resultado**:

```python
print(0 or "hola")   # "hola" — 0 es falsy, evalúa el segundo
print(5 or "hola")   # 5      — 5 es truthy, devuelve el primero
print(0 and "hola")  # 0      — 0 es falsy, devuelve el primero sin evaluar el segundo
```

### 1.4.4. Asignación

El operador básico `=` asigna un valor. Los operadores de asignación compuesta combinan una operación aritmética con la asignación.

```python
x = 10

x += 3   # equivale a: x = x + 3  → 13
x -= 2   # equivale a: x = x - 2  → 11
x *= 4   # equivale a: x = x * 4  → 44
x //= 5  # equivale a: x = x // 5 → 8
x **= 2  # equivale a: x = x ** 2 → 64
x %= 10  # equivale a: x = x % 10 → 4
```

Python **no tiene** operadores `++` ni `--`. Para incrementar se usa `+= 1`.

### 1.4.5. Identidad (is, is not)

`is` compara si dos variables apuntan al **mismo objeto en memoria**, no si tienen el mismo valor. Es fundamentalmente distinto a `==`.

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — mismo valor
print(a is b)   # False — objetos distintos en memoria
print(a is c)   # True  — c apunta al mismo objeto que a
```

Los usos correctos de `is` son dos: comparar con `None` y comparar con los singletons `True`/`False`. Para cualquier otra comparación, se usa `==`.

```python
# Uso correcto de is
if resultado is None:
    manejar_error()

# Trampa clásica de entrevista: small integer caching
x = 256
y = 256
print(x is y)  # True — Python cachea enteros de -5 a 256

x = 257
y = 257
print(x is y)  # False — fuera del rango cacheado, son objetos distintos
```

Python cachea enteros pequeños (-5 a 256) y strings cortos como optimización interna. Esto hace que `is` devuelva `True` para estos valores aunque sean variables distintas — un comportamiento que confunde en entrevistas pero que nunca debe usarse intencionalmente.

### 1.4.6. Pertenencia (in, not in)

`in` comprueba si un elemento existe dentro de una colección. Funciona con strings, listas, tuplas, sets y diccionarios.

```python
frutas = ["manzana", "pera", "uva"]

print("pera" in frutas)      # True
print("kiwi" not in frutas)  # True

# En strings: comprueba subcadenas
email = "usuario@empresa.com"
print("@" in email)          # True
print(".com" in email)       # True

# En diccionarios: comprueba keys, no values
config = {"debug": True, "puerto": 8080}
print("puerto" in config)    # True
print(8080 in config)        # False — 8080 es un value, no una key
```

**Rendimiento:** el comportamiento de `in` depende del tipo de colección.

Sobre una **lista**, Python recorre los elementos uno por uno hasta encontrar el buscado o llegar al final. El tiempo crece linealmente con el tamaño: O(n).

Sobre un **set** o las keys de un **dict**, Python calcula el hash del valor buscado y va directamente a la posición de memoria donde estaría ese elemento. Siempre es una sola operación independientemente del tamaño: O(1).

```python
# O(n): en el peor caso recorre toda la lista
usuarios_lista = ["ana", "pedro", "luis"]
"luis" in usuarios_lista

# O(1): calcula hash y va directo
usuarios_set = {"ana", "pedro", "luis"}
"luis" in usuarios_set
```

Si vas a hacer muchas búsquedas sobre una colección grande, convertirla a `set` una sola vez y buscar en el set es significativamente más eficiente que buscar en la lista repetidamente.

## 1.5. Built-ins de entrada/salida e inspección

Python incluye varias funciones predefinidas que se usan constantemente desde el primer programa: mostrar información por pantalla, leer datos del usuario y consultar el tipo de un valor. Son **built-ins**: están siempre disponibles sin necesidad de importar nada. Aquí se presentan como herramientas del lenguaje. El concepto general de qué es una función y cómo definir las propias se cubre en el tema 7.

### 1.5.1. print()

`print()` muestra valores por la salida estándar (normalmente la consola). Acepta cualquier número de argumentos separados por comas y los imprime uno tras otro separados por un espacio, terminando con un salto de línea.

```python
print("Hola mundo")              # Hola mundo
print("Edad:", 28)               # Edad: 28
print("a", "b", "c")             # a b c
```

El parámetro `sep` controla el separador entre argumentos (por defecto un espacio), y `end` controla qué se imprime al final (por defecto un salto de línea `\n`). Cambiar `end=""` evita el salto de línea, lo que permite encadenar varios `print` en la misma línea.

```python
print("a", "b", "c", sep="-")    # a-b-c
print("sin salto", end=" ")
print("de linea")                # sin salto de linea
```

Para mostrar valores con formato (decimales, alineación, interpolación) la forma idiomática moderna es usar f-strings, ya vistas en la sección 1.3.3.

```python
nombre = "Ana"
saldo = 1234.5
print(f"{nombre}: {saldo:.2f}€") # Ana: 1234.50€
```

### 1.5.2. input()

`input()` lee una línea de texto introducida por el usuario en la consola y devuelve esa línea como un `str`. Acepta un argumento opcional con el mensaje (prompt) que se muestra antes de esperar la entrada.

```python
nombre = input("¿Cómo te llamas? ")
print(f"Hola, {nombre}")
```

**Punto crítico:** `input()` siempre devuelve un `str`, incluso cuando el usuario escribe un número. Para trabajar con la entrada como número hay que convertirla explícitamente con `int()` o `float()`. Olvidar esta conversión es uno de los errores más comunes al empezar.

```python
edad_texto = input("Edad: ")     # "28" — string, no int
edad = int(edad_texto)           # 28 — ahora sí es int
print(edad + 1)                  # 29

# Forma compacta: convertir directamente
edad = int(input("Edad: "))
```

Si el usuario introduce algo que no se puede convertir (por ejemplo, escribe `"hola"` cuando se esperaba un número), `int()` lanza `ValueError`. Manejar estos errores se cubre en el tema dedicado a excepciones.

### 1.5.3. type()

`type()` devuelve el tipo del objeto que se le pasa como argumento. Es útil para depurar e inspeccionar valores cuando no se sabe con qué tipo se está trabajando.

```python
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hola"))    # <class 'str'>
print(type([1, 2]))    # <class 'list'>
print(type(None))      # <class 'NoneType'>
```

`type()` se usa principalmente para depurar. Para comprobar si un objeto es de un tipo determinado dentro de una condición, lo idiomático es usar `isinstance()` (que se cubre en el tema 8.5), porque también acepta subtipos correctamente y permite comprobar varios tipos a la vez.

```python
x = 42

# Funciona, pero no es lo más idiomático
if type(x) == int:
    print("es entero")

# Forma preferida (se verá en tema 8.5)
# if isinstance(x, int):
#     print("es entero")
```
