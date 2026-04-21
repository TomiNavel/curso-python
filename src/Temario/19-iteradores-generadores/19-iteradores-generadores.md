# 19. Iteradores y Generadores

Python convierte la iteración en un mecanismo universal: cualquier objeto puede recorrerse con un bucle `for`, pasarse a `list`, a `sum` o a una comprehension, siempre que cumpla un contrato bien definido. Este contrato se llama **protocolo de iteración** y es la base sobre la que se construyen las listas, los diccionarios, los archivos abiertos, los rangos y muchas otras estructuras aparentemente distintas entre sí. Entender el protocolo no es solo un detalle académico: es la clave para comprender por qué un archivo puede leerse línea a línea sin cargarlo entero en memoria, por qué una comprehension encerrada en paréntesis se comporta de forma distinta a una entre corchetes, y por qué existen funciones como `enumerate` o `zip` que aceptan cualquier cosa recorrible.

Sobre este protocolo, Python ofrece una herramienta especialmente potente: los **generadores**. Un generador es una función que produce valores de forma perezosa, uno a uno, pausando su ejecución entre cada valor y reanudándola cuando se pide el siguiente. Esta simple idea —pausar y reanudar— permite representar secuencias infinitas, procesar ficheros gigantes sin saturar la memoria, componer transformaciones de datos como tuberías eficientes y, en general, separar la producción de los datos de su consumo. Este tema explica primero el protocolo que subyace a toda la iteración en Python, después los generadores como forma elegante de implementarlo y, por último, el concepto de evaluación perezosa junto con `itertools`, el módulo que lleva este estilo hasta sus últimas consecuencias.

---

## 19.1. El protocolo de iteración

### 19.1.1. Iterables vs iteradores (__iter__ y __next__)

En Python conviene distinguir con precisión entre dos conceptos que suelen confundirse: un **iterable** y un **iterador**. Un iterable es cualquier objeto que puede recorrerse con `for`: listas, tuplas, strings, diccionarios, sets, archivos, rangos. Un iterador es el objeto interno que efectivamente produce los elementos uno a uno durante ese recorrido. La diferencia es sutil pero importante: el iterable es la fuente, el iterador es el proceso de consumirla.

Formalmente, un iterable es un objeto que implementa el método `__iter__`, cuya responsabilidad es devolver un iterador nuevo cada vez que se le pide. Un iterador es un objeto que implementa dos métodos: `__iter__`, que debe devolverse a sí mismo, y `__next__`, que produce el siguiente elemento o lanza `StopIteration` cuando ya no quedan más. Esta doble condición —implementar `__iter__` y `__next__`— es lo que convierte un objeto en iterador.

Cuando se escribe `for x in lista`, Python llama internamente a `iter(lista)` para obtener un iterador y después llama repetidamente a `next()` sobre ese iterador hasta que aparece `StopIteration`, momento en el que el bucle termina. Este mecanismo explica por qué una lista puede recorrerse varias veces: cada `for` crea un iterador nuevo a partir de la lista original, y cada iterador mantiene su propio estado interno. En cambio, un iterador ya consumido no puede reiniciarse: una vez agotado, llamarlo de nuevo devolverá inmediatamente `StopIteration`.

```python
numeros = [10, 20, 30]

it = iter(numeros)
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
# next(it) lanzaría StopIteration

it2 = iter(numeros)
print(next(it2))  # 10 — un iterador nuevo empieza de cero
```

La lista `numeros` es un iterable reutilizable: de ella se pueden obtener tantos iteradores independientes como se necesiten. Los iteradores `it` e `it2` son instancias distintas con estado propio. Esta separación entre iterable y iterador es la que permite que dos bucles anidados sobre la misma lista funcionen como se espera.

### 19.1.2. Crear un iterador personalizado

Un iterador personalizado se define como una clase que implementa `__iter__` y `__next__`. El método `__iter__` debe devolver `self`, ya que la propia clase actúa como iterador. El método `__next__` mantiene el estado interno, produce el siguiente valor y lanza `StopIteration` cuando se agota la secuencia. Este patrón es la implementación manual del protocolo, útil para entender qué ocurre por debajo antes de recurrir a los generadores, que automatizan gran parte del trabajo.

```python
class Contador:
    def __init__(self, limite):
        self.limite = limite
        self.actual = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual >= self.limite:
            raise StopIteration
        valor = self.actual
        self.actual += 1
        return valor


for n in Contador(3):
    print(n)  # 0, 1, 2
```

Esta clase actúa simultáneamente como iterable y como iterador. Al declarar `__iter__` como `return self`, cada instancia devuelve una única fuente de iteración: su propio estado interno. Tiene una consecuencia importante: un objeto `Contador` solo puede recorrerse una vez, porque después del recorrido el atributo `actual` ha llegado al límite y no se reinicia. Para permitir múltiples recorridos habría que separar iterable e iterador en dos clases distintas: una que represente la secuencia y otra que, a partir de ella, produzca un iterador nuevo cada vez.

En la práctica, escribir iteradores a mano es raro. Los generadores —la siguiente sección— ofrecen la misma funcionalidad con mucho menos código, manteniendo el estado de forma automática mediante la sentencia `yield`.

### 19.1.3. La función iter() y next()

Las funciones incorporadas `iter` y `next` son la interfaz pública del protocolo de iteración. La función `iter(obj)` devuelve un iterador a partir de un iterable, llamando internamente al método `__iter__` del objeto. La función `next(iterador)` produce el siguiente valor, llamando internamente a `__next__`. Cuando se llega al final de la secuencia, `next` propaga la excepción `StopIteration`.

Aunque el bucle `for` las usa de forma implícita, hay situaciones en las que conviene llamarlas manualmente: para avanzar un paso concreto, para saltarse el primer elemento, para componer varias iteraciones o para obtener el primer valor de un generador sin recorrerlo entero. La función `next` admite también un segundo argumento que actúa como valor por defecto cuando el iterador se ha agotado, evitando tener que capturar `StopIteration` manualmente.

```python
numeros = iter([1, 2, 3])
print(next(numeros))       # 1
print(next(numeros))       # 2
print(next(numeros))       # 3
print(next(numeros, -1))   # -1 — valor por defecto al agotar el iterador
```

El uso del segundo argumento de `next` es un patrón limpio para consumir el primer elemento de una secuencia sin arriesgarse a que falle si está vacía. Resulta especialmente útil con generadores y con expresiones que producen como máximo un valor, ya que evita escribir bloques `try/except` que enturbian el código.

### 19.1.4. StopIteration: cómo se señala el fin de la iteración

`StopIteration` es una excepción específica del protocolo de iteración, cuya única función es señalar que un iterador ha terminado. No es un error en sentido estricto: es la forma normal y esperada de comunicar que no quedan más elementos. Los bucles `for` la capturan silenciosamente y terminan, mientras que las funciones como `list`, `sum` o `max` interpretan su aparición como la señal para detenerse.

Cuando se implementa un iterador a mano, lanzar `StopIteration` es lo que permite que el bucle `for` sepa cuándo parar. En los generadores —que se estudian a continuación— este comportamiento es automático: al llegar al final de la función generadora, Python lanza `StopIteration` por detrás sin que el programador tenga que hacerlo explícitamente. Las excepciones se estudian en el tema 11; aquí basta con entender que `StopIteration` no debe capturarse desde código de usuario salvo en contadas situaciones, porque hacerlo suele romper el flujo natural de iteración.

Hay una sutileza que conviene mencionar: desde Python 3.7 (PEP 479) ya no se puede propagar accidentalmente un `StopIteration` desde dentro de un generador. Si el cuerpo del generador lanza esa excepción, Python la convierte automáticamente en `RuntimeError`, previniendo un antiguo foco de bugs difíciles de detectar. Esta regla protege al programador de errores sutiles, pero también significa que capturar `StopIteration` dentro de un generador y no manejarla correctamente puede provocar un error distinto al esperado.

---

## 19.2. Generadores

### 19.2.1. Qué es un generador y la sentencia yield

Un generador es una función que, en lugar de calcular todos sus resultados de golpe y devolverlos con `return`, los produce uno a uno mediante la sentencia `yield`. Cada vez que la función llega a un `yield`, se detiene y entrega ese valor al exterior. Cuando se le pide el siguiente valor, reanuda exactamente donde se había detenido, con todas sus variables locales intactas. Esta capacidad de **pausar y reanudar** es lo que distingue a un generador de una función normal y lo que lo convierte en la forma más natural de escribir iteradores en Python.

Cuando el intérprete encuentra `yield` en el cuerpo de una función, esa función deja de ser una función ordinaria y se transforma en una **función generadora**. Llamarla no ejecuta su cuerpo: devuelve inmediatamente un objeto generador, que es un iterador completo con `__iter__` y `__next__` ya implementados automáticamente. El cuerpo solo empieza a ejecutarse cuando se le pide el primer valor, y se reanuda parcialmente cada vez que se pide el siguiente.

```python
def contar_hasta(limite):
    actual = 0
    while actual < limite:
        yield actual
        actual += 1


gen = contar_hasta(3)
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2
# next(gen) lanzaría StopIteration

for n in contar_hasta(3):
    print(n)  # 0, 1, 2
```

La función `contar_hasta` describe una secuencia, no la construye. Cuando se ejecuta `gen = contar_hasta(3)`, Python no imprime nada ni calcula nada: simplemente crea el objeto generador. El primer `next(gen)` entra en el cuerpo, ejecuta hasta el `yield`, devuelve el valor `0` y congela el estado justo después de ese `yield`. El siguiente `next(gen)` reanuda exactamente en ese punto, incrementa `actual`, vuelve al inicio del bucle y alcanza otro `yield`. Cuando la condición del bucle deja de cumplirse, la función termina y Python lanza `StopIteration` automáticamente.

Comparado con el iterador manual de la sección anterior, el código es drásticamente más corto y más directo. El generador no requiere declarar una clase, no necesita atributos explícitos para guardar el estado y no exige lanzar `StopIteration` a mano. Todo se deriva automáticamente de la estructura del propio cuerpo de la función.

### 19.2.2. Generadores vs iteradores: cuándo usar cada uno

En términos formales, todo generador es un iterador, pero no todo iterador es un generador. Un generador se escribe como una función con `yield`, mientras que un iterador clásico se escribe como una clase con `__iter__` y `__next__`. El protocolo que exponen al exterior es idéntico —ambos pueden usarse en un `for`, pasarse a `list`, a `sum` o a una comprehension—, de modo que la elección entre uno y otro depende sobre todo de factores de legibilidad y de control sobre el estado.

Los generadores son la forma preferida en la mayoría de los casos. Requieren menos código, mantienen el estado automáticamente entre llamadas y expresan la intención de producir una secuencia con una claridad difícil de superar. Son ideales para representar secuencias calculadas, transformaciones sobre otras iteraciones, lectura perezosa de datos o cualquier situación en la que los valores se generen uno tras otro.

Los iteradores implementados como clase solo resultan preferibles cuando la lógica es compleja, cuando el iterador necesita exponer métodos adicionales más allá de `__next__`, cuando debe soportar operaciones fuera del protocolo estándar (como reinicios, consultas de progreso o ajustes en caliente), o cuando forma parte de una jerarquía de clases donde la orientación a objetos facilita la reutilización. En esos escenarios, el control explícito sobre la instancia compensa la verbosidad añadida. En todos los demás casos, un generador es más breve, más claro y más idiomático.

### 19.2.3. yield from (delegar en sub-generadores)

La expresión `yield from` permite a un generador delegar la producción de valores en otro iterable. En lugar de escribir un bucle que consuma ese iterable y reemita sus valores uno por uno, se utiliza `yield from` para hacer lo mismo en una sola línea. Esta forma es más clara, más rápida y, además, transmite correctamente el estado del sub-generador, incluidos `send`, `throw` y el valor de retorno final.

```python
def pares(limite):
    for n in range(limite):
        if n % 2 == 0:
            yield n


def impares(limite):
    for n in range(limite):
        if n % 2 == 1:
            yield n


def todos(limite):
    yield from pares(limite)
    yield from impares(limite)


print(list(todos(6)))  # [0, 2, 4, 1, 3, 5]
```

La función `todos` produce primero todos los valores del generador `pares` y, cuando este termina, pasa a producir los del generador `impares`. Escribir lo mismo sin `yield from` requeriría dos bucles anidados con sus respectivos `yield`, añadiendo ruido innecesario al código. La expresión `yield from` encapsula ese patrón y deja el propósito de la función mucho más visible.

`yield from` es también la base para componer generadores recursivos —por ejemplo, para recorrer árboles— y para construir tuberías de transformación donde cada generador encadena el resultado del siguiente. Su comportamiento exacto con respecto a `send` y `throw` está documentado en el PEP 380, pero para el uso cotidiano basta entenderlo como "produce todos los elementos de este iterable como si los produjese yo mismo".

### 19.2.4. Generadores infinitos

Un generador puede producir valores indefinidamente, sin que exista una condición natural de parada. Esto sería imposible con una función que devolviese una lista, porque la lista tendría que construirse entera antes de poder devolverse y consumiría memoria ilimitada. Un generador, en cambio, produce cada valor solo cuando se le pide, por lo que puede representar secuencias infinitas de forma perfectamente segura siempre que el consumidor las detenga en algún momento.

```python
def enteros():
    n = 0
    while True:
        yield n
        n += 1


it = enteros()
for _ in range(5):
    print(next(it))  # 0, 1, 2, 3, 4
```

El generador `enteros` es literalmente infinito: su bucle `while True` nunca termina por sí solo. La responsabilidad de detenerlo recae en el código que lo consume, que en este ejemplo solo pide cinco valores. Este patrón es la forma idiomática de representar secuencias matemáticas como números primos, potencias de dos, la sucesión de Fibonacci o cualquier otra generación ilimitada de datos. Combinado con funciones como `itertools.islice`, que corta un iterador tras un número fijo de elementos, permite trabajar con generadores infinitos de forma completamente segura.

### 19.2.5. send() en generadores

Un generador no solo produce valores hacia fuera: también puede recibir valores desde fuera durante su ejecución. El método `send` permite inyectar un valor en un generador pausado, que es recibido como resultado de la expresión `yield` en la que estaba detenido. Esta capacidad convierte a los generadores en **corrutinas ligeras**: objetos que se comunican en dos direcciones con el código que los controla.

```python
def acumulador():
    total = 0
    while True:
        valor = yield total
        if valor is None:
            break
        total += valor


gen = acumulador()
next(gen)            # arranca el generador hasta el primer yield
print(gen.send(10))  # 10
print(gen.send(5))   # 15
print(gen.send(3))   # 18
```

La llamada inicial a `next(gen)` es necesaria para avanzar el generador hasta el primer `yield`, porque un generador recién creado aún no ha empezado a ejecutarse. A partir de ese momento, cada `send(valor)` reanuda el generador, entrega `valor` como resultado del `yield` pausado y ejecuta hasta el siguiente `yield`, cuyo valor devuelve al exterior. Así, el bucle interno del generador recibe progresivamente los números enviados y va acumulando su suma.

El uso de `send` fue uno de los primeros mecanismos de corrutinas en Python y sigue siendo útil en situaciones concretas, aunque gran parte de sus casos de uso han sido absorbidos por `async/await`, que se estudia en el tema 28. En la práctica moderna, `send` se usa raramente en código de aplicación, pero resulta útil en bibliotecas que necesitan un control fino sobre el flujo de un generador.

---

## 19.3. Evaluación perezosa (lazy evaluation)

### 19.3.1. Ventajas de memoria y rendimiento

La **evaluación perezosa** es la estrategia en la que los valores de una secuencia se calculan solo cuando alguien los necesita, en lugar de calcularse todos de antemano y almacenarse en memoria. Los generadores son la encarnación natural de esta idea en Python: cada `yield` produce un valor exactamente en el momento en que se pide, y ese valor deja de ocupar memoria tan pronto como el consumidor lo procesa.

La primera ventaja es el consumo de memoria. Procesar un archivo de varios gigabytes línea a línea con un generador requiere apenas la memoria de una línea en cada instante. Hacerlo cargando el archivo entero en una lista requiere la memoria completa del archivo, lo que en muchos casos es directamente imposible. La segunda ventaja es el tiempo hasta el primer resultado: un generador empieza a producir valores inmediatamente, mientras que una lista debe terminar de construirse entera antes de que el consumidor vea nada. La tercera ventaja es la composición: cuando se encadenan varios generadores en una tubería, los datos fluyen por ella un elemento a la vez, sin necesidad de materializar resultados intermedios.

```python
# Evaluación ávida (eager): construye toda la lista en memoria
cuadrados_lista = [x * x for x in range(10_000_000)]

# Evaluación perezosa: produce los cuadrados uno a uno
cuadrados_gen = (x * x for x in range(10_000_000))

# Ambos permiten iterar sobre los valores, pero solo el segundo
# usa una cantidad de memoria constante durante el recorrido.
total = sum(cuadrados_gen)
```

La diferencia sintáctica entre una list comprehension y una generator expression son los delimitadores: corchetes para la lista, paréntesis para el generador. Esa pequeña diferencia tiene un impacto enorme cuando los datos son grandes. La generator expression del ejemplo procesa diez millones de cuadrados sin asignar una lista intermedia; la list comprehension construye esa lista entera antes de pasarla a `sum`.

La evaluación perezosa no es siempre preferible. Si los datos van a recorrerse varias veces, una estructura materializada (lista, tupla) es más eficiente, ya que un generador se agota tras el primer recorrido y habría que reconstruirlo. También es menos adecuada cuando se necesita acceso aleatorio —un generador no admite indexación— o cuando se requiere conocer la longitud por adelantado. La clave es elegir la herramienta adecuada para cada caso: generadores para procesar grandes volúmenes una sola vez, colecciones para datos que se consultan repetidamente.

### 19.3.2. itertools: cadenas de iteración eficientes

El módulo `itertools` de la biblioteca estándar contiene un conjunto de funciones altamente optimizadas que operan sobre iterables y devuelven iteradores. Todas ellas son perezosas: no construyen listas intermedias, no consumen más memoria de la necesaria y pueden combinarse entre sí para formar tuberías de transformación complejas. Dominar `itertools` es uno de los saltos cualitativos más importantes al pasar de escribir Python funcional a escribir Python idiomático.

Entre sus funciones más útiles se encuentran `chain`, que concatena varios iterables en una sola secuencia; `islice`, que extrae un rango de elementos de un iterador sin soportar índices negativos; `groupby`, que agrupa elementos consecutivos según una clave; `product`, que genera el producto cartesiano de varios iterables; y `combinations`, que produce todas las combinaciones posibles de un cierto tamaño. Cada una de ellas cubre un patrón habitual del procesamiento de datos y lo hace con una eficiencia mucho mayor que una implementación manual equivalente.

```python
from itertools import chain, islice, groupby, product, combinations

print(list(chain([1, 2], [3, 4], [5])))         # [1, 2, 3, 4, 5]

print(list(islice(range(100), 2, 6)))           # [2, 3, 4, 5]

palabras = ["ana", "ada", "bea", "ben", "carlos"]
for letra, grupo in groupby(palabras, key=lambda p: p[0]):
    print(letra, list(grupo))
# a ['ana', 'ada']
# b ['bea', 'ben']
# c ['carlos']

print(list(product([1, 2], ["a", "b"])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

print(list(combinations([1, 2, 3, 4], 2)))
# [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
```

Conviene destacar dos detalles importantes de `itertools`. El primero es que `groupby` solo agrupa elementos **consecutivos** con la misma clave, por lo que normalmente requiere que la entrada esté ordenada previamente por esa misma clave. Aplicarlo a datos desordenados produce grupos fragmentados que rara vez son lo que se espera. El segundo es que todas las funciones del módulo devuelven iteradores que se consumen una sola vez; convertirlos a `list` es necesario para verlos completos, pero hace perder la ventaja de memoria si los datos son grandes.

Combinado con generadores y generator expressions, `itertools` permite expresar transformaciones complejas como una cadena de pasos perezosos, donde cada paso consume del anterior sin materializar resultados intermedios. Este estilo, conocido como **pipeline**, es una de las formas más potentes y legibles de procesar flujos de datos en Python.
