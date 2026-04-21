# Errores Comunes: Type Hints y Typing

## Error 1: Usar Optional cuando se quiere un parámetro con valor por defecto

```python
# MAL — Optional no hace que el parámetro sea omisible
from typing import Optional

def saludar(nombre: Optional[str]) -> str:
    return f"Hola, {nombre or 'invitado'}"

saludar()  # TypeError: missing 1 required positional argument

# BIEN — el valor por defecto es lo que permite omitir el parámetro
def saludar(nombre: str | None = None) -> str:
    return f"Hola, {nombre or 'invitado'}"
```

`Optional[str]` solo dice que el tipo puede ser `str` o `None`. No convierte el parámetro en opcional para la llamada. Para que se pueda omitir, se necesita un valor por defecto.

---

## Error 2: Usar List, Dict, Tuple (de typing) en código moderno

```python
# MAL — deprecado desde Python 3.9
from typing import List, Dict, Tuple

def procesar(datos: List[Dict[str, Tuple[int, int]]]) -> List[str]:
    ...

# BIEN — usar los tipos built-in directamente
def procesar(datos: list[dict[str, tuple[int, int]]]) -> list[str]:
    ...
```

Desde Python 3.9, los tipos built-in (`list`, `dict`, `set`, `tuple`) aceptan parámetros directamente. Las versiones en mayúscula de `typing` están deprecadas y solo se necesitan para mantener compatibilidad con Python 3.8 o anterior.

---

## Error 3: Anotar *args y **kwargs con el tipo del contenedor

```python
# MAL — args ya es una tupla, kwargs ya es un dict
def funcion(*args: tuple[int, ...], **kwargs: dict[str, str]) -> None:
    ...

# BIEN — anotar con el tipo de cada elemento individual
def funcion(*args: int, **kwargs: str) -> None:
    ...
```

Python convierte automáticamente `*args` en una tupla y `**kwargs` en un diccionario. La anotación debe indicar el tipo de cada elemento individual, no el tipo del contenedor. `*args: int` significa «cada argumento posicional es un entero», no «args es un entero».

---

## Error 4: Confundir type hints con validación en tiempo de ejecución

```python
# MAL — asumir que Python rechazará el tipo incorrecto
def calcular(precio: float) -> float:
    return precio * 1.21

calcular("cincuenta")  # Python NO da error por la anotación
# TypeError llega en la multiplicación, no por el type hint
```

Los type hints no producen ningún efecto en tiempo de ejecución. Python los ignora completamente al ejecutar. Para obtener comprobaciones, se necesita una herramienta externa como mypy, o validación explícita con `isinstance`.

---

## Error 5: No parametrizar colecciones en las anotaciones

```python
# MAL — no indica qué contiene la lista
def sumar(numeros: list) -> int:
    return sum(numeros)

# BIEN — especifica el tipo de los elementos
def sumar(numeros: list[int]) -> int:
    return sum(numeros)
```

Una anotación `list` sin parámetros es equivalente a `list[Any]`: mypy no puede verificar qué tipo de elementos contiene. Parametrizar la colección (`list[int]`) permite que mypy detecte errores como pasar una lista de cadenas a una función que espera enteros.

---

## Error 6: Usar Union cuando los tipos comparten una base común

```python
# MAL — innecesariamente específico
def longitud(dato: int | float) -> float:
    return abs(dato)

# BIEN — float ya acepta int en el sistema de tipos de mypy
def longitud(dato: float) -> float:
    return abs(dato)
```

En el sistema de tipos de Python, `int` es compatible con `float` en anotaciones de tipo (aunque no herede de `float` en la jerarquía de clases). Escribir `int | float` es redundante porque mypy ya acepta un `int` donde se espera un `float`. Lo mismo aplica para `int | complex` y `float | complex`.

---

## Error 7: Devolver None implícito sin anotarlo

```python
# MAL — la función puede devolver None pero el tipo no lo refleja
def buscar(datos: list[str], objetivo: str) -> str:
    for item in datos:
        if item == objetivo:
            return item
    # si no encuentra nada, devuelve None implícitamente

# BIEN — reflejar que puede devolver None
def buscar(datos: list[str], objetivo: str) -> str | None:
    for item in datos:
        if item == objetivo:
            return item
    return None
```

Si una función tiene caminos de ejecución sin `return`, Python devuelve `None` implícitamente. Si el tipo de retorno declarado no incluye `None`, mypy señala una inconsistencia. Siempre se debe incluir `None` en el tipo de retorno si la función puede no devolver un valor.

---

## Error 8: Usar Any por pereza en lugar de un tipo preciso

```python
# MAL — desactiva toda comprobación
from typing import Any

def procesar(datos: Any) -> Any:
    return datos["nombre"].upper()

# BIEN — el tipo preciso permite que mypy detecte errores
def procesar(datos: dict[str, str]) -> str:
    return datos["nombre"].upper()
```

`Any` es contagioso: una vez que un valor es `Any`, cualquier operación sobre él produce `Any`, y la comprobación de tipos se pierde en cascada. Usar tipos precisos permite que mypy detecte claves inexistentes, métodos mal escritos o tipos incompatibles.

---

## Error 9: Olvidar que TypedDict es solo para comprobación estática

```python
# MAL — asumir que TypedDict valida en tiempo de ejecución
from typing import TypedDict

class Config(TypedDict):
    host: str
    puerto: int

# Python no da error: TypedDict no valida en ejecución
config: Config = {"host": 123, "puerto": "abc"}
```

`TypedDict` solo afecta a las comprobaciones estáticas de mypy. En tiempo de ejecución, el diccionario es un `dict` normal sin restricciones. Para validación en ejecución se necesitan bibliotecas como pydantic o validación manual.

---

## Error 10: No estrechar el tipo antes de operar con una unión

```python
# MAL — mypy no permite operar directamente sobre la unión
def formatear(valor: int | str) -> str:
    return valor.upper()  # error: "int" has no attribute "upper"

# BIEN — estrechar el tipo con isinstance
def formatear(valor: int | str) -> str:
    if isinstance(valor, str):
        return valor.upper()
    return str(valor)
```

Cuando el tipo es una unión, solo se pueden usar operaciones comunes a todos los tipos de la unión. Para usar operaciones específicas de uno de los tipos, primero hay que estrechar (*narrow*) el tipo con `isinstance`, una comprobación de `is None`, o `assert`.
