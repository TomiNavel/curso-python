# 27. Concurrencia y Paralelismo

Concurrencia y paralelismo son dos de las fuentes más habituales de confusión en Python. Son conceptos relacionados pero distintos, y la diferencia importa especialmente en este lenguaje por una peculiaridad: el GIL (Global Interpreter Lock). Entender esto determina si una aplicación se acelera con threads, con procesos o con nada en absoluto.

En entrevistas, el tema aparece casi siempre en dos formas: conceptual ("diferencia entre concurrencia y paralelismo", "qué es el GIL") y práctica ("¿cómo paralelizarías esta tarea?"). Responder bien requiere saber qué tipo de problema se está resolviendo — CPU-bound o I/O-bound — antes de elegir la herramienta.

## 27.1. Conceptos fundamentales

Antes de hablar de APIs concretas, hay que fijar el vocabulario. Los malentendidos en concurrencia casi siempre vienen de no distinguir concurrencia de paralelismo, o de ignorar el GIL al elegir threads.

### 27.1.1. Concurrencia vs paralelismo

**Concurrencia** es la capacidad de un programa de **progresar en varias tareas** al mismo tiempo, alternando entre ellas. No implica que se ejecuten simultáneamente: pueden ir turnándose en un único core. La concurrencia es un modelo de organización.

**Paralelismo** es la **ejecución simultánea real** de varias tareas en distintos cores o procesadores. Es un requisito físico del hardware: necesita múltiples unidades de cómputo.

Una analogía clásica: un camarero atendiendo dos mesas. Si toma el pedido de la primera, va a la barra, vuelve a por el de la segunda, va a la barra, etc., está siendo **concurrente** (no bloquea la primera mesa mientras sirve a la segunda) pero no **paralelo** (solo hay un camarero). Con dos camareros atendiendo cada uno una mesa, hay paralelismo.

En Python, el modelo asíncrono con `asyncio` (tema 28) es concurrencia pura sin paralelismo: un solo hilo turnándose entre tareas. `multiprocessing` es paralelismo real. `threading` es el caso peculiar — ofrece concurrencia pero el paralelismo está restringido por el GIL.

### 27.1.2. El GIL (Global Interpreter Lock)

El GIL es un mutex global del intérprete CPython (la implementación oficial) que garantiza que **solo un thread ejecuta bytecode Python en un momento dado**. Por su causa, múltiples threads en Python no aprovechan múltiples cores para tareas CPU-bound: aunque el sistema tenga 16 cores, el código Python puro corre como en un solo core.

El GIL existe por razones históricas y de simplicidad. Permite que el recolector de basura y la gestión de referencias sean thread-safe sin sincronización explícita en cada operación. Eliminarlo es un esfuerzo en curso ("nogil" en Python 3.13+) pero en el momento de escribir esto sigue siendo experimental.

La consecuencia práctica es importante:

- Para tareas **CPU-bound** (cálculo puro en Python), los threads no dan paralelismo real. Hay que usar `multiprocessing`.
- Para tareas **I/O-bound** (esperar red, disco, base de datos), los threads sí ayudan: cuando un thread se bloquea esperando una respuesta, libera el GIL y otro thread puede ejecutarse.

El GIL se libera también dentro de funciones C bien diseñadas (NumPy, pandas, operaciones de red). Por eso NumPy con threads sí escala: la parte lenta ocurre en C sin el GIL.

### 27.1.3. CPU-bound vs I/O-bound

Clasificar la tarea es el primer paso antes de elegir herramienta.

- **CPU-bound**: el programa está limitado por la velocidad del procesador. Hace cálculos, transformaciones en memoria, compresión, cifrado. Un solo core trabajando al 100% y el resto a 0% suele indicar CPU-bound.
- **I/O-bound**: el programa pasa la mayor parte del tiempo **esperando**. Peticiones HTTP, lecturas de disco, consultas a base de datos, esperas al usuario. El procesador está mayormente ocioso.

La tabla de decisión para Python es directa:

| Tipo | Herramienta recomendada |
|------|-------------------------|
| I/O-bound, pocas tareas | `threading` o `ThreadPoolExecutor` |
| I/O-bound, muchas tareas | `asyncio` |
| CPU-bound | `multiprocessing` o `ProcessPoolExecutor` |

Elegir mal la herramienta es de los errores más costosos en este tema: paralelizar con threads código CPU-bound no solo no acelera, sino que puede ralentizar por el coste de sincronización. En entrevistas, diagnosticar correctamente el tipo de carga antes de proponer solución demuestra madurez técnica.

## 27.2. Threading

El módulo `threading` permite crear y gestionar hilos de ejecución dentro del mismo proceso. Todos los threads comparten memoria, lo que los hace ligeros pero introduce la necesidad de sincronización cuando acceden a datos compartidos.

### 27.2.1. Crear y ejecutar threads

La forma más común es pasar una función y sus argumentos a `threading.Thread` y llamar a `start()`:

```python
import threading

def tarea(nombre, segundos):
    print(f"{nombre} empieza")
    # Aquí iría el trabajo real
    print(f"{nombre} termina")

t1 = threading.Thread(target=tarea, args=("A", 2))
t2 = threading.Thread(target=tarea, args=("B", 1))

t1.start()
t2.start()
t1.join()   # espera a que t1 termine
t2.join()
```

`start()` arranca el thread y devuelve inmediatamente. `join()` bloquea al thread que llama hasta que el thread terminado. Sin `join()`, el programa principal puede acabar antes que los threads (si no son daemon) y generar comportamientos imprevistos.

Los threads pueden también heredarse de `threading.Thread` y sobreescribir `run`, pero el patrón con `target=` es más común en código moderno.

### 27.2.2. Sincronización (Lock, RLock, Event, Semaphore)

Cuando varios threads acceden a la misma variable, aparecen **condiciones de carrera**: el resultado depende del orden exacto de ejecución, que no es predecible. El módulo `threading` ofrece varias primitivas de sincronización.

**Lock** es el más básico. Un thread adquiere el lock, entra en una sección crítica, y libera el lock. Solo uno a la vez puede estar dentro:

```python
import threading

contador = 0
lock = threading.Lock()

def incrementar():
    global contador
    with lock:
        contador += 1   # sección crítica protegida
```

El patrón `with lock:` es idiomático: adquiere al entrar, libera al salir, incluso si hay excepción. Evita olvidarse de liberar.

**RLock** (reentrant lock) es como Lock pero el mismo thread puede adquirirlo varias veces sin bloquearse. Útil cuando una función con lock llama a otra función del mismo objeto que también usa el lock.

**Event** es una señal binaria que los threads pueden esperar. Un thread llama a `event.wait()` y se bloquea hasta que otro hace `event.set()`:

```python
event = threading.Event()

def consumidor():
    event.wait()
    print("recibida señal")

def productor():
    # ... preparar algo ...
    event.set()
```

**Semaphore** limita el número de threads que pueden ejecutar una sección simultáneamente. Útil para controlar acceso a recursos con capacidad limitada (conexiones HTTP, licencias, etc.):

```python
sem = threading.Semaphore(3)   # máximo 3 simultáneos

def peticion():
    with sem:
        hacer_peticion_http()
```

Estas primitivas cubren la mayoría de casos. El consejo profesional es evitar sincronización manual cuando se puede: `ThreadPoolExecutor` y colas (`queue.Queue`) encapsulan patrones correctos y evitan los errores típicos.

### 27.2.3. Daemon threads

Un **daemon thread** es un thread que no impide al programa terminar. Por defecto, Python espera a que todos los threads no daemon acaben antes de salir. Un thread marcado como daemon es terminado abruptamente cuando el programa principal acaba.

```python
t = threading.Thread(target=tarea, daemon=True)
t.start()
```

Son útiles para tareas de fondo cuyo ciclo de vida está atado al del proceso: heartbeats, monitorización, limpieza periódica. El daemon thread no necesita que el programa espere para terminar; si el programa acaba, el daemon muere con él.

La desventaja es que terminan sin cleanup. Si el thread estaba escribiendo un archivo o en una transacción, puede quedar a medias. Para recursos críticos, el patrón correcto es un thread normal con `Event` para señalizar cierre y `join()` desde el programa principal.

### 27.2.4. ThreadPoolExecutor

`ThreadPoolExecutor` del módulo `concurrent.futures` es la abstracción de alto nivel recomendada para usar threads. Mantiene un pool fijo de workers y distribuye tareas entre ellos, devolviendo `Future` con los resultados:

```python
from concurrent.futures import ThreadPoolExecutor

def descargar(url):
    # ... descarga la URL ...
    return resultado

urls = ["http://a.com", "http://b.com", "http://c.com"]

with ThreadPoolExecutor(max_workers=4) as pool:
    resultados = list(pool.map(descargar, urls))
```

`pool.map(funcion, iterable)` aplica la función a cada elemento en paralelo y devuelve los resultados en el mismo orden que la entrada. Con `submit` y `as_completed` se puede obtener control más fino.

Comparado con gestionar threads a mano, `ThreadPoolExecutor` ofrece tres ventajas: limita el número de threads activos, reusa workers entre tareas (evitando el coste de crear y destruir) y proporciona una API uniforme compartida con `ProcessPoolExecutor`. Es el patrón recomendado en código profesional.

## 27.3. Multiprocessing

El módulo `multiprocessing` crea **procesos** separados en lugar de threads. Cada proceso tiene su propio intérprete Python, su propio GIL, y su propia memoria. Por eso sí aprovecha múltiples cores para tareas CPU-bound — el precio es que la comunicación entre procesos es más cara y los datos no se comparten directamente.

### 27.3.1. Crear y ejecutar procesos

La API se parece deliberadamente a la de `threading`:

```python
import multiprocessing as mp

def calcular_intensivo(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    p = mp.Process(target=calcular_intensivo, args=(10_000_000,))
    p.start()
    p.join()
```

El bloque `if __name__ == "__main__":` es **obligatorio** al usar multiprocessing en scripts. En algunos sistemas (Windows, macOS), cada proceso hijo re-importa el módulo para configurarse; sin el guard, ejecutaría el código de arranque infinitamente.

Crear procesos es más caro que crear threads. Pueden tardar decenas o cientos de milisegundos, frente a microsegundos de un thread. Para tareas cortas, el coste de arranque puede superar al beneficio. Por eso se suelen usar pools que reutilizan procesos.

### 27.3.2. Comunicación entre procesos (Queue, Pipe)

Como los procesos no comparten memoria, pasar datos entre ellos requiere serializar (típicamente con pickle) y transferir por un canal. `multiprocessing` ofrece varias primitivas:

**Queue** es una cola thread-safe y process-safe, similar a la de `queue` pero usable entre procesos:

```python
import multiprocessing as mp

def productor(q):
    for i in range(5):
        q.put(i)

def consumidor(q):
    while True:
        item = q.get()
        if item is None:   # señal de fin
            break
        print(f"recibido: {item}")

if __name__ == "__main__":
    q = mp.Queue()
    p1 = mp.Process(target=productor, args=(q,))
    p2 = mp.Process(target=consumidor, args=(q,))
    p1.start(); p2.start()
    p1.join(); q.put(None); p2.join()
```

**Pipe** es una comunicación unidireccional entre exactamente dos procesos. Es más ligera que Queue pero menos flexible.

Enviar datos tiene un coste: serializar, transferir, deserializar. Para objetos grandes, este coste puede dominar. En la práctica, se diseñan los procesos para minimizar la comunicación: pasar instrucciones cortas, procesar mucho en el worker, devolver solo el resultado final.

### 27.3.3. ProcessPoolExecutor

`ProcessPoolExecutor` es el equivalente a `ThreadPoolExecutor` pero con procesos. La interfaz es idéntica, así que cambiar entre threads y procesos es cambiar el nombre de la clase:

```python
from concurrent.futures import ProcessPoolExecutor

def calcular(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    tareas = [1_000_000, 2_000_000, 3_000_000, 4_000_000]

    with ProcessPoolExecutor(max_workers=4) as pool:
        resultados = list(pool.map(calcular, tareas))
```

Para CPU-bound, el speedup es real: con 4 workers en una máquina de 4 cores, el trabajo se hace aproximadamente en un cuarto del tiempo. La función pasada debe ser picklable (funciones top-level sí lo son; lambdas y funciones anidadas no).

## 27.4. concurrent.futures

El módulo `concurrent.futures` unifica el acceso a threads y procesos con una sola API. Cualquier código que use `ThreadPoolExecutor` se puede cambiar a `ProcessPoolExecutor` modificando solo una línea, lo que facilita probar ambos enfoques y elegir el mejor para cada caso.

### 27.4.1. Interfaz unificada (submit, map, as_completed)

Los tres métodos principales son `submit`, `map` y `as_completed`.

`submit(fn, *args)` envía una tarea al pool y devuelve un `Future`. El `Future` permite consultar si la tarea acabó y obtener el resultado con `.result()`:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as pool:
    futuro = pool.submit(descargar, "http://ejemplo.com")
    resultado = futuro.result()   # bloquea hasta que acabe
```

`map(fn, iterable)` aplica la función a cada elemento y devuelve los resultados **en el orden de la entrada**. Es el equivalente paralelo a `map` builtin:

```python
with ThreadPoolExecutor() as pool:
    resultados = list(pool.map(descargar, urls))
```

`as_completed(futuros)` recibe un iterable de Futures y va produciendo cada uno según terminan, sin esperar al orden original. Es el patrón ideal cuando se quiere procesar resultados conforme llegan:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor() as pool:
    futuros = [pool.submit(descargar, url) for url in urls]
    for f in as_completed(futuros):
        print(f.result())
```

Los Futures capturan excepciones: si la tarea lanzó una, `future.result()` la relanza en el thread que llama. Esto hace que los errores no queden silenciados, como podría ocurrir con un thread sin gestión explícita.

### 27.4.2. Cuándo usar threads vs procesos

Con `concurrent.futures` es trivial probar ambos y medir. La guía general:

- **Threads**: tareas I/O-bound, cualquier cantidad. Peticiones HTTP, lectura de archivos, consultas a bases de datos. Overhead muy bajo; los threads esperan sin consumir CPU.
- **Procesos**: tareas CPU-bound en Python puro. Cálculos numéricos en Python, compresión, parseo complejo. El GIL no limita porque cada proceso tiene el suyo.
- **Funciones C que liberan el GIL**: threads funcionan bien. NumPy, pandas, scikit-learn en sus partes compiladas ya escalan con threads.

Una regla pragmática: si en un benchmark el uso de CPU total en el sistema no supera el 100% (equivalente a un core saturado), la tarea es probablemente I/O-bound o liberadora del GIL, y los threads son suficientes. Si queda limitada a un core con threads, toca procesos.

Elegir la herramienta correcta es más importante que afinar la implementación. Un CPU-bound con threads nunca acelera; un I/O-bound con procesos funciona pero es innecesariamente pesado. Saber diagnosticar antes de elegir es lo que diferencia en entrevistas técnicas.
