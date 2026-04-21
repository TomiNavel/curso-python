# 2. Strings

Los strings en Python son secuencias inmutables de caracteres Unicode. Son uno de los tipos más usados del lenguaje y tienen un ecosistema de métodos muy completo que se pregunta frecuentemente en entrevistas.

## 2.1. Características de Strings

### 2.1.1. Inmutabilidad

Un string no puede modificarse una vez creado. Cualquier operación que parezca modificarlo en realidad crea un nuevo objeto string. La variable original no cambia.

```python
saludo = "hola"
saludo.upper()       # no modifica saludo, devuelve un nuevo string
print(saludo)        # "hola" — sin cambios

saludo = saludo.upper()  # hay que reasignar para conservar el resultado
print(saludo)            # "HOLA"
```

Esto tiene implicaciones de rendimiento: concatenar strings en un bucle con `+=` crea un nuevo objeto en cada iteración. Para construir strings grandes a partir de muchas partes, `"".join(lista)` es mucho más eficiente porque construye el resultado en una sola operación.

```python
# Ineficiente: crea un nuevo string en cada iteración
resultado = ""
for palabra in palabras:
    resultado += palabra  # O(n²) en total

# Eficiente: une todo de una vez
resultado = "".join(palabras)  # O(n)
```

### 2.1.2. Indexing y slicing

Los strings son secuencias, por lo que se puede acceder a caracteres individuales por índice y extraer fragmentos con slicing. Los índices negativos cuentan desde el final.

```python
s = "Python"
#    0 1 2 3 4 5   → índices positivos
#   -6-5-4-3-2-1   → índices negativos

print(s[0])     # "P"  — primer carácter
print(s[-1])    # "n"  — último carácter
print(s[-3])    # "h"  — tercero desde el final
```

El slicing usa la sintaxis `[inicio:fin:paso]`. El índice `fin` no está incluido en el resultado.

```python
s = "Python"

print(s[1:4])   # "yth"  — desde índice 1 hasta 3 (4 no incluido)
print(s[:3])    # "Pyt"  — desde el inicio hasta índice 2
print(s[3:])    # "hon"  — desde índice 3 hasta el final
print(s[::2])   # "Pto"  — cada 2 caracteres
print(s[::-1])  # "nohtyP" — string invertido (paso -1 recorre al revés)
```

### 2.1.3. Concatenación y repetición

El operador `+` concatena strings y `*` los repite. Ambos crean un nuevo string.

```python
nombre = "Ana"
apellido = "García"

nombre_completo = nombre + " " + apellido  # "Ana García"
separador = "-" * 20                       # "--------------------"
```

Para concatenar muchos strings o construir strings dinámicamente, los f-strings o `join()` son más legibles y eficientes que encadenar `+`.

## 2.2. Métodos de Strings

### 2.2.1. Transformación (upper, lower, capitalize, title, strip)

Los métodos de transformación crean un nuevo string con el contenido modificado. Es importante recordar que, al ser los strings inmutables, ninguno de estos métodos modifica el original — siempre devuelven una copia nueva. Si no se asigna el resultado a una variable, el string transformado se pierde.

Estos métodos se usan constantemente en el día a día: normalizar texto para comparaciones (`"Ana" == "ana"` es `False`, pero `"Ana".lower() == "ana".lower()` es `True`), limpiar input del usuario que puede venir con espacios extra, o formatear texto para mostrarlo en pantalla.

```python
texto = "  hola mundo  "

print(texto.upper())       # "  HOLA MUNDO  "
print(texto.lower())       # "  hola mundo  "
print(texto.capitalize())  # "  hola mundo  " — solo pone en mayúscula el primer carácter del string completo
print("hola mundo".capitalize())  # "Hola mundo"
print("hola mundo".title())       # "Hola Mundo" — mayúscula en cada palabra

# strip elimina espacios (u otros caracteres) de los extremos
print(texto.strip())       # "hola mundo"   — ambos extremos
print(texto.lstrip())      # "hola mundo  " — solo izquierda
print(texto.rstrip())      # "  hola mundo" — solo derecha

# strip también elimina caracteres específicos
print("***dato***".strip("*"))  # "dato"
```

### 2.2.2. Búsqueda (find, index, count, startswith, endswith)

Cuando se trabaja con texto es muy habitual necesitar localizar un fragmento dentro de un string: saber si contiene cierta palabra, en qué posición está, cuántas veces aparece, o si empieza o termina con un patrón determinado.

Python ofrece dos métodos para localizar la posición de un substring: `find` e `index`. Ambos buscan la primera ocurrencia y devuelven su índice, pero difieren en cómo manejan el caso de no encontrar nada. `find` devuelve `-1`, lo que permite usarlo en condicionales sin riesgo de error. `index` lanza una excepción `ValueError`, lo que tiene sentido cuando la ausencia del substring indicaría un bug en el programa (no debería pasar).

```python
texto = "el gato y el perro"

# find devuelve el índice de la primera ocurrencia, o -1 si no existe
print(texto.find("gato"))    # 3
print(texto.find("pez"))     # -1

# index hace lo mismo pero lanza ValueError si no encuentra
print(texto.index("gato"))   # 3
# texto.index("pez")         # ValueError — usar find si la ausencia es posible

# count cuenta ocurrencias (no solapadas)
print(texto.count("el"))     # 2

# startswith y endswith aceptan también una tupla de prefijos/sufijos
print(texto.startswith("el"))          # True
print(texto.endswith("perro"))         # True
print(texto.endswith(("gato", "perro")))  # True — cualquiera de los dos
```

### 2.2.3. Validación (isdigit, isalpha, isalnum, isspace)

Los métodos de validación permiten comprobar si todos los caracteres de un string cumplen cierta condición: si son dígitos, letras, alfanuméricos o espacios en blanco. Devuelven `True` solo si **todos** los caracteres cumplen la condición, y `False` si al menos uno no la cumple. Un detalle importante: en strings vacíos (`""`) todos devuelven `False`, porque no hay ningún carácter que pueda cumplir la condición.

Estos métodos son especialmente útiles para validar input del usuario antes de procesarlo — por ejemplo, verificar que un código postal contiene solo dígitos, o que un nombre de usuario tiene solo letras y números.

```python
print("123".isdigit())     # True  — todos son dígitos
print("12.3".isdigit())    # False — el punto no es dígito
print("abc".isalpha())     # True  — todos son letras
print("abc123".isalnum())  # True  — letras o dígitos
print("   ".isspace())     # True  — todos son espacios en blanco

# Uso típico: validar input del usuario
codigo = input("Introduce tu código: ")
if not codigo.isalnum():
    print("El código solo puede contener letras y números")
```

### 2.2.4. División y unión (split, join, partition)

Dividir un string en partes y volver a unirlas es una de las operaciones más comunes en programación. Aparece al procesar archivos CSV, parsear logs, manipular rutas de archivo, extraer datos de URLs, limpiar texto, y un largo etcétera.

`split` toma un string y lo divide en una lista de substrings usando un separador. `join` hace la operación inversa: toma una lista de strings y los une en uno solo, insertando un separador entre cada elemento. Son operaciones complementarias y se usan juntas con mucha frecuencia.

Un detalle que genera confusión al principio: `join` es un método del **separador**, no de la lista. Se escribe `", ".join(lista)`, no `lista.join(", ")`. La razón es que `join` solo tiene sentido con strings, y las listas pueden contener cualquier tipo de dato.

`partition` es una alternativa a `split` cuando solo se necesita dividir en dos partes por la primera ocurrencia del separador. Devuelve siempre exactamente tres valores: lo que hay antes, el separador, y lo que hay después.

```python
# split divide por un separador (por defecto cualquier espacio en blanco)
csv = "ana,pedro,luis,marta"
nombres = csv.split(",")       # ["ana", "pedro", "luis", "marta"]

linea = "  hola   mundo  "
palabras = linea.split()       # ["hola", "mundo"] — split() sin args elimina espacios múltiples

# split con maxsplit limita el número de divisiones
partes = "a:b:c:d".split(":", maxsplit=2)  # ["a", "b", "c:d"]

# join une una lista de strings con un separador
print(", ".join(nombres))      # "ana, pedro, luis, marta"
print("".join(["P", "y", "t", "hon"]))  # "Python"

# partition divide en exactamente tres partes: antes, separador, después
usuario, sep, dominio = "ana@empresa.com".partition("@")
print(usuario)   # "ana"
print(dominio)   # "empresa.com"
```

### 2.2.5. Reemplazo (replace, translate)

Reemplazar fragmentos de texto es otra operación fundamental. Python ofrece dos mecanismos con propósitos distintos.

`replace` sustituye todas las ocurrencias de un substring por otro. Es el método más directo y el que se usa en la mayoría de casos. Opcionalmente se puede limitar el número de sustituciones.

`translate` trabaja a nivel de carácter individual, no de substrings. Usa una tabla de traducción que mapea cada carácter a su reemplazo (o a `None` para eliminarlo). Es más eficiente que encadenar múltiples `replace` cuando se necesita sustituir o eliminar muchos caracteres diferentes a la vez.

```python
texto = "el gato y el perro"

# replace sustituye todas las ocurrencias por defecto
print(texto.replace("el", "un"))          # "un gato y un perro"
print(texto.replace("el", "un", 1))       # "un gato y el perro" — máximo 1 sustitución

# translate usa una tabla de sustitución carácter a carácter
# útil para reemplazar muchos caracteres de una vez (más eficiente que encadenar replace)
tabla = str.maketrans("aeiou", "AEIOU")   # sustituye vocales minúsculas por mayúsculas
print("hola mundo".translate(tabla))      # "hOlA mUndO"

# también puede eliminar caracteres (tercer argumento: caracteres a borrar)
tabla = str.maketrans("", "", "aeiou")    # elimina vocales
print("hola mundo".translate(tabla))      # "hl mnd"
```

## 2.3. Tipos especiales de Strings

### 2.3.1. Strings multilínea

Los strings multilínea se definen con comillas triples (`"""` o `'''`). Preservan los saltos de línea y la indentación exactamente como están escritos en el código.

```python
mensaje = """Estimado usuario,

Su pedido ha sido confirmado.
Gracias por su compra."""

print(mensaje)
# Estimado usuario,
#
# Su pedido ha sido confirmado.
# Gracias por su compra.
```

Un uso muy común es en docstrings (ver sección 1.2.2 del tema anterior). También se usan para queries SQL largas o plantillas de texto sin necesidad de concatenar líneas.

```python
query = """
    SELECT nombre, email
    FROM usuarios
    WHERE activo = true
    ORDER BY nombre
"""
```

Atención: la indentación dentro del string forma parte del contenido. Si el string está dentro de una función indentada, los espacios de indentación del código se incluyen en el string. Para evitarlo se usa `textwrap.dedent()`.

### 2.3.2. Raw strings

Un raw string se define con el prefijo `r` antes de las comillas. En un raw string, las secuencias de escape (`\n`, `\t`, `\\`, etc.) no se interpretan — la barra invertida se trata como un carácter literal.

```python
# Sin raw string: \n es un salto de línea
print("línea1\nlínea2")
# línea1
# línea2

# Con raw string: \n es literalmente barra + n
print(r"línea1\nlínea2")
# línea1\nlínea2
```

Se usa en dos contextos principalmente:

**Expresiones regulares** — los patrones regex usan `\d`, `\w`, `\s`, etc. Sin raw string habría que escribir `\\d`, `\\w`, lo que hace los patrones ilegibles.

```python
import re

# Sin raw string: hay que escapar cada barra
patron = "\\d{3}-\\d{4}"

# Con raw string: mucho más legible
patron = r"\d{3}-\d{4}"

re.match(r"\d{3}-\d{2}-\d{4}", "123-45-6789")
```

**Rutas de Windows** — en Windows las rutas usan `\` que colisiona con las secuencias de escape.

```python
# Sin raw string: \n y \t se interpretan como escape
ruta = "C:\nuevo\archivo.txt"   # \n y \a son escapes

# Con raw string: la barra es literal
ruta = r"C:\nuevo\archivo.txt"  # correcto
```

## 2.4. Formateo de Strings

### 2.4.1. f-strings (Python 3.6+)

Los f-strings son la forma moderna y recomendada de interpolar valores en strings. Se definen con el prefijo `f` y permiten incluir expresiones Python directamente dentro de `{}`.

```python
nombre = "Ana"
edad = 28
precio = 9.995

# Interpolación básica
print(f"Hola, {nombre}. Tienes {edad} años.")

# Expresiones dentro de {}
print(f"El doble de tu edad: {edad * 2}")
print(f"Mayúsculas: {nombre.upper()}")

# Especificadores de formato
print(f"Precio: {precio:.2f}€")       # 2 decimales → "9.99€"
print(f"Porcentaje: {0.857:.1%}")     # porcentaje → "85.7%"
print(f"Entero con ceros: {42:05d}")  # padding → "00042"
print(f"Separador de miles: {1000000:,}")  # → "1,000,000"

# Python 3.8+: f"{variable=}" para debug — muestra nombre y valor
x = 42
print(f"{x=}")  # "x=42"
```

Los f-strings se evalúan en tiempo de ejecución en el punto donde aparecen. Son más rápidos que `format()` y `%` y significativamente más legibles.

### 2.4.2. Formatos anteriores (format(), % formatting)

Antes de los f-strings existían dos mecanismos de formateo. Siguen funcionando y aparecen en código legacy, por lo que es importante reconocerlos.

**`str.format()`** — introducido en Python 2.6. Usa `{}` como marcadores de posición.

```python
# Posicional
"Hola, {}. Tienes {} años.".format("Ana", 28)

# Por nombre
"Hola, {nombre}.".format(nombre="Ana")

# Con formato
"Precio: {:.2f}€".format(9.995)  # "Precio: 9.99€"
```

**`%` formatting** — el formato más antiguo, heredado de C. Usa `%s`, `%d`, `%f` como marcadores.

```python
"Hola, %s. Tienes %d años." % ("Ana", 28)
"Precio: %.2f€" % 9.995
```

En código nuevo, siempre usar f-strings. `format()` tiene sentido cuando la plantilla se construye dinámicamente o se almacena por separado del lugar donde se aplica.

## 2.5. Alineación y Relleno

### 2.5.1. Métodos de alineación (zfill, center, ljust, rjust)

En ocasiones es necesario que un string tenga una longitud fija — por ejemplo, al generar tablas en la terminal, crear identificadores con formato fijo (como "00042"), o alinear columnas de datos en un informe de texto.

Los métodos de alineación producen un nuevo string de la anchura indicada, rellenando con un carácter (espacio por defecto) hasta alcanzarla. Si el string original ya es igual o más largo que la anchura solicitada, se devuelve sin cambios.

```python
texto = "hola"

# ljust: alinea a la izquierda, rellena a la derecha
print(texto.ljust(10))         # "hola      "
print(texto.ljust(10, "-"))    # "hola------"

# rjust: alinea a la derecha, rellena a la izquierda
print(texto.rjust(10))         # "      hola"
print(texto.rjust(10, "-"))    # "------hola"

# center: centra el texto, rellena a ambos lados
print(texto.center(10))        # "   hola   "
print(texto.center(10, "*"))   # "***hola***"

# zfill: rellena con ceros a la izquierda (específico para números)
print("42".zfill(5))           # "00042"
print("-42".zfill(5))          # "-0042" — respeta el signo
```

El caso más habitual de `zfill` es formatear identificadores o códigos numéricos con longitud fija. Los otros tres se usan para alinear columnas en salidas de texto.

Nota: los f-strings pueden hacer lo mismo con especificadores de formato, que suelen ser más concisos en código moderno:

```python
print(f"{'hola':<10}")   # ljust
print(f"{'hola':>10}")   # rjust
print(f"{'hola':^10}")   # center
print(f"{42:05d}")       # zfill equivalente
```

## 2.6. Encoding y Unicode

### 2.6.1. encode() y decode()

Para entender encoding hay que distinguir dos conceptos que a menudo se confunden: **texto** y **bytes**. Un string en Python (`str`) es texto — una secuencia de caracteres abstractos como "a", "ñ" o "日". Un objeto `bytes` es una secuencia de números entre 0 y 255 — datos crudos sin significado inherente.

Dentro de un programa Python, el texto vive como `str` y no hay problema. Pero el mundo exterior (archivos en disco, redes, bases de datos, APIs) no entiende de caracteres abstractos — solo de bytes. Para cruzar esa frontera hace falta un **encoding**: una tabla que define cómo convertir cada carácter en una secuencia de bytes, y viceversa.

`encode()` convierte un string a `bytes` (texto → bytes, para enviar al exterior). `decode()` hace la operación inversa (bytes → texto, para trabajar dentro de Python).

```python
texto = "hola"

# encode: string → bytes
bytes_utf8 = texto.encode("utf-8")    # b'hola'
bytes_latin = texto.encode("latin-1") # b'hola'

# decode: bytes → string
print(bytes_utf8.decode("utf-8"))     # "hola"

# Con caracteres no ASCII la diferencia es visible
texto = "año"
print(texto.encode("utf-8"))          # b'a\xc3\xb1o' — ñ ocupa 2 bytes en UTF-8
print(texto.encode("latin-1"))        # b'a\xf1o'     — ñ ocupa 1 byte en latin-1
```

El error más común: intentar decodificar bytes con un encoding distinto al que se usó para codificarlos.

```python
# Error típico
datos = "año".encode("utf-8")
datos.decode("latin-1")  # no lanza error pero produce texto corrupto ("aÃ±o")
```

### 2.6.2. UTF-8 y otros encodings

Un **encoding** es una tabla que mapea caracteres a secuencias de bytes. El problema histórico: durante décadas cada región del mundo usó su propia tabla, y los ficheros de una región no se leían correctamente en otra.

**UTF-8** resolvió esto siendo un encoding universal que puede representar cualquier carácter Unicode. Es el estándar en la web, APIs, sistemas Unix y Python 3. Usa entre 1 y 4 bytes por carácter — los caracteres ASCII usan 1 byte, igual que en ASCII puro, lo que lo hace compatible hacia atrás.

Los encodings que siguen apareciendo en código legacy o en contextos específicos:

| Encoding | Uso |
|---|---|
| `utf-8` | Estándar universal. Usar siempre en código nuevo. |
| `latin-1` / `iso-8859-1` | Europa occidental. Ficheros legacy españoles/franceses. |
| `cp1252` | Windows Europa occidental. Ficheros creados en Windows. |
| `ascii` | Solo 128 caracteres básicos. Sin acentos ni ñ. |
| `utf-16` | Windows internamente, algunos ficheros Word. |

En Python 3, al abrir ficheros de texto sin especificar encoding se usa el encoding del sistema operativo, que en Windows puede ser `cp1252`. Para evitar sorpresas, siempre especificarlo explícitamente:

```python
# Sin especificar encoding: depende del SO (puede fallar en Windows con caracteres especiales)
with open("datos.txt") as f:
    contenido = f.read()

# Correcto: encoding explícito
with open("datos.txt", encoding="utf-8") as f:
    contenido = f.read()
```

### 2.6.3. chr() y ord()

`chr()` y `ord()` son dos built-ins que convierten entre un carácter y su código Unicode (también llamado *code point*). Cada carácter Unicode tiene asignado un número entero único — por ejemplo, la letra `'A'` es el código `65`, y la letra `'a'` es el código `97`. Estas funciones permiten pasar de uno al otro.

**`ord(caracter)`** recibe un string de **un solo carácter** y devuelve su código Unicode como entero. Si se pasa un string de más de un carácter o vacío, lanza `TypeError`.

**`chr(numero)`** recibe un entero y devuelve el carácter cuyo código Unicode es ese número.

```python
print(ord("A"))     # 65
print(ord("a"))     # 97
print(ord("ñ"))     # 241
print(ord("€"))     # 8364

print(chr(65))      # 'A'
print(chr(97))      # 'a'
print(chr(8364))    # '€'

# Son operaciones inversas
print(chr(ord("A")) == "A")  # True
```

Estas funciones aparecen con frecuencia en problemas de manipulación de strings y entrevistas técnicas. Un patrón habitual es usar la diferencia entre códigos para calcular distancias entre letras o desplazar caracteres alfabéticamente, como en el cifrado César.

```python
# Calcular la posición de una letra en el alfabeto (0-25)
letra = "d"
posicion = ord(letra) - ord("a")
print(posicion)     # 3

# Desplazar una letra N posiciones (cifrado César básico, sin manejo de wraparound)
letra = "a"
desplazada = chr(ord(letra) + 3)
print(desplazada)   # 'd'

# Comprobar si un carácter es una letra minúscula manualmente
caracter = "k"
es_minuscula = ord("a") <= ord(caracter) <= ord("z")
print(es_minuscula) # True
```
