# Errores Comunes: Manejo de Errores y Excepciones

## Error 1: Capturar Exception genérica

```python
# MAL — oculta bugs reales (TypeError, NameError, etc.)
try:
    resultado = procesar(datos)
except Exception:
    resultado = None

# BIEN — capturar solo lo esperado
try:
    resultado = procesar(datos)
except (ValueError, KeyError) as e:
    print(f"Datos inválidos: {e}")
    resultado = None
```

El `except Exception` atrapa todo, incluyendo errores de programación que deberían ser visibles. Un `TypeError` por pasar argumentos incorrectos se silencia en lugar de revelar el bug. Capturar solo las excepciones que se esperan permite que los errores inesperados se propaguen y se detecten.

---

## Error 2: except sin tipo (bare except)

```python
# MAL — captura TODO, incluyendo KeyboardInterrupt y SystemExit
try:
    while True:
        datos = obtener_datos()
except:
    print("Error")  # Ctrl+C no cierra el programa

# BIEN
try:
    while True:
        datos = obtener_datos()
except ConnectionError:
    print("Error de conexión")
```

Un `except:` sin tipo captura `BaseException`, lo que incluye `KeyboardInterrupt` (Ctrl+C) y `SystemExit` (sys.exit). El programa se vuelve imposible de cerrar de forma normal.

---

## Error 3: No usar `as` para acceder al mensaje de error

```python
# MAL — se pierde la información del error
try:
    numero = int(texto)
except ValueError:
    print("Error de conversión")  # ¿qué texto falló?

# BIEN — incluir el mensaje original
try:
    numero = int(texto)
except ValueError as e:
    print(f"No se pudo convertir '{texto}': {e}")
```

Sin `as e`, no se puede acceder al mensaje de la excepción. Registrar el mensaje original ayuda a diagnosticar el problema sin tener que reproducirlo.

---

## Error 4: Código de más dentro del try

```python
# MAL — procesar() podría lanzar ValueError y quedaría atrapado
try:
    datos = cargar(ruta)
    resultado = procesar(datos)
    guardar(resultado)
except ValueError:
    print("Archivo con formato inválido")

# BIEN — solo proteger lo que puede fallar de la forma esperada
try:
    datos = cargar(ruta)
except ValueError:
    print("Archivo con formato inválido")
else:
    resultado = procesar(datos)
    guardar(resultado)
```

Si se mete demasiado código dentro del `try`, se capturan excepciones de líneas que no se pretendía proteger. El `else` permite ejecutar código que depende del éxito del `try` sin exponerlo al `except`.

---

## Error 5: Olvidar que finally siempre se ejecuta

```python
# MAL — el return del finally sobrescribe al del try
def obtener_dato():
    try:
        return "dato válido"
    except Exception:
        return None
    finally:
        return "sobreescrito"  # SIEMPRE se devuelve esto

obtener_dato()  # devuelve "sobreescrito", no "dato válido"
```

Un `return` dentro del `finally` sobrescribe cualquier `return` previo en `try` o `except`. Además, si el `try` lanzó una excepción, el `return` del `finally` la silencia — la excepción desaparece. El `finally` debe usarse solo para limpieza (cerrar archivos, conexiones), nunca para devolver valores.

---

## Error 6: Lanzar strings en lugar de excepciones

```python
# MAL — SyntaxError en Python 3, pero concepto erróneo común
raise "Algo salió mal"  # TypeError: exceptions must derive from BaseException

# MAL — mensaje genérico sin contexto
raise ValueError("error")

# BIEN — excepción tipada con mensaje descriptivo
raise ValueError(f"Se esperaba un entero positivo, se recibió: {valor!r}")
```

`raise` necesita una instancia de una clase que herede de `BaseException`. El mensaje debe incluir qué se esperaba, qué se recibió y, si es útil, el nombre del parámetro.

---

## Error 7: Orden incorrecto de except (genérico antes que específico)

```python
# MAL — FileNotFoundError es un tipo de OSError, nunca se alcanza
try:
    archivo = open("datos.txt")
except OSError:
    print("Error de sistema")
except FileNotFoundError:
    print("Archivo no encontrado")  # código muerto

# BIEN — la más específica primero
try:
    archivo = open("datos.txt")
except FileNotFoundError:
    print("Archivo no encontrado")
except OSError:
    print("Otro error de sistema")
```

Python usa el primer `except` que coincida. `FileNotFoundError` es un tipo más concreto de `OSError`, así que `except OSError` también la captura. Si la excepción general va primero, la específica nunca se ejecuta. Las excepciones más específicas deben ir siempre antes de las más generales.

---

## Error 8: Usar try/except para control de flujo normal

```python
# MAL — usar excepciones como if/else
def buscar_usuario(usuarios, nombre):
    try:
        for u in usuarios:
            if u["nombre"] == nombre:
                return u
            raise ValueError  # lanza excepción como señal de "no encontrado"
    except ValueError:
        return None

# BIEN — usar control de flujo normal
def buscar_usuario(usuarios, nombre):
    for u in usuarios:
        if u["nombre"] == nombre:
            return u
    return None
```

Las excepciones son para situaciones excepcionales, no para flujo normal. Usar `raise` como sustituto de `return None` o de un `if/else` hace el código más difícil de leer y más lento.

---

## Error 9: Silenciar excepciones sin registrarlas

```python
# MAL — el error desaparece sin dejar rastro
try:
    resultado = operacion_critica()
except OperationError:
    pass  # silencio total

# BIEN — al menos registrar el error
import logging

try:
    resultado = operacion_critica()
except OperationError as e:
    logging.error(f"Operación falló: {e}")
    resultado = valor_por_defecto
```

`except: pass` es uno de los antipatrones más peligrosos. Si algo falla, no hay forma de saberlo. Incluso si la excepción es esperada y la recuperación es válida, se debe registrar el evento para poder investigar si ocurre con frecuencia.

---

## Error 10: No usar `raise` sin argumento para relanzar

```python
# MAL — se pierde el traceback original
try:
    resultado = operacion()
except ValueError as e:
    registrar_error(e)
    raise ValueError(str(e))  # traceback nuevo, se pierde el contexto original

# BIEN — relanzar la misma excepción con su traceback
try:
    resultado = operacion()
except ValueError:
    registrar_error(e)
    raise  # preserva el traceback completo
```

Crear una nueva excepción con `raise ValueError(...)` genera un traceback nuevo que empieza en esa línea, perdiendo la información de dónde ocurrió el error originalmente. `raise` sin argumento preserva el traceback completo.
