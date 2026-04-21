# Cheat Sheet: Funciones y Scope (Temas 7-9)

## 1. Definicion de funciones

```python
def nombre(param1, param2):
    """Docstring: descripcion breve."""
    return resultado

# Sin return o return sin valor -> devuelve None
# Retorno multiple (devuelve tupla)
def dividir(a, b):
    return a // b, a % b

cociente, resto = dividir(17, 5)
```

## 2. Parametros y argumentos

```python
# Posicionales y keyword
def saludo(nombre, mensaje="Hola"):    # mensaje tiene valor por defecto
    return f"{mensaje}, {nombre}"

saludo("Ana")                          # posicional
saludo(nombre="Ana")                   # keyword
saludo("Ana", mensaje="Hey")           # mixto

# *args: argumentos posicionales variables (tupla)
def sumar(*args):
    return sum(args)

sumar(1, 2, 3)                         # args = (1, 2, 3)

# **kwargs: argumentos keyword variables (dict)
def config(**kwargs):
    return kwargs

config(host="localhost", port=8080)    # kwargs = {"host": "localhost", "port": 8080}

# Orden obligatorio de parametros
def f(requerido, defecto=0, *args, **kwargs):
    ...

# Desempaquetado en la llamada
lista = [1, 2, 3]
diccionario = {"a": 10}
funcion(*lista, **diccionario)
```

### Parametros solo posicionales y solo keyword

```python
# Solo posicionales (antes de /)  — Python 3.8+
def f(a, b, /):
    ...
f(1, 2)          # OK
f(a=1, b=2)      # ERROR

# Solo keyword (despues de *)
def f(*, a, b):
    ...
f(a=1, b=2)      # OK
f(1, 2)           # ERROR

# Combinacion completa
def f(pos_only, /, normal, *, kw_only):
    ...
```

### Valores por defecto mutables

```python
# MAL: el default mutable se comparte entre llamadas
def agregar(elemento, lista=[]):
    lista.append(elemento)
    return lista

# BIEN: usar None como centinela
def agregar(elemento, lista=None):
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista
```

## 3. Funciones como objetos

```python
# Asignar a variable (sin parentesis)
f = len
f("hola")                              # 4

# En estructuras de datos
operaciones = {"+": lambda a, b: a + b, "-": lambda a, b: a - b}
operaciones["+"](3, 5)                 # 8

# Como argumento
def aplicar(func, valor):
    return func(valor)

aplicar(str.upper, "hola")             # "HOLA"

# key en sorted, max, min
sorted(nombres, key=len)
sorted(personas, key=lambda p: p["edad"])
max(datos, key=lambda x: x[1])
```

## 4. Lambda

```python
# Sintaxis: lambda parametros: expresion
doble = lambda x: x * 2                # evitar esto (asignar lambda)

# Uso correcto: inline, sin asignar
sorted(lista, key=lambda x: x.lower())
filter(lambda x: x > 0, numeros)
map(lambda x: x ** 2, numeros)

# Ternario dentro de lambda
lambda n: "par" if n % 2 == 0 else "impar"

# Limitaciones: solo UNA expresion, sin bloques, sin return explicito
```

## 5. Funciones de orden superior

```python
# map(func, iterable) -> iterador
list(map(str.upper, ["a", "b"]))       # ["A", "B"]

# filter(func, iterable) -> iterador (elementos donde func es truthy)
list(filter(lambda x: x > 0, [-1, 2, -3, 4]))   # [2, 4]

# sorted(iterable, key=func, reverse=bool) -> nueva lista
sorted(palabras, key=len, reverse=True)

# Preferir comprehensions sobre map/filter
[x ** 2 for x in numeros]                         # en vez de map
[x for x in numeros if x > 0]                     # en vez de filter
```

## 6. Recursion

```python
# Estructura: caso base + caso recursivo
def factorial(n):
    if n <= 1:                          # caso base
        return 1
    return n * factorial(n - 1)         # caso recursivo

# Aplanar lista anidada
def aplanar(lista):
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado
```

## 7. Built-in utiles

```python
isinstance(obj, tipo)        # verificar tipo (acepta tupla de tipos)
callable(obj)                # True si es invocable

any(iterable)                # True si al menos uno es truthy
all(iterable)                # True si todos son truthy
# Ambas hacen cortocircuito (se detienen temprano)

any(x > 10 for x in datos)  # con generator expression
all(len(s) > 0 for s in textos)
```

## 8. Scope (LEGB)

```python
# Orden de busqueda de variables:
# 1. Local     — dentro de la funcion actual
# 2. Enclosing — en la funcion contenedora (funciones anidadas)
# 3. Global    — a nivel de modulo
# 4. Built-in  — nombres predefinidos de Python (len, print, etc.)

# Python decide el scope en tiempo de COMPILACION:
# si una variable se asigna en cualquier parte de una funcion, es local en TODA la funcion

x = 10                       # global

def f():
    print(x)                 # lee la global (no hay asignacion local)

def g():
    x = 20                   # crea una LOCAL, no modifica la global
```

### global y nonlocal

```python
# global: modificar variable de modulo desde dentro de una funcion
contador = 0
def incrementar():
    global contador
    contador += 1

# nonlocal: modificar variable de la funcion contenedora
def externa():
    x = 0
    def interna():
        nonlocal x
        x += 1
    interna()
    return x                 # 1

# Evitar global siempre que sea posible
# Preferir: pasar como argumento y devolver con return
```

## 9. Closures

```python
# Un closure se forma cuando:
# 1. Hay una funcion anidada
# 2. La funcion anidada referencia variables del scope contenedor
# 3. La funcion contenedora devuelve la funcion anidada

# Funcion fabrica
def multiplicador(factor):
    def multiplicar(x):
        return x * factor        # captura 'factor' del scope contenedor
    return multiplicar

doble = multiplicador(2)
triple = multiplicador(3)
doble(5)                         # 10
triple(5)                        # 15

# Verificar closure
doble.__closure__                # tupla de celdas
doble.__closure__[0].cell_contents   # 2
```

### Late binding (trampa clasica)

```python
# PROBLEMA: closures capturan REFERENCIAS, no valores
funciones = [lambda: i for i in range(3)]
funciones[0]()    # 2 (no 0!) — todas devuelven 2

# SOLUCION: capturar el valor como argumento por defecto
funciones = [lambda i=i: i for i in range(3)]
funciones[0]()    # 0
funciones[1]()    # 1
funciones[2]()    # 2
```

### Patrones comunes con closures

```python
# Acumulador (mantener estado sin clases)
def crear_contador(inicio=0):
    cuenta = [inicio]            # lista para poder mutar desde el closure
    def incrementar():
        cuenta[0] += 1
        return cuenta[0]
    return incrementar

c = crear_contador()
c()    # 1
c()    # 2

# Configuracion parcial
def logger(nivel):
    def log(mensaje):
        print(f"[{nivel}] {mensaje}")
    return log

info = logger("INFO")
error = logger("ERROR")
info("Inicio")                   # [INFO] Inicio
```
