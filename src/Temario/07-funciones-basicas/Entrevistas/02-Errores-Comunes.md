# Errores Comunes: Funciones Básicas

## Error 1: Confundir `print()` con `return`

```python
# MAL — la función imprime pero no devuelve nada
def calcular_total(precio, cantidad):
    print(precio * cantidad)

total = calcular_total(10, 3)  # Imprime 30
print(total)                    # None — no se puede usar el resultado

# BIEN — devuelve el valor para que el código que llama pueda usarlo
def calcular_total(precio, cantidad):
    return precio * cantidad

total = calcular_total(10, 3)  # No imprime nada
print(total)                    # 30 — ahora sí se puede usar
```

Es el error más común de principiantes. Una función con `print()` muestra el valor en la consola pero no lo devuelve. Si el resultado se necesita para cualquier otra operación (asignar a variable, pasar a otra función, usar en una expresión), se debe usar `return`.

---

## Error 2: Usar una lista como valor por defecto

```python
# MAL — la lista se comparte entre todas las llamadas
def agregar(item, lista=[]):
    lista.append(item)
    return lista

print(agregar("a"))  # ['a']
print(agregar("b"))  # ['a', 'b'] — acumula de llamadas anteriores

# BIEN — crear la lista nueva en cada llamada
def agregar(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

El valor por defecto se evalúa una sola vez (cuando se define la función), no en cada llamada. Con objetos mutables esto produce acumulación inesperada entre llamadas.

---

## Error 3: Olvidar los paréntesis al llamar a una función

```python
def obtener_saludo():
    return "Hola, mundo"

# MAL — sin paréntesis, es una referencia a la función, no una llamada
mensaje = obtener_saludo
print(mensaje)  # <function obtener_saludo at 0x...>

# BIEN — con paréntesis, se ejecuta la función
mensaje = obtener_saludo()
print(mensaje)  # "Hola, mundo"
```

Sin paréntesis, la variable recibe el objeto función en sí, no el resultado de ejecutarla. Es un error silencioso porque no lanza ninguna excepción.

---

## Error 4: Poner argumentos posicionales después de los de nombre

```python
# MAL — SyntaxError
def perfil(nombre, edad, ciudad):
    print(f"{nombre}, {edad}, {ciudad}")

perfil(nombre="Ana", 28, "Madrid")

# BIEN — posicionales primero, por nombre después
perfil("Ana", edad=28, ciudad="Madrid")
```

Python exige que todos los argumentos posicionales vayan antes de los argumentos por nombre. Mezclarlos en otro orden produce un `SyntaxError`.

---

## Error 5: Parámetros con defecto antes de los sin defecto

```python
# MAL — SyntaxError
def saludar(saludo="Hola", nombre):
    print(f"{saludo}, {nombre}")

# BIEN — parámetros sin defecto primero
def saludar(nombre, saludo="Hola"):
    print(f"{saludo}, {nombre}")
```

Python requiere que los parámetros con valor por defecto vayan después de los que no lo tienen. Si se invierte el orden, no hay forma de determinar qué argumento posicional corresponde a cada parámetro.

---

## Error 6: Código después de `return` (código muerto)

```python
# MAL — la línea después de return nunca se ejecuta
def calcular(a, b):
    return a + b
    print("Cálculo completado")  # Código muerto

# BIEN — todo el código necesario va antes del return
def calcular(a, b):
    resultado = a + b
    print("Cálculo completado")
    return resultado
```

`return` termina la ejecución de la función inmediatamente. Cualquier código que venga después es inalcanzable. Algunos IDEs marcan esto como advertencia, pero Python no lanza error.

---

## Error 7: Modificar la lista original dentro de una función

```python
# MAL — efecto secundario: modifica la lista del código que llamó
def ordenar_nombres(nombres):
    nombres.sort()
    return nombres

mis_nombres = ["Pedro", "Ana", "Luis"]
resultado = ordenar_nombres(mis_nombres)
print(mis_nombres)  # ['Ana', 'Luis', 'Pedro'] — ¡la original cambió!

# BIEN — no modifica la original
def ordenar_nombres(nombres):
    return sorted(nombres)

mis_nombres = ["Pedro", "Ana", "Luis"]
resultado = ordenar_nombres(mis_nombres)
print(mis_nombres)  # ['Pedro', 'Ana', 'Luis'] — intacta
```

Las listas se pasan por referencia. Si una función usa `.sort()`, `.append()` o cualquier método que modifique in-place, está alterando la lista original. Si no es la intención, hay que trabajar con una copia o usar funciones que devuelvan un nuevo objeto.

---

## Error 8: No asignar el resultado de `return` a una variable

```python
def sumar(a, b):
    return a + b

# MAL — llama a la función pero descarta el resultado
sumar(3, 5)

# BIEN — almacena el resultado para usarlo
resultado = sumar(3, 5)
print(resultado)  # 8
```

Si una función devuelve un valor con `return` y no se asigna a una variable ni se usa en una expresión, el valor se pierde. La función se ejecuta, pero su resultado no se aprovecha.

---

## Error 9: Confundir `*args` con una lista

```python
def procesar(*args):
    # MAL — intentar usar métodos de lista
    args.append("nuevo")  # AttributeError: tuple has no attribute 'append'

    # BIEN — args es una TUPLA, no una lista
    print(type(args))  # <class 'tuple'>
    lista = list(args)  # Convertir a lista si se necesita modificar
    lista.append("nuevo")
```

`*args` recoge los argumentos en una **tupla**, que es inmutable. Si se necesita modificar los datos, hay que convertirla a lista primero.

---

## Error 10: Desempaquetar con número incorrecto de variables

```python
def obtener_datos():
    return "Ana", 28, "Madrid"

# MAL — ValueError: not enough values to unpack
nombre, edad = obtener_datos()

# MAL — ValueError: too many values to unpack
nombre, edad, ciudad, pais = obtener_datos()

# BIEN — el número de variables debe coincidir
nombre, edad, ciudad = obtener_datos()
```

Al desempaquetar el retorno múltiple de una función, el número de variables del lado izquierdo debe coincidir exactamente con el número de valores retornados. Si no coincide, Python lanza un `ValueError`.

---

## Error 11: Pasar argumentos por nombre a parámetros solo posicionales

```python
def potencia(base, exponente, /):
    return base ** exponente

# MAL — TypeError
potencia(base=2, exponente=10)

# BIEN — solo por posición
potencia(2, 10)
```

Los parámetros antes de `/` no aceptan argumentos por nombre. Este error aparece con frecuencia al usar funciones de la biblioteca estándar que tienen parámetros solo posicionales (como `len(obj, /)`).
