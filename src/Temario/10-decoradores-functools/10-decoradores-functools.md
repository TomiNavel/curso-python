# 10. Decoradores y functools

Los decoradores son una de las herramientas más potentes y características de Python. Permiten modificar o extender el comportamiento de funciones sin cambiar su código, aplicando el principio de separación de responsabilidades: la función hace su trabajo, y el decorador añade funcionalidad transversal (logging, validación, caché, control de acceso). Entender decoradores requiere dominar closures (tema 9), porque un decorador no es más que un closure con un patrón específico.

El módulo `functools` complementa este tema con utilidades que operan sobre funciones: desde crear versiones parcializadas de funciones hasta implementar caché automática de resultados.

---

## 10.1. Decoradores

### 10.1.1. Qué es un decorador y sintaxis @

En cualquier aplicación de cierto tamaño aparece la necesidad de añadir comportamiento transversal a un conjunto de funciones: registrar su ejecución en un log, medir su tiempo de respuesta, validar permisos antes de ejecutarlas o cachear su resultado. La aproximación directa consiste en insertar ese comportamiento dentro del cuerpo de cada función. Esta solución tiene dos inconvenientes graves. El primero es que mezcla la lógica principal de la función con responsabilidades que no le son propias, violando el principio de separación de responsabilidades. El segundo es que produce duplicación: el mismo bloque de código se repite en múltiples funciones, y cualquier modificación posterior obliga a tocar todos los puntos donde se aplicó.

Los decoradores son el mecanismo que Python ofrece para resolver este problema. Un decorador es una abstracción que permite envolver una función dentro de otra, de modo que la lógica transversal quede encapsulada en un único lugar y pueda aplicarse sobre cualquier función sin modificar su código. La función original conserva su definición íntegra; el decorador se limita a interponer una capa adicional que se ejecuta antes, después o alrededor de la invocación original.

La denominación "decorador" proviene de esa idea de interposición: el decorador *decora* la función añadiéndole capacidades sin alterar su implementación. Desde el punto de vista del código que la invoca, la función conserva su nombre y su firma; la capa añadida por el decorador es transparente para el llamante.

**Un decorador es una función de orden superior que recibe otra función como argumento y devuelve una nueva función**, típicamente una versión envuelta de la original. La sintaxis `@decorador` situada sobre una definición de función es una notación abreviada que el intérprete traduce internamente a la asignación manual equivalente:

```python
@mi_decorador
def saludar():
    print("Hola")

# Equivale exactamente a:
def saludar():
    print("Hola")
saludar = mi_decorador(saludar)
```

Comprender esta equivalencia resulta fundamental. El símbolo `@` no introduce ningún mecanismo oculto: Python toma la función recién definida, la pasa como argumento al decorador y reasigna el identificador al valor devuelto. A partir de ese instante, toda invocación de `saludar()` no ejecuta la función original, sino el objeto que `mi_decorador` devolvió —habitualmente una función envoltorio que, en su interior, termina llamando a la original.

### 10.1.2. Crear un decorador básico

Todo decorador responde al mismo patrón estructural: una función externa que recibe la función original, una función interna —denominada envoltorio o *wrapper*— que la invoca añadiendo lógica antes o después, y el retorno del envoltorio para que sustituya a la función decorada. El envoltorio accede a la función original mediante un closure sobre el parámetro `func`.

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes de la función")
        resultado = func(*args, **kwargs)
        print("Después de la función")
        return resultado
    return wrapper

@mi_decorador
def sumar(a, b):
    return a + b

print(sumar(3, 5))
# Antes de la función
# Después de la función
# 8
```

El uso de `*args` y `**kwargs` en la firma del envoltorio permite aceptar cualquier combinación de argumentos posicionales y por palabra clave, y retransmitirlos íntegramente a la función original. De este modo el decorador resulta aplicable a funciones con firmas arbitrarias; omitirlos lo restringiría a funciones con una firma concreta.

Entre otras características, un decorador también puede transformar el valor de retorno de la función original. El siguiente decorador convierte a mayúsculas el texto devuelto por cualquier función que decore:

```python
def en_mayusculas(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        return resultado.upper()
    return wrapper

@en_mayusculas
def saludar(nombre):
    return f"Hola, {nombre}"

print(saludar("Ana"))  # "HOLA, ANA"
```

### 10.1.3. Decoradores con argumentos

A veces se necesita configurar el comportamiento del decorador. Por ejemplo, un decorador que repita la ejecución un número configurable de veces. Para esto se añade un nivel más de anidamiento: una función que recibe los argumentos del decorador y devuelve el decorador real.

```python
def repetir(veces):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(veces=3)
def saludar(nombre):
    print(f"Hola, {nombre}")

saludar("Ana")
# Hola, Ana
# Hola, Ana
# Hola, Ana
```

La mecánica es: `@repetir(veces=3)` primero ejecuta `repetir(veces=3)`, que devuelve `decorador`. Después Python aplica `decorador` a `saludar`, que devuelve `wrapper`. Es decir, se ejecuta `saludar = repetir(veces=3)(saludar)`.

Son tres niveles de funciones anidadas:
1. `repetir(veces)` — recibe la configuración, devuelve el decorador
2. `decorador(func)` — recibe la función, devuelve el wrapper
3. `wrapper(*args, **kwargs)` — ejecuta la lógica

### 10.1.4. Decoradores con @wraps

Toda función en Python lleva asociado un conjunto de metadatos accesibles mediante atributos especiales: `__name__` contiene su nombre, `__doc__` su docstring, `__module__` el módulo donde se definió, y existen otros como `__qualname__` o `__annotations__`. Estos metadatos los consultan herramientas como los depuradores, los generadores de documentación, los frameworks de test y cualquier código que use introspección.

Al decorar una función, el identificador original queda reasignado al envoltorio. En consecuencia, los metadatos que se consultan sobre la función decorada son los del envoltorio, no los de la función original, lo que distorsiona cualquier herramienta que dependa de ellos.

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

print(sumar.__name__)  # "wrapper" — no "sumar"
print(sumar.__doc__)   # None — no "Suma dos números."
```

`functools.wraps` es un decorador del módulo estándar que resuelve este problema: aplicado al envoltorio, copia en él los metadatos de la función original (`__name__`, `__doc__`, `__module__`, `__qualname__`, `__annotations__` y `__wrapped__`). El resultado es un envoltorio indistinguible de la función original desde el punto de vista de la introspección.

Para utilizarlo basta con importarlo al principio del archivo mediante `from functools import wraps`. `functools` forma parte de la biblioteca estándar de Python, por lo que no requiere instalación; el mecanismo completo de módulos e importaciones se estudia en el tema 12.

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

print(sumar.__name__)  # "sumar"
print(sumar.__doc__)   # "Suma dos números."
```

Aplicar `@wraps` debe considerarse parte obligatoria del patrón de cualquier decorador. Sin él, herramientas como `help(sumar)` mostrarán la documentación del envoltorio en lugar de la de la función original, los mensajes de error y las trazas de pila harán referencia a `wrapper` en lugar del nombre real, y frameworks como pytest o Sphinx producirán resultados incorrectos al inspeccionar las funciones decoradas.

### 10.1.5. Apilar decoradores

Se pueden aplicar múltiples decoradores a una misma función. Se apilan de abajo hacia arriba — el decorador más cercano a la función se aplica primero:

```python
@decorador_a
@decorador_b
def funcion():
    pass

# Equivale a:
funcion = decorador_a(decorador_b(funcion))
```

El orden importa. `decorador_b` envuelve a la función original, y `decorador_a` envuelve el resultado de `decorador_b`:

```python
from functools import wraps

def negrita(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def cursiva(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@negrita
@cursiva
def saludo(nombre):
    return f"Hola, {nombre}"

print(saludo("Ana"))  # <b><i>Hola, Ana</i></b>
```

`cursiva` se aplica primero (está más cerca de la función), así que envuelve el texto en `<i>`. Después `negrita` envuelve el resultado en `<b>`. Si se invirtiera el orden, el resultado sería `<i><b>Hola, Ana</b></i>`.

---

## 10.2. functools

El módulo `functools` contiene funciones de orden superior — funciones que actúan sobre otras funciones. Ya se ha visto `wraps` en la sección anterior; aquí se cubren las tres utilidades más usadas del módulo.

`functools` forma parte de la biblioteca estándar de Python, por lo que no requiere instalación. Para usar sus utilidades basta con importarlas al principio del archivo mediante `from functools import <nombre>`. El mecanismo completo de módulos e importaciones se estudia en el tema 12.

### 10.2.1. partial()

`functools.partial` crea una nueva función a partir de otra, fijando algunos de sus argumentos. Es útil cuando se necesita una función con menos parámetros que la original, sin tener que definir una nueva función o usar una lambda.

```python
from functools import partial

def potencia(base, exponente):
    return base ** exponente

# Crear versiones especializadas fijando el exponente
cuadrado = partial(potencia, exponente=2)
cubo = partial(potencia, exponente=3)

print(cuadrado(5))  # 25
print(cubo(5))      # 125
```

`partial` es una alternativa más legible a las lambdas cuando solo se fijan argumentos:

```python
# Con lambda — funciona pero es más verboso
cuadrado = lambda base: potencia(base, exponente=2)

# Con partial — más directo
cuadrado = partial(potencia, exponente=2)
```

Un uso frecuente es con callbacks o funciones que esperan una firma específica:

```python
from functools import partial

def formatear_precio(cantidad, moneda="€", decimales=2):
    return f"{cantidad:.{decimales}f} {moneda}"

# Crear formateadores especializados
precio_eur = partial(formatear_precio, moneda="€", decimales=2)
precio_btc = partial(formatear_precio, moneda="BTC", decimales=8)

print(precio_eur(19.5))      # "19.50 €"
print(precio_btc(0.00045))   # "0.00045000 BTC"
```

### 10.2.2. reduce()

`functools.reduce` colapsa un iterable en un único valor aplicando de forma acumulativa una función binaria a sus elementos. El procesamiento avanza de izquierda a derecha: la función recibe los dos primeros elementos del iterable y produce un resultado parcial; ese resultado se combina con el siguiente elemento mediante la misma función, y así sucesivamente hasta agotar el iterable. El valor final es el resultado de la última invocación.

```python
from functools import reduce

numeros = [1, 2, 3, 4, 5]

# Secuencia de cálculo: ((((1+2)+3)+4)+5) = 15
suma = reduce(lambda a, b: a + b, numeros)
print(suma)  # 15
```

`reduce` admite un tercer argumento opcional que actúa como valor inicial del acumulador. Cuando se proporciona, la primera invocación de la función binaria recibe ese valor y el primer elemento del iterable, en lugar de los dos primeros elementos. Este valor inicial resulta imprescindible si el iterable puede estar vacío: sin él, `reduce` lanza `TypeError` al no disponer de ningún valor sobre el que operar.

```python
# Con valor inicial: el acumulador parte de 100
suma_desde_100 = reduce(lambda a, b: a + b, numeros, 100)
print(suma_desde_100)  # 115

# Con iterable vacío y valor inicial, el resultado es el propio valor inicial
reduce(lambda a, b: a + b, [], 0)  # 0
```

En el Python moderno, el uso directo de `reduce` ha quedado relegado a casos específicos. La mayoría de las operaciones acumulativas frecuentes disponen de alternativas nativas más legibles y eficientes: `sum()` para sumas, `max()` y `min()` para extremos, `math.prod()` para productos, y las comprehensions o los bucles explícitos para transformaciones complejas. De hecho, Guido van Rossum —creador del lenguaje— trasladó `reduce` de las funciones integradas al módulo `functools` en Python 3 precisamente para desincentivar su uso indiscriminado. Su aplicación se justifica únicamente cuando la operación acumulativa no posee un equivalente nativo y resulta más clara expresada como reducción que como bucle.

### 10.2.3. lru_cache() y @cache

`functools.lru_cache` es un decorador que aplica memoización automática sobre la función decorada. El término *memoización* describe la técnica de almacenar los resultados de una función para reutilizarlos en llamadas posteriores con los mismos argumentos, evitando recalcularlos. Internamente, `lru_cache` mantiene un diccionario cuyas claves son las combinaciones de argumentos ya vistas y cuyos valores son los resultados correspondientes; cuando la función se invoca, el decorador comprueba primero si los argumentos actuales están en esa tabla y, si lo están, devuelve el valor almacenado sin ejecutar el cuerpo de la función.

El acrónimo *LRU* significa *Least Recently Used*. Se refiere a la política de desalojo que aplica la caché cuando alcanza su capacidad máxima: al llegar al límite, los resultados cuyo acceso es más antiguo se descartan para dejar espacio a las nuevas entradas. Esta estrategia prioriza mantener en memoria los valores consultados con mayor frecuencia reciente.

El ejemplo canónico de su utilidad es la sucesión de Fibonacci calculada recursivamente. Sin caché, cada llamada a `fibonacci(n)` genera dos llamadas a `fibonacci(n-1)` y `fibonacci(n-2)`, lo que produce un árbol de invocaciones de tamaño exponencial con innumerables subproblemas repetidos. Con caché, cada valor `fibonacci(k)` se calcula una única vez y se reutiliza, reduciendo la complejidad temporal de exponencial a lineal.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))  # 12586269025 — cálculo instantáneo gracias a la caché
```

El parámetro `maxsize` determina la capacidad máxima de la caché, expresada en número de entradas almacenadas. En el ejemplo, la caché conserva hasta 128 resultados; si se superase ese límite, las entradas menos recientemente usadas serían descartadas. La función decorada expone además dos métodos auxiliares para inspeccionar y gestionar su estado:

```python
print(fibonacci.cache_info())
# CacheInfo(hits=48, misses=51, maxsize=128, currsize=51)

fibonacci.cache_clear()  # elimina todas las entradas almacenadas
```

`cache_info()` devuelve una tupla con nombre que informa de los aciertos (*hits*), los fallos (*misses*), la capacidad configurada y la ocupación actual. Esta información resulta útil para evaluar la efectividad de la memoización: una proporción alta de aciertos indica que la caché está cumpliendo su propósito, mientras que una proporción baja sugiere que los argumentos rara vez se repiten y la caché aporta poco.

Desde Python 3.9, el módulo `functools` incluye el decorador `@cache` como abreviatura de `@lru_cache(maxsize=None)`. Al establecer `maxsize=None` se desactiva el límite de capacidad, de modo que la caché crece sin restricciones y nunca desaloja entradas.

```python
from functools import cache

@cache
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

La elección entre `@cache` y `@lru_cache` depende del rango de valores con que la función vaya a invocarse. Para funciones cuyo dominio es acotado y conocido —como el factorial o Fibonacci dentro de un rango razonable—, `@cache` resulta adecuado por su simplicidad. En cambio, para funciones que pueden recibir un número potencialmente ilimitado de argumentos distintos, `@cache` provocaría un crecimiento ilimitado del consumo de memoria; en ese escenario es preferible `@lru_cache(maxsize=N)` con un límite razonable.

Existe una restricción importante aplicable a ambos decoradores: los argumentos de la función memoizada deben ser *hashables*, es decir, inmutables y con una implementación válida de `__hash__`. Esta limitación se deriva de que los argumentos se utilizan como claves del diccionario interno que implementa la caché, y los diccionarios de Python solo admiten claves hashables. En consecuencia, no pueden memoizarse funciones que reciban listas, diccionarios o conjuntos como parámetros; sí pueden recibir tuplas, cadenas, números o `frozenset`.
