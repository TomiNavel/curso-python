# 17. Clases Abstractas y Protocolos

A medida que un programa orientado a objetos crece, aparece la necesidad de definir **contratos**: conjuntos de operaciones que varias clases deben ofrecer, aunque cada una las implemente a su manera. Una función que procesa formas geométricas no necesita saber si recibe un círculo o un rectángulo; solo necesita garantizar que el objeto sepa calcular su área. Un sistema de pagos no necesita conocer los detalles de cada pasarela; solo necesita confiar en que cada una expone un método para cobrar.

Python ofrece dos mecanismos complementarios para expresar estos contratos. Las **clases abstractas** definen una jerarquía explícita mediante herencia: una clase base declara los métodos que las subclases están obligadas a implementar, y Python impide instanciar una subclase incompleta. Los **protocolos** adoptan un enfoque distinto, basado en la forma del objeto: cualquier clase que ofrezca los métodos requeridos satisface el protocolo, sin necesidad de heredar de nada. Ambos enfoques persiguen el mismo objetivo —garantizar que un objeto cumple un contrato—, pero responden a situaciones diferentes.

---

## 17.1. Clases abstractas (ABC)

### 17.1.1. Qué es una clase abstracta y para qué sirve

Una **clase abstracta** es una clase diseñada para servir como base de otras, pero que no puede instanciarse por sí misma. Su propósito es declarar un conjunto de métodos que las subclases están obligadas a implementar, garantizando así que todas las clases derivadas compartan una interfaz común.

Sin clases abstractas, el programador puede heredar de una clase base y olvidarse de implementar algunos métodos. El error solo aparece cuando el código intenta llamar al método ausente, normalmente durante la ejecución y a veces en circunstancias difíciles de reproducir. Las clases abstractas adelantan ese error al momento de crear el objeto: si la subclase no implementa todos los métodos abstractos, Python lanza `TypeError` al instanciarla.

Considérese el siguiente escenario: un programa gestiona distintos tipos de figuras geométricas y necesita calcular el área de cada una. Sin un contrato explícito, nada impide crear una subclase que olvide definir el método `area`:

```python
class Figura:
    def area(self):
        pass  # las subclases deberían sobrescribirlo

class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    # olvido: no defino area()

t = Triangulo(5, 3)
print(t.area())  # None — el error pasa desapercibido
```

El método `area` existe (heredado de `Figura`), devuelve `None` y el programa continúa con datos incorrectos. Una clase abstracta convierte este olvido en un error inmediato y explícito.

### 17.1.2. ABC y @abstractmethod

El módulo `abc` (*Abstract Base Classes*) de la biblioteca estándar proporciona las herramientas para definir clases abstractas. Su uso requiere dos elementos: heredar de `ABC` y marcar los métodos que las subclases deben implementar con el decorador `@abstractmethod`.

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass
```

A partir de esta declaración, Python aplica dos restricciones. Primero, la propia clase `Figura` no puede instanciarse:

```python
f = Figura()
# TypeError: Can't instantiate abstract class Figura
# with abstract methods area, perimetro
```

Segundo, cualquier subclase que no implemente **todos** los métodos abstractos tampoco puede instanciarse:

```python
class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura / 2
    # falta perimetro()

t = Triangulo(5, 3)
# TypeError: Can't instantiate abstract class Triangulo
# with abstract method perimetro
```

El error aparece en el momento de crear el objeto, no más tarde cuando se intenta usar el método ausente. Una subclase completa sí puede instanciarse sin problemas:

```python
class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


r = Rectangulo(5, 3)
print(r.area())       # 15
print(r.perimetro())  # 16
```

`ABC` y `@abstractmethod` pertenecen al módulo `abc`, que forma parte de la biblioteca estándar de Python. Para usarlos basta con importarlos al inicio del archivo mediante `from abc import ABC, abstractmethod`. El mecanismo completo de módulos e importaciones se estudia en el tema 12.

### 17.1.3. Métodos abstractos y concretos en una misma clase

Una clase abstracta no está obligada a tener todos sus métodos marcados como abstractos. Puede —y con frecuencia debe— contener métodos **concretos** con una implementación completa que las subclases heredan sin modificar. Esta combinación es uno de los usos más valiosos de las clases abstractas: permite definir código común en la base y dejar abiertos únicamente los puntos de personalización.

El patrón se conoce como *plantilla* (*template method pattern*). La clase abstracta implementa el esqueleto de un algoritmo invocando métodos abstractos, y las subclases solo rellenan las partes variables:

```python
from abc import ABC, abstractmethod

class Notificacion(ABC):
    def __init__(self, destinatario, mensaje):
        self.destinatario = destinatario
        self.mensaje = mensaje

    def enviar(self):
        # método concreto: define el flujo común
        print(f"Preparando envío a {self.destinatario}")
        self._transmitir()
        print("Envío completado")

    @abstractmethod
    def _transmitir(self):
        # método abstracto: cada subclase define cómo transmitir
        pass


class NotificacionEmail(Notificacion):
    def _transmitir(self):
        print(f"Enviando email: {self.mensaje}")


class NotificacionSMS(Notificacion):
    def _transmitir(self):
        print(f"Enviando SMS: {self.mensaje}")


email = NotificacionEmail("ana@example.com", "Bienvenida")
email.enviar()
# Preparando envío a ana@example.com
# Enviando email: Bienvenida
# Envío completado
```

`enviar` es un método concreto que define el flujo común: preparación, transmisión y confirmación. `_transmitir` es el punto de extensión que cada subclase implementa según su canal. Este diseño evita duplicar la lógica común en cada subclase y garantiza que el flujo sea consistente.

Una clase abstracta también puede tener atributos, constructor y métodos auxiliares concretos. Lo único que la distingue de una clase normal es la presencia de al menos un método marcado con `@abstractmethod`, lo que impide su instanciación directa.

### 17.1.4. Combinar @property con @abstractmethod

Los métodos abstractos no se limitan a métodos normales. El decorador `@abstractmethod` puede combinarse con `@property` para obligar a las subclases a definir una propiedad concreta. El orden de los decoradores es importante: `@property` debe aparecer **encima** de `@abstractmethod`.

```python
from abc import ABC, abstractmethod

class Vehiculo(ABC):
    @property
    @abstractmethod
    def num_ruedas(self):
        pass

    @property
    @abstractmethod
    def tipo(self):
        pass


class Coche(Vehiculo):
    @property
    def num_ruedas(self):
        return 4

    @property
    def tipo(self):
        return "Automóvil"


class Moto(Vehiculo):
    @property
    def num_ruedas(self):
        return 2

    @property
    def tipo(self):
        return "Motocicleta"


c = Coche()
print(c.num_ruedas)  # 4
print(c.tipo)        # Automóvil
```

Este patrón es útil cuando el contrato incluye valores que conceptualmente son atributos (no acciones), pero se necesita forzar a cada subclase a definirlos de forma explícita. Si `Coche` omitiera la property `num_ruedas`, Python impediría su instanciación igual que con cualquier otro método abstracto.

---

## 17.2. Protocolos (structural subtyping)

### 17.2.1. Qué es un protocolo (typing.Protocol)

Un **protocolo** es una forma de definir un contrato basada en la **forma** del objeto, no en su jerarquía de clases. En lugar de exigir que un objeto herede de una clase base concreta, un protocolo declara qué métodos y atributos debe tener el objeto para ser considerado válido. Cualquier clase que cumpla esa forma satisface el protocolo automáticamente, sin necesidad de heredar de nada.

Este enfoque se conoce como *structural subtyping* (subtipado estructural) y contrasta con el *nominal subtyping* de las clases abstractas, donde la relación se establece por herencia explícita. Python siempre ha seguido de facto el principio de *duck typing* —"si anda como un pato y grazna como un pato, es un pato"—, y los protocolos permiten formalizar esa idea con comprobación de tipos estática.

Los protocolos se definen heredando de `typing.Protocol`:

```python
from typing import Protocol

class Dibujable(Protocol):
    def dibujar(self) -> None:
        ...


class Circulo:
    def dibujar(self) -> None:
        print("Dibujando círculo")


class Texto:
    def dibujar(self) -> None:
        print("Dibujando texto")


def renderizar(elemento: Dibujable) -> None:
    elemento.dibujar()


renderizar(Circulo())  # Dibujando círculo
renderizar(Texto())    # Dibujando texto
```

Ni `Circulo` ni `Texto` heredan de `Dibujable`. Sin embargo, ambas clases ofrecen un método `dibujar` con la firma correcta, y por tanto satisfacen el protocolo. Un verificador de tipos estático como `mypy` aceptará las llamadas a `renderizar` sin objeciones.

El cuerpo de un método en un protocolo suele ser `...` (tres puntos, el objeto `Ellipsis` de Python). Es una convención que indica "este método es una declaración, no una implementación". También puede usarse `pass`; ambos funcionan igual.

Los protocolos son útiles en tres situaciones concretas. Primera, cuando se quieren tipar funciones que aceptan objetos de clases que no controlamos —por ejemplo, clases de bibliotecas externas— sin obligar a modificarlas. Segunda, cuando el contrato es demasiado pequeño para justificar una jerarquía de herencia. Tercera, cuando se trabaja con código existente que ya sigue *duck typing* y se quiere añadir verificación de tipos sin reescribirlo.

`Protocol` pertenece al módulo `typing`, que forma parte de la biblioteca estándar. Se importa con `from typing import Protocol`. El tema 20 profundiza en el sistema de tipos de Python y en las herramientas de verificación estática como `mypy`.

### 17.2.2. ABC vs Protocol: cuándo usar cada uno

Clases abstractas y protocolos resuelven el mismo problema —garantizar que un objeto cumple un contrato— pero desde enfoques opuestos. Elegir uno u otro depende de si se controla la jerarquía de clases, de si se necesita compartir código entre subclases y de si la verificación debe ocurrir en tiempo de ejecución o en tiempo de análisis estático.

**Las clases abstractas son apropiadas cuando:**

Existe una jerarquía natural y las subclases comparten lógica común. La clase abstracta puede contener métodos concretos que las subclases heredan, lo que evita duplicar código. Además, la verificación ocurre en tiempo de ejecución: Python impide instanciar subclases incompletas, con o sin verificador de tipos. Son la elección adecuada cuando se diseña una jerarquía propia y se quiere garantizar que todas sus subclases respetan un contrato explícito.

**Los protocolos son apropiados cuando:**

El objetivo es aceptar cualquier objeto con una forma determinada, sin imponer una jerarquía. Esto incluye clases de terceros que no se pueden modificar, estructuras ajenas que casualmente cumplen el contrato, o situaciones donde imponer herencia sería artificial. Los protocolos se apoyan en verificación estática (con `mypy` u otras herramientas) y no necesitan modificar las clases existentes. Son la elección adecuada cuando el contrato es una forma, no una identidad.

**Resumen comparativo:**

| Aspecto | Clase abstracta (ABC) | Protocol |
|---------|-----------------------|----------|
| Relación | Nominal (herencia explícita) | Estructural (misma forma) |
| Declaración | `class X(ABC)` + subclases heredan | Subclases no heredan de nada |
| Verificación | En tiempo de ejecución | Estática (mypy) |
| Código compartido | Sí (métodos concretos) | No (solo firmas) |
| Uso típico | Jerarquías propias con lógica común | Aceptar objetos ajenos por su forma |
| Error ante incumplimiento | `TypeError` al instanciar | Error de mypy antes de ejecutar |

En la práctica, ambos mecanismos coexisten en el mismo proyecto. Una biblioteca puede exponer una clase abstracta para que los usuarios deriven sus propias implementaciones compartiendo lógica común, y al mismo tiempo aceptar protocolos en sus funciones públicas para permitir integraciones con código externo que no hereda de nada. La regla práctica es: si se diseña una jerarquía propia y se quiere compartir código, usar `ABC`; si se quiere aceptar objetos por su forma sin imponer herencia, usar `Protocol`.
