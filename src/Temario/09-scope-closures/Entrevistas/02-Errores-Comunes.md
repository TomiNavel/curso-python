# Errores Comunes: Scope y Closures

## Error 1: UnboundLocalError por asignación posterior

```python
x = 10

def funcion():
    print(x)  # UnboundLocalError
    x = 20

funcion()
```

Python decide el scope en **tiempo de compilación**. Al ver `x = 20` dentro de la función, marca `x` como local en toda la función, incluso antes de la línea de asignación. Cuando `print(x)` se ejecuta, la variable local existe pero no tiene valor.

**Solución**: si se necesita leer la global y luego reasignar, usar `global x`. Si no se necesita reasignar, simplemente no hacer la asignación dentro de la función.

---

## Error 2: Usar `global` en lugar de pasar argumentos

```python
# MAL — estado oculto, difícil de testear
resultado = []

def agregar_item(item):
    global resultado
    resultado.append(item)

# BIEN — explícito y predecible
def agregar_item(lista, item):
    lista.append(item)
    return lista

resultado = []
agregar_item(resultado, "nuevo")
```

`global` crea dependencias ocultas: para entender qué hace la función hay que buscar variables definidas en otro lugar del archivo. Pasar los datos como argumentos hace que la función sea autocontenida y testeable.

---

## Error 3: Intentar usar `nonlocal` sin función contenedora

```python
x = 10

def funcion():
    nonlocal x  # SyntaxError: no binding for nonlocal 'x' found
    x += 1
```

`nonlocal` solo funciona para variables del scope Enclosing (una función que contiene a la actual). No sirve para variables globales — para eso existe `global`.

```python
# BIEN — nonlocal con función contenedora
def externa():
    x = 10
    def interna():
        nonlocal x
        x += 1
    interna()
    print(x)  # 11
```

---

## Error 4: Creer que el closure captura el valor en el momento de la definición

```python
def crear():
    x = 1
    def leer():
        return x
    x = 99  # se modifica después de definir leer()
    return leer

print(crear()())  # 99, no 1
```

El closure captura una **referencia** a la variable, no una copia de su valor. El valor que devuelve es el que tiene la variable en el momento de la **llamada**, no de la definición. Este comportamiento sorprende a quienes vienen de lenguajes donde los closures capturan valores.

---

## Error 5: Late binding en bucles (la trampa del for + lambda)

```python
# MAL — todas las funciones devuelven 4
funciones = []
for i in range(5):
    funciones.append(lambda: i)

print([f() for f in funciones])  # [4, 4, 4, 4, 4]
```

Las cinco lambdas capturan la misma variable `i`. Cuando el bucle termina, `i` vale 4 y todas leen ese valor.

```python
# BIEN — capturar el valor con argumento por defecto
funciones = []
for i in range(5):
    funciones.append(lambda i=i: i)

print([f() for f in funciones])  # [0, 1, 2, 3, 4]
```

El parámetro `i=i` se evalúa en el momento de la definición, creando una copia independiente del valor para cada lambda. Este es probablemente el error más preguntado en entrevistas sobre closures.

---

## Error 6: Confundir función anidada con closure

```python
def externa():
    def interna():
        return 42
    return interna

f = externa()
print(f.__closure__)  # None — NO es un closure
```

No toda función anidada es un closure. Si la función interna no referencia ninguna variable del scope de la externa, no hay nada que capturar. Es una función anidada común, no un closure.

```python
# Esto SÍ es un closure — captura 'x'
def externa(x):
    def interna():
        return x
    return interna

f = externa(10)
print(f.__closure__[0].cell_contents)  # 10
```

---

## Error 7: Ocultar nombres built-in con variables

```python
# MAL — oculta la función built-in list
list = [1, 2, 3]
print(list("abc"))  # TypeError: 'list' object is not callable

# MAL — oculta la función built-in print
print = "hola"
print("mundo")  # TypeError: 'str' object is not callable
```

Al asignar un valor a un nombre que coincide con un built-in, la variable global oculta el nombre del scope Built-in (regla LEGB: Global se busca antes que Built-in). Nombres que se ocultan con frecuencia: `list`, `dict`, `str`, `type`, `id`, `input`, `sum`, `max`, `min`.

```python
# Para restaurar un built-in ocultado
del list  # elimina la variable global, el built-in vuelve a ser visible
```

---

## Error 8: Mutar un objeto capturado creyendo que es inmutable

```python
def crear_acumulador():
    total = 0
    def agregar(valor):
        total += valor  # UnboundLocalError
        return total
    return agregar
```

`total += valor` es una asignación (`total = total + valor`), lo que hace que Python marque `total` como local en `agregar()`. Al intentar leer `total` para sumarle `valor`, la variable local no tiene valor todavía.

```python
# Solución 1 — nonlocal
def crear_acumulador():
    total = 0
    def agregar(valor):
        nonlocal total
        total += valor
        return total
    return agregar

# Solución 2 — usar un contenedor mutable (lista)
def crear_acumulador():
    total = [0]  # la lista es mutable, no se reasigna
    def agregar(valor):
        total[0] += valor  # muta el contenido, no reasigna total
        return total[0]
    return agregar
```

La solución con `nonlocal` es más clara. La solución con lista funciona porque `total[0] += valor` muta el contenido de la lista sin reasignar la variable `total` en sí.

---

## Error 9: Creer que `global` dentro de una función anidada apunta al scope enclosing

```python
x = "global"

def externa():
    x = "enclosing"

    def interna():
        global x
        x = "cambiado"

    interna()
    print(x)  # "enclosing" — la x de externa() no cambió

externa()
print(x)  # "cambiado" — global modificó la x del módulo
```

`global` siempre apunta al scope del módulo, sin importar cuántos niveles de anidamiento haya. Para modificar la variable de la función contenedora, se debe usar `nonlocal`.

---

## Error 10: Crear closures innecesarios cuando una clase o `functools.partial` serían más claros

```python
# Closure que empieza a ser difícil de seguir
def crear_procesador(formato, precision, moneda):
    def procesar(cantidad):
        if formato == "simple":
            return f"{cantidad:.{precision}f} {moneda}"
        elif formato == "completo":
            return f"Total: {cantidad:.{precision}f} {moneda} (IVA incluido)"
    return procesar

# Más claro con una clase si el estado crece
class Procesador:
    def __init__(self, formato, precision, moneda):
        self.formato = formato
        self.precision = precision
        self.moneda = moneda

    def procesar(self, cantidad):
        if self.formato == "simple":
            return f"{cantidad:.{self.precision}f} {self.moneda}"
        elif self.formato == "completo":
            return f"Total: {cantidad:.{self.precision}f} {self.moneda} (IVA incluido)"
```

Los closures son ideales para funciones simples con poco estado capturado. Cuando la lógica crece o se necesitan múltiples métodos, una clase es más mantenible y explícita.
