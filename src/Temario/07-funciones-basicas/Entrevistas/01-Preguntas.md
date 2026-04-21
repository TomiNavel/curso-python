# Preguntas de Entrevista: Funciones Básicas

1. ¿Cuál es la diferencia entre un parámetro y un argumento?
2. ¿Qué diferencia hay entre `print()` y `return` dentro de una función?
3. ¿Qué devuelve una función que no tiene `return`?
4. ¿Qué son los argumentos posicionales y los argumentos por nombre (keyword)? ¿Se pueden mezclar?
5. ¿Por qué no se deben usar objetos mutables como valores por defecto en los parámetros de una función?
6. ¿Qué es `*args` y para qué sirve?
7. ¿Qué es `**kwargs` y en qué se diferencia de `*args`?
8. ¿Cuál es el orden obligatorio de los parámetros cuando se combinan normales, `*args` y `**kwargs`?
9. ¿Qué significa que las funciones en Python son objetos de primera clase?
10. ¿Para qué sirve un docstring y en qué se diferencia de un comentario?
11. ¿Qué hace el operador `*` cuando se usa al llamar a una función, no al definirla?
12. ¿Qué es el retorno múltiple en Python? ¿Qué tipo de dato devuelve realmente?
13. ¿Por qué es importante que una función haga una sola cosa?
14. ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)` cuando se usan dentro de una función?
15. ¿Qué ocurre si llamas a una función con más argumentos posicionales de los que acepta?
16. ¿Qué significa el `/` en la firma de una función? ¿Y el `*`?

---

### R1. ¿Cuál es la diferencia entre un parámetro y un argumento?

Un **parámetro** es la variable que aparece en la definición de la función. Un **argumento** es el valor concreto que se pasa al llamarla.

```python
def saludar(nombre):   # "nombre" es el parámetro
    print(f"Hola, {nombre}")

saludar("Ana")         # "Ana" es el argumento
```

En la práctica se usan como sinónimos, pero la distinción importa para entender la documentación oficial y comunicarse con precisión en una entrevista.

### R2. ¿Qué diferencia hay entre `print()` y `return` dentro de una función?

`print()` muestra un valor en la consola como efecto secundario, pero la función no devuelve ese valor. `return` devuelve el valor al código que llamó a la función, donde se puede almacenar en una variable, usar en una expresión o pasar a otra función.

```python
def con_print(n):
    print(n * 2)

def con_return(n):
    return n * 2

resultado = con_print(5)   # Imprime 10, pero resultado es None
resultado = con_return(5)  # No imprime nada, pero resultado es 10
```

### R3. ¿Qué devuelve una función que no tiene `return`?

Devuelve `None` implícitamente. Lo mismo ocurre si tiene `return` sin valor (`return` a secas). Este comportamiento es importante porque si se intenta operar con el resultado de una función que no retorna nada, se estará trabajando con `None`.

### R4. ¿Qué son los argumentos posicionales y los argumentos por nombre (keyword)? ¿Se pueden mezclar?

Los **posicionales** se asignan según su orden en la llamada. Los **de nombre** se asignan explícitamente con `parametro=valor`, por lo que su orden no importa.

Se pueden mezclar, pero los posicionales deben ir **antes** que los de nombre:

```python
def perfil(nombre, edad, ciudad):
    print(f"{nombre}, {edad}, {ciudad}")

# Mixto — correcto
perfil("Ana", ciudad="Madrid", edad=28)

# MAL — SyntaxError: positional argument follows keyword argument
perfil(nombre="Ana", 28, "Madrid")
```

### R5. ¿Por qué no se deben usar objetos mutables como valores por defecto en los parámetros de una función?

Porque el objeto por defecto se crea **una sola vez** cuando se define la función, no en cada llamada. Si es mutable (lista, diccionario, set), las modificaciones persisten entre llamadas:

```python
def agregar(item, lista=[]):
    lista.append(item)
    return lista

print(agregar("a"))  # ['a']
print(agregar("b"))  # ['a', 'b'] — la misma lista de la llamada anterior
```

La solución estándar es usar `None` como valor por defecto y crear el objeto mutable dentro de la función.

### R6. ¿Qué es `*args` y para qué sirve?

`*args` es un parámetro que recoge todos los argumentos posicionales adicionales en una **tupla**. Permite que una función acepte un número variable de argumentos sin definirlos uno a uno.

```python
def sumar(*args):
    total = 0
    for n in args:
        total += n
    return total

sumar(1, 2)        # 3
sumar(1, 2, 3, 4)  # 10
```

El nombre `args` es una convención; lo que importa es el `*`.

### R7. ¿Qué es `**kwargs` y en qué se diferencia de `*args`?

`**kwargs` recoge los argumentos **por nombre** adicionales en un **diccionario**, mientras que `*args` recoge los **posicionales** en una tupla.

```python
def mostrar(**kwargs):
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar(nombre="Ana", edad=28)
# nombre: Ana
# edad: 28
```

### R8. ¿Cuál es el orden obligatorio de los parámetros cuando se combinan normales, `*args` y `**kwargs`?

1. Parámetros normales (con o sin valor por defecto)
2. `*args`
3. `**kwargs`

```python
def funcion(obligatorio, opcional="x", *args, **kwargs):
    pass
```

Alterar este orden produce un `SyntaxError`.

### R9. ¿Qué significa que las funciones en Python son objetos de primera clase?

Significa que las funciones se pueden tratar como cualquier otro valor: asignarlas a variables, almacenarlas en listas o diccionarios, pasarlas como argumento a otras funciones y devolverlas como resultado de una función.

```python
def doble(n):
    return n * 2

operacion = doble          # Asignar a variable
print(operacion(5))        # 10
print(type(operacion))     # <class 'function'>
```

Este concepto es la base de patrones avanzados como callbacks, decoradores y funciones de orden superior.

### R10. ¿Para qué sirve un docstring y en qué se diferencia de un comentario?

Un docstring es un string literal que se coloca como primera sentencia del cuerpo de una función. Documenta qué hace la función, qué recibe y qué devuelve. A diferencia de un comentario (`#`), Python lo almacena como atributo `__doc__` del objeto función y lo utilizan herramientas como `help()` y los IDEs para mostrar información contextual.

```python
def doble(n):
    """Devuelve el doble del número recibido."""
    return n * 2

print(doble.__doc__)  # "Devuelve el doble del número recibido."
```

### R11. ¿Qué hace el operador `*` cuando se usa al llamar a una función, no al definirla?

Al llamar a una función, `*` **desempaqueta** un iterable (lista, tupla) en argumentos posicionales individuales. De forma análoga, `**` desempaqueta un diccionario en argumentos por nombre:

```python
def sumar(a, b, c):
    return a + b + c

numeros = [1, 2, 3]
sumar(*numeros)    # Equivale a sumar(1, 2, 3)

datos = {"a": 1, "b": 2, "c": 3}
sumar(**datos)     # Equivale a sumar(a=1, b=2, c=3)
```

### R12. ¿Qué es el retorno múltiple en Python? ¿Qué tipo de dato devuelve realmente?

Cuando una función devuelve varios valores separados por comas, Python los empaqueta automáticamente en una **tupla**:

```python
def dividir(a, b):
    return a // b, a % b

resultado = dividir(17, 5)
print(resultado)        # (3, 2)
print(type(resultado))  # <class 'tuple'>

# Lo habitual es desempaquetar
cociente, resto = dividir(17, 5)
```

No existe un "retorno múltiple" como tal en Python; es simplemente retorno de una tupla con desempaquetado implícito.

### R13. ¿Por qué es importante que una función haga una sola cosa?

Porque una función con una sola responsabilidad es más fácil de entender, de probar, de depurar y de reutilizar. Si una función hace varias cosas, un cambio en una de ellas puede romper las demás. Además, funciones pequeñas y enfocadas se pueden componer para construir comportamientos complejos sin que cada pieza individual sea difícil de entender.

Una señal de que una función hace demasiado es necesitar un "y" para describirla: "esta función valida los datos **y** los guarda **y** envía un email".

### R14. ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)` cuando se usan dentro de una función?

`lista.sort()` modifica la lista original **in-place** y devuelve `None`. `sorted(lista)` crea y devuelve una lista **nueva** sin modificar la original.

Dentro de una función, esta diferencia es crítica: si la función recibe una lista como argumento y usa `.sort()`, está modificando la lista del código que la llamó (efecto secundario). Si usa `sorted()`, la lista original queda intacta.

```python
def obtener_ordenados(lista):
    return sorted(lista)  # No modifica la original — más seguro
```

### R15. ¿Qué ocurre si llamas a una función con más argumentos posicionales de los que acepta?

Python lanza un `TypeError` indicando que la función recibió más argumentos de los esperados:

```python
def sumar(a, b):
    return a + b

sumar(1, 2, 3)
# TypeError: sumar() takes 2 positional arguments but 3 were given
```

Si se necesita que la función acepte un número variable de argumentos, se puede usar `*args`.

### R16. ¿Qué significa el `/` en la firma de una función? ¿Y el `*`?

- `/` marca que los parámetros **anteriores** a él son **solo posicionales**: no se pueden pasar por nombre.
- `*` marca que los parámetros **posteriores** a él son **solo keyword**: deben pasarse por nombre obligatoriamente.

```python
def funcion(a, /, b, *, c):
    pass

funcion(1, 2, c=3)       # BIEN
funcion(1, b=2, c=3)     # BIEN
# funcion(a=1, b=2, c=3) # TypeError — a es solo posicional
# funcion(1, 2, 3)       # TypeError — c es solo keyword
```
