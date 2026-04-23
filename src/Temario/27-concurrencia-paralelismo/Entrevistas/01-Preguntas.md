# Preguntas de Entrevista: Concurrencia y Paralelismo

1. ¿Cuál es la diferencia entre concurrencia y paralelismo?
2. ¿Qué es el GIL y qué implica al usar threads en Python?
3. ¿Cómo distingues una tarea CPU-bound de una I/O-bound?
4. ¿Cuándo usarías `threading` y cuándo `multiprocessing`?
5. ¿Qué es una condición de carrera y cómo se previene?
6. ¿Qué diferencia hay entre `Lock` y `RLock`?
7. ¿Qué ventajas aporta `concurrent.futures` sobre gestionar threads y procesos a mano?
8. ¿Qué hace `ThreadPoolExecutor.map` y en qué orden devuelve los resultados?
9. ¿Para qué sirve `as_completed`?
10. ¿Qué es un daemon thread y qué riesgos tiene?

---

### R1. ¿Cuál es la diferencia entre concurrencia y paralelismo?

Concurrencia es la capacidad de un programa de **progresar en varias tareas al mismo tiempo**, alternando entre ellas. Paralelismo es la **ejecución simultánea real** de varias tareas en distintos cores o procesadores. La concurrencia es un modelo de organización; el paralelismo es un requisito físico del hardware.

Un programa concurrente puede no ser paralelo — por ejemplo, asyncio ejecuta varias corrutinas en un único hilo, alternando cuando una espera. Un programa paralelo es necesariamente concurrente. La distinción importa en Python porque el GIL permite concurrencia con threads pero limita el paralelismo del bytecode, obligando a elegir procesos cuando se busca paralelismo real para cálculo puro.

### R2. ¿Qué es el GIL y qué implica al usar threads en Python?

El GIL (Global Interpreter Lock) es un mutex del intérprete CPython que garantiza que solo un thread ejecuta bytecode Python en un momento dado. Su consecuencia directa es que los threads no dan paralelismo real para tareas CPU-bound en Python puro: aunque la máquina tenga muchos cores, el código Python se ejecuta como en uno solo.

El GIL se libera en esperas de I/O y en muchas funciones C bien diseñadas (NumPy, pandas, operaciones de red). Por eso threading sigue siendo útil para I/O-bound: mientras un thread espera una respuesta, otro puede trabajar. Para CPU-bound en Python puro, la solución es `multiprocessing`, donde cada proceso tiene su propio GIL. En Python 3.13 hay trabajo experimental para eliminar el GIL ("nogil"), pero aún no es el comportamiento por defecto.

### R3. ¿Cómo distingues una tarea CPU-bound de una I/O-bound?

Una tarea CPU-bound está limitada por la velocidad del procesador: cálculos, transformaciones en memoria, compresión, cifrado. Al monitorizar, se ve un core al 100% y los demás ociosos. Una tarea I/O-bound pasa la mayor parte del tiempo esperando: red, disco, base de datos, teclado. El uso de CPU es bajo aunque el programa tarde mucho.

La forma empírica de distinguirlas es medir. Si la tarea tarda 10 segundos y durante esos 10 segundos un core va al 100% con el resto ocioso, es CPU-bound. Si la CPU no se mueve casi pero el tiempo pasa, es I/O-bound. La diferenciación es crítica porque decide qué herramienta acelera: threads para I/O, procesos para CPU.

### R4. ¿Cuándo usarías `threading` y cuándo `multiprocessing`?

`threading` para tareas **I/O-bound** (peticiones HTTP, lecturas de archivos, consultas a BD) o para tareas CPU-bound que se ejecutan en librerías que liberan el GIL (NumPy, pandas). Es ligero: los threads comparten memoria, se crean rápido y consumen poco. La limitación es el GIL para código Python puro.

`multiprocessing` para tareas **CPU-bound en Python puro**. Cada proceso tiene su propio intérprete y su propio GIL, así que escalan a múltiples cores. El coste es mayor: crear procesos es lento, la memoria no se comparte directamente (hay que serializar para comunicar), y el overhead es más alto. Si la tarea es corta, el coste de arrancar procesos puede superar al beneficio.

### R5. ¿Qué es una condición de carrera y cómo se previene?

Una condición de carrera es un bug que aparece cuando varios threads acceden a datos compartidos y el resultado depende del orden exacto de ejecución, que no es predecible. Un ejemplo clásico es dos threads incrementando un contador: `x += 1` no es atómico (implica leer, sumar, escribir), y dos threads pueden leer el mismo valor antes de que cualquiera escriba, perdiendo un incremento.

Se previenen con primitivas de sincronización que protegen las secciones críticas. `Lock` es la más básica: solo un thread a la vez puede estar dentro del bloque `with lock:`. Otras soluciones son evitar el estado compartido por diseño (usar colas, pasar inmutables), o usar estructuras thread-safe (`queue.Queue`, `collections.deque` para operaciones simples). En código profesional, diseñar para no compartir estado es mejor que sincronizar compartido.

### R6. ¿Qué diferencia hay entre `Lock` y `RLock`?

`Lock` es un lock simple: el thread que lo adquiere debe liberarlo antes de que cualquiera (incluido él mismo) pueda adquirirlo. Si el mismo thread intenta adquirir un Lock que ya tiene, se bloquea indefinidamente (deadlock consigo mismo).

`RLock` (reentrant lock) permite al mismo thread adquirir el lock varias veces. Cuenta las adquisiciones y solo se libera del todo cuando las liberaciones igualan las adquisiciones. Es útil cuando una función que usa un lock llama a otra función del mismo módulo que también lo usa; con `Lock` habría deadlock. En código nuevo suele ser preferible diseñar para no necesitar reentrada (factorizar la lógica para que el lock se adquiera en un único punto), pero `RLock` es la red de seguridad cuando la recursión es inevitable.

### R7. ¿Qué ventajas aporta `concurrent.futures` sobre gestionar threads y procesos a mano?

Tres ventajas principales. **Abstracción uniforme**: la misma API vale para threads (`ThreadPoolExecutor`) y procesos (`ProcessPoolExecutor`), así que probar ambos y elegir es cambiar una línea. **Gestión del pool**: reutiliza workers, limita el número activo, evita el coste de crear y destruir para cada tarea. **Captura de excepciones en Futures**: si una tarea falla, la excepción se relanza en el thread que llama a `.result()`, en lugar de quedar perdida en un thread que muere sin avisar.

Para la mayoría de casos profesionales, `concurrent.futures` es la herramienta recomendada. Solo se baja a `threading.Thread` o `multiprocessing.Process` cuando se necesita control fino que el pool no da (daemon threads, ciclos de vida largos, coordinación compleja).

### R8. ¿Qué hace `ThreadPoolExecutor.map` y en qué orden devuelve los resultados?

`pool.map(funcion, iterable)` aplica la función a cada elemento del iterable en paralelo, usando los workers del pool, y devuelve un iterador con los resultados **en el mismo orden que la entrada**. Es el equivalente paralelo al `map` builtin.

El orden de los resultados no coincide con el orden en que las tareas terminan: aunque la tercera tarea termine antes que la primera, `map` espera a que la primera esté lista para devolverla primero. Esta garantía de orden es útil cuando el código necesita asociar entradas con salidas por posición. Si no importa el orden y se quiere procesar resultados según terminan, la herramienta es `as_completed`.

### R9. ¿Para qué sirve `as_completed`?

`as_completed(futuros)` recibe una colección de Futures y produce cada uno según termina, sin esperar al orden original. Es el patrón ideal cuando el código quiere empezar a procesar resultados en cuanto están disponibles, o mostrar progreso en tiempo real.

Por ejemplo, al descargar 100 URLs en paralelo, `map` obligaría a esperar a que la primera acabe antes de procesar nada, aunque la 50 ya esté lista. `as_completed` devuelve el primer Future que termine, procesamos su resultado y seguimos. Es más eficiente cuando el tiempo de procesar cada resultado no es despreciable frente al tiempo de esperarlos, o cuando el orden de llegada es una señal útil (por ejemplo, para timeouts dinámicos).

### R10. ¿Qué es un daemon thread y qué riesgos tiene?

Un daemon thread es un thread que no impide al programa principal terminar. Python espera a que todos los threads no daemon acaben antes de salir; los daemon se cortan abruptamente cuando el programa principal acaba.

Son útiles para tareas de fondo atadas al ciclo de vida del proceso: heartbeats, monitorización, limpieza periódica. El riesgo es el corte abrupto: si el daemon estaba en medio de escribir un archivo, hacer una petición HTTP o gestionar una transacción, puede dejar el estado inconsistente. Para recursos críticos no se usan daemons; el patrón correcto es un thread normal con un `Event` para señalizar parada limpia y `join()` al salir. En entrevistas, saber cuándo no usar daemons demuestra criterio — mucha gente los usa por defecto sin pensar en las implicaciones.
