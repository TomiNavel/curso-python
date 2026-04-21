# Errores Comunes: Iteradores y Generadores

## 1. Confundir un iterador agotado con un iterable reutilizable

Uno de los errores más frecuentes al trabajar con generadores es suponer que pueden recorrerse varias veces como si fuesen listas. Un generador es un iterador de un solo uso: una vez que ha producido todos sus valores, el siguiente intento de recorrerlo no produce nada.

```python
numeros = (x * x for x in range(5))
print(list(numeros))  # [0, 1, 4, 9, 16]
print(list(numeros))  # [] — ya no produce nada
```

La solución es, o bien materializar el generador en una lista si se va a recorrer varias veces, o bien definir una función generadora que se llame de nuevo cada vez que se necesite un recorrido nuevo. Escribir `numeros = (x*x for x in range(5))` crea un generador único; escribir `def cuadrados(): yield from (x*x for x in range(5))` crea una fábrica reutilizable.

## 2. Usar corchetes donde se debería usar paréntesis

Cuando se pasa una comprehension como único argumento a una función, la sintaxis de paréntesis puede omitirse. Esto lleva a confundir list comprehensions con generator expressions sin darse cuenta. `sum([x*x for x in range(1_000_000)])` y `sum(x*x for x in range(1_000_000))` producen el mismo resultado, pero el primero construye una lista de un millón de elementos en memoria antes de sumarlos, mientras que el segundo procesa los valores de uno en uno.

La diferencia de memoria puede ser la diferencia entre un programa que funciona y otro que agota la RAM. Al escribir comprehensions dentro de llamadas a `sum`, `max`, `any`, `all`, `min` o constructores como `set` y `tuple`, preferir siempre la versión sin corchetes a menos que se necesite una lista por alguna razón específica.

## 3. Olvidar el `return self` en `__iter__` al implementar un iterador a mano

Un iterador personalizado implementado como clase debe tener `__iter__` que devuelva `self`. Omitir este método, o hacer que devuelva otra cosa, rompe el protocolo y hace que el objeto deje de funcionar correctamente en un `for` o en `list()`.

```python
class Malo:
    def __init__(self, n):
        self.n = n
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n

# TypeError: 'Malo' object is not iterable
for x in Malo(3):
    print(x)
```

Sin `__iter__`, la clase implementa solo la mitad del protocolo: puede producir valores con `next()`, pero Python no sabe cómo obtener un iterador a partir de ella. La solución es añadir `def __iter__(self): return self`.

## 4. Propagar un `StopIteration` accidental dentro de un generador

Desde Python 3.7 (PEP 479), si un `StopIteration` se propaga sin capturar desde dentro del cuerpo de un generador, Python la convierte automáticamente en `RuntimeError`. Esto ocurre típicamente al llamar a `next()` sobre un iterador dentro de un generador sin proporcionar un valor por defecto.

```python
def primeros_pares(iterable):
    it = iter(iterable)
    while True:
        valor = next(it)  # si se agota, StopIteration se propaga
        if valor % 2 == 0:
            yield valor
```

La forma correcta es usar `next(it, centinela)` o capturar explícitamente la excepción con `try/except StopIteration`. Pero en la práctica lo más limpio es usar un bucle `for`: `for valor in iterable: if valor % 2 == 0: yield valor`, que termina limpiamente cuando el iterable se agota.

## 5. Construir listas intermedias innecesarias en tuberías de datos

Un patrón antipático habitual es encadenar operaciones `map`, `filter` o comprehensions materializando una lista en cada paso. Cuando los datos son grandes, cada paso duplica la memoria utilizada sin necesidad.

```python
# Construye tres listas completas en memoria
datos = list(range(1_000_000))
filtrados = [x for x in datos if x % 3 == 0]
elevados = [x * x for x in filtrados]
print(sum(elevados))
```

La versión perezosa procesa cada elemento una sola vez, sin listas intermedias: `sum(x * x for x in range(1_000_000) if x % 3 == 0)`. En una tubería real con varios pasos, usar generator expressions o funciones generadoras intermedias mantiene el consumo de memoria constante, independientemente del tamaño de la entrada.

## 6. Aplicar `groupby` sobre datos no ordenados

`itertools.groupby` agrupa elementos **consecutivos** que comparten la misma clave, no todos los elementos que la comparten. Si los datos no están ordenados por esa clave, el resultado son grupos fragmentados que rara vez son lo esperado.

```python
from itertools import groupby

datos = ["ana", "bea", "ada", "ben"]
for letra, grupo in groupby(datos, key=lambda p: p[0]):
    print(letra, list(grupo))
# a ['ana']
# b ['bea']
# a ['ada']   ← "ana" y "ada" quedan separadas
# b ['ben']
```

La solución es ordenar los datos por la misma clave antes de agrupar: `sorted(datos, key=lambda p: p[0])`. Este comportamiento es intencional y eficiente —`groupby` trabaja en O(n) sin materializar diccionarios—, pero exige que el programador conozca esta precondición.

## 7. Llamar a `send` antes de haber avanzado el generador

El método `send` reanuda un generador en la expresión `yield` donde estaba pausado. Si el generador es nuevo, todavía no se ha ejecutado nada y no hay ningún `yield` en el que reanudar. En esa situación, solo se permite `send(None)` o `next()`.

```python
def gen():
    x = yield 1
    yield x

g = gen()
g.send(10)  # TypeError: can't send non-None value to a just-started generator
```

La secuencia correcta es avanzar primero con `next(g)` o `g.send(None)` para llegar al primer `yield`, y después usar `send(valor)` para inyectar valores a partir de ese punto.

## 8. Esperar que un iterador tenga longitud

Un iterador no conoce cuántos elementos va a producir: no tiene sentido llamar a `len()` sobre un generador o sobre el resultado de `map`, `filter` o `itertools.chain`. Hacerlo lanza `TypeError`.

```python
cuadrados = (x * x for x in range(10))
len(cuadrados)  # TypeError: object of type 'generator' has no len()
```

Si se necesita conocer la cantidad de elementos, hay dos opciones: materializar el generador en una lista (`len(list(cuadrados))`, consumiéndolo) o contar sobre la marcha con `sum(1 for _ in cuadrados)`. Ambas opciones consumen el generador, así que no puede reutilizarse después.

## 9. Confundir una función generadora con su resultado

Una función generadora, definida con `def` y `yield`, es una función como cualquier otra. Llamarla devuelve un generador; la función en sí misma no es el generador. Este matiz se olvida con facilidad.

```python
def contar():
    yield 1
    yield 2

print(contar)         # <function contar at ...>
print(contar())       # <generator object contar at ...>
print(list(contar()))  # [1, 2]
```

Pasar `contar` sin los paréntesis a un `for` falla silenciosamente en algunos contextos y con un error en otros. La regla es simple: para obtener valores de una función generadora, hay que llamarla como a cualquier función. Esto permite, además, crear tantos generadores independientes como se necesiten.

## 10. Usar una función generadora para algo que debería ser una función normal

No todo código que usa `yield` debería usarlo. Un generador tiene sentido cuando se trata de producir una secuencia de valores perezosamente o cuando el estado entre valores es no trivial. Para funciones que simplemente devuelven un valor o que tienen pocos efectos secundarios, un generador introduce complejidad innecesaria: hay que recordar iterarlo para que se ejecute, y el `return` se comporta de forma distinta.

```python
def grabar_log(mensaje):
    yield f"[log] {mensaje}"  # ¿por qué yield?

grabar_log("algo")  # No imprime nada: el cuerpo no se ha ejecutado
```

En este caso, el programador probablemente quería una función normal que devolviese la cadena con `return`. El error es sutil porque llamar a la función no lanza ningún aviso: simplemente no hace nada. La señal de alarma debería saltar al comprobar que la función no produce efectos. Usar `yield` exige una intención clara: producir una secuencia de valores que alguien consumirá iterativamente.
