# Preguntas de Entrevista: Fechas y Tiempo

1. ¿Qué diferencia hay entre `date`, `time` y `datetime`?
2. ¿Qué es un `timedelta` y por qué no tiene campos de meses ni años?
3. ¿Qué diferencia hay entre un `datetime` naive y uno aware?
4. ¿Por qué se recomienda trabajar en UTC en el backend?
5. ¿Cuál es la diferencia entre `time.time()` y `time.perf_counter()`?
6. ¿Qué hacen `strftime` y `strptime`?
7. ¿Por qué es buena práctica usar `isoformat` y `fromisoformat` cuando sea posible?
8. ¿Cómo se convierte un `datetime` aware entre zonas horarias?
9. ¿Por qué los objetos del módulo `datetime` son inmutables?
10. ¿Qué problemas introduce el horario de verano (DST) al hacer aritmética con fechas?

---

### R1. ¿Qué diferencia hay entre `date`, `time` y `datetime`?

`date` representa un día calendario sin información de hora: año, mes y día. Es el tipo correcto para conceptos que no tienen hora, como una fecha de nacimiento o un festivo. `time` representa una hora del día sin fecha: hora, minutos, segundos y microsegundos. Se usa poco en la práctica; suele aparecer al separar componentes de un `datetime` o al representar horarios recurrentes como "apertura a las 9:00".

`datetime` combina ambos: fecha + hora en un único objeto, representando un instante concreto. Es el tipo habitual en código profesional cuando se registra "cuándo ocurrió algo". Mezclar `date` y `datetime` lanza `TypeError` al comparar, así que hay que elegir con cuidado el tipo según lo que se modela.

### R2. ¿Qué es un `timedelta` y por qué no tiene campos de meses ni años?

`timedelta` representa una duración, una diferencia entre dos instantes. Sumarlo a un `datetime` da otro `datetime` desplazado; restar dos `datetime` da un `timedelta`. Admite días, horas, minutos, segundos, microsegundos y semanas, pero **no meses ni años** porque su longitud no es fija: un mes puede tener 28–31 días, un año puede tener 365 o 366. Sumar "un mes" es una operación ambigua — ¿el día equivalente del mes siguiente? ¿30 días? ¿el último día si el siguiente mes no tiene ese día? — y `timedelta` no asume ninguna.

Para aritmética con meses o años se usa `dateutil.relativedelta`, que permite especificar explícitamente la semántica deseada. Es una librería externa pero es el estándar de facto para este caso.

### R3. ¿Qué diferencia hay entre un `datetime` naive y uno aware?

Un `datetime` **aware** tiene información de zona horaria asociada (atributo `tzinfo` distinto de `None`). Un `datetime` **naive** no la tiene: representa "las 14:30 de algún sitio no especificado". Aware sabe en qué zona está y puede convertirse a otras; naive es ambiguo y requiere que el programador recuerde qué zona asume.

En la práctica, los naive son una fuente muy común de bugs. Comparar un naive con un aware lanza `TypeError`, y asumir que un naive es UTC (cuando en realidad era hora local, o al revés) produce errores silenciosos que pueden desplazar fechas por horas. La regla profesional es usar aware siempre que la fecha cruce sistemas o zonas horarias.

### R4. ¿Por qué se recomienda trabajar en UTC en el backend?

UTC es una referencia absoluta y estable: no tiene horario de verano, no cambia por decisiones políticas locales, y es la misma en todo el mundo. Si el backend guarda y opera en UTC, toda la aritmética de fechas es consistente independientemente de dónde esté el servidor, dónde estén los usuarios o cómo cambie la política local de cualquier país.

Las conversiones a zonas locales se hacen solo en la capa de presentación: al mostrar datos al usuario, se convierte a su zona; al recibir datos, se convierte inmediatamente a UTC al entrar al sistema. Este patrón — UTC internamente, local solo en los bordes — elimina casi todos los bugs de zona horaria.

### R5. ¿Cuál es la diferencia entre `time.time()` y `time.perf_counter()`?

`time.time()` devuelve el tiempo actual como segundos desde el epoch Unix. Es útil para timestamps, pero depende del reloj del sistema: si este se ajusta durante la medición (por NTP, cambio de zona horaria, horario de verano), los resultados pueden saltar o incluso ir hacia atrás.

`time.perf_counter()` usa el reloj monotónico más preciso del sistema y no se ve afectado por ajustes. Devuelve segundos también, pero su valor absoluto no tiene significado — solo sirve para medir intervalos restando dos lecturas. Es la opción correcta para benchmarks y cualquier medida precisa de duración. Usar `time.time()` para medir tiempos de ejecución es una mala práctica que sigue viéndose en muchos ejemplos antiguos.

### R6. ¿Qué hacen `strftime` y `strptime`?

`strftime` ("format time") convierte un `datetime` a string según un patrón con marcadores (`%Y`, `%m`, `%d`, etc.). `strptime` ("parse time") hace lo inverso: parsea un string según un formato explícito y devuelve un `datetime`. La `f` en `strftime` se asocia con "format" (formatear), la `p` en `strptime` con "parse" (analizar).

`strptime` lanza `ValueError` si el texto no encaja exactamente con el formato. Para inputs con variaciones es frágil; se recomienda fijar siempre el formato explícito o usar `dateutil.parser.parse` cuando el formato es desconocido. Los marcadores siguen la convención de C y hay que consultarlos casi siempre — pocos los recordamos todos.

### R7. ¿Por qué es buena práctica usar `isoformat` y `fromisoformat` cuando sea posible?

ISO 8601 (`YYYY-MM-DDTHH:MM:SS`) es el estándar internacional para representar fechas en texto. Es legible, inequívoco y, gracias al orden de los componentes, ordenable alfabéticamente (coincide con el orden cronológico). Es el formato de facto en APIs JSON y en bases de datos modernas.

`isoformat()` y `fromisoformat()` (desde Python 3.7, ampliado en 3.11) no requieren escribir patrones `strftime`: menos código, menos riesgo de errores de formato, mayor interoperabilidad. Para intercambio entre sistemas, ISO es la elección por defecto; los formatos locales como `DD/MM/YYYY` se reservan para presentar a usuarios humanos.

### R8. ¿Cómo se convierte un `datetime` aware entre zonas horarias?

Con el método `astimezone(otra_zona)`, que preserva el instante absoluto y cambia la representación a la nueva zona. Por ejemplo, las 14:30 UTC se convierten a 16:30 Madrid en verano (UTC+2) o 15:30 en invierno (UTC+1); es el mismo momento expresado en otra zona.

Desde Python 3.9, la forma recomendada de obtener zonas es `ZoneInfo` del módulo `zoneinfo`, que usa la base de datos IANA y gestiona correctamente DST y cambios históricos. Intentar `astimezone` sobre un datetime naive lanza `ValueError` porque no se sabe de qué zona partir. Este error es el típico al olvidar marcar como aware un datetime que venía de otro sistema.

### R9. ¿Por qué los objetos del módulo `datetime` son inmutables?

La inmutabilidad facilita razonar sobre el código: un `datetime` pasado como argumento no puede modificarse por la función receptora. Permite usarlos como claves de diccionario y elementos de conjunto, algo muy útil al indexar eventos por fecha. Además, hace trivial la comparación y el hashing.

Por consecuencia, cualquier operación que "modifique" una fecha devuelve un objeto nuevo: `replace`, `astimezone`, operaciones aritméticas con `timedelta`. En la práctica, esto lleva a código más claro y menos propenso a bugs que si los objetos fueran mutables.

### R10. ¿Qué problemas introduce el horario de verano (DST) al hacer aritmética con fechas?

El DST hace que ciertos días del año tengan 23 o 25 horas en lugar de 24, según si se adelanta o se atrasa el reloj. Esto rompe la intuición de que "sumar 24 horas equivale a al día siguiente a la misma hora". Justo el día del cambio, sumar `timedelta(hours=24)` puede dar un resultado con hora distinta del "mismo momento del día siguiente".

La recomendación para evitar este tipo de bug es hacer toda la aritmética en UTC (que no tiene DST) y convertir a la zona local solo al mostrar. Si por fuerza hay que hacer aritmética en zona local, se usa `ZoneInfo` con `astimezone` después de cada operación para normalizar la representación. Las librerías como `dateutil.relativedelta` también tienen en cuenta DST correctamente al usar `months=1`, `years=1`, etc.
