# Errores Comunes: Fechas y Tiempo

## Error 1. Usar `datetime.now()` sin zona horaria

`datetime.now()` sin argumentos devuelve un datetime naive con la hora local del sistema. En servidores desplegados en distintas regiones, la "hora local" varía; guardar o comparar estos valores produce desfases silenciosos.

```python
from datetime import datetime, timezone

# MAL: naive, depende de la zona del servidor
creado = datetime.now()

# BIEN: aware en UTC, consistente en cualquier servidor
creado = datetime.now(timezone.utc)
```

La regla profesional es generar siempre aware en UTC y convertir a local solo al presentar al usuario.

---

## Error 2. Comparar un datetime naive con uno aware

Python no permite comparar directamente naive y aware: lanza `TypeError`. Esto ocurre a menudo al mezclar `datetime.now()` (naive) con datetimes que vienen de APIs o bases de datos (aware).

```python
from datetime import datetime, timezone

aware = datetime(2026, 4, 22, tzinfo=timezone.utc)
naive = datetime.now()

# MAL: TypeError: can't compare offset-naive and offset-aware datetimes
if naive > aware:
    ...

# BIEN: ser consistente — todo aware
if datetime.now(timezone.utc) > aware:
    ...
```

El error al menos es visible. Peor es asumir que un naive "es UTC" y operar con él como si lo fuera: funciona en desarrollo y rompe en producción.

---

## Error 3. Usar `time.time()` para medir duraciones

`time.time()` depende del reloj del sistema, que puede ajustarse por NTP o por cambios de hora. Para benchmarks o medidas precisas, la duración puede quedar mal calculada.

```python
import time

# MAL: afectado por ajustes del reloj del sistema
t0 = time.time()
funcion_lenta()
duracion = time.time() - t0

# BIEN: reloj monotónico, no afectado por ajustes
t0 = time.perf_counter()
funcion_lenta()
duracion = time.perf_counter() - t0
```

`perf_counter` no da un timestamp útil (su valor absoluto no significa nada) pero es la opción correcta para medir intervalos.

---

## Error 4. Intentar sumar meses con `timedelta`

`timedelta` no acepta meses ni años porque su duración es variable. Intentar `timedelta(months=1)` lanza `TypeError`. Implementar "un mes después" a mano suele fallar con fines de mes.

```python
from datetime import date, timedelta

# MAL: TypeError
siguiente = date(2026, 1, 31) + timedelta(months=1)

# MAL: 30 días no es lo mismo que "un mes"
siguiente = date(2026, 1, 31) + timedelta(days=30)   # 2026-03-02, no 02-28

# BIEN: dateutil.relativedelta conoce meses y fin de mes
from dateutil.relativedelta import relativedelta
siguiente = date(2026, 1, 31) + relativedelta(months=1)   # 2026-02-28
```

`dateutil` es una librería externa pero es el estándar para aritmética con meses y años. Para sumar días fijos, `timedelta(days=N)` es correcto.

---

## Error 5. Olvidar que `strptime` falla si el formato no encaja exactamente

`datetime.strptime` exige coincidencia exacta: espacios extra, separadores distintos o mayúsculas diferentes lanzan `ValueError`.

```python
from datetime import datetime

# MAL: el texto tiene espacio extra y strptime falla
datetime.strptime("22 /04/2026", "%d/%m/%Y")  # ValueError

# BIEN: normalizar antes de parsear o usar dateutil para tolerar variaciones
texto = texto.replace(" ", "")
datetime.strptime(texto, "%d/%m/%Y")
```

Para inputs de usuarios con formatos variables, `dateutil.parser.parse` es más flexible — útil en prototipos, pero menos predecible que fijar el formato.

---

## Error 6. Comparar fechas como strings sin formato ISO

Comparar fechas como strings funciona solo si el formato coincide alfabéticamente con el orden cronológico. ISO 8601 cumple esta propiedad; formatos como `DD/MM/YYYY` no.

```python
# MAL: orden alfabético no cronológico
"01/05/2026" < "22/04/2026"   # True (01 < 22), pero mayo es después

# BIEN: comparar objetos date o usar formato ISO
from datetime import date
date(2026, 5, 1) < date(2026, 4, 22)   # False
"2026-05-01" < "2026-04-22"            # False (ISO funciona alfabéticamente)
```

Para ordenar o comparar, convertir a `date`/`datetime` es lo más seguro. Si se guarda como string, ISO es el único formato que permite comparación alfabética correcta.

---

## Error 7. Asumir que "un día" equivale a 24 horas cerca de DST

En zonas con horario de verano, el día del cambio tiene 23 o 25 horas reales. Sumar `timedelta(days=1)` puede dejar la hora desplazada respecto al día equivalente.

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

madrid = ZoneInfo("Europe/Madrid")
# 28/03/2026 es cambio a horario de verano
dt = datetime(2026, 3, 28, 10, 0, tzinfo=madrid)

# MAL: +24h no es "mismo momento del día siguiente" por el cambio DST
dt_maniana = dt + timedelta(days=1)   # hora distinta a las 10:00 del día siguiente

# BIEN: operar en UTC y convertir solo al mostrar
dt_utc = dt.astimezone(ZoneInfo("UTC"))
dt_maniana = (dt_utc + timedelta(days=1)).astimezone(madrid)
```

Para aritmética en zonas con DST, lo más limpio es pasar a UTC, sumar el delta, y volver a la zona deseada.

---

## Error 8. Usar `time.sleep` en código `asyncio`

`time.sleep` bloquea el hilo entero, incluyendo el event loop de `asyncio`. Todo el programa asíncrono se congela durante ese tiempo.

```python
import asyncio
import time

# MAL: bloquea todo el event loop
async def tarea():
    time.sleep(2)

# BIEN: pausa solo esta corrutina, el loop sigue libre
async def tarea():
    await asyncio.sleep(2)
```

En código síncrono normal, `time.sleep` es correcto. En asyncio, siempre `asyncio.sleep`.

---

## Error 9. Usar `date.today()` donde se necesita un `datetime`

`date.today()` devuelve un `date`, sin información de hora. Si se mezcla con `datetime` en comparaciones o en APIs que esperan un instante, aparecen errores.

```python
from datetime import date, datetime

hoy = date.today()
evento = datetime(2026, 4, 22, 14, 30)

# MAL: TypeError: can't compare datetime.date to datetime.datetime
if evento > hoy:
    ...

# BIEN: convertir explícitamente
if evento.date() > hoy:
    ...
```

La regla es no mezclar tipos. Si el contexto trabaja con instantes, usar `datetime` en todas partes; si son solo fechas, `date`.

---

## Error 10. Escapar incorrectamente los marcadores de `strftime`

Los marcadores empiezan por `%`. Si se quiere un `%` literal en el formato, hay que escribir `%%`. Olvidarlo produce texto con caracteres inesperados o, peor, interpretación como marcador distinto.

```python
from datetime import datetime

dt = datetime(2026, 4, 22)

# MAL: %H sin hora produce 00 inesperadamente en contexto distinto
dt.strftime("Progreso: 50%")   # el % suelto puede comportarse raro

# BIEN: escapar con %%
dt.strftime("Progreso: 50%%")   # 'Progreso: 50%'
```

Escapar `%%` es el detalle que se olvida al mezclar fechas con texto que contiene porcentajes literales.
