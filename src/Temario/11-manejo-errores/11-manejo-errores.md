# 11. Manejo de Errores y Excepciones

Cuando un programa se encuentra con una situación que no puede resolver — un archivo que no existe, una división entre cero, un tipo de dato inesperado — Python lanza una excepción. Si nadie la captura, el programa se detiene con un traceback. El manejo de excepciones permite interceptar estos errores, responder a ellos de forma controlada y, cuando es necesario, lanzar los propios. Es una herramienta fundamental para escribir programas robustos que no se rompen ante lo inesperado.

---

## 11.1. Excepciones en Python

### 11.1.1. Qué es una excepción

Una excepción es un objeto que Python crea automáticamente cuando ocurre un error durante la ejecución del programa. Este objeto contiene información sobre qué salió mal: el tipo de error, un mensaje descriptivo y el traceback (la cadena de llamadas que llevó al error).

Cuando se lanza una excepción, Python interrumpe el flujo normal del programa y busca un manejador (`except`) que pueda capturarla. Si no encuentra ninguno en la función actual, sube al contexto que la llamó, y así sucesivamente. Si ningún contexto la captura, el programa termina mostrando el traceback.

```python
# Python crea una excepción automáticamente al encontrar un error
numero = int("abc")  # ValueError: invalid literal for int() with base 10: 'abc'

# El traceback muestra la cadena de llamadas hasta el error
# Traceback (most recent call last):
#   File "ejemplo.py", line 1, in <module>
#     numero = int("abc")
# ValueError: invalid literal for int() with base 10: 'abc'
```

Es importante distinguir entre errores de sintaxis y excepciones. Un `SyntaxError` ocurre antes de que el programa se ejecute — Python no puede compilar el código. Las excepciones ocurren durante la ejecución, cuando el código es sintácticamente correcto pero encuentra una situación imposible.

### 11.1.2. Jerarquía de excepciones (BaseException, Exception)

Todas las excepciones en Python forman un árbol organizado por niveles de generalidad. En la raíz está `BaseException`, el tipo más general. De ella se derivan todas las demás, y `Exception` es la base de todas las excepciones que un programa debería capturar. Los conceptos de clases y herencia que sustentan esta organización se estudiarán formalmente en los temas 13 y 15; por ahora basta con entender el árbol como un mapa de "quién es un tipo más concreto de quién".

```
BaseException
├── SystemExit            # sys.exit() — no capturar
├── KeyboardInterrupt     # Ctrl+C — no capturar
├── GeneratorExit         # cierre de generador — no capturar
└── Exception             # base de todas las excepciones "normales"
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    ├── AttributeError
    ├── FileNotFoundError
    ├── ZeroDivisionError
    ├── RuntimeError
    └── ...
```

La distinción es importante: `SystemExit`, `KeyboardInterrupt` y `GeneratorExit` se derivan directamente de `BaseException`, no de `Exception`. Esto significa que un `except Exception` no las captura, lo cual es correcto — no se debe impedir que `Ctrl+C` cierre el programa ni que `sys.exit()` funcione.

```python
# except Exception NO captura KeyboardInterrupt ni SystemExit
try:
    while True:
        pass
except Exception:
    # Ctrl+C NO entra aquí — sigue propagándose y el programa se detiene
    print("Esto no se ejecuta con Ctrl+C")

# except BaseException SÍ las captura (casi nunca se debe usar)
try:
    while True:
        pass
except BaseException:
    # Ctrl+C SÍ entra aquí — mala práctica
    print("Capturé hasta Ctrl+C")
```

### 11.1.3. Excepciones comunes

Estas son las excepciones que aparecen con más frecuencia en el día a día y en entrevistas:

**`TypeError`** — se usa un tipo incorrecto para una operación:

```python
"hola" + 5          # TypeError: can only concatenate str to str
len(42)             # TypeError: object of type 'int' has no len()
```

**`ValueError`** — el tipo es correcto pero el valor no es válido:

```python
int("abc")          # ValueError: invalid literal for int()
int("3.14")         # ValueError: invalid literal for int() with base 10
list.remove([], 5)  # ValueError: list.remove(x): x not in list
```

**`KeyError`** — se accede a una clave que no existe en un diccionario:

```python
datos = {"nombre": "Ana"}
datos["edad"]       # KeyError: 'edad'
```

**`IndexError`** — se accede a un índice fuera de rango:

```python
lista = [1, 2, 3]
lista[5]            # IndexError: list index out of range
```

**`AttributeError`** — se accede a un atributo que no existe:

```python
numero = 42
numero.append(3)    # AttributeError: 'int' object has no attribute 'append'
```

**`FileNotFoundError`** — se intenta abrir un archivo que no existe:

```python
open("no_existe.txt")  # FileNotFoundError: No such file or directory
```

**`ZeroDivisionError`** — división entre cero:

```python
10 / 0              # ZeroDivisionError: division by zero
```

**`NameError`** — se usa una variable que no está definida:

```python
print(variable_inexistente)  # NameError: name 'variable_inexistente' is not defined
```

**`UnboundLocalError`** — caso especial de `NameError` (visto en el tema 9):

```python
x = 10
def funcion():
    print(x)        # UnboundLocalError — Python ve x = ... más abajo
    x = 20          # y marca x como local en tiempo de compilación
```

---

## 11.2. try / except / else / finally

### 11.2.1. Sintaxis básica de try/except

El bloque `try/except` permite capturar excepciones y responder a ellas en lugar de dejar que el programa se detenga. El código que puede fallar va dentro del `try`, y la respuesta al error va dentro del `except`.

```python
try:
    numero = int(input("Ingresa un número: "))
    print(f"El doble es {numero * 2}")
except ValueError:
    print("Eso no es un número válido")
```

Cuando Python ejecuta el bloque `try`, si ocurre una excepción, salta inmediatamente al `except` correspondiente — el resto del `try` no se ejecuta. Si no ocurre ninguna excepción, el `except` se ignora.

Para acceder al mensaje de la excepción se usa `as`:

```python
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")  # Error: division by zero
    print(type(e))        # <class 'ZeroDivisionError'>
```

### 11.2.2. Capturar excepciones específicas

Siempre se deben capturar excepciones específicas, nunca un `except` genérico sin tipo. Capturar `Exception` a ciegas oculta errores reales y hace que los bugs sean difíciles de encontrar.

```python
# MAL — captura todo, incluso errores de programación
try:
    resultado = mi_funcion()
except:
    print("Algo salió mal")  # ¿Qué salió mal? No se sabe

# MAL — casi igual de malo, oculta TypeError, NameError, etc.
try:
    resultado = mi_funcion()
except Exception:
    print("Algo salió mal")

# BIEN — captura solo lo que se espera que pueda fallar
try:
    resultado = mi_funcion()
except ValueError:
    print("El valor no es válido")
```

La razón es simple: si se captura todo, un `TypeError` por un bug en el código (por ejemplo, pasar argumentos en orden incorrecto) se traga silenciosamente en lugar de revelar el problema.

### 11.2.3. Capturar múltiples excepciones

Se pueden capturar diferentes excepciones con diferentes respuestas, o agrupar varias en un solo `except`:

```python
# Respuestas diferentes para cada excepción
try:
    valor = datos[clave]
    numero = int(valor)
except KeyError:
    print(f"La clave '{clave}' no existe")
except ValueError:
    print(f"El valor '{valor}' no es un número")

# Misma respuesta para varias excepciones — tupla en el except
try:
    resultado = int(texto) / divisor
except (ValueError, ZeroDivisionError) as e:
    print(f"Operación inválida: {e}")
```

El orden importa cuando las excepciones tienen relación de herencia. Python usa el primer `except` que coincida, así que las excepciones más específicas deben ir antes de las más generales:

```python
# MAL — FileNotFoundError nunca se alcanza porque hereda de OSError
try:
    open("archivo.txt")
except OSError:
    print("Error de sistema")
except FileNotFoundError:  # nunca se ejecuta
    print("Archivo no encontrado")

# BIEN — la más específica primero
try:
    open("archivo.txt")
except FileNotFoundError:
    print("Archivo no encontrado")
except OSError:
    print("Otro error de sistema")
```

### 11.2.4. El bloque else

El bloque `else` se ejecuta solo si el `try` completo se ejecutó sin excepciones. Permite separar el código que puede fallar del código que depende de su éxito.

```python
try:
    numero = int(input("Número: "))
except ValueError:
    print("No es un número válido")
else:
    # Solo se ejecuta si int() no lanzó ValueError
    print(f"El cuadrado es {numero ** 2}")
```

La ventaja de `else` sobre poner más código dentro del `try` es que evita capturar excepciones que no se esperaban. Si el cálculo del cuadrado lanzara una excepción (por ejemplo, un `OverflowError`), no quedaría atrapada en el `except ValueError`.

```python
# Sin else — si procesar_datos() lanza ValueError, se captura por error
try:
    datos = cargar_archivo()
    resultado = procesar_datos(datos)  # este ValueError no debería capturarse
except ValueError:
    print("Archivo inválido")

# Con else — solo captura el ValueError de cargar_archivo()
try:
    datos = cargar_archivo()
except ValueError:
    print("Archivo inválido")
else:
    resultado = procesar_datos(datos)
```

### 11.2.5. El bloque finally

El bloque `finally` se ejecuta siempre, haya o no excepción, e incluso si hay un `return` dentro del `try` o del `except`. Se usa para limpieza de recursos: cerrar archivos, conexiones de red, liberar locks.

```python
archivo = None
try:
    archivo = open("datos.txt")
    contenido = archivo.read()
except FileNotFoundError:
    print("Archivo no encontrado")
finally:
    # Se ejecuta SIEMPRE — haya error o no
    if archivo:
        archivo.close()
        print("Archivo cerrado")
```

El `finally` se ejecuta incluso con `return`:

```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("Operación completada")  # se imprime SIEMPRE

dividir(10, 2)   # imprime "Operación completada", devuelve 5.0
dividir(10, 0)   # imprime "Operación completada", devuelve None
```

**Combinación completa `try/except/else/finally`:**

```python
try:
    resultado = operacion_riesgosa()
except TipoError:
    manejar_error()
else:
    # Solo si no hubo excepción
    usar_resultado(resultado)
finally:
    # SIEMPRE, pase lo que pase
    limpiar_recursos()
```

El orden de ejecución es: `try` → (si hay error) `except` → (si no hay error) `else` → (siempre) `finally`.

---

## 11.3. Lanzar excepciones

### 11.3.1. La sentencia raise

La sentencia `raise` permite lanzar excepciones manualmente. Se usa cuando el código detecta una condición inválida que no puede resolver — un argumento fuera de rango, un estado inconsistente, una precondición que no se cumple.

```python
def dividir(a, b):
    if b == 0:
        raise ValueError("El divisor no puede ser cero")
    return a / b

def calcular_edad(anio_nacimiento):
    if anio_nacimiento < 1900 or anio_nacimiento > 2026:
        raise ValueError(f"Año de nacimiento inválido: {anio_nacimiento}")
    return 2026 - anio_nacimiento
```

Siempre se lanza una instancia de una clase de excepción, nunca un string u otro tipo. El mensaje debe ser descriptivo — explicar qué está mal y, si es posible, incluir el valor que causó el problema.

```python
# MAL — mensaje genérico que no ayuda a diagnosticar
raise ValueError("valor inválido")

# BIEN — indica qué está mal y cuál es el valor
raise ValueError(f"La edad debe ser positiva, se recibió: {edad}")
```

Se puede lanzar una excepción sin argumento para relanzar la excepción actual:

```python
raise  # relanza la última excepción (solo dentro de un except)
```

### 11.3.2. Re-lanzar excepciones (raise sin argumento)

Dentro de un bloque `except`, se puede capturar una excepción, hacer algo con ella (por ejemplo, registrarla en un log) y luego relanzarla para que el código que llamó a esta función también la reciba.

```python
def procesar_archivo(ruta):
    try:
        with open(ruta) as f:
            return f.read()
    except FileNotFoundError:
        print(f"LOG: archivo no encontrado: {ruta}")
        raise  # relanza la MISMA excepción con su traceback original
```

El `raise` sin argumento preserva el traceback original, lo cual es fundamental para depuración. Si en lugar de `raise` se hiciera `raise FileNotFoundError(...)`, se perdería la información de dónde ocurrió el error originalmente.

**Encadenar excepciones con `raise ... from ...`:**

Cuando se quiere lanzar una excepción diferente pero manteniendo la referencia a la causa original:

```python
def cargar_configuracion(ruta):
    try:
        with open(ruta) as f:
            datos = f.read()
    except FileNotFoundError as e:
        # Lanza una excepción más descriptiva, encadenada a la original
        raise RuntimeError(f"No se pudo cargar la configuración: {ruta}") from e
```

El traceback mostrará ambas excepciones: la causa original (`FileNotFoundError`) y la nueva (`RuntimeError`), conectadas por el mensaje "The above exception was the direct cause of the following exception".

---

## 11.4. Excepciones personalizadas

### 11.4.1. Crear excepciones propias (herencia de Exception)

Python permite crear excepciones propias para representar errores específicos del dominio de la aplicación. La forma básica consiste en escribir una clase que herede de `Exception`. Los conceptos de clases y herencia se explican en detalle en los temas 13 y 15; por ahora basta con entender la siguiente línea como una receta: se declara un nombre nuevo para el error y se indica que es un tipo de excepción.

```python
class SaldoInsuficienteError(Exception):
    pass

class CuentaNoEncontradaError(Exception):
    pass

def retirar(cuenta, monto):
    if monto > cuenta["saldo"]:
        raise SaldoInsuficienteError(
            f"Saldo insuficiente: disponible {cuenta['saldo']}, solicitado {monto}"
        )
    cuenta["saldo"] -= monto
```

Con esta definición, `SaldoInsuficienteError` se comporta igual que cualquier otra excepción: puede lanzarse con `raise`, capturarse con `except` y recibe un mensaje descriptivo como argumento. La ventaja frente a usar un `ValueError` genérico es que el nombre del error comunica exactamente qué ha fallado, y quien captura la excepción puede distinguirla de otros errores sin inspeccionar el mensaje.

Una vez estudiados los temas 13 (Clases y Objetos) y 15 (Herencia), se podrán añadir atributos personalizados a las excepciones, construir jerarquías de errores para capturar a distintos niveles de granularidad y aprovechar al máximo este mecanismo.

### 11.4.2. Cuándo crear excepciones personalizadas

Las excepciones personalizadas se justifican cuando:

- **El error es específico del dominio** — `SaldoInsuficienteError` comunica mucho más que `ValueError("saldo insuficiente")`. Quien captura la excepción puede distinguirla de otros `ValueError` sin revisar el mensaje.
- **Se necesita distinguir entre errores distintos** — si una función puede fallar por motivos diferentes (saldo insuficiente, cuenta bloqueada, cuenta no encontrada), una excepción distinta para cada caso permite que el `except` reaccione de forma específica.

No se deben crear excepciones personalizadas cuando una excepción estándar comunica lo mismo: si el error es simplemente "el valor es inválido", un `ValueError` con un buen mensaje es suficiente.

---

## 11.5. Buenas prácticas

### 11.5.1. EAFP vs LBYL

Python favorece el estilo **EAFP** (*Easier to Ask Forgiveness than Permission*): intentar la operación y capturar la excepción si falla, en lugar de verificar todas las condiciones antes de actuar.

El estilo opuesto es **LBYL** (*Look Before You Leap*): verificar condiciones antes de ejecutar.

```python
# LBYL — verificar antes de actuar
if "clave" in diccionario:
    valor = diccionario["clave"]
else:
    valor = "por defecto"

# EAFP — intentar y capturar (estilo Pythónico)
try:
    valor = diccionario["clave"]
except KeyError:
    valor = "por defecto"
```

EAFP es preferido en Python por varias razones:

- **Evita condiciones de carrera** — entre la verificación y la acción, el estado puede cambiar (especialmente con archivos o recursos compartidos).
- **Es más eficiente cuando el caso exitoso es el más común** — el coste de entrar en un `try` sin excepción es casi nulo, mientras que la verificación previa se ejecuta siempre.
- **Es más legible** — el camino feliz está claro, y el manejo de error está separado.

Dicho esto, LBYL es adecuado cuando la verificación es barata y la excepción es costosa o común:

```python
# LBYL es razonable aquí — verificar el tipo antes de operar
if isinstance(valor, str):
    resultado = valor.upper()
```

En la práctica, Python ofrece mecanismos que combinan ambos estilos: `dict.get(clave, defecto)` evita tanto el `if` como el `try/except`.

### 11.5.2. No capturar Exception genérica

Ya se mencionó en la sección 11.2.2, pero merece énfasis como buena práctica: capturar `Exception` sin discriminar es uno de los errores más comunes y peligrosos.

```python
# PELIGROSO — oculta bugs reales
try:
    resultado = procesar(datos)
except Exception:
    resultado = None  # ¿Qué falló? TypeError, KeyError, un bug?

# CORRECTO — solo captura lo esperado
try:
    resultado = procesar(datos)
except (ValueError, KeyError) as e:
    print(f"Datos inválidos: {e}")
    resultado = None
```

La única situación donde capturar `Exception` es aceptable es en el nivel más alto de una aplicación (un servidor web, un bucle principal) donde se necesita que el programa no se detenga. Incluso en ese caso, se debe registrar la excepción completa para poder depurarla.

### 11.5.3. Mensajes de error descriptivos

Un buen mensaje de error reduce el tiempo de depuración de minutos a segundos. Debe responder tres preguntas: qué se esperaba, qué se recibió y, si es posible, dónde.

```python
# MAL
raise ValueError("valor inválido")

# BIEN
raise ValueError(f"Se esperaba un entero positivo, se recibió: {valor!r}")

# BIEN — incluye contexto
raise ValueError(
    f"El parámetro 'edad' debe estar entre 0 y 150, se recibió: {edad}"
)
```

El uso de `!r` (repr) en f-strings es útil para distinguir `""` (string vacío) de `None`, o `"42"` (string) de `42` (entero).

### 11.5.4. ExceptionGroup y except* (Python 3.11+)

Python 3.11 introdujo `ExceptionGroup`, que permite representar múltiples excepciones que ocurren simultáneamente (por ejemplo, en código concurrente donde varias tareas fallan al mismo tiempo). La sintaxis `except*` permite capturar excepciones específicas dentro del grupo.

```python
# ExceptionGroup agrupa varias excepciones
grupo = ExceptionGroup("errores de validación", [
    ValueError("campo 'nombre' vacío"),
    TypeError("campo 'edad' no es entero"),
    ValueError("campo 'email' formato inválido")
])

# except* captura por tipo dentro del grupo
try:
    raise grupo
except* ValueError as eg:
    print(f"Errores de valor: {eg.exceptions}")
    # (ValueError("campo 'nombre' vacío"), ValueError("campo 'email' formato inválido"))
except* TypeError as eg:
    print(f"Errores de tipo: {eg.exceptions}")
    # (TypeError("campo 'edad' no es entero"),)
```

La diferencia fundamental con `except` normal es que `except*` puede ejecutar múltiples ramas para el mismo `ExceptionGroup` — una para cada tipo de excepción presente en el grupo. Con `except` normal, solo se ejecuta una rama.

Esta funcionalidad es relevante en código asíncrono (tema avanzado) y en bibliotecas como `asyncio` que manejan tareas concurrentes. A nivel de entrevista, basta con saber que existe y para qué sirve.
