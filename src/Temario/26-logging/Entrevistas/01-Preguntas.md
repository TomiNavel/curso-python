# Preguntas de Entrevista: Logging

1. ¿Por qué es mejor usar `logging` que `print` en código de producción?
2. ¿Qué significa cada nivel (DEBUG, INFO, WARNING, ERROR, CRITICAL) y cuándo usarlos?
3. ¿Qué diferencia hay entre un logger, un handler y un formatter?
4. ¿Por qué se recomienda usar `logging.getLogger(__name__)` en cada módulo?
5. ¿Qué problema tiene `basicConfig` al llamarse más de una vez?
6. ¿Qué hace `logger.exception` y cuándo se usa?
7. ¿Por qué los loggers forman una jerarquía por nombre con puntos?
8. ¿Es buena idea configurar handlers dentro de cada módulo de la aplicación?
9. ¿Qué diferencia hay entre `StreamHandler` y `FileHandler`?
10. ¿Cómo se configura el logging desde un archivo externo?

---

### R1. ¿Por qué es mejor usar `logging` que `print` en código de producción?

`logging` añade automáticamente contexto que `print` no tiene: timestamp, nivel de gravedad, nombre del logger (que normalmente identifica el módulo). Además permite dirigir los mensajes a distintos destinos (consola, archivo, servicios externos) y filtrar por nivel sin tocar el código que emite — basta con cambiar la configuración.

El punto más práctico es el filtrado. En producción se quiere ver WARNING o peor; cuando hay un problema, se sube el nivel a DEBUG para diagnosticar. Con `print`, toda la verbosidad está siempre activa o hay que tocar código para silenciarla. Otro beneficio crítico: `logging.exception` incluye el traceback completo de la excepción actual, lo que con `print(e)` solo muestra el mensaje y se pierde información valiosa de diagnóstico.

### R2. ¿Qué significa cada nivel (DEBUG, INFO, WARNING, ERROR, CRITICAL) y cuándo usarlos?

DEBUG es información detallada útil solo al diagnosticar problemas; normalmente no se muestra en producción. INFO describe operaciones normales del sistema: usuario autenticado, pedido procesado, arranque completado. WARNING señala algo inesperado pero manejable, como un reintento tras fallo, una configuración deprecada, un caché vacío que se regenerará. ERROR indica que una operación ha fallado y no se ha completado — un pago rechazado, un archivo que no se pudo guardar. CRITICAL es un fallo grave que compromete la aplicación entera: base de datos caída, servicio externo esencial inaccesible.

La regla práctica es que los niveles reflejan **acciones**: WARNING pide revisar, ERROR pide investigar, CRITICAL exige respuesta inmediata. Usar CRITICAL para un error recuperable o INFO para un evento importante rompe las expectativas del equipo que monitoriza los logs.

### R3. ¿Qué diferencia hay entre un logger, un handler y un formatter?

El **logger** es quien emite los mensajes; es el objeto que el código invoca (`logger.info(...)`). Los mensajes llegan a uno o varios **handlers**, que deciden qué hacer con ellos: escribir a consola, a archivo, enviar por red, rotar archivos. Cada handler tiene su propio nivel y su propio **formatter**, que convierte el registro log en texto.

Esta separación en tres capas permite configuraciones sofisticadas con poca fricción: un mismo logger envía a varios handlers, cada uno con su nivel y formato. Por ejemplo, consola con mensajes cortos y archivo con timestamps completos. Es la diferencia entre "añadir un nuevo destino" (añadir handler) y "cambiar cómo se formatean los logs existentes" (tocar un formatter), que son operaciones independientes.

### R4. ¿Por qué se recomienda usar `logging.getLogger(__name__)` en cada módulo?

`__name__` contiene el nombre del módulo (`app.pagos.tarjetas`), así que el logger hereda la jerarquía del proyecto automáticamente. En los logs aparece de dónde viene cada mensaje sin tener que etiquetarlos a mano, y se puede configurar el nivel de todo un subsistema modificando un único logger (por ejemplo, DEBUG solo para `app.pagos`).

El contraste es con `logging.info(...)` directo o `getLogger("miapp")`. El primero siempre usa el logger raíz, perdiendo contexto. El segundo funciona pero fuerza un nombre arbitrario en lugar de reflejar la estructura real del código. El patrón `getLogger(__name__)` es la convención en todos los proyectos profesionales y se espera en cualquier entrevista.

### R5. ¿Qué problema tiene `basicConfig` al llamarse más de una vez?

Por defecto, `basicConfig` **se ignora silenciosamente** si el logger raíz ya tiene handlers configurados. No lanza warning ni error: simplemente no hace nada. Esto despista: alguien cambia el nivel o el formato y aparentemente no surte efecto porque otra parte del código llamó a `basicConfig` antes.

Desde Python 3.8 existe el parámetro `force=True`, que elimina los handlers previos antes de aplicar la nueva configuración. Para escenarios dinámicos (tests, notebooks, reconfiguración durante el arranque) es imprescindible. Sin `force`, la solución es manipular `logging.root.handlers` a mano o diseñar el código para que `basicConfig` solo se llame una vez, en el punto de entrada.

### R6. ¿Qué hace `logger.exception` y cuándo se usa?

`logger.exception(mensaje)` emite un log a nivel ERROR **incluyendo el traceback completo de la excepción actual**. Solo tiene sentido llamarlo desde dentro de un bloque `except`, porque consulta internamente la excepción en curso. Equivale a `logger.error(mensaje, exc_info=True)`.

Es la forma correcta de registrar errores capturados. Sin el traceback, un "error al procesar el pedido" ayuda poco al diagnóstico; con traceback, se identifica exactamente qué línea, qué tipo de excepción y qué cadena de llamadas la produjo. Sustituir `print(e)` por `logger.exception(...)` es una mejora enorme con esfuerzo mínimo.

### R7. ¿Por qué los loggers forman una jerarquía por nombre con puntos?

La jerarquía permite configurar el logging por zonas. Si tengo `app.pagos`, `app.pagos.tarjetas`, `app.pagos.transferencias` y configuro `app.pagos` en nivel DEBUG, todos sus descendientes heredan ese nivel. Puedo diagnosticar un problema en pagos sin activar DEBUG en toda la aplicación.

Además de herencia de nivel, por defecto los logs de un logger se **propagan** hacia sus ancestros, así que los handlers configurados en `app` o en el logger raíz reciben los mensajes de cualquier descendiente. Este modelo refleja la estructura lógica del proyecto: el logging se configura de arriba hacia abajo, y las partes concretas solo emiten mensajes.

### R8. ¿Es buena idea configurar handlers dentro de cada módulo de la aplicación?

No. Los módulos deben **emitir** logs con `getLogger(__name__)` pero no configurar handlers. La configuración se hace una única vez, en el punto de entrada de la aplicación. Así, cambiar el formato o añadir un destino afecta a todo el sistema desde un único sitio.

Configurar handlers en módulos tiene dos problemas: si el módulo se importa dos veces (o en tests), los handlers se duplican y los mensajes salen repetidos; y si el usuario del módulo (por ejemplo, una librería externa que importa el módulo) quiere dirigir los logs a otro sitio, no puede. La regla profesional es que **las librerías nunca configuran handlers**; solo los emiten. La aplicación final es la que configura.

### R9. ¿Qué diferencia hay entre `StreamHandler` y `FileHandler`?

`StreamHandler` escribe a cualquier stream (por defecto `stderr`, pero se puede pasar otro como `sys.stdout` o un `StringIO`). Es lo que usa `basicConfig` internamente. `FileHandler` es un caso especializado que abre un archivo en modo append y escribe cada log como una línea. Acepta `encoding` y el modo de apertura.

Para producción se prefieren los handlers rotativos: `RotatingFileHandler` cierra el archivo cuando alcanza un tamaño y abre otro, manteniendo un histórico acotado; `TimedRotatingFileHandler` rota por intervalo de tiempo. Evitan que un archivo de log crezca indefinidamente y llene el disco. Existen también handlers para syslog, correo, HTTP y servicios externos como ELK; todos heredan la misma interfaz básica.

### R10. ¿Cómo se configura el logging desde un archivo externo?

Con `logging.config.dictConfig(diccionario)` o `logging.config.fileConfig(ruta)`. El primero acepta un diccionario (normalmente cargado de YAML o JSON) con la configuración completa de loggers, handlers y formatters. Es la forma recomendada en aplicaciones modernas.

Poner la configuración en un archivo externo permite cambiar el logging sin redesplegar código: distintos archivos para desarrollo, staging y producción. Al arrancar, la app lee el archivo según el entorno y configura todo de un tirón. Este patrón es el estándar en frameworks web (Django, FastAPI) y en aplicaciones empresariales, y mencionarlo en una entrevista demuestra familiaridad con el despliegue real.
