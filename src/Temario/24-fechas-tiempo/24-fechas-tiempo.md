# 24. Fechas y Tiempo

Trabajar con fechas y tiempos parece simple hasta que entran en juego zonas horarias, horario de verano, formatos de parsing, o la diferencia entre "cuánto dura algo" y "qué hora es". Es uno de los temas donde más bugs sutiles aparecen en producción: una conversión mal hecha entre UTC y hora local puede desplazar reservas enteras, cobrar en el día equivocado o registrar eventos con una hora errónea.

En entrevistas, este tema se evalúa a nivel conceptual (naive vs aware, diferencia entre `time` y `datetime`, por qué UTC en el backend) y práctico (parsear una fecha desde string, calcular duraciones, formatear salidas legibles). Python ofrece dos módulos complementarios: `datetime` para trabajar con fechas como objetos, y `time` para operaciones de bajo nivel y medición.

## 24.1. El módulo datetime

El módulo `datetime` es el trabajo habitual con fechas en código profesional. Expone cuatro clases principales: `date`, `time`, `datetime` y `timedelta`. Las tres primeras representan instantes o componentes; `timedelta` representa duraciones.

Todos los objetos del módulo son **inmutables**: cualquier operación que "modifique" una fecha devuelve un objeto nuevo. Esto simplifica el razonamiento y permite usarlos como claves de diccionarios o elementos de conjuntos.

### 24.1.1. date, time, datetime

Cada clase representa una parte distinta de la información temporal:

- `date` representa un día calendario: año, mes y día. Sin hora.
- `time` representa una hora del día: horas, minutos, segundos y microsegundos. Sin fecha.
- `datetime` combina ambas: fecha + hora en un único objeto.

```python
from datetime import date, time, datetime

d = date(2026, 4, 22)                 # solo fecha
t = time(14, 30, 15)                  # solo hora
dt = datetime(2026, 4, 22, 14, 30)    # fecha + hora
```

La diferencia entre usar `date` o `datetime` no es trivial. `date` es el tipo correcto cuando el concepto no tiene hora — una fecha de nacimiento, un día festivo, el cierre contable de un mes. `datetime` es para instantes — el momento en que se registró un evento, la hora de inicio de una reunión. Mezclar ambos lleva a bugs: comparar un `date` con un `datetime` lanza `TypeError`, y confundir "día" con "instante a las 00:00:00" puede desplazar fechas por una hora al cambiar la zona horaria.

La clase `time` sola (sin fecha) se usa poco en la práctica. Suele aparecer al separar componentes de un `datetime` o al representar horarios recurrentes (por ejemplo, "apertura a las 9:00").

### 24.1.2. Crear y acceder a componentes (year, month, day, hour, minute)

Los objetos se crean pasando los componentes como argumentos al constructor, en el orden `año, mes, día, hora, minuto, segundo, microsegundo` para `datetime`. Los campos de tiempo son opcionales y por defecto valen cero.

```python
from datetime import datetime

dt = datetime(2026, 4, 22, 14, 30)
dt.year        # 2026
dt.month       # 4
dt.day         # 22
dt.hour        # 14
dt.minute      # 30
dt.second      # 0
dt.weekday()   # 2 (miércoles; 0=lunes, 6=domingo)
```

Los atributos son de solo lectura. Para obtener un objeto modificado se usa el método `replace`, que devuelve una copia con los campos indicados cambiados:

```python
dt.replace(hour=9, minute=0)   # 2026-04-22 09:00:00
```

`replace` es la forma idiomática de "empezar a las 9:00 del mismo día", "poner el primer día del mes" (`replace(day=1)`), etc. Nunca se mutan los objetos originales.

### 24.1.3. datetime.now() y datetime.today()

Para obtener el instante actual, `datetime.now()` y `datetime.today()` son prácticamente equivalentes y devuelven un `datetime` naive (sin información de zona horaria) con la hora local del sistema.

```python
from datetime import datetime

ahora = datetime.now()       # 2026-04-22 10:15:32.123456
hoy = datetime.today()       # equivalente a now() sin argumentos
hoy_fecha = date.today()     # solo la fecha: 2026-04-22
```

`now()` acepta un argumento de zona horaria para obtener un `datetime` aware:

```python
from datetime import datetime, timezone
datetime.now(timezone.utc)   # instante actual en UTC con tz
```

Usar `datetime.now()` sin zona horaria es una de las decisiones más peligrosas del tema: produce datetimes naive que parecen "obvios" pero son ambiguos en cualquier sistema que no corra en UTC. La regla en backend es trabajar siempre con `datetime.now(timezone.utc)` o similar, y reservar los naive para código que no cruza zonas horarias.

## 24.2. Aritmética de fechas

Las operaciones aritméticas sobre fechas tienen un tipo central: `timedelta`, que representa una duración. Sumar o restar `timedelta` a un `datetime` da otro `datetime`. Restar dos `datetime` da un `timedelta`. Esta simetría hace la aritmética temporal limpia y predecible.

### 24.2.1. timedelta (sumar y restar tiempo)

Un `timedelta` se construye pasando unidades: días, horas, minutos, segundos, milisegundos, microsegundos, semanas. **No hay meses ni años** porque su duración varía (un mes puede tener 28-31 días, un año puede tener 365 o 366). Sumar "un mes" es una operación ambigua que `timedelta` deliberadamente no soporta.

```python
from datetime import datetime, timedelta

dt = datetime(2026, 4, 22, 10, 0)
dt + timedelta(days=7)                  # una semana después
dt + timedelta(hours=5, minutes=30)     # 5h 30min después
dt - timedelta(days=30)                 # 30 días antes
```

Para "un mes después", hay que decidir qué significa: ¿el mismo día del mes siguiente? ¿30 días? ¿el último día si el siguiente mes no tiene ese día? Esas decisiones dependen del negocio y suelen implementarse explícitamente, a veces con ayuda de la librería `dateutil` y su `relativedelta`.

`timedelta` soporta todas las operaciones aritméticas habituales: sumas entre deltas, multiplicación por un escalar, división por otro delta para obtener la proporción.

```python
semana = timedelta(days=7)
mes = 4 * semana            # timedelta(days=28)
(mes / semana)              # 4.0
```

### 24.2.2. Comparar fechas

Los objetos `date` y `datetime` se comparan con los operadores habituales (`<`, `<=`, `==`, `>`), respetando el orden cronológico. Restar dos `datetime` devuelve un `timedelta`, que también se puede comparar entre sí:

```python
inicio = datetime(2026, 4, 22, 9, 0)
fin = datetime(2026, 4, 22, 17, 30)

if inicio < fin:
    duracion = fin - inicio           # timedelta(hours=8, minutes=30)
    print(duracion.total_seconds())   # 30600.0
```

`total_seconds()` convierte cualquier `timedelta` en un float con la duración total en segundos, útil para medidas, logs o comparaciones con umbrales expresados en segundos.

Hay una trampa al comparar: un `datetime` naive y un `datetime` aware no se pueden comparar entre sí — lanza `TypeError`. Este error se ve a veces al mezclar `datetime.now()` (naive) con datetimes que vienen de una API (aware). La solución es ser consistente y trabajar siempre en aware (con zona horaria) en código que cruza sistemas.

## 24.3. Formateo y parsing

Convertir entre `datetime` y `str` es una tarea constante: logs, APIs, interfaces, bases de datos. Python ofrece dos familias de funciones: `strftime`/`strptime` con formato libre, y las funciones ISO (`isoformat`, `fromisoformat`) para un formato estándar específico.

### 24.3.1. strftime() (fecha → string)

`strftime("formato")` convierte un `datetime` a string según un patrón con marcadores. Los marcadores siguen una convención estándar de C que no es intuitiva y que casi todos acabamos buscando en la documentación cada vez.

Los más usados son:

- `%Y` año con 4 dígitos (2026)
- `%m` mes con ceros (01–12)
- `%d` día del mes con ceros (01–31)
- `%H` hora 24h con ceros (00–23)
- `%M` minuto (00–59)
- `%S` segundo (00–59)
- `%A` nombre del día (Wednesday)
- `%B` nombre del mes (April)

```python
from datetime import datetime

dt = datetime(2026, 4, 22, 14, 30)
dt.strftime("%Y-%m-%d")             # '2026-04-22'
dt.strftime("%d/%m/%Y %H:%M")       # '22/04/2026 14:30'
dt.strftime("%A, %d de %B de %Y")   # 'Wednesday, 22 de April de 2026'
```

Los nombres de días y meses siguen el **locale** del sistema. Para garantizar el mismo resultado entre sistemas, se fija el locale con `locale.setlocale` o se formatea con marcadores numéricos y se traduce manualmente.

### 24.3.2. strptime() (string → fecha)

`datetime.strptime(texto, "formato")` es la operación inversa: parsea un string según un formato explícito y devuelve un `datetime`. Si el texto no encaja con el formato, lanza `ValueError`.

```python
from datetime import datetime

dt = datetime.strptime("22/04/2026", "%d/%m/%Y")
dt = datetime.strptime("2026-04-22 14:30:00", "%Y-%m-%d %H:%M:%S")
```

El formato tiene que coincidir exactamente con el texto: cualquier espacio o separador distinto genera `ValueError`. Para inputs de usuarios con variaciones (espacios extra, formatos mixtos) suele ser mejor usar la librería `dateutil` (`dateutil.parser.parse`), que intenta adivinar el formato — útil para prototipos pero menos predecible que fijar el formato explícitamente.

### 24.3.3. Formato ISO 8601 (isoformat, fromisoformat)

ISO 8601 es el estándar internacional para representar fechas: `YYYY-MM-DD` para fechas y `YYYY-MM-DDTHH:MM:SS` para instantes. Es legible, ordenable alfabéticamente (coincide con el orden cronológico), e inequívoco. Es el formato recomendado para intercambio de datos entre sistemas.

Python ofrece métodos dedicados que evitan tener que escribir patrones:

```python
from datetime import datetime

dt = datetime(2026, 4, 22, 14, 30)
dt.isoformat()                              # '2026-04-22T14:30:00'

parseado = datetime.fromisoformat("2026-04-22T14:30:00")
```

Desde Python 3.11, `fromisoformat` acepta cualquier string ISO 8601 válido, incluyendo zonas horarias (`"2026-04-22T14:30:00+00:00"`). En versiones anteriores era más restrictivo y solo aceptaba el formato exacto que produce `isoformat`.

En APIs JSON, el formato ISO es el estándar de facto. Cualquier sistema moderno produce y consume ISO; formatos locales como `DD/MM/YYYY` se reservan para la interfaz con humanos.

## 24.4. El módulo time

El módulo `time` ofrece acceso a funciones de bajo nivel del sistema relacionadas con el tiempo. Frente a `datetime`, que trabaja con objetos y componentes calendario, `time` trabaja con timestamps (segundos desde el epoch) y mediciones.

### 24.4.1. time.time() y time.perf_counter()

`time.time()` devuelve el tiempo actual como un float con los segundos transcurridos desde el epoch Unix (1 de enero de 1970 UTC). Es útil como timestamp para logs, como semilla reproducible, o para calcular intervalos con precisión de segundo.

```python
import time

t0 = time.time()
procesar_datos()
duracion = time.time() - t0
print(f"Tardó {duracion:.2f} segundos")
```

Para medir duraciones con precisión alta y de forma resistente a ajustes del reloj del sistema, `time.perf_counter()` es preferible. Devuelve también segundos pero usa el reloj monotónico más preciso disponible.

```python
import time

t0 = time.perf_counter()
funcion_bajo_medicion()
duracion = time.perf_counter() - t0
```

La diferencia práctica aparece en benchmarks: si el reloj del sistema se ajusta durante la medición (NTP, cambio de zona horaria, horario de verano), `time.time()` puede devolver duraciones negativas o saltos. `perf_counter()` no se ve afectado y es la opción correcta para cualquier medida precisa.

### 24.4.2. time.sleep()

`time.sleep(segundos)` pausa la ejecución del hilo actual durante el número de segundos indicado. Acepta floats para fracciones de segundo.

```python
import time

for intento in range(3):
    if hacer_peticion():
        break
    time.sleep(2)   # espera 2 segundos antes de reintentar
```

En código asíncrono (con `asyncio`), `time.sleep` bloquea el event loop y no debe usarse — la alternativa asíncrona es `asyncio.sleep`. En hilos normales, `time.sleep` es el patrón habitual para backoff entre reintentos, polling con retardo, o simplemente ralentizar un bucle.

`sleep` no es un temporizador exacto: el sistema operativo puede devolver el control algo después del tiempo pedido. Para aplicaciones que dependen de timing preciso se combinan `sleep` con mediciones de `perf_counter` que ajustan las siguientes esperas.

## 24.5. Zonas horarias

Las zonas horarias son la fuente número uno de bugs reales en software que maneja tiempo. Un servidor en Madrid procesa eventos de usuarios en Tokio, la base de datos guarda en UTC, el frontend muestra en la zona del usuario, y alguna conversión tiene que pasar entre las tres. Hacer esto bien requiere dos ideas: distinguir naive de aware, y adoptar la práctica de trabajar en UTC internamente.

### 24.5.1. Naive vs aware datetimes

Un `datetime` es **aware** (consciente) si tiene información de zona horaria asociada; es **naive** (ingenuo) si no la tiene. La diferencia se comprueba con el atributo `tzinfo`: si vale `None`, es naive.

```python
from datetime import datetime, timezone

naive = datetime(2026, 4, 22, 14, 30)
aware = datetime(2026, 4, 22, 14, 30, tzinfo=timezone.utc)

naive.tzinfo   # None
aware.tzinfo   # datetime.timezone.utc
```

Un datetime naive no se puede convertir entre zonas horarias porque no sabe "en qué hora está expresado". Naive significa "las 14:30 de algún sitio" — si se supone que es hora local o UTC depende del contexto y es responsabilidad del programador recordarlo.

La regla profesional es: **todo lo que cruza sistemas debe ser aware**, preferiblemente en UTC. Los naive se reservan para lógica puramente local que no interactúa con zonas horarias. Mezclar ambos lleva a `TypeError` al comparar o restar, lo que al menos hace el bug visible — peor es asumir que un naive "es UTC" y operar con él como si lo fuera.

### 24.5.2. zoneinfo (Python 3.9+)

El módulo `zoneinfo` de la librería estándar (añadido en Python 3.9) da acceso a la base de datos IANA de zonas horarias, que incluye todas las zonas del mundo con sus reglas históricas de DST y cambios políticos.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

madrid = ZoneInfo("Europe/Madrid")
tokio = ZoneInfo("Asia/Tokyo")

dt = datetime(2026, 4, 22, 14, 30, tzinfo=madrid)
dt_tokio = dt.astimezone(tokio)
print(dt_tokio)   # 2026-04-22 21:30:00+09:00
```

`astimezone(otra_zona)` convierte un datetime aware de una zona a otra preservando el instante absoluto. Este es el método correcto: modifica la representación, no el momento en el tiempo.

Las zonas con DST (horario de verano) son especialmente delicadas. `ZoneInfo` maneja correctamente los cambios — sumar 24 horas a un datetime justo antes del cambio puede dar una hora distinta de "mismo momento del día siguiente", porque el día del cambio tiene 23 o 25 horas reales. Por eso la aritmética en zonas con DST suele hacerse en UTC y convertirse solo para mostrar.

El patrón recomendado en backend es: guardar siempre en UTC aware, operar en UTC, convertir a la zona del usuario únicamente en la capa de presentación. Cualquier fecha que entra al sistema desde fuera se convierte a UTC inmediatamente; cualquier fecha que sale se convierte a la zona del destinatario. Con esta disciplina, los bugs de zona horaria se reducen drásticamente.
