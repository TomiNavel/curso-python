# 18. Dataclasses y Enums

Al escribir clases en Python es habitual encontrarse con dos patrones repetitivos. El primero es la clase que existe principalmente para agrupar datos: recibe varios atributos en el constructor, los asigna a `self`, define un `__repr__` para poder imprimirla, y quizá un `__eq__` para compararla con otras instancias. El código resultante es largo, repetitivo y aporta poco valor más allá del contenedor. El segundo patrón es el conjunto de constantes relacionadas: estados de un pedido, prioridades de una tarea, colores de un semáforo. Representarlos con cadenas o números mágicos dispersos por el código es frágil y propenso a errores.

Python ofrece dos herramientas de la biblioteca estándar para resolver estos problemas con precisión. Las **dataclasses** automatizan la creación de clases orientadas a datos, generando métodos comunes a partir de una declaración breve. Los **enums** proporcionan un tipo específico para conjuntos finitos de valores relacionados, dotándolos de identidad, iteración y comparación segura. Ambas abstracciones reducen drásticamente el código repetitivo y hacen el resultado más legible, más seguro y más fácil de mantener.

---

## 18.1. Dataclasses

### 18.1.1. El problema: boilerplate en __init__, __repr__, __eq__

Cuando una clase existe esencialmente para agrupar datos, escribirla a mano implica repetir tres bloques casi idénticos: el constructor que asigna cada argumento a su atributo, un `__repr__` que muestra todos los atributos y un `__eq__` que los compara uno a uno. Este código es mecánico, verboso y una fuente habitual de errores sutiles, como olvidar actualizar el `__repr__` al añadir un atributo nuevo.

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto(x={self.x}, y={self.y})"

    def __eq__(self, otro):
        if not isinstance(otro, Punto):
            return NotImplemented
        return self.x == otro.x and self.y == otro.y
```

Una clase con cinco atributos multiplica este problema: el constructor enumera los cinco, el `__repr__` los enumera de nuevo, y el `__eq__` los compara uno a uno. El código termina ocupando decenas de líneas sin aportar lógica real. Además, estas clases suelen necesitar también `__hash__`, comparaciones de orden, o inmutabilidad, y cada uno de esos añadidos requiere más código repetitivo.

Las dataclasses surgieron en Python 3.7 precisamente para eliminar este boilerplate. Con una sola línea —un decorador— el compilador genera automáticamente `__init__`, `__repr__`, `__eq__` y otros métodos según lo que se declare.

### 18.1.2. @dataclass: sintaxis y campos

El decorador `@dataclass` se aplica a una clase cuyos atributos se declaran al nivel de la clase, acompañados de una anotación de tipo. Python interpreta esas declaraciones como **campos** de la dataclass y genera automáticamente los métodos correspondientes.

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: float
    y: float


p = Punto(3.0, 4.0)
print(p)           # Punto(x=3.0, y=4.0)
print(p == Punto(3.0, 4.0))  # True
```

Con esta declaración, `@dataclass` genera un `__init__` que acepta `x` e `y` como parámetros y los asigna a los atributos correspondientes, un `__repr__` que muestra el nombre de la clase y todos los campos, y un `__eq__` que compara dos instancias campo por campo. El programador solo declara qué campos tiene la clase; el resto es automático.

Las anotaciones de tipo son obligatorias porque son la señal que `@dataclass` usa para detectar los campos. Sin anotación, un atributo se considera un atributo de clase normal y no un campo. El tipo declarado no se comprueba en tiempo de ejecución —Python acepta cualquier valor—, pero sirve como documentación y permite a herramientas como `mypy` verificar el uso. El sistema de tipos se estudia en detalle en el tema 20.

Los campos se convierten en parámetros del `__init__` en el orden en que aparecen. Esto significa que el orden de declaración determina el orden de los argumentos posicionales al crear la instancia.

### 18.1.3. Valores por defecto y field()

Un campo puede tener un valor por defecto asignado directamente tras la anotación de tipo, igual que los parámetros de una función. Los campos con valor por defecto deben aparecer después de los campos sin valor por defecto, por la misma razón que en las funciones.

```python
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    edad: int = 0
    activo: bool = True


u1 = Usuario("Ana")
u2 = Usuario("Luis", 30, False)
print(u1)  # Usuario(nombre='Ana', edad=0, activo=True)
print(u2)  # Usuario(nombre='Luis', edad=30, activo=False)
```

Hay una restricción importante: los valores por defecto **mutables** (listas, diccionarios, sets) no pueden asignarse directamente. Python lo detecta y lanza un error al definir la clase. Esta restricción existe porque, si Python permitiera una lista como valor por defecto, todas las instancias compartirían la misma lista —el mismo problema que con los argumentos por defecto mutables en funciones—.

La solución es usar la función `field` del módulo `dataclasses`, que permite especificar un **factory** (una función sin argumentos que se llama cada vez que se crea una instancia para generar un valor nuevo):

```python
from dataclasses import dataclass, field

@dataclass
class Carrito:
    cliente: str
    productos: list = field(default_factory=list)


c1 = Carrito("Ana")
c2 = Carrito("Luis")
c1.productos.append("Libro")
print(c1.productos)  # ['Libro']
print(c2.productos)  # []  — lista independiente
```

`default_factory=list` significa "llama a `list()` cada vez que se cree una instancia sin especificar `productos`". Cada instancia recibe su propia lista, evitando el problema de estado compartido.

`field` también permite configurar otras propiedades del campo. Los más útiles son `repr=False` (para excluir un campo del `__repr__` generado, útil con datos sensibles o voluminosos) y `compare=False` (para excluirlo del `__eq__`).

### 18.1.4. frozen=True (dataclasses inmutables)

Por defecto, los atributos de una dataclass se pueden modificar después de crear la instancia. En muchos casos esto no es deseable: los objetos que representan datos —una coordenada, una fecha, una configuración— se benefician de ser inmutables, porque así se pueden compartir sin miedo a mutaciones inesperadas y se pueden usar como claves de diccionarios o elementos de sets.

El parámetro `frozen=True` del decorador convierte la dataclass en inmutable. Cualquier intento de reasignar un atributo lanza `FrozenInstanceError`:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordenada:
    latitud: float
    longitud: float


madrid = Coordenada(40.4168, -3.7038)
print(madrid)  # Coordenada(latitud=40.4168, longitud=-3.7038)

madrid.latitud = 0  # FrozenInstanceError
```

Una dataclass frozen también obtiene automáticamente un `__hash__` consistente con su `__eq__`, lo que permite usarla como clave de diccionario o elemento de un set. Las dataclasses no-frozen son no-hashables por defecto, porque dos objetos iguales podrían volverse distintos tras una mutación.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordenada:
    latitud: float
    longitud: float


distancias = {
    Coordenada(40.4168, -3.7038): "Madrid",
    Coordenada(41.3851, 2.1734): "Barcelona",
}
print(distancias[Coordenada(40.4168, -3.7038)])  # Madrid
```

La inmutabilidad de `frozen=True` es superficial: si un campo contiene un objeto mutable (una lista, por ejemplo), el campo en sí no puede reasignarse, pero su contenido sí puede modificarse. Para una inmutabilidad profunda hay que usar tipos inmutables en los campos (tuplas en lugar de listas, `frozenset` en lugar de `set`).

### 18.1.5. order=True (comparación automática)

Por defecto, una dataclass solo genera `__eq__`, que permite comparar dos instancias con `==` y `!=`. No genera los métodos de comparación de orden (`<`, `<=`, `>`, `>=`), porque ordenar datos arbitrarios no siempre tiene sentido. El parámetro `order=True` del decorador fuerza la generación de esos cuatro métodos.

La comparación se realiza campo por campo en el orden en que fueron declarados, como si fuera una tupla. Esto significa que el orden de declaración importa: el primer campo tiene prioridad, y solo en caso de empate se pasa al segundo.

```python
from dataclasses import dataclass

@dataclass(order=True)
class Version:
    mayor: int
    menor: int
    parche: int


v1 = Version(1, 2, 3)
v2 = Version(1, 2, 5)
v3 = Version(2, 0, 0)

print(v1 < v2)   # True  — empate en mayor y menor, v1 menor en parche
print(v2 < v3)   # True  — v2 menor en mayor
print(sorted([v3, v1, v2]))  # [v1, v2, v3]
```

El orden se deriva de la posición de los campos en la clase, no de su nombre. Si se quiere un orden distinto al de los atributos "naturales", conviene reordenar los campos o —si eso rompe la claridad de la API— implementar los métodos de comparación manualmente.

Hay un caso especial cuando `order=True` se combina con campos que no deberían participar en la comparación (por ejemplo, un identificador técnico que no define el orden). En esas situaciones se usa `field(compare=False)` para excluir el campo del ordenamiento.

### 18.1.6. slots=True (Python 3.10+)

Python almacena los atributos de las instancias en un diccionario interno llamado `__dict__`. Esto hace que añadir nuevos atributos sobre la marcha sea trivial, pero tiene un coste: cada instancia arrastra el diccionario, lo que consume más memoria y ralentiza ligeramente el acceso a los atributos.

El parámetro `slots=True` (disponible desde Python 3.10) genera automáticamente la declaración `__slots__` en la clase, reservando un espacio fijo para cada campo y eliminando el `__dict__`. Esto reduce significativamente el consumo de memoria —especialmente útil cuando se crean muchas instancias de la misma dataclass— y suele acelerar ligeramente el acceso a los atributos.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Punto:
    x: float
    y: float


p = Punto(1.0, 2.0)
print(p.x, p.y)     # 1.0 2.0
p.x = 10            # OK: x sigue siendo un slot declarado

p.z = 5             # AttributeError: 'Punto' object has no attribute 'z'
```

La contrapartida es que ya no se pueden añadir atributos nuevos a la instancia fuera de los declarados: todo atributo debe estar en los slots. Esto es exactamente lo que se quería en una dataclass —los campos son los únicos datos que la clase debe tener—, por lo que rara vez supone un problema.

`slots=True` también es incompatible con la herencia múltiple de clases que ya tienen `__dict__`, y requiere cuidado al heredar de otras dataclasses con slots. Para la mayoría de dataclasses sencillas, activar `slots=True` es una optimización recomendable sin coste aparente.

### 18.1.7. __post_init__

El constructor generado por `@dataclass` se limita a asignar los argumentos a los atributos correspondientes. No deja espacio para lógica adicional: validaciones, cálculos derivados, normalización de datos. Para esos casos, las dataclasses ofrecen el método especial `__post_init__`, que se llama automáticamente al final del `__init__` generado.

```python
from dataclasses import dataclass

@dataclass
class Rectangulo:
    base: float
    altura: float

    def __post_init__(self):
        if self.base <= 0 or self.altura <= 0:
            raise ValueError("Las dimensiones deben ser positivas")
        self.area = self.base * self.altura


r = Rectangulo(3, 4)
print(r.area)  # 12

r2 = Rectangulo(-1, 4)  # ValueError: Las dimensiones deben ser positivas
```

`__post_init__` es el lugar adecuado para validar invariantes, derivar atributos calculados a partir de otros campos o realizar cualquier inicialización que no quepa en la simple asignación de argumentos. Se ejecuta después de que todos los campos hayan sido asignados, por lo que dentro del método ya se puede acceder a `self.x`, `self.y`, etc.

El método de excepciones y la sentencia `raise` se estudian en el tema 11.

---

## 18.2. Enums

### 18.2.1. Qué es un Enum y para qué sirve

Un **Enum** (abreviatura de *enumeration*) es un tipo que representa un conjunto finito y nombrado de valores relacionados. Se usa cuando un atributo solo puede tomar uno de varios estados bien definidos: el estado de un pedido (pendiente, enviado, entregado, cancelado), la prioridad de una tarea (baja, media, alta), el color de un semáforo, los días de la semana.

Sin enums, estos valores suelen representarse con cadenas o números mágicos. El problema de ese enfoque es que el código pierde seguridad: nada impide escribir `"entregdo"` en lugar de `"entregado"` y el error solo se descubre cuando una comparación falla silenciosamente. Tampoco hay un lugar centralizado donde consultar cuáles son los valores válidos.

```python
# Sin Enum: propenso a errores
pedido.estado = "pendiente"
if pedido.estado == "pendinte":  # typo silencioso
    ...
```

Un enum convierte esos valores en constantes nombradas pertenecientes a un tipo. La referencia `Estado.PENDIENTE` se verifica al cargar el código: si está mal escrita, Python lanza `AttributeError` inmediatamente. Además, las comparaciones son por identidad, lo que las hace más rápidas y explícitas.

Los enums también aportan iteración —se pueden recorrer todos los valores—, conversión por nombre o por valor, y protección contra la creación de valores nuevos en tiempo de ejecución.

### 18.2.2. Crear enums (Enum, IntEnum, StrEnum)

La forma básica de declarar un enum es heredar de `Enum` y listar los miembros como atributos de clase con un valor asociado. Por convención, los nombres de los miembros se escriben en mayúsculas.

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = 1
    ENVIADO = 2
    ENTREGADO = 3
    CANCELADO = 4


print(Estado.PENDIENTE)        # Estado.PENDIENTE
print(Estado.PENDIENTE.name)   # 'PENDIENTE'
print(Estado.PENDIENTE.value)  # 1
```

Cada miembro tiene dos propiedades: `name` (el nombre como cadena) y `value` (el valor asociado). Los miembros de un `Enum` son objetos únicos: `Estado.PENDIENTE is Estado.PENDIENTE` siempre es `True`, y se recomienda compararlos con `is` en lugar de `==`, aunque ambos funcionan.

Los valores asociados pueden ser de cualquier tipo, pero usarlos directamente en comparaciones requiere acceso explícito a `.value`. Para evitarlo cuando los valores son enteros o cadenas, Python ofrece dos variantes especializadas: `IntEnum` y `StrEnum`.

`IntEnum` hereda además de `int`, de modo que sus miembros se comportan como enteros en todos los contextos donde se espera un `int`:

```python
from enum import IntEnum

class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


print(Prioridad.ALTA > Prioridad.BAJA)  # True
print(Prioridad.ALTA + 1)               # 4  — se suma como entero
```

`StrEnum` (disponible desde Python 3.11) hace lo equivalente con cadenas: sus miembros son instancias de `str` y se pueden usar directamente en comparaciones, interpolación de cadenas o concatenación:

```python
from enum import StrEnum

class Color(StrEnum):
    ROJO = "rojo"
    VERDE = "verde"
    AZUL = "azul"


print(Color.ROJO == "rojo")  # True
print(f"El color es {Color.ROJO}")  # El color es rojo
```

El uso de `IntEnum` y `StrEnum` sacrifica parte de la protección de los enums —sus miembros ya no son estrictamente de un tipo cerrado— a cambio de interoperabilidad con código existente que espera enteros o cadenas. Para código nuevo sin esa necesidad, `Enum` es la opción más segura.

### 18.2.3. Acceso por nombre y por valor

Un enum permite recuperar un miembro a partir de su nombre o de su valor. El acceso por nombre se hace con la sintaxis de diccionario sobre la clase del enum, pasando el nombre como cadena:

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = 1
    ENVIADO = 2
    ENTREGADO = 3


e = Estado["ENVIADO"]
print(e)  # Estado.ENVIADO
```

Si el nombre no existe, Python lanza `KeyError`. Este acceso es útil cuando se deserializan datos —por ejemplo, al leer un estado desde un archivo JSON donde viene guardado como cadena—.

El acceso por valor se hace llamando a la propia clase del enum como si fuera un constructor, pasando el valor:

```python
e = Estado(2)
print(e)  # Estado.ENVIADO
```

Si el valor no corresponde a ningún miembro, Python lanza `ValueError`. Este patrón es el más común al convertir valores externos (enteros de una base de datos, cadenas de una API) en miembros del enum.

Ambas formas de acceso son valiosas para integrar enums con sistemas externos que no conocen el tipo. Internamente, se prefiere siempre el acceso directo por nombre (`Estado.ENVIADO`), que es más claro y más eficiente.

### 18.2.4. Iterar sobre un Enum

Un enum es iterable: al recorrerlo con un bucle `for`, se obtienen sus miembros en el orden en que fueron declarados. Esta propiedad es útil para generar menús, validar entradas o construir diccionarios derivados del enum.

```python
from enum import Enum

class DiaSemana(Enum):
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7


for dia in DiaSemana:
    print(f"{dia.name}: {dia.value}")
# LUNES: 1
# MARTES: 2
# ...
# DOMINGO: 7
```

Además de la iteración con `for`, los enums exponen otras utilidades. `len(DiaSemana)` devuelve el número de miembros. `list(DiaSemana)` produce una lista con todos ellos. `DiaSemana.__members__` es un diccionario ordenado que mapea nombres a miembros, útil cuando se necesita acceso explícito por nombre.

```python
print(len(DiaSemana))              # 7
print(list(DiaSemana)[0])          # DiaSemana.LUNES
print(list(DiaSemana.__members__.keys()))
# ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
```

La iteración respeta el orden de declaración, no el orden de los valores. Esto significa que, aunque los valores sean números desordenados o cadenas, el recorrido sigue siempre el orden del código fuente.
