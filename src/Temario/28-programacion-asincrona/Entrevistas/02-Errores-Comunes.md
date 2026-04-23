# Errores Comunes: Programación Asíncrona

## Error 1. Olvidar el `await`

Llamar a una corrutina sin `await` crea el objeto corrutina pero no lo ejecuta. Python emite un warning pero no falla en runtime, así que el bug es silencioso.

```python
import asyncio

async def obtener_usuario():
    await asyncio.sleep(0.1)
    return {"nombre": "Ana"}

# MAL: solo crea el objeto, la corrutina no corre
usuario = obtener_usuario()
print(usuario)   # <coroutine object obtener_usuario at ...>

# BIEN: await ejecuta y obtiene el resultado
usuario = await obtener_usuario()
print(usuario)   # {'nombre': 'Ana'}
```

Los editores modernos subrayan la llamada sin await. Activar los linters correspondientes detecta el 99% de estos errores antes de ejecutar.

---

## Error 2. Usar `time.sleep` en código async

`time.sleep` bloquea el thread y, con él, todo el event loop. Mientras dura el sleep, ninguna otra corrutina avanza.

```python
import asyncio, time

# MAL: bloquea el loop entero durante 2 segundos
async def tarea():
    time.sleep(2)

# BIEN: cede el control al loop, que ejecuta otras tareas
async def tarea():
    await asyncio.sleep(2)
```

La misma regla aplica a `requests.get`, lecturas de archivo con `open`, `input` y cualquier otra operación bloqueante. En contexto async hay que usar las versiones asíncronas o delegar con `loop.run_in_executor`.

---

## Error 3. Ejecutar corrutinas secuencialmente cuando podrían ir en paralelo

Si varias corrutinas son independientes, hacer await una tras otra desperdicia tiempo.

```python
# MAL: total = suma de todas las esperas
async def main():
    r1 = await descargar("a.com")
    r2 = await descargar("b.com")
    r3 = await descargar("c.com")

# BIEN: total ≈ el más lento
async def main():
    r1, r2, r3 = await asyncio.gather(
        descargar("a.com"),
        descargar("b.com"),
        descargar("c.com"),
    )
```

Este error es el que más impacto tiene en rendimiento real. El código "funciona" secuencialmente, pero sin aprovechar la concurrencia de asyncio, que es justamente por lo que se adoptó.

---

## Error 4. No capturar excepciones en `gather` cuando importa

Por defecto, la primera excepción cancela las demás corrutinas y se propaga al código que hizo await sobre gather. Si una petición falla, las otras 99 se pierden.

```python
# MAL: una excepción cancela todas, pierdes resultados que sí funcionaron
resultados = await asyncio.gather(*[descargar(u) for u in urls])

# BIEN: excepciones convertidas en elementos de la lista de resultados
resultados = await asyncio.gather(
    *[descargar(u) for u in urls],
    return_exceptions=True,
)
validos = [r for r in resultados if not isinstance(r, Exception)]
```

`return_exceptions=True` es la opción correcta cuando los fallos parciales son tolerables (descargar lo que se pueda, procesar lo que llegue).

---

## Error 5. Olvidar guardar la referencia a una Task

Si se crea una Task y no se guarda referencia, el recolector puede eliminarla mientras está corriendo y cancelarla silenciosamente.

```python
# MAL: task puede ser recogida por el GC antes de terminar
async def main():
    asyncio.create_task(tarea_fondo())
    await asyncio.sleep(100)

# BIEN: guardar referencia para que sobreviva
async def main():
    task = asyncio.create_task(tarea_fondo())
    await asyncio.sleep(100)
    await task
```

Para varias tasks de fondo, el patrón es guardarlas en una lista o conjunto del ámbito actual. Desde Python 3.11, `asyncio.TaskGroup` gestiona esto automáticamente.

---

## Error 6. Hacer CPU-bound dentro del event loop

Un cálculo pesado sin awaits bloquea el loop entero durante toda su ejecución. Si un cálculo tarda 5 segundos, durante esos 5 segundos ninguna otra corrutina avanza.

```python
# MAL: bloquea el loop
async def procesar(datos):
    return sum(i * i for i in range(100_000_000))

# BIEN: delegar en un pool
async def procesar(datos):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, calcular, datos)
```

Para CPU-bound real, procesos (`ProcessPoolExecutor`) son la solución, no threads. `run_in_executor` con `ProcessPoolExecutor` combina async con multiprocessing.

---

## Error 7. Crear una nueva ClientSession por petición

Cada petición HTTP con `aiohttp` dentro de una nueva sesión reinicia el TLS handshake y el pool de conexiones. Es lento y derrochador.

```python
# MAL: sesión nueva en cada petición
async def descargar(url):
    async with aiohttp.ClientSession() as sesion:
        async with sesion.get(url) as r:
            return await r.text()

# BIEN: sesión compartida entre peticiones
async def main():
    async with aiohttp.ClientSession() as sesion:
        resultados = await asyncio.gather(
            *[descargar(sesion, u) for u in urls]
        )
```

La sesión reutiliza conexiones TCP y cachea DNS. Para clientes con muchas peticiones, la diferencia de rendimiento es de varias veces.

---

## Error 8. Mezclar librerías síncronas en código async sin `run_in_executor`

Usar `requests`, `psycopg2`, `boto3` síncrono y otras librerías bloqueantes dentro de una corrutina congela el event loop. No emite warnings; simplemente rompe el rendimiento.

```python
# MAL: requests bloquea el loop
async def descargar(url):
    r = requests.get(url)
    return r.text

# BIEN: delegar a un thread
async def descargar(url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: requests.get(url).text)

# MEJOR: librería async nativa
async def descargar(sesion, url):
    async with sesion.get(url) as r:
        return await r.text()
```

La regla es que en código async todas las dependencias deben ser async o delegarse a un executor. No hay atajos: una llamada bloqueante oculta puede destruir el rendimiento del sistema entero.

---

## Error 9. No imponer timeouts en operaciones de red

Sin timeout, una petición a un servidor lento o caído puede colgar la corrutina indefinidamente, acumulando tareas pendientes que nunca liberan recursos.

```python
# MAL: si el servidor no responde, cuelga para siempre
respuesta = await sesion.get(url)

# BIEN: timeout explícito
respuesta = await asyncio.wait_for(sesion.get(url), timeout=10)

# También: aiohttp acepta timeout en la sesión o la petición
timeout = aiohttp.ClientTimeout(total=10)
async with aiohttp.ClientSession(timeout=timeout) as sesion:
    ...
```

En entrevistas se pregunta por manejo de timeouts casi siempre que sale asyncio. La respuesta esperada incluye "todo lo que sale a red tiene timeout".

---

## Error 10. Confundir `asyncio.Task` con `concurrent.futures.Future`

Ambos se llaman "futures" en documentación pero no son intercambiables. `asyncio.Task` corre en el event loop, se espera con await, y cancelarlo funciona cooperativamente. `concurrent.futures.Future` viene de ThreadPool/ProcessPool, se espera con `.result()` (bloqueante), y no se integra directamente con await.

```python
# Task de asyncio — await
task = asyncio.create_task(corrutina())
resultado = await task

# Future de concurrent.futures — .result() (bloquea)
future = pool.submit(funcion)
resultado = future.result()

# Para unir ambos mundos
loop = asyncio.get_running_loop()
resultado = await loop.run_in_executor(pool, funcion, arg)
```

`run_in_executor` es el puente entre ambos sistemas. Fuera de ese caso, se usan por separado según el contexto.
