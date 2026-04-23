# 26. Logging

El logging es la disciplina de dejar rastro de lo que hace un programa mientras se ejecuta. En desarrollo, los `print` sirven para depurar; en producción no: cuando algo falla a las tres de la mañana en un servidor al que no puedes entrar, lo único que tienes son los logs. Un sistema con logging bien diseñado se diagnostica en minutos; uno sin logs obliga a reproducir el problema a ciegas.

En entrevistas es un tema práctico: no requiere memorizar APIs complejas, pero sí tener criterio sobre qué registrar, con qué nivel y dónde enviarlo. La diferencia entre alguien que ha trabajado con sistemas reales y alguien que solo ha escrito scripts se nota rápidamente al hablar de logs.

## 26.1. El módulo logging

Python ofrece `logging` en la biblioteca estándar. Es potente y flexible — quizá demasiado flexible: configurarlo mal es fácil. La clave es entender tres conceptos que colaboran: **logger** (quién emite), **handler** (hacia dónde), **formatter** (cómo se ve). Para empezar, `basicConfig` hace todo esto de un plumazo con valores razonables.

### 26.1.1. Por qué logging en lugar de print

`print` parece suficiente hasta que el código crece. Los problemas aparecen uno a uno: los prints van siempre a stdout, no se pueden silenciar sin tocar código, no tienen timestamp, no indican gravedad, no identifican qué módulo los emitió. En un sistema con varios servicios, leer logs hechos a base de prints es un ejercicio de arqueología.

`logging` resuelve todo eso. Un mensaje `logger.info("usuario creado")` lleva automáticamente timestamp, nivel, nombre del logger, y puede dirigirse a consola, archivo, syslog o servicios externos — todo configurable desde fuera del código. Lo más importante es que los logs tienen **niveles**: puedes pedir al sistema "solo WARNING o peor" sin modificar una sola línea del código que emite. Un `print` nunca se calla.

Otra ventaja crítica: en producción se reconfigura el logging sin redesplegar. Cambiar el nivel de verbosidad para diagnosticar un problema es una operación de configuración; con prints habría que cambiar código y hacer release.

### 26.1.2. Niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Los cinco niveles estándar representan la gravedad del evento:

- **DEBUG**: información detallada para diagnóstico. No se suele mostrar en producción.
- **INFO**: operaciones normales del sistema. "Usuario X se ha autenticado", "Pedido Y procesado".
- **WARNING**: algo inesperado pero manejable. "Reintento tras fallo de red", "Configuración deprecada".
- **ERROR**: algo ha fallado y una operación no ha completado. "No se pudo procesar el pago".
- **CRITICAL**: fallo grave que puede comprometer la aplicación. "Base de datos inaccesible".

Cada nivel incluye los anteriores en gravedad. Configurar el logger en `WARNING` significa que WARNING, ERROR y CRITICAL se emiten; DEBUG e INFO se descartan silenciosamente.

```python
import logging

logging.debug("detalle de depuración")      # normalmente oculto
logging.info("operación completada")
logging.warning("conexión lenta")
logging.error("no se pudo guardar")
logging.critical("base de datos caída")
```

La elección del nivel es donde se aplica criterio profesional. Un error recuperable no es CRITICAL; un estado de arranque no es WARNING. En entrevistas, explicar cuándo usarías cada nivel demuestra que has lidiado con sistemas reales, no solo con ejemplos de laboratorio.

### 26.1.3. Configuración básica (basicConfig)

`logging.basicConfig()` configura el sistema con un handler que escribe a stderr con un formato por defecto. Acepta parámetros para cambiar nivel, formato y destino:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("sistema arrancado")
# 2026-04-22 10:15:32 - INFO - root - sistema arrancado
```

Los marcadores del `format` son atributos del registro log:

- `%(asctime)s`: timestamp formateado.
- `%(levelname)s`: nombre del nivel (INFO, WARNING...).
- `%(name)s`: nombre del logger.
- `%(message)s`: el mensaje.
- `%(module)s`: módulo desde donde se emitió.
- `%(lineno)d`: línea del código.

`basicConfig` solo tiene efecto **si no hay handlers configurados todavía**. Si se llama dos veces, la segunda se ignora sin warning. Este detalle sorprende al principio: modificar la configuración después de arrancar requiere manipular los handlers a mano.

Para scripts y aplicaciones pequeñas, `basicConfig` es suficiente. Para sistemas con requisitos de varios destinos (archivo + consola + servicio externo), se configuran handlers y formatters explícitamente, como veremos a continuación.

## 26.2. Handlers y formatters

Un logger emite registros; quién decide qué hacer con ellos son los **handlers**. Un handler puede escribir a consola, a archivo, rotar archivos por tamaño, enviar por correo, publicar en un servicio externo. Cada handler tiene su propio nivel y su propio formatter, así que un mismo logger puede producir una salida breve en consola y otra detallada en un archivo.

### 26.2.1. StreamHandler y FileHandler

`StreamHandler` escribe a un stream (por defecto `stderr`). Es lo que usa `basicConfig` internamente. `FileHandler` escribe a un archivo:

```python
import logging

logger = logging.getLogger("miapp")
logger.setLevel(logging.DEBUG)

consola = logging.StreamHandler()
consola.setLevel(logging.INFO)

archivo = logging.FileHandler("app.log", encoding="utf-8")
archivo.setLevel(logging.DEBUG)

logger.addHandler(consola)
logger.addHandler(archivo)
```

Con esta configuración, DEBUG e INFO van al archivo, pero solo INFO y superiores aparecen en consola. El patrón "archivo detallado + consola resumida" es el más habitual en servicios productivos: los operadores ven en consola lo relevante, y el archivo guarda todo para diagnóstico posterior.

Para logs de producción se suelen usar handlers más avanzados: `RotatingFileHandler` (rota por tamaño), `TimedRotatingFileHandler` (rota por tiempo), o handlers que envían a servicios externos como ELK o Loki. Todos heredan de la misma jerarquía y se configuran igual.

### 26.2.2. Formateo de mensajes (Formatter)

Un `Formatter` define cómo se convierte cada registro en texto. Se aplica al handler, no al logger, lo que permite distintos formatos para distintos destinos:

```python
import logging

formato_consola = logging.Formatter("%(levelname)s: %(message)s")
formato_archivo = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

consola.setFormatter(formato_consola)
archivo.setFormatter(formato_archivo)
```

En consola interesa brevedad ("ERROR: no se pudo guardar"); en archivo, contexto completo (timestamp, módulo, nivel). Separar el formato por destino es una de las razones para salir de `basicConfig` y configurar handlers a mano.

Un marcador muy útil es `%(exc_info)s` combinado con `logger.error(..., exc_info=True)` o `logger.exception(...)`, que incluye el traceback completo de la excepción actual en el log. Sin eso, "se lanzó un ValueError" ayuda poco; con traceback, el diagnóstico es inmediato.

### 26.2.3. Múltiples handlers

Un logger puede tener varios handlers, y cada uno decide qué hacer independientemente. El patrón típico en aplicaciones reales es tres destinos:

1. **Consola** (StreamHandler): nivel INFO, formato corto, para operación diaria.
2. **Archivo general** (RotatingFileHandler): nivel INFO, formato completo, para auditoría.
3. **Archivo de errores** (FileHandler, level=ERROR): solo errores, para revisión rápida.

```python
logger = logging.getLogger("miapp")
logger.setLevel(logging.DEBUG)

for handler in [consola, archivo_general, archivo_errores]:
    logger.addHandler(handler)
```

Los handlers no filtran mensajes del logger, sino que cada uno los recibe todos y decide según su propio nivel si los procesa. Esto es la base de configuraciones flexibles: el logger emite al nivel más bajo posible, y los handlers recortan para cada destino.

## 26.3. Loggers jerárquicos

Los loggers no son objetos sueltos: forman una **jerarquía** basada en sus nombres separados por puntos. El logger `app.pagos.tarjetas` desciende de `app.pagos`, que desciende de `app`, que desciende del logger raíz. La jerarquía controla dos cosas: qué nivel se aplica (se hereda del ancestro si no se define localmente) y por qué handlers pasan los registros (se propagan hacia arriba por defecto).

### 26.3.1. getLogger() y jerarquía por nombre

`logging.getLogger(nombre)` devuelve el logger con ese nombre, creándolo si no existe. El patrón profesional es usar `__name__` como nombre del logger en cada módulo:

```python
# en app/pagos/tarjetas.py
import logging

logger = logging.getLogger(__name__)   # nombre = "app.pagos.tarjetas"

def cobrar(usuario, importe):
    logger.info(f"cobro iniciado para {usuario}")
```

Con este patrón, cada módulo tiene su propio logger automáticamente y la jerarquía refleja la estructura del proyecto. Configurando el logger `app.pagos` en nivel DEBUG se activan los debug de tarjetas, cuentas y cualquier submódulo de pagos, sin tocar otras partes del sistema.

Una práctica importante: **no se configuran handlers en los loggers de cada módulo**. Los módulos solo emiten logs con `getLogger(__name__)`; la configuración de handlers se hace una sola vez, en el punto de entrada de la aplicación, sobre el logger raíz o uno principal.

### 26.3.2. Logging en aplicaciones con múltiples módulos

La arquitectura recomendada separa tres responsabilidades:

- **Módulos individuales**: obtienen su logger con `logging.getLogger(__name__)` y emiten mensajes. No configuran nada.
- **Punto de entrada de la aplicación**: configura handlers, formatters y niveles una vez al arrancar.
- **Librerías**: emiten en sus propios loggers sin configurar handlers; dejan que quien las use decida qué hacer con sus logs.

```python
# main.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def main():
    setup_logging()
    # importar y ejecutar los módulos de la app
    ...

if __name__ == "__main__":
    main()
```

Con esta estructura, cambiar el formato o añadir un handler afecta a toda la aplicación desde un único punto. Los módulos no necesitan saber nada de cómo se configuran los logs; solo los emiten.

En aplicaciones grandes, la configuración suele leerse de un archivo YAML o JSON con `logging.config.dictConfig`, permitiendo distintos perfiles (desarrollo, staging, producción) sin cambiar código. Es el patrón estándar en proyectos profesionales, y mencionarlo en una entrevista demuestra familiaridad con sistemas de verdad.
