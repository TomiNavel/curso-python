# Errores Comunes: Logging

## Error 1. Usar `print` en código que va a producción

El print debugging es útil en desarrollo, pero dejarlo en código que va a producción ensucia la salida estándar, no se puede filtrar y pierde información contextual.

```python
# MAL: print en código productivo
def procesar(pedido):
    print(f"procesando pedido {pedido.id}")
    ...

# BIEN: logger con nivel apropiado
logger = logging.getLogger(__name__)

def procesar(pedido):
    logger.info(f"procesando pedido {pedido.id}")
    ...
```

El logger se silencia en producción si el nivel está en WARNING, incluye timestamp y módulo, y puede dirigirse a cualquier destino sin tocar código.

---

## Error 2. Llamar a `basicConfig` más de una vez sin `force=True`

`basicConfig` se ignora silenciosamente si ya hay handlers en el logger raíz. Código que parece reconfigurar el logging simplemente no hace nada.

```python
# MAL: la segunda llamada no tiene efecto, el nivel DEBUG no se aplica
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)   # ignorada

# BIEN: force=True elimina handlers previos antes de aplicar
logging.basicConfig(level=logging.DEBUG, force=True)
```

Desde Python 3.8, `force=True` resuelve el problema. Sin él, el diseño correcto es llamar a `basicConfig` una sola vez en el arranque.

---

## Error 3. Usar `logging.info(...)` directo en lugar de un logger por módulo

`logging.info(...)` usa siempre el logger raíz, perdiendo la información del módulo y la capacidad de filtrar por zonas del código.

```python
# MAL: pierde el nombre del módulo en el log
import logging
logging.info("pedido creado")

# BIEN: el nombre del módulo queda reflejado en el log
logger = logging.getLogger(__name__)
logger.info("pedido creado")
```

El patrón profesional es declarar `logger = logging.getLogger(__name__)` al inicio de cada módulo y usarlo siempre, nunca las funciones del módulo `logging`.

---

## Error 4. Loggear errores con `logger.error(e)` en lugar de `logger.exception`

`logger.error(e)` solo registra el mensaje de la excepción, perdiendo el traceback que identifica dónde y por qué se produjo.

```python
try:
    procesar(pedido)
except Exception as e:
    # MAL: solo muestra "division by zero", sin traceback
    logger.error(e)

    # BIEN: incluye traceback completo
    logger.exception("error procesando pedido")
```

`logger.exception` solo funciona dentro de un bloque except (consulta la excepción activa). Para cualquier error capturado, es la opción correcta.

---

## Error 5. Configurar handlers en módulos de librería

Si una librería añade handlers al logger, sobrescribe las decisiones de configuración del usuario y puede duplicar mensajes.

```python
# MAL: una librería NO debería hacer esto
# dentro de milibreria/__init__.py
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# BIEN: la librería solo emite; la aplicación configura
logger = logging.getLogger(__name__)
# ... usar logger.info, logger.warning, etc.
```

La librería emite logs con su propio nombre. La aplicación final decide qué hacer con ellos. Para silenciar por defecto a las librerías, Python añade un `NullHandler` por convención al logger raíz de la librería.

---

## Error 6. Concatenar strings en el mensaje en lugar de usar `%s` o f-strings

Construir el mensaje con concatenación o f-string se evalúa siempre, aunque el log vaya a descartarse por nivel.

```python
# MAL: el f-string se construye aunque el log esté descartado
logger.debug(f"procesando datos: {datos_muy_grandes.to_dict()}")

# BIEN: con formato estilo %, el argumento solo se convierte si el log pasa
logger.debug("procesando datos: %s", datos_muy_grandes.to_dict())
```

En casos con construcción costosa del argumento, el estilo `%s` evita trabajo inútil cuando el nivel filtra el mensaje. Para mensajes simples, los f-strings son más legibles y la ganancia es marginal; el criterio profesional es usar `%s` solo cuando el argumento es caro de construir.

---

## Error 7. No poner `exc_info=True` al loggear errores fuera de `except`

Si quieres incluir la excepción actual pero usas `error` en lugar de `exception`, hay que pasar explícitamente `exc_info=True`.

```python
try:
    procesar(pedido)
except Exception:
    # MAL: solo el mensaje
    logger.error("fallo procesando")

    # BIEN: con traceback
    logger.error("fallo procesando", exc_info=True)

    # MEJOR: logger.exception hace lo mismo de forma idiomática
    logger.exception("fallo procesando")
```

`logger.exception` es el patrón correcto; `logger.error(..., exc_info=True)` funciona igual pero se usa cuando quieres un nivel distinto (por ejemplo, `logger.warning(..., exc_info=True)`).

---

## Error 8. Loggear información sensible (contraseñas, tokens, datos personales)

Los logs suelen ir a archivos, servicios externos o ELK centralizados. Información sensible allí puede convertirse en un problema de seguridad y de cumplimiento legal (GDPR).

```python
# MAL: expone credenciales en logs
logger.info(f"login de {usuario} con contraseña {contraseña}")
logger.debug(f"petición con headers {headers}")   # token puede venir en Authorization

# BIEN: solo lo necesario
logger.info(f"login de {usuario}")
logger.debug(f"petición con headers redactados")
```

La regla es asumir que los logs los puede leer más gente de la esperada. En proyectos regulados hay que definir qué campos se pueden loggear y aplicar redacción automática a los sensibles.

---

## Error 9. Niveles mal elegidos que generan ruido o falsos negativos

Registrar eventos normales como WARNING satura los logs y hace imposible detectar problemas reales. Registrar fallos como INFO los oculta.

```python
# MAL: abuso de WARNING para cosas que no son warnings
def validar_edad(edad):
    if edad < 18:
        logger.warning(f"usuario menor: {edad}")   # no es warning, es lógica de negocio

# BIEN: INFO para operación normal, WARNING solo si algo inesperado pasa
    if edad < 18:
        logger.info(f"usuario menor: {edad}")
```

Los equipos de operaciones suelen configurar alertas cuando aparecen muchos WARNING. Si la mitad son ruido, las alertas dejan de tener valor. La elección de nivel es una decisión de diseño que requiere criterio.

---

## Error 10. Dejar que los logs crezcan indefinidamente

Un `FileHandler` simple escribe sin límite. Un servicio activo puede generar gigabytes al día y llenar el disco.

```python
# MAL: archivo que crece sin parar
handler = logging.FileHandler("app.log")

# BIEN: rotación por tamaño (5 archivos de 10MB)
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=5)
```

`RotatingFileHandler` y `TimedRotatingFileHandler` son los patrones estándar en producción. En infraestructuras con gestor de logs centralizado (ELK, Loki, CloudWatch), los archivos locales se leen y se borran por el agente del gestor, pero aun así es buena idea limitar el tamaño local.
