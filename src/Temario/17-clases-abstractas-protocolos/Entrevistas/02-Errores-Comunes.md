# Errores Comunes: Clases Abstractas y Protocolos

## Error 1: Olvidar heredar de `ABC` y esperar que `@abstractmethod` funcione

```python
from abc import abstractmethod

class Figura:  # MAL — no hereda de ABC
    @abstractmethod
    def area(self):
        pass

class Cuadrado(Figura):
    pass  # no implementa area

c = Cuadrado()      # NO lanza error
print(c.area())     # None — la "abstracción" no tiene efecto
```

`@abstractmethod` solo tiene efecto si la clase hereda de `ABC` (o usa `metaclass=ABCMeta`). Sin esa herencia, el decorador se convierte en una anotación sin consecuencias: las subclases pueden omitir el método y Python las instancia sin problemas.

```python
from abc import ABC, abstractmethod

class Figura(ABC):  # correcto
    @abstractmethod
    def area(self):
        pass
```

---

## Error 2: Intentar instanciar la propia clase abstracta

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sonido(self):
        pass

a = Animal()
# TypeError: Can't instantiate abstract class Animal
# with abstract method sonido
```

Una clase abstracta está diseñada para ser heredada, no instanciada. Intentar crear un objeto directamente siempre lanza `TypeError`. Si se necesita una instancia "genérica", hay que crear una subclase concreta que implemente todos los métodos abstractos.

---

## Error 3: Implementar solo algunos métodos abstractos

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

class Circulo(Figura):
    def area(self):
        return 3.14 * 5 ** 2
    # falta perimetro()

c = Circulo()
# TypeError: Can't instantiate abstract class Circulo
# with abstract method perimetro
```

Una subclase debe implementar **todos** los métodos abstractos para poder instanciarse. Implementar parcialmente es válido a nivel de definición —la clase se puede declarar— pero instanciarla produce `TypeError`.

---

## Error 4: Invertir el orden de `@property` y `@abstractmethod`

```python
from abc import ABC, abstractmethod

class Vehiculo(ABC):
    @abstractmethod  # MAL — va debajo, no encima
    @property
    def num_ruedas(self):
        pass
```

El orden correcto es `@property` **encima** de `@abstractmethod`. Invertirlo produce un comportamiento incorrecto: el decorador `@abstractmethod` no recibe una property, sino una función normal, y la abstracción puede no funcionar como se espera.

```python
class Vehiculo(ABC):
    @property         # primero
    @abstractmethod   # después
    def num_ruedas(self):
        pass
```

---

## Error 5: Creer que un protocolo verifica en tiempo de ejecución

```python
from typing import Protocol

class Dibujable(Protocol):
    def dibujar(self) -> None:
        ...

class Texto:
    pass  # no implementa dibujar

def renderizar(elemento: Dibujable) -> None:
    elemento.dibujar()

renderizar(Texto())
# AttributeError: 'Texto' object has no attribute 'dibujar'
```

Los protocolos se verifican estáticamente con herramientas como `mypy`. En tiempo de ejecución, Python no comprueba que el objeto realmente cumpla el protocolo: la llamada se ejecuta y el error aparece al intentar usar el método ausente. Si se quiere verificación en tiempo de ejecución, hay que usar `@runtime_checkable` y `isinstance()`, aunque esa comprobación solo verifica la presencia de los métodos, no sus firmas.

---

## Error 6: Heredar de un protocolo creyendo que es obligatorio

```python
from typing import Protocol

class Dibujable(Protocol):
    def dibujar(self) -> None:
        ...

class Boton(Dibujable):  # innecesario
    def dibujar(self) -> None:
        print("Botón")
```

La ventaja principal de los protocolos es precisamente que **no requieren herencia**. Una clase satisface un protocolo por tener la forma correcta, no por heredar de él. Heredar explícitamente no está prohibido, pero elimina la flexibilidad que hace útiles a los protocolos en primer lugar (aceptar clases de terceros sin modificarlas).

---

## Error 7: Definir métodos abstractos con `pass` y esperar que devuelvan algo

```python
from abc import ABC, abstractmethod

class Calculadora(ABC):
    @abstractmethod
    def sumar(self, a, b):
        return a + b  # MAL — lógica en método abstracto "olvidada"

class Concreta(Calculadora):
    def sumar(self, a, b):
        return super().sumar(a, b)  # devuelve None si no hay implementación propia
```

Un método abstracto puede tener cuerpo (útil cuando se quiere ofrecer una implementación por defecto que las subclases pueden extender con `super()`), pero es un patrón avanzado y poco común. En general, el cuerpo de un método abstracto debe ser `pass`: su propósito es declarar el contrato, no proporcionar lógica.

---

## Error 8: Usar clases abstractas cuando un protocolo es más adecuado

```python
from abc import ABC, abstractmethod

# MAL — fuerza a heredar, aunque las clases ya existen
class Dibujable(ABC):
    @abstractmethod
    def dibujar(self):
        pass

# La clase Boton ya existe en una librería externa
# que no podemos modificar para que herede de Dibujable
```

Si se trabaja con clases que no se controlan (librerías externas, código legacy), una clase abstracta obliga a crear adaptadores o a modificar el código ajeno. Un protocolo resuelve el problema sin tocar ninguna clase: basta con que los objetos tengan la forma correcta.

---

## Error 9: Protocolos con atributos y olvidar declararlos

```python
from typing import Protocol

class Punto(Protocol):
    x: float
    y: float

class MiPunto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distancia(p: Punto) -> float:
    return (p.x ** 2 + p.y ** 2) ** 0.5
```

Los protocolos pueden declarar atributos además de métodos. Es fácil olvidar esto y definir solo métodos, obligando a las clases a exponer los datos mediante getters innecesarios. Si el contrato requiere un atributo, declararlo directamente en el protocolo es más claro y más Pythónico.

---

## Error 10: Métodos concretos en una clase abstracta que dependen de métodos no implementados

```python
from abc import ABC, abstractmethod

class Repositorio(ABC):
    @abstractmethod
    def obtener(self, id):
        pass

    def obtener_o_fallar(self, id):
        resultado = self.obtener(id)  # llama al método abstracto
        if resultado is None:
            raise ValueError(f"No se encontró {id}")
        return resultado
```

Esto no es un error —es precisamente el patrón plantilla— pero sí un punto de confusión frecuente. Los métodos concretos de una clase abstracta pueden invocar métodos abstractos. Cuando una subclase implementa los abstractos, los concretos heredados funcionan automáticamente usando la implementación concreta. El error aparece solo si se intenta llamar al método concreto sobre la clase abstracta directamente, cosa imposible porque no se puede instanciar.
