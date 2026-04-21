# Python

## 1. Fundamentos de Python

- **1.1. Instalación y Primer Programa**
  - 1.1.1. Qué es Python
  - 1.1.2. Instalación de Python
  - 1.1.3. El intérprete y ejecutar scripts
  - 1.1.4. Entorno de trabajo y gestión de paquetes
- **1.2. Sintaxis Básica**
  - 1.2.1. Indentación y estructura
  - 1.2.2. Comentarios y docstrings
  - 1.2.3. Variables y constantes
  - 1.2.4. Convenciones de nombres (PEP 8)
- **1.3. Tipos de Datos Primitivos**
  - 1.3.1. Números (int, float, complex)
  - 1.3.2. Built-ins numéricas (abs, round, pow, divmod, bin, hex, oct)
  - 1.3.3. Strings (creación y características básicas)
  - 1.3.4. Booleanos y truthiness
  - 1.3.5. None
  - 1.3.6. Conversión de tipos (int, float, str, bool)
- **1.4. Operadores**
  - 1.4.1. Aritméticos
  - 1.4.2. Comparación
  - 1.4.3. Lógicos y cortocircuito
  - 1.4.4. Asignación
  - 1.4.5. Identidad (is, is not)
  - 1.4.6. Pertenencia (in, not in)
- **1.5. Built-ins de entrada/salida e inspección**
  - 1.5.1. print()
  - 1.5.2. input()
  - 1.5.3. type()

## 2. Strings

- **2.1. Características de Strings**
  - 2.1.1. Inmutabilidad
  - 2.1.2. Indexing y slicing
  - 2.1.3. Concatenación y repetición
- **2.2. Métodos de Strings**
  - 2.2.1. Transformación (upper, lower, capitalize, title, strip)
  - 2.2.2. Búsqueda (find, index, count, startswith, endswith)
  - 2.2.3. Validación (isdigit, isalpha, isalnum, isspace)
  - 2.2.4. División y unión (split, join, partition)
  - 2.2.5. Reemplazo (replace, translate)
- **2.3. Tipos especiales de Strings**
  - 2.3.1. Strings multilínea
  - 2.3.2. Raw strings
- **2.4. Formateo de Strings**
  - 2.4.1. f-strings (Python 3.6+)
  - 2.4.2. Formatos anteriores (format(), % formatting)
- **2.5. Alineación y Relleno**
  - 2.5.1. Métodos de alineación (zfill, center, ljust, rjust)
- **2.6. Encoding y Unicode**
  - 2.6.1. encode() y decode()
  - 2.6.2. UTF-8 y otros encodings
  - 2.6.3. chr() y ord()

## 3. Listas y Tuplas

- **3.1. Listas**
  - 3.1.1. Creación y acceso
  - 3.1.2. Slicing
  - 3.1.3. Métodos de modificación (append, insert, extend, remove, pop, clear)
  - 3.1.4. Eliminar elementos (del por índice)
  - 3.1.5. Métodos de consulta (index, count)
  - 3.1.6. Built-ins con iterables (len, max, min, sum)
  - 3.1.7. Ordenamiento (sort, sorted, reverse, reversed)
  - 3.1.8. Constructores de colecciones (list, tuple, set, dict)
  - 3.1.9. Copia (shallow vs deep copy)
  - 3.1.10. Listas anidadas (matrices)
  - 3.1.11. List comprehensions (introducción)
- **3.2. Tuplas**
  - 3.2.1. Características e inmutabilidad
  - 3.2.2. Creación y acceso
  - 3.2.3. Operaciones con tuplas
  - 3.2.4. Desempaquetado (unpacking)
  - 3.2.5. Named tuples

## 4. Diccionarios y Sets

- **4.1. Diccionarios**
  - 4.1.1. Características y hash tables
  - 4.1.2. Creación y acceso
  - 4.1.3. Métodos (get, keys, values, items, update, pop, setdefault, fromkeys)
  - 4.1.4. Counter
- **4.2. Sets**
  - 4.2.1. Características y unicidad
  - 4.2.2. Creación de sets
  - 4.2.3. Operaciones de conjuntos (union, intersection, difference, symmetric_difference)
  - 4.2.4. Métodos de sets (add, remove, discard, pop, update)
  - 4.2.5. frozenset
- **4.3. Iteración sobre diccionarios** *(requiere tema 5)*
- **4.4. Ordenamiento de diccionarios** *(requiere temas 5 y 8)*
- **4.5. defaultdict** *(requiere tema 5)*
- **4.6. deque y OrderedDict** *(requiere tema 5)*

## 5. Control de Flujo

- **5.1. Condicionales**
  - 5.1.1. if, elif, else
  - 5.1.2. Operador ternario
  - 5.1.3. Expresiones booleanas, short-circuit y truthiness
  - 5.1.4. Walrus operator (:=, Python 3.8+)
  - 5.1.5. match/case (Python 3.10+)
- **5.2. Bucles**
  - 5.2.1. for loop
  - 5.2.2. while loop
  - 5.2.3. break, continue, pass
  - 5.2.4. else en bucles
- **5.3. Funciones de iteración**
  - 5.3.1. range()
  - 5.3.2. enumerate()
  - 5.3.3. zip()

## 6. Comprehensions

- **6.1. List Comprehensions**
  - 6.1.1. Sintaxis básica
  - 6.1.2. Comprehension con condición (filtrado)
  - 6.1.3. Comprehension con if/else (transformación condicional)
  - 6.1.4. Comprehensions anidadas
- **6.2. Dict Comprehensions**
- **6.3. Set Comprehensions**
- **6.4. Generator Expressions**
  - 6.4.1. Cuándo usar generator expressions
  - 6.4.2. Limitaciones de los generadores
- **6.5. Cuándo usar y cuándo no usar comprehensions**

## 7. Funciones Básicas

- **7.1. Definición y llamada**
  - 7.1.1. Sintaxis básica
  - 7.1.2. Pasar datos a una función
  - 7.1.3. La sentencia return
  - 7.1.4. Retorno múltiple
- **7.2. Parámetros y argumentos**
  - 7.2.1. Argumentos posicionales y por nombre (keyword)
  - 7.2.2. Valores por defecto
  - 7.2.3. *args: argumentos posicionales variables
  - 7.2.4. **kwargs: argumentos por nombre variables
  - 7.2.5. Desempaquetado de argumentos con * y **
  - 7.2.6. Parámetros solo posicionales y solo keyword (/ y *)
- **7.3. Docstrings**
- **7.4. Funciones como objetos**
  - 7.4.1. Asignar funciones a variables
  - 7.4.2. Funciones en estructuras de datos
  - 7.4.3. Funciones como argumento
- **7.5. Buenas prácticas**
  - 7.5.1. Una función, una tarea
  - 7.5.2. Nombres descriptivos
  - 7.5.3. Evitar efectos secundarios inesperados

## 8. Funciones Avanzadas

- **8.1. Funciones lambda**
  - 8.1.1. Sintaxis y concepto
  - 8.1.2. Cuándo usar lambda
  - 8.1.3. Limitaciones de lambda
- **8.2. Funciones de orden superior**
  - 8.2.1. map()
  - 8.2.2. filter()
  - 8.2.3. sorted() con key y reverse
  - 8.2.4. map y filter vs comprehensions
- **8.3. Recursión**
  - 8.3.1. Concepto y caso base
  - 8.3.2. Recursión vs iteración
  - 8.3.3. Recursión con estructuras de datos
- **8.4. Funciones built-in útiles**
  - 8.4.1. isinstance()
  - 8.4.2. callable()
  - 8.4.3. any() y all()
  - 8.4.4. zip() y enumerate() con funciones

## 9. Scope y Closures

- **9.1. Scope (ámbito de variables)**
  - 9.1.1. Scope local y global
  - 9.1.2. La regla LEGB (Local, Enclosing, Global, Built-in)
  - 9.1.3. La sentencia global
  - 9.1.4. La sentencia nonlocal
- **9.2. Closures**
  - 9.2.1. Funciones anidadas
  - 9.2.2. Qué es un closure y cómo se forma
  - 9.2.3. Late binding en closures (la trampa del for + lambda)
  - 9.2.4. Casos de uso de closures

## 10. Decoradores y functools

- **10.1. Decoradores**
  - 10.1.1. Qué es un decorador y sintaxis @
  - 10.1.2. Crear un decorador básico
  - 10.1.3. Decoradores con argumentos
  - 10.1.4. Decoradores con @wraps
  - 10.1.5. Apilar decoradores
- **10.2. functools**
  - 10.2.1. partial()
  - 10.2.2. reduce()
  - 10.2.3. lru_cache() y @cache

## 11. Manejo de Errores y Excepciones

- **11.1. Excepciones en Python**
  - 11.1.1. Qué es una excepción
  - 11.1.2. Jerarquía de excepciones (BaseException, Exception)
  - 11.1.3. Excepciones comunes (TypeError, ValueError, KeyError, IndexError, AttributeError)
- **11.2. try / except / else / finally**
  - 11.2.1. Sintaxis básica de try/except
  - 11.2.2. Capturar excepciones específicas
  - 11.2.3. Capturar múltiples excepciones
  - 11.2.4. El bloque else
  - 11.2.5. El bloque finally
- **11.3. Lanzar excepciones**
  - 11.3.1. La sentencia raise
  - 11.3.2. Re-lanzar excepciones (raise sin argumento)
- **11.4. Excepciones personalizadas**
  - 11.4.1. Crear excepciones propias (herencia de Exception)
  - 11.4.2. Cuándo crear excepciones personalizadas
- **11.5. Buenas prácticas**
  - 11.5.1. EAFP vs LBYL
  - 11.5.2. No capturar Exception genérica
  - 11.5.3. Mensajes de error descriptivos
  - 11.5.4. ExceptionGroup y except* (Python 3.11+)

## 12. Módulos, Paquetes y Entornos Virtuales

- **12.1. Módulos**
  - 12.1.1. Qué es un módulo
  - 12.1.2. import, from...import, alias (as)
  - 12.1.3. El módulo __main__ y if __name__ == "__main__"
  - 12.1.4. La variable __all__
- **12.2. Paquetes**
  - 12.2.1. Estructura de un paquete (__init__.py)
  - 12.2.2. Imports absolutos y relativos
  - 12.2.3. Organización de un proyecto
- **12.3. Módulos de la librería estándar**
  - 12.3.1. os y pathlib
  - 12.3.2. sys
  - 12.3.3. math y random
  - 12.3.4. collections, functools e itertools (ya vistos)
  - 12.3.5. copy, operator y string
- **12.4. Entornos virtuales y pip**
  - 12.4.1. Qué es un entorno virtual y por qué usarlo
  - 12.4.2. venv: crear y activar
  - 12.4.3. pip: instalar y gestionar dependencias
  - 12.4.4. requirements.txt y pyproject.toml

## 13. Clases y Objetos

- **13.1. Conceptos fundamentales**
  - 13.1.1. Qué es una clase y qué es un objeto
  - 13.1.2. Definir una clase y crear instancias
  - 13.1.3. El método __init__ y self
  - 13.1.4. Atributos de instancia vs atributos de clase
  - 13.1.5. __slots__
- **13.2. Métodos**
  - 13.2.1. Métodos de instancia
  - 13.2.2. Métodos de clase (@classmethod)
  - 13.2.3. Métodos estáticos (@staticmethod)
  - 13.2.4. Cuándo usar cada tipo
- **13.3. Representación de objetos**
  - 13.3.1. __str__ y __repr__
- **13.4. Introspección de atributos**
  - 13.4.1. getattr() y setattr()
  - 13.4.2. hasattr() y delattr()

## 14. Métodos Especiales y Dunder Methods

- **14.1. Qué son los dunder methods**
- **14.2. Operadores aritméticos (__add__, __sub__, __mul__, __truediv__)**
- **14.3. Operadores de comparación (__eq__, __lt__, __le__, __gt__, __ge__)**
  - 14.3.1. @total_ordering
- **14.4. Contenedores (__len__, __getitem__, __setitem__, __delitem__, __contains__)**
- **14.5. Iteración (__iter__, __next__)**
- **14.6. Contexto (__enter__, __exit__)**
- **14.7. Llamabilidad (__call__)**
- **14.8. Booleano y formato (__bool__, __format__)**
- **14.9. Hashing (__hash__)**

## 15. Herencia, Polimorfismo y Composición

- **15.1. Herencia**
  - 15.1.1. Concepto y sintaxis
  - 15.1.2. super() y el MRO (Method Resolution Order)
  - 15.1.3. Sobreescribir métodos
  - 15.1.4. Herencia múltiple y el problema del diamante
- **15.2. Polimorfismo**
  - 15.2.1. Duck typing
  - 15.2.2. Polimorfismo con herencia
  - 15.2.3. isinstance() e issubclass() en contexto de herencia
- **15.3. Composición vs herencia**
  - 15.3.1. Qué es composición
  - 15.3.2. Cuándo usar herencia y cuándo composición

## 16. Encapsulación y Properties

- **16.1. Encapsulación en Python**
  - 16.1.1. Convención de nombre: público, _protegido, __privado
  - 16.1.2. Name mangling (__atributo)
- **16.2. Properties**
  - 16.2.1. El problema: acceso directo vs getters/setters
  - 16.2.2. @property (getter)
  - 16.2.3. @atributo.setter
  - 16.2.4. @atributo.deleter
  - 16.2.5. Properties calculadas

## 17. Clases Abstractas y Protocolos

- **17.1. Clases abstractas (ABC)**
  - 17.1.1. Qué es una clase abstracta y para qué sirve
  - 17.1.2. ABC y @abstractmethod
  - 17.1.3. Métodos abstractos y concretos en una misma clase
  - 17.1.4. Combinar @property con @abstractmethod
- **17.2. Protocolos (structural subtyping)**
  - 17.2.1. Qué es un protocolo (typing.Protocol)
  - 17.2.2. ABC vs Protocol: cuándo usar cada uno

## 18. Dataclasses y Enums

- **18.1. Dataclasses**
  - 18.1.1. El problema: boilerplate en __init__, __repr__, __eq__
  - 18.1.2. @dataclass: sintaxis y campos
  - 18.1.3. Valores por defecto y field()
  - 18.1.4. frozen=True (dataclasses inmutables)
  - 18.1.5. order=True (comparación automática)
  - 18.1.6. slots=True (Python 3.10+)
  - 18.1.7. __post_init__
- **18.2. Enums**
  - 18.2.1. Qué es un Enum y para qué sirve
  - 18.2.2. Crear enums (Enum, IntEnum, StrEnum)
  - 18.2.3. Acceso por nombre y por valor
  - 18.2.4. Iterar sobre un Enum

## 19. Iteradores y Generadores

- **19.1. El protocolo de iteración**
  - 19.1.1. Iterables vs iteradores (__iter__ y __next__)
  - 19.1.2. Crear un iterador personalizado
  - 19.1.3. La función iter() y next()
  - 19.1.4. StopIteration: cómo se señala el fin de la iteración
- **19.2. Generadores**
  - 19.2.1. Qué es un generador y la sentencia yield
  - 19.2.2. Generadores vs iteradores: cuándo usar cada uno
  - 19.2.3. yield from (delegar en sub-generadores)
  - 19.2.4. Generadores infinitos
  - 19.2.5. send() en generadores
- **19.3. Evaluación perezosa (lazy evaluation)**
  - 19.3.1. Ventajas de memoria y rendimiento
  - 19.3.2. itertools: cadenas de iteración eficientes (chain, islice, groupby, product, combinations)

## 20. Type Hints y Typing

- **20.1. Type hints básicos**
  - 20.1.1. Sintaxis y tipos primitivos (int, str, float, bool, None)
  - 20.1.2. Colecciones (list, dict, set, tuple)
  - 20.1.3. Optional y Union (X | Y)
  - 20.1.4. Any
  - 20.1.5. Tipo de retorno y parámetros de funciones
- **20.2. Type hints avanzados**
  - 20.2.1. TypeAlias y type (Python 3.12)
  - 20.2.2. Literal
  - 20.2.3. TypeVar y genéricos
  - 20.2.4. Callable
  - 20.2.5. TypedDict
  - 20.2.6. ClassVar y Final
- **20.3. Herramientas de verificación**
  - 20.3.1. mypy: instalación y uso básico
  - 20.3.2. Errores comunes de tipado y cómo resolverlos

## 21. Context Managers

- **21.1. La sentencia with**
  - 21.1.1. Qué problema resuelve (gestión automática de recursos)
  - 21.1.2. Sintaxis y flujo de ejecución
- **21.2. Crear context managers**
  - 21.2.1. Con clase (__enter__ y __exit__)
  - 21.2.2. Con @contextmanager (contextlib)
  - 21.2.3. Cuándo usar cada enfoque
- **21.3. Context managers múltiples y anidados**
- **21.4. suppress() y otras utilidades de contextlib**

## 22. Trabajo con Archivos y Serialización

- **22.1. Lectura y escritura de archivos**
  - 22.1.1. open() y modos de apertura (r, w, a, x, b)
  - 22.1.2. El parámetro encoding
  - 22.1.3. Leer archivos (read, readline, readlines)
  - 22.1.4. Escribir archivos (write, writelines)
  - 22.1.5. Archivos como iteradores (lectura línea a línea)
- **22.2. pathlib**
  - 22.2.1. Path: crear y manipular rutas
  - 22.2.2. Operaciones con archivos y directorios
  - 22.2.3. pathlib vs os.path
  - 22.2.4. Recorrer directorios (os.walk y Path.rglob)
- **22.3. Serialización**
  - 22.3.1. JSON (json.dumps, json.loads, json.dump, json.load)
  - 22.3.2. CSV (csv.reader, csv.writer, csv.DictReader, csv.DictWriter)
  - 22.3.3. pickle (serialización binaria de objetos Python)

## 23. Expresiones Regulares

- **23.1. Fundamentos de regex**
  - 23.1.1. Qué son y cuándo usarlas
  - 23.1.2. Sintaxis básica (caracteres literales, metacaracteres)
  - 23.1.3. Clases de caracteres (\d, \w, \s, [], [^])
  - 23.1.4. Cuantificadores (*, +, ?, {n}, {n,m})
  - 23.1.5. Anclas (^, $, \b)
- **23.2. El módulo re**
  - 23.2.1. re.search(), re.match(), re.fullmatch()
  - 23.2.2. re.findall() y re.finditer()
  - 23.2.3. re.sub() y re.split()
  - 23.2.4. Grupos de captura y grupos con nombre
  - 23.2.5. Flags (re.IGNORECASE, re.MULTILINE, re.DOTALL)
- **23.3. Patrones comunes**
  - 23.3.1. Validación (email, teléfono, URL)
  - 23.3.2. Extracción de datos de texto
  - 23.3.3. Greedy vs lazy (cuantificadores codiciosos y perezosos)

## 24. Fechas y Tiempo

- **24.1. El módulo datetime**
  - 24.1.1. date, time, datetime
  - 24.1.2. Crear y acceder a componentes (year, month, day, hour, minute)
  - 24.1.3. datetime.now() y datetime.today()
- **24.2. Aritmética de fechas**
  - 24.2.1. timedelta (sumar y restar tiempo)
  - 24.2.2. Comparar fechas
- **24.3. Formateo y parsing**
  - 24.3.1. strftime() (fecha → string)
  - 24.3.2. strptime() (string → fecha)
  - 24.3.3. Formato ISO 8601 (isoformat, fromisoformat)
- **24.4. El módulo time**
  - 24.4.1. time.time() y time.perf_counter()
  - 24.4.2. time.sleep()
- **24.5. Zonas horarias**
  - 24.5.1. Naive vs aware datetimes
  - 24.5.2. zoneinfo (Python 3.9+)

## 25. Testing y Debugging

- **25.1. Testing con pytest**
  - 25.1.1. Instalación y convenciones (test_, assert)
  - 25.1.2. Escribir y ejecutar tests
  - 25.1.3. Fixtures
  - 25.1.4. Parametrización (@pytest.mark.parametrize)
  - 25.1.5. Testear excepciones (pytest.raises)
  - 25.1.6. Cobertura de tests (coverage, pytest-cov)
- **25.2. unittest**
  - 25.2.1. TestCase y métodos assert
  - 25.2.2. setUp y tearDown
  - 25.2.3. pytest vs unittest
- **25.3. Mocking**
  - 25.3.1. unittest.mock (Mock, patch)
  - 25.3.2. Cuándo usar mocks y cuándo no
- **25.4. Debugging**
  - 25.4.1. print debugging y f-strings
  - 25.4.2. breakpoint() y pdb
  - 25.4.3. El debugger del IDE

## 26. Logging

- **26.1. El módulo logging**
  - 26.1.1. Por qué logging en lugar de print
  - 26.1.2. Niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - 26.1.3. Configuración básica (basicConfig)
- **26.2. Handlers y formatters**
  - 26.2.1. StreamHandler y FileHandler
  - 26.2.2. Formateo de mensajes (Formatter)
  - 26.2.3. Múltiples handlers
- **26.3. Loggers jerárquicos**
  - 26.3.1. getLogger() y jerarquía por nombre
  - 26.3.2. Logging en aplicaciones con múltiples módulos

## 27. Concurrencia y Paralelismo

- **27.1. Conceptos fundamentales**
  - 27.1.1. Concurrencia vs paralelismo
  - 27.1.2. El GIL (Global Interpreter Lock)
  - 27.1.3. CPU-bound vs I/O-bound
- **27.2. Threading**
  - 27.2.1. Crear y ejecutar threads
  - 27.2.2. Sincronización (Lock, RLock, Event, Semaphore)
  - 27.2.3. Daemon threads
  - 27.2.4. ThreadPoolExecutor
- **27.3. Multiprocessing**
  - 27.3.1. Crear y ejecutar procesos
  - 27.3.2. Comunicación entre procesos (Queue, Pipe)
  - 27.3.3. ProcessPoolExecutor
- **27.4. concurrent.futures**
  - 27.4.1. Interfaz unificada (submit, map, as_completed)
  - 27.4.2. Cuándo usar threads vs procesos

## 28. Programación Asíncrona

- **28.1. Fundamentos de async**
  - 28.1.1. Qué es programación asíncrona y cuándo usarla
  - 28.1.2. El event loop
  - 28.1.3. async def y await
- **28.2. asyncio**
  - 28.2.1. asyncio.run() y coroutines
  - 28.2.2. asyncio.gather() (ejecutar tareas concurrentes)
  - 28.2.3. asyncio.create_task()
  - 28.2.4. Timeouts y cancelación
- **28.3. Patrones comunes**
  - 28.3.1. Peticiones HTTP asíncronas (aiohttp)
  - 28.3.2. async for, async with y async generators
  - 28.3.3. asyncio.Queue (productor-consumidor)
  - 28.3.4. Async vs threading: cuándo usar cada uno
