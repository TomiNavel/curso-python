# Errores Comunes: Concurrencia y Paralelismo

## Error 1. Usar threads para tareas CPU-bound

El GIL impide que los threads Python ejecuten bytecode en paralelo. Usarlos para código CPU-intensivo puro no solo no acelera, sino que puede ralentizar por el overhead de sincronización.

```python
# MAL: no hay aceleración, el GIL limita a un core
from concurrent.futures import ThreadPoolExecutor

def calcular(n):
    return sum(i * i for i in range(n))

with ThreadPoolExecutor() as pool:
    resultados = list(pool.map(calcular, [10_000_000] * 8))

# BIEN: procesos se reparten los cores
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as pool:
    resultados = list(pool.map(calcular, [10_000_000] * 8))
```

Para tareas CPU-bound en Python puro, la herramienta correcta es `ProcessPoolExecutor` o `multiprocessing`.

---

## Error 2. Modificar variables compartidas sin Lock

Cuando varios threads incrementan un contador sin sincronización, las actualizaciones se pisan y el resultado es menor al esperado.

```python
import threading

contador = 0

def incrementar():
    global contador
    for _ in range(100_000):
        contador += 1   # NO es atómico

# MAL: el resultado casi nunca es 400_000
threads = [threading.Thread(target=incrementar) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(contador)

# BIEN: proteger la operación con un Lock
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(100_000):
        with lock:
            contador += 1
```

La alternativa idiomática es evitar el estado compartido: usar colas (`queue.Queue`) o estructuras thread-safe para comunicar entre threads.

---

## Error 3. Olvidar `if __name__ == "__main__":` con multiprocessing

En Windows y macOS, cada proceso hijo re-importa el módulo al arrancar. Sin el guard, el código de arranque se ejecuta infinitamente, creando procesos que crean procesos.

```python
# MAL: sin guard, crea procesos sin fin en Windows/macOS
import multiprocessing as mp

def tarea(n):
    return n * n

pool = mp.Pool(4)
resultados = pool.map(tarea, [1, 2, 3, 4])

# BIEN: guard obligatorio
if __name__ == "__main__":
    pool = mp.Pool(4)
    resultados = pool.map(tarea, [1, 2, 3, 4])
```

Es uno de los primeros errores de todo el que usa multiprocessing por primera vez. En Linux con `fork` no se nota porque el proceso hijo se bifurca sin re-importar, pero el código no es portable sin el guard.

---

## Error 4. No hacer `join()` y que el programa termine antes que los threads

Sin `join`, el programa principal puede acabar mientras los threads siguen ejecutándose. Los threads no-daemon impiden el cierre, pero si hay daemons, se cortan abruptamente.

```python
import threading

# MAL: main puede acabar antes que los threads terminen su trabajo
def tarea():
    # ... trabajo que puede tardar ...
    ...

t1 = threading.Thread(target=tarea)
t1.start()
# falta t1.join(), main sigue y puede acabar

# BIEN: esperar a que el thread termine
t1 = threading.Thread(target=tarea)
t1.start()
t1.join()
```

Cuando hay varios threads, el patrón es arrancarlos todos primero y hacer join después a todos, para que trabajen concurrentemente y no uno tras otro.

---

## Error 5. Arrancar y unir en el mismo bucle

Arrancar cada thread y hacer `join()` inmediatamente hace que los threads se ejecuten secuencialmente, perdiendo cualquier beneficio de concurrencia.

```python
# MAL: cada thread termina antes de arrancar el siguiente
for tarea in tareas:
    t = threading.Thread(target=trabajar, args=(tarea,))
    t.start()
    t.join()   # bloquea hasta terminar antes de pasar al siguiente

# BIEN: arrancar todos, luego esperar todos
threads = []
for tarea in tareas:
    t = threading.Thread(target=trabajar, args=(tarea,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

Con `ThreadPoolExecutor.map` o `submit + as_completed` este error desaparece porque el pool gestiona la ejecución correctamente.

---

## Error 6. Ignorar excepciones que ocurren en threads

Un thread que lanza una excepción no gestionada **no propaga** al thread principal. Se pierde silenciosamente, y el thread muere sin más aviso.

```python
import threading

def tarea_que_falla():
    raise ValueError("error")

# MAL: la excepción se pierde, el main no se entera
t = threading.Thread(target=tarea_que_falla)
t.start()
t.join()

# BIEN: usar ThreadPoolExecutor, future.result() relanza la excepción
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as pool:
    futuro = pool.submit(tarea_que_falla)
    futuro.result()   # relanza ValueError en el main
```

`concurrent.futures` captura las excepciones en el Future y las relanza al llamar a `.result()`. Es una razón más para preferirlo frente a gestionar threads a mano.

---

## Error 7. Pasar funciones no picklables a multiprocessing

Los procesos hijo reciben la función y los argumentos **serializados con pickle**. Funciones lambda, anidadas o métodos dinámicos no son picklables.

```python
# MAL: lambda no se puede pickle
with ProcessPoolExecutor() as pool:
    pool.map(lambda x: x * 2, numeros)   # PicklingError

# BIEN: función top-level
def duplicar(x):
    return x * 2

with ProcessPoolExecutor() as pool:
    pool.map(duplicar, numeros)
```

La restricción aplica a cualquier argumento: si pasas un objeto con atributos no picklables, falla. Diseñar las funciones y los datos con picklability en mente es parte del uso correcto de multiprocessing.

---

## Error 8. Olvidar tamaño del pool por defecto

`ThreadPoolExecutor` y `ProcessPoolExecutor` sin argumentos usan tamaños por defecto que no siempre son los óptimos. Pocos workers desaprovechan recursos; demasiados sobrecargan el sistema.

```python
# Por defecto, ThreadPoolExecutor usa min(32, os.cpu_count() + 4)
# Por defecto, ProcessPoolExecutor usa os.cpu_count()

# Para I/O-bound con muchas esperas (HTTP), más workers suele ser mejor
with ThreadPoolExecutor(max_workers=50) as pool: ...

# Para CPU-bound, más procesos que cores no suele ayudar
with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool: ...
```

La regla práctica es medir: probar varios tamaños con carga real y elegir el que minimiza el tiempo total. Los valores por defecto son razonables pero rara vez óptimos.

---

## Error 9. Usar sleep para sincronizar threads

Introducir `time.sleep` para "darle tiempo" a otro thread es una solución frágil que falla de forma intermitente bajo carga.

```python
# MAL: sincronización basada en sleep, flakey
def consumidor():
    time.sleep(1)   # "seguro que el productor ya preparó los datos"
    usar(datos)

# BIEN: Event u otra primitiva de sincronización
event = threading.Event()

def productor():
    preparar_datos()
    event.set()

def consumidor():
    event.wait()
    usar(datos)
```

Los `sleep` arbitrarios son señal de diseño incorrecto. En entrevistas se considera mala práctica clásica; las primitivas de sincronización (Event, Lock, Condition) son la forma correcta de coordinar.

---

## Error 10. Daemon threads para trabajo importante

Los daemon threads mueren abruptamente cuando el main acaba. Usarlos para operaciones que deben completar — escribir un archivo, cerrar una conexión, enviar una métrica — puede dejar estado inconsistente.

```python
# MAL: si el main acaba, la escritura puede quedarse a medias
def guardar_estado():
    escribir_archivo()

t = threading.Thread(target=guardar_estado, daemon=True)
t.start()

# BIEN: thread normal con join para garantizar que termina
t = threading.Thread(target=guardar_estado)
t.start()
try:
    # ... main ...
finally:
    t.join()
```

Daemon threads solo son apropiados para tareas cuyo corte no causa problemas: loops de monitorización que la app puede reiniciar, timers que no guardan estado persistente. Para cualquier cosa con efecto duradero, thread normal con cierre limpio.
