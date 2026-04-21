# Errores Comunes: Context Managers

## 1. Olvidar el `try/finally` en `@contextmanager`

Sin `try/finally`, el código de limpieza posterior al `yield` no se ejecuta si hay una excepción en el bloque `with`.

```python
# MAL: si el bloque with lanza excepción, la limpieza no ocurre
@contextmanager
def recurso():
    print("Adquiriendo")
    yield
    print("Liberando")  # Nunca se ejecuta si hay excepción

# BIEN: try/finally garantiza la limpieza
@contextmanager
def recurso():
    print("Adquiriendo")
    try:
        yield
    finally:
        print("Liberando")  # Se ejecuta siempre
```

---

## 2. Devolver `True` desde `__exit__` sin intención

Si `__exit__` devuelve un valor truthy por accidente, las excepciones se suprimen silenciosamente. Esto puede ocultar errores reales.

```python
# MAL: devuelve la cadena (truthy), suprime TODAS las excepciones
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cerrar()
    return "cerrado"  # Truthy: suprime excepciones

# BIEN: devolver False o None explícitamente
def __exit__(self, exc_type, exc_val, exc_tb):
    self.cerrar()
    return False
```

---

## 3. Confundir el valor de retorno de `__enter__` con `self`

`__enter__` puede devolver cualquier objeto. Si no devuelve nada (retorna `None`), la variable `as` será `None`, no el context manager.

```python
# MAL: __enter__ no devuelve nada, variable es None
class Gestor:
    def __enter__(self):
        self.conectar()
        # No hay return → devuelve None

    def __exit__(self, *args):
        self.desconectar()

with Gestor() as g:
    g.hacer_algo()  # AttributeError: 'NoneType' has no attribute 'hacer_algo'

# BIEN: devolver self
class Gestor:
    def __enter__(self):
        self.conectar()
        return self  # La variable as apunta al propio objeto
```

---

## 4. Usar `with` sin `as` cuando se necesita la referencia

Omitir `as` cuando se necesita operar con el recurso dentro del bloque.

```python
# MAL: no se puede acceder al archivo
with open("datos.txt"):
    contenido = ???  # No hay variable para leer

# BIEN: capturar la referencia con as
with open("datos.txt") as f:
    contenido = f.read()
```

---

## 5. Intentar reutilizar un context manager basado en `@contextmanager`

Un generador solo puede recorrerse una vez. Intentar usar el mismo objeto generador en dos bloques `with` falla.

```python
@contextmanager
def recurso():
    print("Abriendo")
    try:
        yield "datos"
    finally:
        print("Cerrando")

# MAL: guardar el resultado de la llamada e intentar usarlo dos veces
cm = recurso()
with cm as r:
    print(r)  # Funciona

with cm as r:  # RuntimeError: generator didn't yield
    print(r)

# BIEN: llamar a la función cada vez para crear un generador nuevo
with recurso() as r:
    print(r)

with recurso() as r:
    print(r)
```

---

## 6. No cerrar recursos manualmente si no se usa `with`

Asignar el resultado de `open()` a una variable sin `with` y olvidar llamar a `close()`. El recurso queda abierto hasta que el recolector de basura lo libere.

```python
# MAL: el archivo puede quedar abierto indefinidamente
f = open("datos.txt")
contenido = f.read()
# f.close() olvidado — si hay excepción antes, nunca se cierra

# BIEN: usar with
with open("datos.txt") as f:
    contenido = f.read()
```

---

## 7. Suprimir excepciones demasiado amplias con `suppress`

Usar `suppress(Exception)` o tipos demasiado genéricos oculta errores que deberían detectarse.

```python
# MAL: oculta CUALQUIER excepción, incluidos errores de programación
with suppress(Exception):
    resultado = int(datos["valor"])  # KeyError y ValueError se ocultan

# BIEN: suprimir solo la excepción específica esperada
with suppress(KeyError):
    resultado = datos["valor"]
```

---

## 8. Poner el `yield` fuera de `try` en `@contextmanager` cuando hay limpieza

Si el `yield` está dentro del `try` pero la limpieza está en un `except` en lugar de `finally`, la limpieza solo ocurre cuando hay error, no en el camino normal.

```python
# MAL: la limpieza solo ocurre si hay excepción
@contextmanager
def recurso():
    print("Abriendo")
    try:
        yield
    except Exception:
        print("Cerrando")  # Solo se ejecuta si hay error

# BIEN: usar finally para limpiar siempre
@contextmanager
def recurso():
    print("Abriendo")
    try:
        yield
    finally:
        print("Cerrando")  # Se ejecuta siempre
```

---

## 9. Asumir que `__exit__` no se llama si hay excepción en `__enter__`

Si `__enter__` lanza una excepción, `__exit__` no se ejecuta. Los recursos adquiridos parcialmente dentro de `__enter__` deben limpiarse dentro del propio `__enter__`.

```python
# MAL: si paso_2 falla, paso_1 nunca se limpia
class Gestor:
    def __enter__(self):
        self.paso_1()  # Adquiere recurso A
        self.paso_2()  # Falla → __exit__ NO se llama → recurso A queda abierto
        return self

    def __exit__(self, *args):
        self.limpiar_paso_2()
        self.limpiar_paso_1()

# BIEN: limpiar dentro de __enter__ si hay fallo parcial
class Gestor:
    def __enter__(self):
        self.paso_1()
        try:
            self.paso_2()
        except:
            self.limpiar_paso_1()
            raise
        return self
```

---

## 10. Anidar `with` innecesariamente cuando se pueden agrupar

Usar bloques `with` anidados cuando una sola sentencia con comas es más clara y produce menos indentación.

```python
# INNECESARIO: tres niveles de indentación
with open("entrada.txt") as entrada:
    with open("salida.txt", "w") as salida:
        with open("log.txt", "a") as log:
            # Código con triple indentación

# MEJOR: agrupar en una sentencia (Python 3.10+ con paréntesis)
with (
    open("entrada.txt") as entrada,
    open("salida.txt", "w") as salida,
    open("log.txt", "a") as log,
):
    # Código con una sola indentación
```
