# Preguntas de Entrevista: Programación Asíncrona

1. ¿Qué es asyncio y qué problema resuelve?
2. ¿Cuál es la diferencia entre una función normal y una definida con `async def`?
3. ¿Qué hace `await` exactamente?
4. ¿Qué es el event loop y cómo ejecuta las corrutinas?
5. ¿Qué diferencia hay entre `asyncio.gather` y hacer varios `await` secuenciales?
6. ¿Cuándo usarías `asyncio.create_task`?
7. ¿Qué ocurre si una corrutina lanza excepción dentro de `asyncio.gather`?
8. ¿Cuándo conviene asyncio y cuándo threading?
9. ¿Por qué no se deben hacer operaciones bloqueantes dentro de código async?
10. ¿Qué hace `asyncio.wait_for` y cómo se implementa un timeout?

---

### R1. ¿Qué es asyncio y qué problema resuelve?

`asyncio` es la biblioteca estándar de Python para programación asíncrona basada en corrutinas y un event loop. Resuelve el problema de gestionar muchas operaciones I/O-bound concurrentes sin el coste de crear threads ni la complejidad de la sincronización. Un único hilo alterna entre tareas que ceden el control al esperar I/O, lo que escala a miles de conexiones simultáneas con poca memoria.

El caso de uso típico es un servidor web o un cliente que hace cientos de peticiones HTTP en paralelo. Con threads, cada conexión consumiría recursos del sistema; con asyncio, todas comparten el mismo thread y el overhead por tarea es mínimo. Es la base de frameworks modernos como FastAPI, aiohttp o discord.py.

### R2. ¿Cuál es la diferencia entre una función normal y una definida con `async def`?

`async def` define una **corrutina**: llamarla no ejecuta su cuerpo, sino que devuelve un objeto corrutina. El cuerpo se ejecuta cuando algo hace `await` sobre ese objeto (o se programa con `create_task`, `ensure_future`, etc.).

Una función normal ejecuta su cuerpo inmediatamente al llamarse. Una corrutina es una receta de ejecución que necesita un event loop para correr. Dentro del cuerpo de una corrutina, se puede usar `await`, `async for` y `async with`, que solo tienen sentido en contexto asíncrono.

### R3. ¿Qué hace `await` exactamente?

`await expresion` espera a que un **awaitable** (corrutina, Task, Future) se complete y devuelve su resultado. Mientras espera, cede el control al event loop, que puede ejecutar otras tareas pendientes. Cuando el awaitable termina, el event loop reanuda la corrutina que tenía el `await`.

Solo se puede usar dentro de funciones `async def`. Llamarlo fuera lanza `SyntaxError`. Olvidar un `await` cuando se necesita es un bug típico: la corrutina no se ejecuta, Python emite un warning ("coroutine was never awaited") pero el programa continúa con valores incorrectos.

### R4. ¿Qué es el event loop y cómo ejecuta las corrutinas?

El event loop es un bucle que mantiene una cola de tareas pendientes. En cada iteración ejecuta las tareas que están listas (no suspendidas por `await`), comprueba qué I/O ha completado, y reanuda las tareas que estaban esperando ese I/O. El loop es cooperativo: las tareas deciden cuándo ceder el control mediante `await`.

No hay interrupciones. Si una tarea hace un cálculo largo sin awaits, bloquea el loop entero y ninguna otra tarea progresa. Por eso en código async hay que evitar operaciones CPU-intensivas o bloqueantes; para eso existe `loop.run_in_executor`, que las ejecuta en un pool de threads sin bloquear el loop.

### R5. ¿Qué diferencia hay entre `asyncio.gather` y hacer varios `await` secuenciales?

`await corrutina_a(); await corrutina_b()` ejecuta las corrutinas **una después de otra**: la segunda no empieza hasta que la primera termine. Si cada una tarda 1 segundo, el total son 2 segundos.

`asyncio.gather(corrutina_a(), corrutina_b())` las ejecuta **concurrentemente**: ambas empiezan a la vez y se solapan en el tiempo mientras esperan I/O. Para corrutinas que tardan el mismo tiempo, el total se acerca al de la más lenta, no a la suma. Es el patrón principal para aprovechar la concurrencia de asyncio.

### R6. ¿Cuándo usarías `asyncio.create_task`?

Para lanzar una corrutina en segundo plano cuyo resultado no quieres esperar inmediatamente. `create_task` programa la corrutina en el loop y devuelve una Task que empieza a correr enseguida. El flujo principal sigue sin bloquearse.

Casos típicos: tareas de fondo (heartbeats, monitorización), consumidores de una cola, servidores que aceptan conexiones y crean una task por cada una. Hay un detalle importante: hay que guardar referencia a la task (en una lista, por ejemplo) porque si el recolector la elimina, la tarea puede cancelarse inesperadamente.

### R7. ¿Qué ocurre si una corrutina lanza excepción dentro de `asyncio.gather`?

Por defecto, si una corrutina lanza una excepción, `gather` cancela las demás y propaga la excepción al código que hizo `await` sobre el gather. Esto significa que un solo fallo invalida todo el resultado, incluso si otras corrutinas habrían terminado correctamente.

Con `return_exceptions=True`, las excepciones se convierten en elementos de la lista de resultados en lugar de propagarse. Esto permite procesar los resultados exitosos y gestionar los fallos individualmente. Saber esta opción es crítico en código real: sistemas que hacen 100 peticiones en paralelo no pueden caer si una de ellas falla.

### R8. ¿Cuándo conviene asyncio y cuándo threading?

`asyncio` brilla con muchas operaciones I/O-bound concurrentes (cientos o miles): servidores HTTP, scrapers, clientes de varias APIs, chats en tiempo real. No paga coste por thread, no necesita sincronización, y escala a cualquier número de conexiones mientras quepan en memoria.

`threading` es más simple para pocas tareas (decenas) cuando el código ya es síncrono y las librerías no tienen versión async. No requiere cambiar a async-first y cualquier función bloqueante funciona. La regla: si tu problema es "tengo muchas peticiones HTTP que hacer", asyncio; si es "quiero paralelizar 5 tareas I/O", threading es más directo.

La otra variable es el ecosistema. Si tus librerías (base de datos, clientes HTTP) no tienen versión async, mezclar código sync en un loop async es problemático. `run_in_executor` existe pero complica; en ese caso, threads o procesos puros son más limpios.

### R9. ¿Por qué no se deben hacer operaciones bloqueantes dentro de código async?

Porque el event loop es cooperativo y de un solo hilo. Mientras una corrutina ejecuta una operación bloqueante (`time.sleep`, `requests.get`, un cálculo pesado), **todas las demás tareas del loop están paradas**: no pueden avanzar ni siquiera las que no tienen nada que ver. Esto anula todo el beneficio de asyncio.

Las alternativas son tres: usar versiones async de las librerías (`asyncio.sleep`, `aiohttp`, `asyncpg`), delegar a un pool de threads con `loop.run_in_executor` para operaciones bloqueantes inevitables, o rediseñar la parte pesada para que ceda el control periódicamente. Confundir `time.sleep` con `asyncio.sleep` dentro de una corrutina es un bug clásico y una pregunta frecuente en entrevistas.

### R10. ¿Qué hace `asyncio.wait_for` y cómo se implementa un timeout?

`asyncio.wait_for(awaitable, timeout)` ejecuta el awaitable con un tiempo límite. Si termina a tiempo, devuelve su resultado; si no, lanza `asyncio.TimeoutError` y cancela el awaitable en curso.

```python
try:
    resultado = await asyncio.wait_for(operacion(), timeout=5.0)
except asyncio.TimeoutError:
    # ... manejar el timeout ...
```

En código real, cualquier operación de red debe tener timeout para evitar que un servidor sin respuesta cuelgue todo el sistema. Los frameworks modernos suelen imponer timeouts por defecto. La implementación propia debe capturar `TimeoutError` y decidir qué hacer: reintentar, cancelar, devolver un valor por defecto, propagar al usuario.
