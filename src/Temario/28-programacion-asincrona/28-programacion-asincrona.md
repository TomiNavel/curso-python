# 28. Programación Asíncrona

La programación asíncrona es la forma moderna de gestionar muchas operaciones I/O-bound sin los costes de crear threads ni la complejidad de la sincronización. En lugar de varios hilos que se turnan gestionados por el sistema operativo, un solo hilo alterna entre corrutinas cuando estas se bloquean esperando. El modelo cambia la mentalidad: ya no hay "threads que avanzan en paralelo", sino "tareas que ceden el control al esperar".

En entrevistas es un tema cada vez más frecuente. Los frameworks modernos (FastAPI, aiohttp, discord.py) lo usan como modelo principal, y saber escribir y razonar sobre código async distingue a candidatos con experiencia reciente. Explicar bien cuándo conviene y cuándo no es lo que más se valora, más que dominar cada detalle de la API.

## 28.1. Fundamentos de async

Para entender async hay que desprenderse de la intuición de "ejecución secuencial" y pensar en términos de **puntos de suspensión**. Una corrutina empieza a ejecutarse, llega a un `await`, cede el control al event loop, y más tarde se reanuda cuando lo que esperaba está listo. Mientras está suspendida, el event loop ejecuta otras corrutinas.

### 28.1.1. Qué es programación asíncrona y cuándo usarla

La programación asíncrona es un modelo de concurrencia donde un único hilo gestiona múltiples tareas **no bloqueantes**. Cuando una tarea espera (red, disco, timer), no bloquea el hilo: cede el control al event loop, que ejecuta otra tarea pendiente, y vuelve a la primera cuando su espera acaba.

El caso de uso natural es **I/O-bound masivo**: servidores web que atienden miles de conexiones simultáneas, scrapers que descargan cientos de páginas, clientes que consultan varias APIs a la vez. En esos escenarios, asyncio es más eficiente que threads: no paga el coste de crear un thread por conexión, y no necesita sincronización porque todo corre en un solo hilo.

No es útil para todo. Para CPU-bound, asyncio no da paralelismo y puede ser más lento (el event loop no puede ejecutar otras tareas mientras una está calculando). Para I/O simple (unas pocas peticiones secuenciales), threads son más directos. La regla práctica: **si vas a tener cientos o miles de operaciones I/O concurrentes, asyncio merece la pena; si son pocas, threads son más simples**.

Otro factor es el ecosistema: asyncio obliga a usar librerías asíncronas (`aiohttp` en lugar de `requests`, `asyncpg` en lugar de `psycopg2`). Si las librerías que necesitas no tienen versión async, no puedes usar asyncio sin workarounds.

### 28.1.2. El event loop

El **event loop** es el núcleo de asyncio. Es un bucle que mantiene una cola de tareas pendientes: las ejecuta una a una, suspende las que esperan I/O, y reanuda las que están listas. Todo el modelo asyncio gira alrededor de este componente.

```python
import asyncio

async def saludar():
    print("hola")
    await asyncio.sleep(1)
    print("adiós")

asyncio.run(saludar())
```

`asyncio.run()` arranca el event loop, ejecuta la corrutina pasada, y cierra el loop al terminar. Es la forma estándar de entrar en código async desde código síncrono. Dentro de código que ya es async, se usa directamente `await` en lugar de llamar a `run`.

La intuición más útil es que el event loop es cooperativo: las corrutinas deciden cuándo ceder el control (en cada `await`). No hay interrupciones; si una corrutina no tiene `await`, nadie más se ejecuta. Por eso una operación CPU-intensiva dentro de async es problemática: bloquea todo el loop.

### 28.1.3. async def y await

`async def` define una **corrutina**: una función que, al llamarse, devuelve un objeto corrutina en lugar de ejecutar su cuerpo directamente. El cuerpo solo se ejecuta cuando se hace `await` sobre ese objeto (o se programa en el loop de otra forma).

```python
async def obtener_usuario(id):
    await asyncio.sleep(0.1)   # simula I/O
    return {"id": id, "nombre": "Ana"}

# Llamada NO ejecuta el cuerpo, solo crea el objeto corrutina
coro = obtener_usuario(1)
print(coro)   # <coroutine object obtener_usuario at ...>

# await ejecuta y obtiene el resultado
usuario = await obtener_usuario(1)   # solo válido dentro de async def
```

`await` solo puede usarse dentro de funciones `async def`. Intenta obtener el resultado de una corrutina u otro awaitable (Task, Future); mientras espera, cede el control al event loop. Al reanudarse, el `await` devuelve el valor.

Olvidar el `await` es uno de los bugs más típicos: `obtener_usuario(1)` sin await crea el objeto pero no lo ejecuta. Python incluso avisa con un warning ("coroutine was never awaited"), pero no es un error en tiempo de ejecución. En IDEs modernos, un linter avisa antes.

## 28.2. asyncio

`asyncio` es la biblioteca de la librería estándar para programación asíncrona. Ofrece el event loop, primitivas para crear y coordinar tareas, y herramientas para sincronización (Lock, Queue, Event, todas en versión async).

### 28.2.1. asyncio.run() y coroutines

`asyncio.run(corrutina)` es el punto de entrada idiomático desde código síncrono. Crea un nuevo event loop, ejecuta la corrutina hasta que termine, y cierra el loop.

```python
import asyncio

async def main():
    print("empieza")
    await asyncio.sleep(1)
    print("termina")

asyncio.run(main())
```

Conviene que toda la aplicación async tenga un único `main()` y que `asyncio.run()` se llame solo una vez. Llamar a `run` varias veces en el mismo programa funciona pero no es habitual: típicamente se estructura todo dentro del `main` y se arranca una vez.

Hay entornos donde ya hay un loop activo (Jupyter notebooks, FastAPI, la consola de Pyodide en el navegador). En esos casos `asyncio.run()` falla con "cannot run current event loop" o similar; se usa `await` directo a nivel top, o `loop.run_until_complete` si se quiere control explícito.

### 28.2.2. asyncio.gather() (ejecutar tareas concurrentes)

`asyncio.gather(*corrutinas)` ejecuta varias corrutinas concurrentemente y devuelve la lista de resultados cuando todas terminan. Es el patrón principal para paralelismo en asyncio.

```python
import asyncio

async def descargar(url):
    await asyncio.sleep(1)   # simula petición HTTP
    return f"contenido de {url}"

async def main():
    urls = ["a.com", "b.com", "c.com"]
    resultados = await asyncio.gather(*[descargar(u) for u in urls])
    print(resultados)

asyncio.run(main())
```

Sin gather, `await descargar(a)`, `await descargar(b)` y `await descargar(c)` se ejecutan secuencialmente: total 3 segundos. Con gather, las tres empiezan a la vez y terminan en aproximadamente 1 segundo — el tiempo de la más lenta.

Si alguna corrutina lanza excepción, `gather` la propaga y cancela las demás (salvo con `return_exceptions=True`, que mete las excepciones como resultados en la lista). Saber manejar errores dentro de gather es una de las preguntas más comunes en entrevistas con experiencia.

### 28.2.3. asyncio.create_task()

`asyncio.create_task(corrutina)` programa la corrutina para ejecutarse en el event loop y devuelve un objeto `Task`. La tarea empieza a correr inmediatamente, sin esperar a que se haga `await` sobre ella.

```python
async def tarea_fondo():
    while True:
        await asyncio.sleep(5)
        print("todavía vivo")

async def main():
    asyncio.create_task(tarea_fondo())   # arranca y sigue
    await asyncio.sleep(20)   # main continúa mientras la tarea corre

asyncio.run(main())
```

Es útil para tareas en segundo plano cuyo resultado no interesa inmediatamente. Frente a `gather`, `create_task` no sincroniza: las tareas corren independientemente y pueden seguir vivas cuando otras ya acabaron. Para esperarlas explícitamente, se hace `await task`.

Hay un detalle importante: hay que guardar una referencia a la task. Si el recolector la recoge porque no hay referencias, la tarea puede cancelarse inesperadamente. El patrón habitual es guardarlas en una lista o conjunto del ámbito actual.

### 28.2.4. Timeouts y cancelación

`asyncio.wait_for(corrutina, timeout)` ejecuta la corrutina con un tiempo límite. Si no acaba en ese tiempo, la cancela y lanza `TimeoutError`.

```python
async def main():
    try:
        resultado = await asyncio.wait_for(descargar_lento(), timeout=5.0)
    except asyncio.TimeoutError:
        print("la descarga tardó demasiado")
```

La cancelación en asyncio funciona lanzando `CancelledError` dentro de la corrutina en el siguiente `await`. El código puede capturarla para hacer limpieza, pero debe propagarla después (salvo casos muy específicos); suprimirla puede dejar tareas descontroladas.

Saber gestionar timeouts es casi obligatorio en código async real: cualquier operación de red debe tener timeout para no colgar el sistema entero si un servidor no responde. Los frameworks modernos lo imponen por defecto.

## 28.3. Patrones comunes

Más allá de la API, hay patrones que aparecen una y otra vez en código async profesional. Conocerlos permite escribir código idiomático y reconocer cuándo un diseño se está complicando de más.

### 28.3.1. Peticiones HTTP asíncronas (aiohttp)

`aiohttp` es la librería estándar de facto para clientes HTTP async. La API se parece a `requests` pero con `async/await` y context managers async.

```python
import aiohttp
import asyncio

async def descargar(sesion, url):
    async with sesion.get(url) as respuesta:
        return await respuesta.text()

async def main():
    urls = ["https://a.com", "https://b.com"]
    async with aiohttp.ClientSession() as sesion:
        contenidos = await asyncio.gather(
            *[descargar(sesion, u) for u in urls]
        )
    print(len(contenidos))

asyncio.run(main())
```

El patrón crítico es reutilizar el `ClientSession` entre peticiones. Crear una sesión por petición es un error común: se paga el coste de inicialización (TLS handshake, pool de conexiones) cada vez. Una sesión compartida amortiza esos costes y reutiliza conexiones.

Alternativas modernas son `httpx` (cliente sincrónico y async en la misma librería, con API casi idéntica a requests) y `aiohttp` (más antiguo, con servidor incluido). Ambos son opciones válidas según el resto del stack.

### 28.3.2. async for, async with y async generators

Las estructuras async tienen sus versiones de `for` y `with`. `async with` espera que el objeto implemente `__aenter__` y `__aexit__`; `async for` espera un iterador async (`__aiter__` y `__anext__`).

```python
async with sesion.get(url) as resp:    # sesión async
    async for chunk in resp.content:   # streaming async
        procesar(chunk)
```

Los **generadores async** usan `async def` con `yield`:

```python
async def eventos():
    for i in range(5):
        await asyncio.sleep(1)
        yield i

async def main():
    async for evento in eventos():
        print(evento)
```

Este patrón es útil para streams de datos donde cada elemento requiere esperar (chunks de red, eventos de un WebSocket, filas de una consulta paginada). Sustituye de forma elegante los bucles con `asyncio.sleep` y flags de control.

### 28.3.3. asyncio.Queue (productor-consumidor)

`asyncio.Queue` es una cola thread-safe para el modelo productor-consumidor en async. Permite coordinar corrutinas que producen y consumen datos sin compartir estado directamente.

```python
import asyncio

async def productor(cola):
    for i in range(5):
        await asyncio.sleep(0.5)
        await cola.put(i)
    await cola.put(None)   # señal de fin

async def consumidor(cola):
    while True:
        item = await cola.get()
        if item is None:
            break
        print(f"procesando {item}")

async def main():
    cola = asyncio.Queue()
    await asyncio.gather(productor(cola), consumidor(cola))

asyncio.run(main())
```

La cola hace dos cosas importantes: bloquea al productor si la cola se llena (cuando se especifica `maxsize`), y bloquea al consumidor cuando está vacía. Ambos esperan cooperativamente sin consumir CPU.

Este patrón es la base de muchos sistemas async: pipelines de procesamiento, rate limiters, schedulers. Saberlo implementar desde cero es una pregunta clásica en entrevistas de sistemas backend.

### 28.3.4. Async vs threading: cuándo usar cada uno

Es la pregunta que cualquier ingeniero Python debería saber responder con criterio:

- **Async** es óptimo para I/O-bound con **muchas tareas concurrentes** (cientos o miles). No paga coste por thread, todo el estado cabe en un solo hilo, no necesita sincronización, escala a cualquier número de conexiones siempre que quepan en memoria.
- **Threading** es óptimo para I/O-bound con **pocas tareas** (decenas). La API es más simple, el código no necesita ser async-first, y cualquier librería bloqueante funciona sin adaptaciones.
- **Async es peor que threading** cuando hay que usar librerías síncronas: mezclar llamadas bloqueantes en un event loop congela todo el sistema. La solución es `run_in_executor`, pero complica el código.
- **Ninguno es bueno para CPU-bound**. Para eso, multiprocessing.

Otra variable es el equipo y el stack: escribir código async requiere disciplina y familiaridad; si el resto del proyecto es síncrono, introducir async parcialmente suele generar más problemas que beneficios. En proyectos greenfield modernos, async-first es una buena decisión; en proyectos existentes, la migración rara vez compensa.
