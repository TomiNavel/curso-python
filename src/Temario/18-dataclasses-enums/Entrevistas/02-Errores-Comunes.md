# Errores Comunes — Dataclasses y Enums

## 1. Usar una lista (u otro mutable) como valor por defecto

```python
from dataclasses import dataclass

@dataclass
class Carrito:
    productos: list = []  # ValueError al definir la clase
```

Python detecta explícitamente este patrón y lanza un error al cargar la clase. La razón es la misma que con los argumentos por defecto mutables en funciones: si se permitiera, todas las instancias compartirían la misma lista y las mutaciones se propagarían entre ellas. La solución correcta es usar `field(default_factory=list)`, que genera una lista nueva por cada instancia.

## 2. Olvidar la anotación de tipo en un campo

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x = 0.0   # sin anotación: NO es un campo
    y: float = 0.0
```

Sin anotación de tipo, `x` no se considera un campo de la dataclass: es un atributo de clase normal y no aparece en el `__init__` generado. El programador cree que está declarando dos campos y en realidad solo declara uno. Este error es silencioso y solo se descubre cuando se intenta crear una instancia pasando `x` como argumento.

## 3. Colocar un campo con valor por defecto antes de uno sin valor

```python
from dataclasses import dataclass

@dataclass
class Usuario:
    edad: int = 0
    nombre: str   # TypeError al definir la clase
```

En el `__init__` generado, los parámetros con valor por defecto deben ir después de los parámetros sin valor por defecto, igual que en una función normal. Python lanza un error al crear la clase. La solución es reordenar los campos, declarando primero los obligatorios.

## 4. Asumir que `frozen=True` hace la dataclass profundamente inmutable

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Pedido:
    cliente: str
    items: list = field(default_factory=list)


p = Pedido("Ana")
p.items.append("Libro")   # funciona: la lista sí es mutable
p.cliente = "Luis"        # FrozenInstanceError
```

`frozen=True` impide reasignar los campos de la instancia, pero no congela los objetos contenidos dentro de esos campos. Si un campo es una lista, su contenido puede modificarse sin error. Para una inmutabilidad real, hay que usar tipos inmutables (tuplas en lugar de listas, `frozenset` en lugar de `set`).

## 5. Esperar que `order=True` genere también `__eq__`

```python
from dataclasses import dataclass

@dataclass(order=True, eq=False)
class Tarea:
    prioridad: int
    titulo: str
```

Si se desactiva `eq`, la comparación de igualdad pasa a heredarse de `object` —es decir, por identidad—, pero los métodos de orden generados por `order=True` siguen comparando campo por campo. El resultado es incoherente: dos instancias con los mismos valores se ordenan correctamente pero `==` devuelve `False`. La regla práctica es dejar `eq=True` (el valor por defecto) cuando se usa `order=True`.

## 6. Comparar enums con cadenas o enteros esperando igualdad

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = "pendiente"

print(Estado.PENDIENTE == "pendiente")  # False
```

Un miembro de `Enum` es un objeto propio del enum, no es intercambiable con su valor subyacente. La comparación con la cadena devuelve `False`. Para comparar con cadenas se usa `Estado.PENDIENTE.value == "pendiente"`, o mejor aún, se recurre a `StrEnum` si la intención del diseño es precisamente esa interoperabilidad.

## 7. Usar `IntEnum` (o `StrEnum`) cuando no hace falta

```python
from enum import IntEnum

class Color(IntEnum):
    ROJO = 1
    VERDE = 2
    AZUL = 3
```

`IntEnum` hereda de `int`, lo que hace que sus miembros se comporten como enteros en comparaciones aritméticas. Esto sacrifica el aislamiento del enum: `Color.ROJO == 1` es `True`, `Color.ROJO + 1` devuelve `2`. Si no hay una razón concreta para que los miembros se comporten como enteros, conviene usar `Enum` simple, que ofrece mayor seguridad al impedir mezclas accidentales con valores primitivos.

## 8. Modificar un Enum tras su definición

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = 1
    ENVIADO = 2

Estado.NUEVO = 3  # AttributeError
```

Los enums son cerrados: no se pueden añadir, modificar ni eliminar miembros tras su creación. Esto es intencional y forma parte de sus garantías de seguridad. Si se necesitan valores dinámicos, el enum es la herramienta equivocada y conviene usar otra estructura, como un diccionario o una clase normal.

## 9. Confundir `name` y `value` de un miembro de Enum

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = 1

print(Estado.PENDIENTE)         # Estado.PENDIENTE (repr)
print(Estado.PENDIENTE.name)    # 'PENDIENTE'
print(Estado.PENDIENTE.value)   # 1
```

Un miembro de Enum tiene dos atributos: `name` es la cadena con el nombre del miembro tal como aparece en el código, y `value` es el valor asociado al miembro. Confundirlos lleva a errores en la serialización (guardar `value` cuando se quería guardar `name`, o al revés) y en la reconstrucción posterior del miembro.

## 10. Hacer cálculos pesados en `__post_init__` sin considerar el coste

```python
from dataclasses import dataclass

@dataclass
class Informe:
    datos: list

    def __post_init__(self):
        self.resumen = calcular_resumen_caro(self.datos)
```

`__post_init__` se ejecuta cada vez que se crea una instancia. Si contiene operaciones costosas, el coste se paga en cada construcción, aunque luego no se use el resultado. Para atributos derivados cuyo cálculo es caro y no siempre se necesita, suele ser preferible usar un método o una property en lugar de calcularlos en `__post_init__`. Las properties se estudiaron en el tema 16.
