# Preguntas de Entrevista: Iteradores y Generadores

## Preguntas

1. ¿Cuál es la diferencia entre un iterable y un iterador en Python?
2. ¿Qué métodos debe implementar una clase para ser considerada un iterador?
3. ¿Qué ocurre exactamente cuando Python ejecuta un bucle `for x in obj`?
4. ¿Qué es `StopIteration` y por qué no debe capturarse normalmente desde código de usuario?
5. ¿Qué es una función generadora y en qué se diferencia de una función normal?
6. ¿Qué diferencia hay entre una list comprehension y una generator expression? ¿Cuándo conviene usar cada una?
7. ¿Qué hace exactamente `yield from` y por qué es preferible a un bucle con `yield`?
8. ¿Cómo pueden representarse secuencias infinitas en Python sin agotar la memoria?
9. ¿Qué hace el método `send` de un generador y para qué se utiliza?
10. ¿Qué ventajas aporta `itertools` frente a escribir bucles manuales?
11. ¿Por qué un generador solo puede recorrerse una vez?
12. ¿Qué es la evaluación perezosa y qué ventajas tiene sobre la evaluación ávida?

---

## Respuestas

### 1. ¿Cuál es la diferencia entre un iterable y un iterador en Python?

Un **iterable** es cualquier objeto que puede recorrerse con `for`: listas, tuplas, strings, diccionarios, archivos. Formalmente, implementa el método `__iter__`, que devuelve un iterador nuevo cada vez que se le pide. Un **iterador** es el objeto que produce efectivamente los elementos uno a uno: implementa `__iter__` (que devuelve `self`) y `__next__` (que devuelve el siguiente valor o lanza `StopIteration`).

La distinción es importante porque un iterable puede recorrerse varias veces —cada recorrido crea un iterador nuevo con estado propio—, mientras que un iterador, una vez consumido, no puede reiniciarse. Una lista es un iterable reutilizable; el resultado de llamar a `iter(lista)` es un iterador de un solo uso.

### 2. ¿Qué métodos debe implementar una clase para ser considerada un iterador?

Debe implementar dos métodos: `__iter__`, que devuelve `self`, y `__next__`, que produce el siguiente valor y lanza `StopIteration` cuando se agota la secuencia. Devolver `self` desde `__iter__` es lo que permite que el propio objeto se use como iterador en un `for`.

Si la clase solo implementa `__iter__` y devuelve otro objeto distinto, no es un iterador: es un iterable que produce iteradores externos. Los dos patrones son válidos, pero resuelven problemas diferentes: el primero cuando el objeto es consumido una sola vez, el segundo cuando se quiere permitir múltiples recorridos independientes.

### 3. ¿Qué ocurre exactamente cuando Python ejecuta un bucle `for x in obj`?

Python llama internamente a `iter(obj)` para obtener un iterador a partir del iterable. A continuación, llama repetidamente a `next()` sobre ese iterador, asignando el valor devuelto a la variable `x` y ejecutando el cuerpo del bucle en cada iteración. Cuando `next()` lanza `StopIteration`, Python la captura silenciosamente y termina el bucle.

Este mecanismo es lo que permite que el `for` funcione con cualquier objeto que cumpla el protocolo de iteración, sin importar si es una lista, un diccionario, un archivo o un generador personalizado.

### 4. ¿Qué es `StopIteration` y por qué no debe capturarse normalmente desde código de usuario?

`StopIteration` es una excepción específica del protocolo de iteración cuya única función es señalar que un iterador ha terminado. No representa un error: es la forma normal de comunicar el fin de la secuencia. Los bucles `for` y funciones como `list`, `sum` o `max` la capturan internamente para saber cuándo detenerse.

Capturarla explícitamente en código de usuario suele ser un síntoma de que se está reimplementando el protocolo a mano en lugar de usar un `for`. Además, desde Python 3.7 (PEP 479), propagar accidentalmente un `StopIteration` desde dentro de un generador lanza `RuntimeError`, precisamente para evitar bugs difíciles de diagnosticar causados por capturas incorrectas.

### 5. ¿Qué es una función generadora y en qué se diferencia de una función normal?

Una función generadora es una función que contiene al menos una sentencia `yield`. Al llamarla, no ejecuta su cuerpo ni devuelve un valor ordinario: devuelve un objeto generador, que es un iterador con `__iter__` y `__next__` implementados automáticamente. Su cuerpo solo empieza a ejecutarse cuando se le pide el primer valor, y se **pausa** en cada `yield`, reanudándose exactamente en el mismo punto cuando se pide el siguiente.

La diferencia clave frente a una función normal es que el estado local —variables, posición en el código— se conserva entre llamadas sucesivas. Esto permite escribir iteradores con una fracción del código que requeriría una clase equivalente, y expresar con claridad secuencias potencialmente infinitas.

### 6. ¿Qué diferencia hay entre una list comprehension y una generator expression? ¿Cuándo conviene usar cada una?

Una list comprehension construye inmediatamente una lista completa en memoria con todos los resultados. Una generator expression, escrita con paréntesis en lugar de corchetes, produce un generador perezoso que calcula cada valor solo cuando se pide. La diferencia en consumo de memoria puede ser enorme: una list comprehension sobre diez millones de elementos reserva memoria para diez millones de objetos; una generator expression equivalente usa memoria constante.

Conviene una list comprehension cuando los datos van a recorrerse varias veces, cuando se necesita acceder por índice, o cuando la colección es pequeña y la eficiencia no es crítica. Conviene una generator expression cuando los datos se procesan una sola vez, cuando se encadenan varias transformaciones en una tubería, o cuando la fuente es muy grande y materializar toda la secuencia sería costoso o imposible.

### 7. ¿Qué hace exactamente `yield from` y por qué es preferible a un bucle con `yield`?

`yield from iterable` delega la producción de valores en otro iterable: cada valor que ese iterable produce se emite como si lo produjese el generador actual. Es equivalente en apariencia a un `for x in iterable: yield x`, pero con dos ventajas importantes. La primera es la claridad: el propósito del código es más directo. La segunda es la semántica completa: `yield from` transmite correctamente `send`, `throw` y el valor final de retorno del sub-generador, cosa que un bucle manual no hace.

Su uso más habitual es componer generadores, aplanar estructuras anidadas mediante recursión, o construir tuberías donde un generador encadena el contenido de otro.

### 8. ¿Cómo pueden representarse secuencias infinitas en Python sin agotar la memoria?

Con un generador que contenga un bucle sin condición de parada (por ejemplo, `while True`) y un `yield` dentro. Como el generador calcula sus valores uno por uno y solo cuando se los piden, el cuerpo del bucle solo se ejecuta tantas veces como iteraciones consuma el código que lo usa. La memoria ocupada en cada instante se limita al estado local del generador y al último valor producido.

La responsabilidad de parar recae en quien consume: un `for` con `break`, una llamada a `itertools.islice`, o un contador que limite el número de valores procesados. Combinar generadores infinitos con `islice`, `takewhile` o filtros perezosos es el patrón idiomático para trabajar con secuencias ilimitadas de forma segura.

### 9. ¿Qué hace el método `send` de un generador y para qué se utiliza?

`send(valor)` reanuda un generador pausado inyectando un valor en él: ese valor se convierte en el resultado de la expresión `yield` en la que el generador estaba detenido. Esto permite una comunicación bidireccional entre el código que consume el generador y el propio generador, que pasa a comportarse como una corrutina ligera. Antes de la primera llamada a `send` con un valor distinto de `None`, hay que avanzar el generador hasta el primer `yield` con `next()` o `send(None)`.

En la práctica moderna, `send` se usa poco en código de aplicación porque gran parte de sus casos de uso han sido absorbidos por `async/await`. Sigue siendo útil en bibliotecas que implementan máquinas de estados o flujos de control personalizados sobre generadores.

### 10. ¿Qué ventajas aporta `itertools` frente a escribir bucles manuales?

`itertools` contiene funciones altamente optimizadas que operan sobre iterables y devuelven iteradores perezosos. Frente a un bucle manual, ofrece tres ventajas. La primera es **eficiencia**: están implementadas en C y son típicamente más rápidas que una versión escrita en Python puro. La segunda es **memoria**: al ser perezosas, no materializan listas intermedias, lo que resulta crítico cuando se procesan volúmenes grandes de datos. La tercera es **legibilidad**: nombres como `chain`, `groupby`, `islice` o `combinations` expresan la intención con una claridad que un bucle equivalente rara vez alcanza.

Funciones especialmente útiles incluyen `chain` para concatenar iterables, `islice` para cortar un rango de elementos, `groupby` para agrupar valores consecutivos por una clave, `product` para producto cartesiano y `combinations` para combinaciones sin repetición.

### 11. ¿Por qué un generador solo puede recorrerse una vez?

Un generador es un iterador, no un iterable reutilizable. Al crearlo, su estado interno apunta al inicio del cuerpo, y cada llamada a `next` avanza la ejecución hasta el siguiente `yield`. Cuando el cuerpo termina, el generador queda en un estado agotado del que no puede volver: llamar a `next` de nuevo devolverá inmediatamente `StopIteration`.

Esto contrasta con una lista o una tupla, que son iterables: cada vez que se las pasa a un `for`, Python crea un iterador nuevo a partir de ellas. Si se quiere recorrer varias veces la misma secuencia generada, hay dos opciones: materializarla con `list()` (perdiendo la ventaja de memoria) o definir una función que construya un generador nuevo cada vez que se la llama.

### 12. ¿Qué es la evaluación perezosa y qué ventajas tiene sobre la evaluación ávida?

La evaluación perezosa calcula cada valor de una secuencia solo cuando alguien lo pide, en lugar de calcularlos todos de antemano. Los generadores y `itertools` son sus dos representantes naturales en Python. Sus ventajas son tres. **Memoria**: no hay que reservar espacio para almacenar todos los resultados a la vez, lo que permite procesar datos mucho mayores que la memoria disponible. **Tiempo hasta el primer resultado**: un consumidor puede empezar a procesar valores en cuanto se produce el primero, sin esperar a que termine todo el cálculo. **Composición**: varios pasos encadenados de generadores forman una tubería en la que cada elemento fluye de un paso al siguiente sin materializar resultados intermedios.

La evaluación ávida (construir una lista completa) sigue siendo preferible cuando los datos se recorren varias veces, cuando se necesita acceso aleatorio por índice, cuando se requiere conocer la longitud total por adelantado, o cuando la colección es pequeña y la simplicidad pesa más que la eficiencia.
