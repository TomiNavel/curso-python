# 20. Type Hints y Typing

Python es un lenguaje de tipado dinámico: las variables no tienen un tipo fijo declarado, y es el intérprete quien comprueba los tipos en tiempo de ejecución. Esta flexibilidad permite escribir código breve y expresivo, pero tiene un coste. A medida que un programa crece, resulta cada vez más difícil saber qué tipo de dato espera una función, qué devuelve, o qué contiene una estructura de datos. Los errores de tipo —pasar una cadena donde se esperaba un entero, por ejemplo— solo se descubren al ejecutar el código y provocar una excepción.

Los **type hints** (anotaciones de tipo) son una extensión de la sintaxis de Python, introducida de forma progresiva a partir de Python 3.5, que permite declarar los tipos esperados de variables, parámetros, valores de retorno y estructuras de datos. Estas anotaciones no cambian el comportamiento del programa en tiempo de ejecución —Python las ignora por completo—, pero cumplen tres funciones importantes: documentan el código de forma precisa y verificable, permiten que herramientas externas como **mypy** detecten errores de tipo antes de ejecutar el programa, y mejoran el autocompletado y la navegación en editores e IDEs.

El módulo `typing` de la biblioteca estándar proporciona los tipos y utilidades necesarios para expresar anotaciones complejas: tipos genéricos, uniones, tipos opcionales, tipos literales, protocolos, etc. A partir de Python 3.9 y 3.10, muchas de estas construcciones se simplificaron y se integraron directamente en la sintaxis del lenguaje, reduciendo la dependencia del módulo `typing`.

---

## 20.1. Type hints básicos

### 20.1.1. Sintaxis y tipos primitivos (int, str, float, bool, None)

La sintaxis de un type hint es una anotación que acompaña al nombre de la variable, separada por dos puntos. Para los tipos primitivos de Python, se usan directamente los nombres de las clases built-in.

```python
nombre: str = "Ana"
edad: int = 30
altura: float = 1.75
activo: bool = True
```

La anotación no impide asignar un valor de otro tipo —Python no la comprueba en tiempo de ejecución—, pero una herramienta como mypy señalaría la inconsistencia:

```python
edad: int = "treinta"  # Python no da error, pero mypy sí
```

El tipo `None` se anota directamente como `None`:

```python
resultado: None = None
```

Las anotaciones de tipo son expresiones que Python evalúa al cargar el módulo, pero no utiliza más allá de almacenarlas en el atributo `__annotations__` del objeto donde se declaran. Esto significa que anotar no tiene coste en rendimiento más allá del momento de carga.

### 20.1.2. Colecciones (list, dict, set, tuple)

Desde Python 3.9, los tipos de colecciones built-in (`list`, `dict`, `set`, `tuple`) aceptan parámetros de tipo directamente, usando corchetes para indicar qué contienen.

```python
nombres: list[str] = ["Ana", "Luis", "Marta"]
edades: dict[str, int] = {"Ana": 30, "Luis": 25}
etiquetas: set[str] = {"python", "typing"}
coordenada: tuple[float, float] = (3.0, 4.0)
```

Cada colección se parametriza de forma distinta:

- `list[T]` — lista cuyos elementos son de tipo `T`.
- `dict[K, V]` — diccionario con claves de tipo `K` y valores de tipo `V`.
- `set[T]` — conjunto cuyos elementos son de tipo `T`.
- `tuple[T1, T2, ...]` — tupla con un número fijo de elementos, cada uno con su tipo. Para una tupla de longitud variable con elementos homogéneos se usa `tuple[T, ...]` (con puntos suspensivos literales).

```python
# Tupla de longitud fija: exactamente (str, int, bool)
registro: tuple[str, int, bool] = ("Ana", 30, True)

# Tupla de longitud variable: cualquier número de enteros
numeros: tuple[int, ...] = (1, 2, 3, 4, 5)
```

Las colecciones pueden anidarse para describir estructuras complejas:

```python
# Lista de diccionarios con claves str y valores int
inventario: list[dict[str, int]] = [
    {"manzanas": 5, "peras": 3},
    {"naranjas": 8}
]
```

En versiones anteriores a Python 3.9, era necesario importar los equivalentes del módulo `typing` (`List`, `Dict`, `Set`, `Tuple` con mayúscula inicial). A partir de 3.9, los tipos built-in con minúscula son la forma recomendada y las versiones en mayúscula de `typing` están deprecadas.

### 20.1.3. Optional y Union (X | Y)

Cuando una variable puede contener un valor de más de un tipo, se usa una **unión**. Desde Python 3.10, la sintaxis es el operador `|` directamente entre los tipos:

```python
resultado: int | str = 42
resultado = "error"  # también válido
```

El caso más frecuente es una variable que puede contener un valor o `None`. Esto se conoce como tipo **opcional**:

```python
# Las dos formas son equivalentes
nombre: str | None = None
nombre = "Ana"
```

Antes de Python 3.10, se usaban `Union` y `Optional` del módulo `typing`:

```python
from typing import Optional, Union

resultado: Union[int, str] = 42
nombre: Optional[str] = None  # equivalente a Union[str, None]
```

Un error conceptual frecuente es pensar que `Optional[str]` significa «el parámetro es opcional y puede omitirse». No es así: `Optional[str]` significa que el tipo puede ser `str` o `None`. Un parámetro «opcional» en el sentido de que se puede omitir al llamar a la función se consigue con un valor por defecto, no con `Optional`:

```python
# El parámetro acepta str o None, pero es obligatorio en la llamada
def saludar(nombre: str | None) -> str:
    if nombre is None:
        return "Hola, invitado"
    return f"Hola, {nombre}"

# El parámetro tiene valor por defecto: se puede omitir en la llamada
def saludar(nombre: str = "invitado") -> str:
    return f"Hola, {nombre}"
```

### 20.1.4. Any

El tipo `Any` del módulo `typing` representa «cualquier tipo». Una variable anotada como `Any` desactiva las comprobaciones de tipo para esa variable: mypy no señala ningún error al usarla, independientemente de las operaciones que se realicen sobre ella.

```python
from typing import Any

dato: Any = 42
dato = "texto"   # sin error
dato = [1, 2, 3] # sin error
print(dato.metodo_inventado())  # mypy no avisa, aunque fallará en ejecución
```

`Any` es útil en dos situaciones: al migrar código existente sin anotaciones —permite ir anotando gradualmente sin que mypy lance errores en las partes no migradas— y al interactuar con bibliotecas externas que no proporcionan información de tipos. Fuera de estos casos, `Any` debería evitarse porque anula precisamente la protección que los type hints ofrecen.

### 20.1.5. Tipo de retorno y parámetros de funciones

Las funciones se anotan indicando el tipo de cada parámetro y el tipo de retorno tras una flecha `->`:

```python
def sumar(a: int, b: int) -> int:
    return a + b

def buscar(texto: str, subcadena: str) -> int | None:
    indice = texto.find(subcadena)
    return indice if indice != -1 else None
```

Las funciones que no devuelven nada explícitamente (las que terminan sin `return` o con `return` sin valor) tienen tipo de retorno `None`:

```python
def saludar(nombre: str) -> None:
    print(f"Hola, {nombre}")
```

Los parámetros con valor por defecto se anotan normalmente, y el valor por defecto va después de la anotación:

```python
def crear_usuario(nombre: str, edad: int = 0, activo: bool = True) -> dict[str, str | int | bool]:
    return {"nombre": nombre, "edad": edad, "activo": activo}
```

Los parámetros `*args` y `**kwargs` se anotan con el tipo de cada elemento individual, no con el tipo del contenedor:

```python
# Cada argumento posicional es un int (args será tuple[int, ...])
def sumar_todos(*args: int) -> int:
    return sum(args)

# Cada valor es un str (kwargs será dict[str, str])
def configurar(**kwargs: str) -> None:
    for clave, valor in kwargs.items():
        print(f"{clave} = {valor}")
```

---

## 20.2. Type hints avanzados

### 20.2.1. TypeAlias y type (Python 3.12)

Cuando una anotación de tipo es larga o se repite en múltiples lugares, se puede asignar a un alias para mejorar la legibilidad. Un alias de tipo es simplemente una asignación de un tipo a un nombre.

Antes de Python 3.12, la forma recomendada era usar `TypeAlias` del módulo `typing` para distinguir un alias de tipo de una variable normal:

```python
from typing import TypeAlias

# Sin TypeAlias, no queda claro si es un alias o una variable
Coordenada = tuple[float, float]       # ¿alias o variable?

# Con TypeAlias, la intención es explícita
Coordenada: TypeAlias = tuple[float, float]

def distancia(a: Coordenada, b: Coordenada) -> float:
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5
```

A partir de Python 3.12, se introdujo la sentencia `type` como parte de la sintaxis del lenguaje, eliminando la necesidad de importar nada:

```python
type Coordenada = tuple[float, float]
type Resultado = dict[str, list[int]]

def procesar(datos: Resultado) -> list[Coordenada]:
    ...
```

La sentencia `type` también evalúa el tipo de forma perezosa (*lazy*), lo que significa que el tipo referenciado no necesita estar definido en el momento de declarar el alias. Esto resuelve problemas de referencias circulares que antes requerían cadenas como anotaciones.

### 20.2.2. Literal

`Literal` permite restringir un tipo a un conjunto concreto de valores literales. Mientras que `str` acepta cualquier cadena, `Literal["rojo", "verde", "azul"]` solo acepta esas tres cadenas específicas.

```python
from typing import Literal

def semaforo(color: Literal["rojo", "amarillo", "verde"]) -> str:
    acciones = {
        "rojo": "Detenerse",
        "amarillo": "Precaución",
        "verde": "Avanzar"
    }
    return acciones[color]

semaforo("rojo")      # correcto
semaforo("morado")    # mypy señala error
```

`Literal` acepta enteros, cadenas, bytes, booleanos y `None`. No acepta objetos arbitrarios ni expresiones calculadas. Es especialmente útil para funciones cuyo comportamiento cambia según un argumento que solo admite ciertos valores — una alternativa al uso de enums cuando la interfaz es sencilla y no justifica definir un tipo nuevo.

### 20.2.3. TypeVar y genéricos

Los **genéricos** permiten escribir funciones y clases que trabajan con cualquier tipo, sin perder la información del tipo concreto. Un `TypeVar` declara una variable de tipo que se resuelve al tipo concreto en cada uso.

```python
from typing import TypeVar

T = TypeVar("T")

def primero(elementos: list[T]) -> T:
    return elementos[0]

# mypy infiere que resultado es str
resultado = primero(["a", "b", "c"])

# mypy infiere que resultado es int
resultado = primero([1, 2, 3])
```

Sin `TypeVar`, la alternativa sería anotar con `Any`, pero eso perdería la relación entre el tipo de entrada y el de salida. Con `TypeVar`, mypy sabe que si se pasa una `list[str]`, el resultado es `str`.

Un `TypeVar` puede restringirse a un conjunto de tipos con `bound` o con valores explícitos:

```python
from typing import TypeVar

# T puede ser cualquier tipo que sea subtipo de int o float
Numero = TypeVar("Numero", int, float)

def maximo(a: Numero, b: Numero) -> Numero:
    return a if a > b else b
```

A partir de Python 3.12, la sintaxis de genéricos se simplificó con parámetros de tipo directamente en la definición de función o clase, eliminando la necesidad de declarar `TypeVar` manualmente:

```python
# Python 3.12+ — sintaxis simplificada
def primero[T](elementos: list[T]) -> T:
    return elementos[0]
```

Las clases genéricas siguen el mismo patrón. Se declara el parámetro de tipo y se usa en los métodos:

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Pila(Generic[T]):
    def __init__(self) -> None:
        self._elementos: list[T] = []

    def apilar(self, elemento: T) -> None:
        self._elementos.append(elemento)

    def desapilar(self) -> T:
        return self._elementos.pop()


pila_enteros: Pila[int] = Pila()
pila_enteros.apilar(42)

pila_textos: Pila[str] = Pila()
pila_textos.apilar("hola")
```

### 20.2.4. Callable

El tipo `Callable` describe funciones y objetos invocables. Su forma es `Callable[[tipos_parametros], tipo_retorno]`:

```python
from typing import Callable

def aplicar(funcion: Callable[[int, int], int], a: int, b: int) -> int:
    return funcion(a, b)

resultado = aplicar(lambda x, y: x + y, 3, 5)  # 8
```

`Callable[[int, int], int]` indica «una función que acepta dos enteros y devuelve un entero». Los tipos de los parámetros van en una lista como primer argumento, y el tipo de retorno como segundo.

Para funciones sin parámetros se usa una lista vacía:

```python
Generador = Callable[[], str]  # función sin parámetros que devuelve str
```

Cuando no se quiere especificar los tipos de los parámetros (solo el tipo de retorno), se usa `...` (puntos suspensivos):

```python
# Cualquier función que devuelva int, sin importar sus parámetros
Operacion = Callable[..., int]
```

`Callable` es útil para anotar funciones de orden superior, callbacks y decoradores.

### 20.2.5. TypedDict

`TypedDict` define un tipo de diccionario con claves específicas, cada una con su propio tipo. A diferencia de `dict[str, int]`, que exige que todas las claves y todos los valores sean del mismo tipo, `TypedDict` permite que cada clave tenga un tipo distinto.

```python
from typing import TypedDict

class Usuario(TypedDict):
    nombre: str
    edad: int
    activo: bool


usuario: Usuario = {"nombre": "Ana", "edad": 30, "activo": True}
```

mypy verifica que el diccionario contenga exactamente las claves declaradas y que cada valor tenga el tipo correcto:

```python
# mypy señala error: falta la clave "activo"
usuario: Usuario = {"nombre": "Ana", "edad": 30}

# mypy señala error: "edad" debería ser int
usuario: Usuario = {"nombre": "Ana", "edad": "treinta", "activo": True}
```

Las claves opcionales se declaran con `NotRequired` (Python 3.11+) o con `total=False`:

```python
from typing import TypedDict, NotRequired

class Usuario(TypedDict):
    nombre: str
    edad: int
    email: NotRequired[str]  # esta clave es opcional


# Ambos son válidos
u1: Usuario = {"nombre": "Ana", "edad": 30}
u2: Usuario = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
```

`TypedDict` es especialmente útil para anotar datos JSON, respuestas de APIs y cualquier diccionario con estructura conocida.

### 20.2.6. ClassVar y Final

`ClassVar` indica que un atributo pertenece a la clase, no a las instancias. En una dataclass, un campo marcado con `ClassVar` no se incluye en el `__init__` generado:

```python
from typing import ClassVar
from dataclasses import dataclass

@dataclass
class Contador:
    nombre: str
    total: ClassVar[int] = 0  # atributo de clase, no de instancia
```

`Final` indica que un nombre no debe reasignarse después de su asignación inicial. Es el equivalente a declarar una constante:

```python
from typing import Final

MAX_INTENTOS: Final = 3
PI: Final[float] = 3.14159

MAX_INTENTOS = 5  # mypy señala error: no se puede reasignar un Final
```

`Final` también puede aplicarse a atributos de clase y métodos (para indicar que una subclase no debe sobrescribirlos), aunque su comprobación es únicamente estática — Python no impide la reasignación en tiempo de ejecución.

---

## 20.3. Herramientas de verificación

### 20.3.1. mypy: instalación y uso básico

Los type hints por sí solos no producen ningún efecto en la ejecución del programa. Para obtener valor de ellos, es necesario usar un **verificador de tipos estático** que analice el código fuente y señale inconsistencias sin ejecutarlo. **mypy** es el verificador más extendido y el estándar de referencia en el ecosistema Python.

La instalación se realiza con pip:

```
pip install mypy
```

Para verificar un archivo o un directorio, se ejecuta mypy desde la línea de comandos:

```
mypy archivo.py
mypy mi_proyecto/
```

mypy analiza las anotaciones de tipo y señala los errores que encuentra. Un ejemplo sencillo:

```python
# ejemplo.py
def duplicar(n: int) -> int:
    return n * 2

resultado: str = duplicar(5)
```

```
$ mypy ejemplo.py
ejemplo.py:4: error: Incompatible types in assignment
    (expression has type "int", variable has type "str")
```

mypy detecta que `duplicar` devuelve `int`, pero la variable `resultado` está anotada como `str`. Este tipo de error es exactamente el que los type hints pretenden prevenir antes de que el programa llegue a ejecutarse.

La adopción de mypy puede ser gradual. No es necesario anotar todo el código de golpe: mypy solo verifica lo que está anotado, y se puede ir ampliando la cobertura poco a poco. El modo estricto (`mypy --strict`) exige que todo el código esté completamente anotado, pero no es necesario usarlo desde el principio.

### 20.3.2. Errores comunes de tipado y cómo resolverlos

Los errores más habituales que mypy detecta son:

**Tipo incompatible en asignación o retorno:**

```python
def longitud(texto: str) -> int:
    return len(texto)

resultado: str = longitud("hola")
# error: Incompatible types in assignment (expression has type "int", variable has type "str")
```

Solución: corregir la anotación de la variable o el tipo de retorno de la función.

**Atributo o método inexistente:**

```python
def procesar(dato: int | str) -> str:
    return dato.upper()  # error: "int" has no attribute "upper"
```

Cuando el tipo es una unión, solo se pueden usar métodos comunes a todos los tipos. Se debe estrechar el tipo primero:

```python
def procesar(dato: int | str) -> str:
    if isinstance(dato, str):
        return dato.upper()
    return str(dato)
```

**Argumento con tipo incorrecto:**

```python
def saludar(nombre: str) -> None:
    print(f"Hola, {nombre}")

saludar(42)
# error: Argument 1 to "saludar" has incompatible type "int"; expected "str"
```

**Valor posiblemente None:**

```python
def buscar(datos: dict[str, int], clave: str) -> int:
    return datos.get(clave)
    # error: Incompatible return value type (got "int | None", expected "int")
```

`dict.get()` puede devolver `None` si la clave no existe. mypy exige que se maneje este caso:

```python
def buscar(datos: dict[str, int], clave: str) -> int | None:
    return datos.get(clave)

# O garantizar que la clave existe:
def buscar(datos: dict[str, int], clave: str) -> int:
    return datos[clave]  # lanza KeyError si no existe, pero el tipo es int
```

**Colección sin tipo parametrizado:**

```python
def sumar_lista(numeros: list) -> int:
    return sum(numeros)
# mypy --strict: error: Missing type parameters for generic type "list"
```

En modo estricto, mypy exige que las colecciones estén parametrizadas. Solución: `list[int]`.

Estas comprobaciones estáticas son las que hacen de mypy una herramienta valiosa: permiten detectar categorías enteras de errores (tipos incorrectos, valores nulos no manejados, atributos inexistentes) durante el desarrollo, antes de que el código llegue a producción.
