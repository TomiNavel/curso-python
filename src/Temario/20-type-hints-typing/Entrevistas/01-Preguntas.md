# Preguntas de Entrevista — Type Hints y Typing

1. ¿Qué son los type hints en Python y qué efecto tienen en tiempo de ejecución?
2. ¿Cuál es la diferencia entre `Optional[str]` y un parámetro con valor por defecto?
3. ¿Cómo se anota una tupla de longitud fija y una de longitud variable?
4. ¿Qué es `Any` y cuándo es apropiado usarlo?
5. ¿Qué es un `TypeVar` y qué problema resuelve?
6. ¿Cómo se anota una función que recibe otra función como parámetro?
7. ¿Qué diferencia hay entre `dict[str, int]` y un `TypedDict`?
8. ¿Qué indica `Final` y qué ocurre si se reasigna un valor marcado como `Final`?
9. ¿Qué es `Literal` y en qué se diferencia de un Enum?
10. ¿Qué es mypy y qué tipo de errores detecta?
11. ¿Cómo se resuelve el error de mypy «X has no attribute Y» cuando el tipo es una unión?
12. ¿Cuál es la diferencia entre `list` y `List` (de typing) en las anotaciones?

---

## Respuestas

**1. ¿Qué son los type hints en Python y qué efecto tienen en tiempo de ejecución?**

Los type hints son anotaciones en la sintaxis de Python que declaran los tipos esperados de variables, parámetros y valores de retorno. Python los almacena en el atributo `__annotations__` del objeto correspondiente, pero no los comprueba ni los utiliza durante la ejecución del programa. Asignar un valor de tipo incorrecto a una variable anotada no produce ningún error en tiempo de ejecución. Su utilidad es triple: documentan el código de forma precisa, permiten que herramientas como mypy detecten errores de tipo de forma estática (sin ejecutar el código), y mejoran el autocompletado y la navegación en editores e IDEs.

**2. ¿Cuál es la diferencia entre `Optional[str]` y un parámetro con valor por defecto?**

`Optional[str]` (equivalente a `str | None`) describe el **tipo** del parámetro: indica que puede ser una cadena o `None`. No dice nada sobre si el parámetro se puede omitir al llamar a la función. Un parámetro con valor por defecto (`nombre: str = "invitado"`) indica que el parámetro se puede omitir en la llamada, y si se omite, toma el valor indicado. Son conceptos independientes: un parámetro puede ser `Optional` y obligatorio (debe pasarse explícitamente, pero acepta `None`), o puede tener valor por defecto sin ser `Optional` (se puede omitir, pero no acepta `None`).

**3. ¿Cómo se anota una tupla de longitud fija y una de longitud variable?**

Una tupla de longitud fija se anota enumerando el tipo de cada posición: `tuple[str, int, bool]` significa «una tupla con exactamente tres elementos: una cadena, un entero y un booleano». Una tupla de longitud variable con elementos homogéneos se anota usando puntos suspensivos: `tuple[int, ...]` significa «una tupla con cualquier número de enteros». La diferencia clave es que la forma fija especifica la cantidad exacta de elementos y permite que cada uno tenga un tipo distinto, mientras que la forma variable describe una secuencia inmutable de elementos del mismo tipo.

**4. ¿Qué es `Any` y cuándo es apropiado usarlo?**

`Any` es un tipo especial del módulo `typing` que desactiva las comprobaciones de tipo para la variable o parámetro anotado. mypy no señala ningún error al usar un valor `Any`, independientemente de las operaciones que se realicen. Es apropiado en dos situaciones: al migrar código existente sin anotaciones, para ir anotando gradualmente sin que mypy lance errores en las partes pendientes; y al interactuar con bibliotecas externas que no proporcionan información de tipos. Fuera de estos casos, `Any` debería evitarse porque elimina la protección que los type hints ofrecen.

**5. ¿Qué es un `TypeVar` y qué problema resuelve?**

Un `TypeVar` declara una variable de tipo que se resuelve al tipo concreto en cada uso, permitiendo escribir funciones y clases genéricas. El problema que resuelve es preservar la relación entre tipos de entrada y salida. Sin `TypeVar`, una función que devuelve un elemento de una lista tendría que anotarse con `Any`, perdiendo la información del tipo. Con `TypeVar`, si se pasa `list[str]` a una función anotada como `def primero(elementos: list[T]) -> T`, mypy infiere que el retorno es `str`. El `TypeVar` actúa como un «comodín con memoria»: puede ser cualquier tipo, pero una vez resuelto a uno concreto en un uso dado, se mantiene consistente.

**6. ¿Cómo se anota una función que recibe otra función como parámetro?**

Con `Callable` del módulo `typing`. La forma es `Callable[[tipos_parametros], tipo_retorno]`. Por ejemplo, `Callable[[int, str], bool]` describe una función que acepta un entero y una cadena y devuelve un booleano. Los tipos de los parámetros van en una lista como primer argumento de `Callable`, y el tipo de retorno como segundo. Para funciones sin parámetros se usa `Callable[[], T]`, y si no se quieren especificar los parámetros se usa `Callable[..., T]`.

**7. ¿Qué diferencia hay entre `dict[str, int]` y un `TypedDict`?**

`dict[str, int]` describe un diccionario donde todas las claves son cadenas y todos los valores son enteros, sin restricción sobre qué claves existen ni cuántas hay. Un `TypedDict` describe un diccionario con claves específicas y conocidas, donde cada clave puede tener un tipo de valor distinto. Por ejemplo, un `TypedDict` con `nombre: str` y `edad: int` exige que el diccionario contenga exactamente esas claves, con esos tipos. `TypedDict` es adecuado para datos con estructura fija (respuestas de APIs, configuraciones), mientras que `dict[K, V]` es apropiado para colecciones homogéneas de pares clave-valor.

**8. ¿Qué indica `Final` y qué ocurre si se reasigna un valor marcado como `Final`?**

`Final` indica que un nombre no debe reasignarse después de su asignación inicial — es el equivalente a declarar una constante. Si se intenta reasignar, mypy señala un error. Sin embargo, Python no impide la reasignación en tiempo de ejecución: `Final` es una indicación puramente estática. La comprobación solo la hacen herramientas como mypy. `Final` también puede aplicarse a atributos de clase para indicar que las subclases no deben sobrescribirlos.

**9. ¿Qué es `Literal` y en qué se diferencia de un Enum?**

`Literal` restringe un tipo a un conjunto concreto de valores literales: `Literal["rojo", "verde"]` solo acepta esas dos cadenas. Un Enum define un tipo nuevo con miembros que tienen identidad propia y no son intercambiables con cadenas o enteros. La diferencia práctica es que `Literal` opera solo a nivel de tipos — en tiempo de ejecución, el valor sigue siendo una cadena o un entero normal. Un Enum, en cambio, existe como tipo en tiempo de ejecución: un miembro de `Color` no es una cadena, y compararlo con una cadena devuelve `False` (salvo con `StrEnum`). `Literal` es adecuado para interfaces sencillas donde definir un Enum sería innecesario; los Enums son preferibles cuando se necesita un tipo con identidad propia, iteración o lógica asociada.

**10. ¿Qué es mypy y qué tipo de errores detecta?**

mypy es un verificador de tipos estático para Python. Analiza el código fuente y las anotaciones de tipo sin ejecutar el programa, señalando inconsistencias. Los errores que detecta incluyen: tipos incompatibles en asignaciones y retornos, llamadas a funciones con argumentos del tipo incorrecto, acceso a atributos o métodos que no existen en el tipo declarado, valores posiblemente `None` que se usan sin comprobar, y colecciones sin parametrizar en modo estricto. La adopción puede ser gradual: mypy solo verifica lo que está anotado, y no es necesario anotar todo el código de golpe.

**11. ¿Cómo se resuelve el error de mypy «X has no attribute Y» cuando el tipo es una unión?**

Cuando una variable tiene un tipo unión (por ejemplo, `int | str`), mypy solo permite operaciones que sean válidas para todos los tipos de la unión. Si se intenta llamar a `.upper()` sobre `int | str`, mypy señala error porque `int` no tiene ese método. La solución es **estrechar el tipo** (*type narrowing*) antes de la operación, típicamente con `isinstance`: `if isinstance(dato, str): dato.upper()`. Dentro del bloque `if`, mypy sabe que `dato` es `str` y permite usar sus métodos. Otras formas de estrechamiento son `assert isinstance(...)`, comprobaciones de `is None` / `is not None`, y `type()`.

**12. ¿Cuál es la diferencia entre `list` y `List` (de typing) en las anotaciones?**

Antes de Python 3.9, los tipos built-in como `list`, `dict` y `set` no podían parametrizarse directamente en las anotaciones (escribir `list[int]` era un error de sintaxis). Para indicar «lista de enteros» se usaba `List[int]` del módulo `typing`. A partir de Python 3.9, los tipos built-in aceptan parámetros directamente (`list[int]`, `dict[str, int]`), y las versiones en mayúscula de `typing` (`List`, `Dict`, `Set`, `Tuple`) quedaron deprecadas. En código nuevo, siempre se deben usar los tipos built-in con minúscula.
