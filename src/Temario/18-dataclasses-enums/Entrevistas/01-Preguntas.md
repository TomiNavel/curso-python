# Preguntas de Entrevista — Dataclasses y Enums

1. ¿Qué es una dataclass y qué problema resuelve?
2. ¿Qué métodos genera automáticamente el decorador `@dataclass` por defecto?
3. ¿Por qué las anotaciones de tipo son obligatorias en los campos de una dataclass?
4. ¿Por qué no se puede usar una lista como valor por defecto de un campo y cómo se soluciona?
5. ¿Qué hace `frozen=True` y qué implicaciones tiene sobre `__hash__`?
6. ¿Qué genera `order=True` y cómo decide el orden de comparación entre campos?
7. ¿Qué es `slots=True` y qué ventajas e inconvenientes tiene?
8. ¿Cuándo se utiliza `__post_init__` y qué ocurre dentro de él?
9. ¿Qué es un Enum y en qué se diferencia de usar cadenas o números mágicos?
10. ¿Cuál es la diferencia entre `Enum`, `IntEnum` y `StrEnum`?
11. ¿Cómo se accede a un miembro de un Enum por su nombre y por su valor?
12. ¿Cómo se itera sobre un Enum y en qué orden se obtienen los miembros?

---

## Respuestas

**1. ¿Qué es una dataclass y qué problema resuelve?**

Una dataclass es una clase marcada con el decorador `@dataclass` del módulo `dataclasses`, cuyo propósito es representar datos de forma concisa. Resuelve el problema del código repetitivo (*boilerplate*) que aparece cuando una clase existe principalmente para agrupar atributos: en una clase normal, hay que escribir manualmente el `__init__`, el `__repr__` y el `__eq__`, enumerando los campos en cada uno. Con `@dataclass`, esos métodos se generan automáticamente a partir de la declaración de los campos. El resultado es un código más breve, más legible y menos propenso a errores de mantenimiento (por ejemplo, olvidar actualizar el `__repr__` al añadir un campo).

**2. ¿Qué métodos genera automáticamente el decorador `@dataclass` por defecto?**

Por defecto, `@dataclass` genera tres métodos: `__init__`, que acepta los campos como parámetros y los asigna a los atributos correspondientes; `__repr__`, que devuelve una representación en cadena con el nombre de la clase y todos los campos; y `__eq__`, que compara dos instancias campo por campo. No genera los métodos de comparación de orden (`<`, `<=`, `>`, `>=`) a menos que se active `order=True`, ni un `__hash__` personalizado salvo cuando la dataclass es frozen.

**3. ¿Por qué las anotaciones de tipo son obligatorias en los campos de una dataclass?**

Porque `@dataclass` usa las anotaciones como señal para detectar qué atributos son campos. Un atributo declarado al nivel de la clase sin anotación se considera un atributo de clase normal, no un campo, y no se incluye en el `__init__` generado. Esto es una decisión de diseño: Python no comprueba los tipos en tiempo de ejecución, pero la presencia de la anotación es lo que distingue un campo de dataclass de un simple atributo de clase. Sin anotación, el decorador no sabría qué tiene que procesar.

**4. ¿Por qué no se puede usar una lista como valor por defecto de un campo y cómo se soluciona?**

Porque, si se permitiera, todas las instancias de la dataclass compartirían la misma lista —el mismo objeto en memoria—, exactamente el mismo problema que el argumento por defecto mutable en funciones. Una mutación en una instancia afectaría a todas las demás. Python detecta este patrón y lanza un error al definir la clase. La solución es usar `field(default_factory=list)`, que indica a la dataclass que cree una nueva lista cada vez que se instancia la clase. `default_factory` acepta cualquier función sin argumentos que produzca el valor inicial, lo que también cubre diccionarios, sets o constructores personalizados.

**5. ¿Qué hace `frozen=True` y qué implicaciones tiene sobre `__hash__`?**

`frozen=True` convierte la dataclass en inmutable: cualquier intento de asignar un valor a un campo después de la creación lanza `FrozenInstanceError`. Esto permite usar las instancias como claves de diccionario o elementos de un set, porque su identidad no puede cambiar. Como consecuencia, una dataclass frozen obtiene automáticamente un `__hash__` consistente con su `__eq__`. Las dataclasses no-frozen son no-hashables por defecto, porque dos instancias iguales podrían volverse distintas tras una mutación, invalidando las estructuras hash. Hay que tener en cuenta que la inmutabilidad es superficial: si un campo contiene un objeto mutable, como una lista, su contenido puede modificarse aunque el campo en sí no pueda reasignarse.

**6. ¿Qué genera `order=True` y cómo decide el orden de comparación entre campos?**

`order=True` hace que `@dataclass` genere los cuatro métodos de comparación de orden: `__lt__`, `__le__`, `__gt__` y `__ge__`. La comparación se realiza campo por campo en el orden en que los campos fueron declarados, como si se comparara una tupla con los valores en ese mismo orden. Es decir: primero se compara el primer campo; si empatan, se pasa al segundo; y así sucesivamente. Esto significa que el orden de declaración de los campos importa: para ordenar correctamente hay que listarlos en la prioridad en que deben compararse. Si se necesita excluir un campo del ordenamiento, se puede declarar con `field(compare=False)`.

**7. ¿Qué es `slots=True` y qué ventajas e inconvenientes tiene?**

`slots=True` (disponible desde Python 3.10) hace que la dataclass declare automáticamente `__slots__`, reservando un espacio fijo para cada campo y eliminando el `__dict__` de las instancias. La ventaja es un menor consumo de memoria —relevante cuando se crean miles o millones de instancias— y un acceso a atributos ligeramente más rápido. El inconveniente es que ya no se pueden añadir atributos nuevos a la instancia fuera de los declarados en los slots; cualquier intento lanza `AttributeError`. También introduce restricciones con la herencia múltiple: no se puede combinar fácilmente con clases que ya tienen `__dict__`. Para la mayoría de dataclasses sencillas, `slots=True` es una optimización recomendable y sin efectos adversos, porque el propósito mismo de una dataclass es tener un conjunto fijo de campos.

**8. ¿Cuándo se utiliza `__post_init__` y qué ocurre dentro de él?**

`__post_init__` se utiliza cuando la inicialización no se limita a asignar los argumentos a los campos, sino que necesita lógica adicional: validar invariantes, calcular atributos derivados a partir de otros, normalizar datos, etc. Se llama automáticamente al final del `__init__` generado, cuando todos los campos ya han sido asignados. Dentro del método, `self.x`, `self.y`, etc. ya están disponibles con sus valores. Es el lugar adecuado para comprobar que los datos cumplen las condiciones que la clase espera y lanzar excepciones si no es así, o para derivar valores que no forman parte de los campos declarados pero que dependen de ellos.

**9. ¿Qué es un Enum y en qué se diferencia de usar cadenas o números mágicos?**

Un Enum es un tipo que representa un conjunto finito y nombrado de valores relacionados. A diferencia de usar cadenas o números dispersos por el código, un enum centraliza los valores válidos en un único lugar, los expone como constantes con identidad propia (un miembro de un enum no es intercambiable con un entero o una cadena en general), y permite que el intérprete detecte errores de escritura al cargar el código: una referencia como `Estado.PENDIENTEE` lanza `AttributeError` inmediatamente, mientras que una cadena `"pendientee"` solo fallaría silenciosamente al comparar. Los enums también ofrecen iteración, conversión por nombre o valor, y son más expresivos en el código porque indican claramente que el valor pertenece a un dominio cerrado.

**10. ¿Cuál es la diferencia entre `Enum`, `IntEnum` y `StrEnum`?**

`Enum` es la forma base: sus miembros son objetos de un tipo cerrado, y comparar un miembro con un entero o una cadena devuelve `False` —aunque el valor subyacente coincida—. `IntEnum` hereda además de `int`, de modo que sus miembros se comportan como enteros en todos los contextos donde se espera un `int`: se pueden comparar con otros enteros, sumar, usar en operaciones aritméticas. `StrEnum` (Python 3.11+) hace lo equivalente con cadenas: sus miembros son instancias de `str` y se pueden usar directamente en interpolación o concatenación. La contrapartida de `IntEnum` y `StrEnum` es que pierden parte del aislamiento típico de los enums, porque los valores pueden intercambiarse con los tipos primitivos correspondientes. Para código nuevo sin necesidades de interoperabilidad, `Enum` es la opción más segura; `IntEnum` y `StrEnum` son útiles cuando se necesita compatibilidad con APIs que esperan enteros o cadenas.

**11. ¿Cómo se accede a un miembro de un Enum por su nombre y por su valor?**

Por nombre, se usa la sintaxis de diccionario sobre la clase del enum: `Estado["PENDIENTE"]`. Si el nombre no existe, Python lanza `KeyError`. Por valor, se llama a la clase del enum como si fuera un constructor: `Estado(1)`. Si el valor no corresponde a ningún miembro, Python lanza `ValueError`. Ambas formas son útiles al integrar el enum con datos externos: el acceso por valor es habitual al deserializar información de una base de datos donde los estados se almacenan como enteros, y el acceso por nombre es común al leer valores desde un JSON donde vienen como cadenas. Dentro del código interno, se prefiere siempre la referencia directa (`Estado.PENDIENTE`), que es más clara y eficiente.

**12. ¿Cómo se itera sobre un Enum y en qué orden se obtienen los miembros?**

Un enum es iterable directamente: `for estado in Estado` recorre sus miembros en el orden en que fueron declarados en el código fuente, no en el orden de sus valores. Esto significa que, aunque los valores estén desordenados o no sean comparables (por ejemplo, cadenas), la iteración respeta el orden léxico del código. Además de `for`, se puede convertir el enum en una lista con `list(Estado)`, obtener su longitud con `len(Estado)`, o acceder al diccionario `Estado.__members__`, que mapea nombres a miembros y permite introspección explícita. La iteración es útil para generar menús, validar entradas o construir diccionarios derivados del enum.
