# 21. Context Managers

En cualquier programa que trabaje con recursos externos —archivos, conexiones de red, bloqueos de concurrencia, transacciones de base de datos— existe un patrón recurrente: adquirir el recurso, operar con él y asegurar su liberación al terminar, incluso si se produce un error. En lenguajes sin mecanismos específicos, este patrón se implementa con bloques `try/finally`, lo cual resulta repetitivo y propenso a olvidos. Python resuelve este problema con los **context managers** y la sentencia `with`.

Un context manager es un objeto que define dos operaciones: qué hacer al entrar en un bloque de código y qué hacer al salir, garantizando que la segunda se ejecute siempre, independientemente de si el bloque termina normalmente o por una excepción. Este mecanismo encapsula la lógica de adquisición y liberación de recursos en un solo lugar, eliminando la posibilidad de olvidar la limpieza.

El módulo `contextlib` de la biblioteca estándar complementa el protocolo con utilidades que simplifican la creación de context managers y ofrecen herramientas adicionales como supresión de excepciones y gestión de pilas de recursos.

---

## 21.1. La sentencia with

### 21.1.1. Qué problema resuelve (gestión automática de recursos)

El problema fundamental es garantizar que un recurso se libere después de usarlo, sin importar lo que ocurra durante su uso. Considerar el caso más común: abrir un archivo.

Sin `with`, la forma segura de manejar un archivo requiere un bloque `try/finally`:

```python
archivo = open("datos.txt", "r")
try:
    contenido = archivo.read()
    # ... procesar contenido ...
finally:
    archivo.close()
```

El bloque `finally` garantiza que `close()` se ejecute incluso si `read()` o el procesamiento lanzan una excepción. Pero este patrón tiene dos problemas prácticos. Primero, es verboso: tres líneas adicionales que no aportan información sobre la lógica del programa. Segundo, depende del programador: si alguien olvida el `try/finally`, el archivo queda abierto y el sistema operativo mantiene el recurso bloqueado hasta que el recolector de basura lo libere, algo que en CPython ocurre pronto pero que en otras implementaciones (PyPy, Jython) puede retrasarse indefinidamente.

La sentencia `with` elimina ambos problemas: la liberación del recurso está garantizada por la propia sintaxis, no por la disciplina del programador.

### 21.1.2. Sintaxis y flujo de ejecución

La sentencia `with` tiene esta forma:

```python
with expresion as variable:
    # cuerpo del bloque
```

El flujo de ejecución es el siguiente:

1. Python evalúa `expresion`, que debe producir un objeto context manager (un objeto con métodos `__enter__` y `__exit__`).
2. Se llama al método `__enter__` del context manager. El valor que devuelve se asigna a `variable` (si se usa `as`).
3. Se ejecuta el cuerpo del bloque `with`.
4. Al terminar el bloque —ya sea normalmente o por una excepción—, Python llama a `__exit__`. Si hubo excepción, `__exit__` recibe información sobre ella; si no, recibe `None` en todos sus argumentos.

```python
with open("datos.txt", "r") as archivo:
    contenido = archivo.read()
# Aquí el archivo ya está cerrado, haya habido error o no
```

Es importante entender que la variable creada por `as` no se limita al bloque `with`: sigue existiendo después, como cualquier otra variable en el ámbito actual. Lo que cambia es el estado del recurso: el archivo existe como objeto, pero está cerrado.

```python
with open("datos.txt") as f:
    datos = f.read()

# f sigue existiendo, pero está cerrado
print(f.closed)  # True
# f.read() lanzaría ValueError: I/O operation on closed file
```

La cláusula `as` es opcional. Cuando la operación de limpieza es lo único que importa y no se necesita una referencia al recurso, puede omitirse:

```python
with open("log.txt", "a") as f:
    f.write("entrada\n")

# Equivalente sin as cuando no se necesita el objeto:
# with algun_context_manager():
#     hacer_algo()
```

---

## 21.2. Crear context managers

### 21.2.1. Con clase (\_\_enter\_\_ y \_\_exit\_\_)

Un context manager basado en clase es un objeto que implementa dos métodos especiales:

- `__enter__(self)`: se ejecuta al entrar en el bloque `with`. El valor que devuelve es lo que se asigna a la variable tras `as`. Es habitual devolver `self`, pero puede devolver cualquier objeto.
- `__exit__(self, exc_type, exc_val, exc_tb)`: se ejecuta al salir del bloque, siempre. Recibe tres argumentos que describen la excepción en curso, o `None` si no hubo excepción. Si devuelve `True`, la excepción se suprime; si devuelve `False` (o `None`, que es falsy), la excepción se propaga normalmente.

```python
class Temporizador:
    """Mide el tiempo transcurrido dentro del bloque with."""

    def __enter__(self):
        import time
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.duracion = time.perf_counter() - self.inicio
        print(f"Tiempo: {self.duracion:.4f}s")
        return False  # No suprimir excepciones


with Temporizador() as t:
    suma = sum(range(1_000_000))

print(f"Resultado: {suma}")
# Tiempo: 0.0234s
# Resultado: 499999500000
```

Los tres parámetros de `__exit__` proporcionan información completa sobre cualquier excepción:

- `exc_type`: la clase de la excepción (por ejemplo, `ValueError`).
- `exc_val`: la instancia de la excepción (el mensaje y los datos).
- `exc_tb`: el traceback.

Si el bloque termina sin error, los tres son `None`.

```python
class ConexionSimulada:
    def __enter__(self):
        print("Abriendo conexion")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Error durante la conexion: {exc_val}")
        print("Cerrando conexion")
        return False  # Propagar la excepcion si la hubo


with ConexionSimulada() as conn:
    print("Usando conexion")
    # raise ValueError("fallo simulado")  # Descomentar para probar
# Abriendo conexion
# Usando conexion
# Cerrando conexion
```

Un aspecto que merece atención es el valor de retorno de `__exit__`. Devolver `True` suprime la excepción, es decir, el programa continúa después del bloque `with` como si no hubiera ocurrido ningún error. Esto es útil en casos muy específicos, pero peligroso como práctica general: suprimir excepciones silenciosamente puede ocultar errores reales. La convención es devolver `False` (o no devolver nada, ya que `None` es falsy) a menos que la supresión sea deliberada y documentada.

### 21.2.2. Con @contextmanager (contextlib)

El módulo `contextlib` proporciona el decorador `@contextmanager`, que permite crear context managers a partir de funciones generadoras sin necesidad de definir una clase completa. Esto reduce considerablemente el código necesario para context managers sencillos.

La función decorada debe contener exactamente un `yield`. Todo lo que precede al `yield` equivale a `__enter__`, el valor que produce el `yield` es lo que se asigna a la variable `as`, y todo lo que sigue al `yield` equivale a `__exit__`.

```python
from contextlib import contextmanager

@contextmanager
def temporizador():
    import time
    inicio = time.perf_counter()
    yield  # Aqui se ejecuta el cuerpo del with
    duracion = time.perf_counter() - inicio
    print(f"Tiempo: {duracion:.4f}s")


with temporizador():
    suma = sum(range(1_000_000))
```

Si se desea que el bloque `with` reciba un valor a través de `as`, se usa `yield valor`:

```python
from contextlib import contextmanager

@contextmanager
def directorio_temporal():
    import tempfile
    import shutil
    ruta = tempfile.mkdtemp()
    try:
        yield ruta  # Se asigna a la variable as
    finally:
        shutil.rmtree(ruta)


with directorio_temporal() as ruta:
    print(f"Trabajando en {ruta}")
# El directorio temporal se elimina al salir
```

El bloque `try/finally` dentro de la función generadora es esencial cuando el código posterior al `yield` debe ejecutarse incluso si se produce una excepción en el bloque `with`. Sin él, una excepción haría que la ejecución nunca llegara al código de limpieza después del `yield`.

```python
from contextlib import contextmanager

@contextmanager
def recurso_gestionado(nombre):
    print(f"Adquiriendo {nombre}")
    try:
        yield nombre
    finally:
        # Este bloque se ejecuta siempre, con o sin excepcion
        print(f"Liberando {nombre}")


with recurso_gestionado("base de datos") as r:
    print(f"Usando {r}")
# Adquiriendo base de datos
# Usando base de datos
# Liberando base de datos
```

### 21.2.3. Cuándo usar cada enfoque

La elección entre clase y `@contextmanager` depende de la complejidad y la reutilización:

**Usar `@contextmanager`** cuando el context manager es simple, tiene poca lógica y no necesita mantener estado complejo entre `__enter__` y `__exit__`. Es ideal para envolver operaciones de adquisición/liberación en pocas líneas.

**Usar una clase** cuando:
- El context manager necesita mantener estado accesible a través de métodos y atributos (como el `Temporizador` que expone `self.duracion`).
- La lógica de `__exit__` es compleja o necesita inspeccionar la excepción en detalle.
- Se desea que el context manager sea también un objeto con comportamiento propio, no solo un envoltorio de recurso.

En la práctica, `@contextmanager` cubre la mayoría de casos simples. Las clases se reservan para context managers que son a la vez gestores de recursos y objetos con identidad propia.

---

## 21.3. Context managers múltiples y anidados

Cuando se necesitan varios recursos simultáneamente, Python permite agruparlos en una sola sentencia `with` separándolos por comas:

```python
with open("entrada.txt") as entrada, open("salida.txt", "w") as salida:
    for linea in entrada:
        salida.write(linea.upper())
```

Esto es equivalente a anidar dos sentencias `with`:

```python
with open("entrada.txt") as entrada:
    with open("salida.txt", "w") as salida:
        for linea in entrada:
            salida.write(linea.upper())
```

Ambas formas garantizan que cada recurso se libere correctamente. La versión con comas es preferible cuando no hay lógica entre la adquisición de uno y otro recurso, porque reduce la indentación.

Desde Python 3.10, la sentencia `with` admite paréntesis para dividir la lista de context managers en varias líneas, lo cual mejora la legibilidad cuando se manejan muchos recursos:

```python
with (
    open("archivo1.txt") as f1,
    open("archivo2.txt") as f2,
    open("archivo3.txt", "w") as f3,
):
    # Los tres archivos están abiertos
    f3.write(f1.read() + f2.read())
```

El orden de liberación es el inverso al de adquisición: el último recurso abierto es el primero en cerrarse. Esto es el mismo principio LIFO que sigue una pila.

---

## 21.4. suppress() y otras utilidades de contextlib

El módulo `contextlib` ofrece varias utilidades que complementan el mecanismo de context managers.

### suppress()

`suppress` crea un context manager que suprime las excepciones indicadas. Es una alternativa más limpia a un bloque `try/except` con `pass` cuando se desea ignorar deliberadamente una excepción específica.

```python
from contextlib import suppress

# En lugar de:
try:
    import os
    os.remove("temporal.txt")
except FileNotFoundError:
    pass

# Se puede escribir:
with suppress(FileNotFoundError):
    import os
    os.remove("temporal.txt")
```

Se pueden suprimir varias excepciones a la vez:

```python
from contextlib import suppress

with suppress(FileNotFoundError, PermissionError):
    import os
    os.remove("temporal.txt")
```

`suppress` solo debe usarse cuando ignorar la excepción es la acción correcta. No es un sustituto general de `try/except`: si la excepción requiere alguna acción (registrar un log, reintentar, notificar), `try/except` sigue siendo la herramienta adecuada.

### redirect_stdout y redirect_stderr

Estos context managers redirigen la salida estándar o de error a otro destino durante la ejecución del bloque:

```python
from contextlib import redirect_stdout
import io

buffer = io.StringIO()
with redirect_stdout(buffer):
    print("Este texto va al buffer")

capturado = buffer.getvalue()
print(f"Capturado: {capturado}")
# Capturado: Este texto va al buffer
```

### closing()

`closing` envuelve un objeto que tiene método `close()` pero no implementa el protocolo de context manager. Al salir del bloque, llama a `close()` automáticamente:

```python
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("https://ejemplo.com")) as pagina:
    contenido = pagina.read()
# pagina.close() se llama automaticamente
```

En la práctica, la mayoría de objetos modernos de la biblioteca estándar ya implementan el protocolo de context manager directamente, por lo que `closing` se usa principalmente con bibliotecas externas que no lo hacen.

### ExitStack

`ExitStack` gestiona una pila dinámica de context managers, útil cuando el número de recursos no se conoce de antemano:

```python
from contextlib import ExitStack

archivos_a_abrir = ["datos1.txt", "datos2.txt", "datos3.txt"]

with ExitStack() as pila:
    archivos = [pila.enter_context(open(nombre)) for nombre in archivos_a_abrir]
    # Todos los archivos están abiertos
    for f in archivos:
        print(f.readline())
# Todos los archivos se cierran al salir, en orden inverso
```

`ExitStack` también permite registrar funciones de limpieza arbitrarias con `callback`:

```python
from contextlib import ExitStack

def limpiar(nombre):
    print(f"Limpiando {nombre}")

with ExitStack() as pila:
    pila.callback(limpiar, "recurso A")
    pila.callback(limpiar, "recurso B")
    print("Trabajando")
# Trabajando
# Limpiando recurso B
# Limpiando recurso A
```

Las funciones registradas con `callback` se ejecutan en orden LIFO (la última registrada se ejecuta primero), siguiendo el mismo principio que la pila de context managers.
