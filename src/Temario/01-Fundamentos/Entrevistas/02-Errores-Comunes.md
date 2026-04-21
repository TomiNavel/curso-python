# 1. Fundamentos de Python — Errores Comunes

## E1. Usar `==` en lugar de `is` para comparar con None

```python
# MAL
if resultado == None:
    print("sin resultado")

# BIEN
if resultado is None:
    print("sin resultado")
```

`==` invoca el método `__eq__` del objeto, que puede estar sobreescrito y devolver resultados inesperados. `is` compara identidad de objeto directamente — como `None` es un singleton, `is None` siempre es correcto. PEP 8 lo exige explícitamente.

## E2. Comparar floats con `==`

```python
# MAL — devuelve False por imprecisión de punto flotante
if 0.1 + 0.2 == 0.3:
    print("iguales")

# BIEN
import math
if math.isclose(0.1 + 0.2, 0.3):
    print("iguales")
```

Los floats IEEE 754 no pueden representar ciertos decimales de forma exacta. Comparar con `==` falla silenciosamente. Usar `math.isclose()` para comparaciones, o `decimal.Decimal` para cálculos financieros.

## E3. Confiar en `is` para comparar valores

```python
# MAL — funciona por casualidad con enteros pequeños
a = 256
b = 256
if a is b:  # True, pero solo porque Python cachea -5 a 256
    print("iguales")

a = 257
b = 257
if a is b:  # False — el mismo código falla con otro número
    print("iguales")

# BIEN — usar == para comparar valores
if a == b:
    print("iguales")
```

`is` compara identidad (mismo objeto en memoria), no valor. Que funcione con enteros pequeños es un detalle de implementación, no un comportamiento garantizado.

## E4. Mezclar espacios y tabulaciones

```python
# MAL — lanza TabError en Python 3
if True:
    print("con espacios")
	print("con tabulación")  # TabError

# BIEN — siempre 4 espacios, configurar el editor para convertir tabs en espacios
if True:
    print("con espacios")
    print("con espacios")
```

Python 3 no permite mezclar espacios y tabulaciones en el mismo bloque. Configurar el editor para insertar 4 espacios al pulsar Tab.

## E5. Asumir que `int()` redondea

```python
# MAL — esperar redondeo
x = int(3.9)
print(x)  # 3, no 4 — int() trunca, no redondea

# BIEN — usar round() para redondear
x = round(3.9)
print(x)  # 4
```

`int()` siempre trunca hacia cero (elimina la parte decimal). Para redondeo estándar se usa `round()`.

## E6. No entender el cortocircuito de `or`

```python
# MAL — esperar que valor sea siempre un bool
valor = 0 or "por defecto"
print(valor)  # "por defecto" — 0 es falsy, se evalúa el segundo operando

# Esto es un problema si 0 es un valor válido
cantidad = 0
cantidad = cantidad or 10
print(cantidad)  # 10 — se perdió el 0 porque es falsy
```

`or` devuelve el primer valor truthy. Si `0`, `""` o `[]` son valores válidos en tu contexto, no se puede usar `or` como valor por defecto — hay que comprobar explícitamente con `is None`.

```python
# BIEN — comprobar None explícitamente
cantidad = 0
if cantidad is None:
    cantidad = 10
print(cantidad)  # 0 — se preserva el valor
```

## E7. Usar nombres que colisionan con builtins

```python
# MAL — sobrescribe la función built-in list()
list = [1, 2, 3]
# Ahora list() no funciona:
list("abc")  # TypeError: 'list' object is not callable

# MAL — sobrescribe type(), id(), input(), etc.
type = "admin"
id = 42

# BIEN — usar nombres descriptivos o añadir sufijo
user_list = [1, 2, 3]
user_type = "admin"
user_id = 42
```

Python permite reasignar cualquier nombre, incluyendo funciones built-in. No hay error ni advertencia — simplemente dejan de funcionar. Los más comunes: `list`, `dict`, `type`, `id`, `input`, `str`, `int`.

## E8. Confundir `=` con `==` en condicionales

```python
# MAL — en Python esto es un SyntaxError (a diferencia de C/Java)
if x = 5:       # SyntaxError: invalid syntax
    print(x)

# BIEN
if x == 5:
    print(x)
```

Python no permite asignación dentro de un `if` con `=` (a diferencia de C, donde `if (x = 5)` es válido y fuente de bugs). Esto es una protección deliberada del lenguaje. Desde Python 3.8 existe el operador walrus `:=` para asignación dentro de expresiones, pero es un tema posterior.

## E9. No usar f-strings cuando se concatena con `+`

```python
# MAL — verboso y propenso a errores de tipo
nombre = "Ana"
edad = 28
mensaje = "Hola, " + nombre + ". Tienes " + str(edad) + " años."

# BIEN — f-string, más legible y sin necesidad de convertir tipos
mensaje = f"Hola, {nombre}. Tienes {edad} años."
```

La concatenación con `+` requiere que todos los operandos sean strings (hay que convertir con `str()`). Los f-strings manejan la conversión automáticamente y son más legibles.
