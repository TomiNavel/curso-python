# Preguntas de Entrevista: Clases Abstractas y Protocolos

1. ¿Qué es una clase abstracta y para qué sirve?
2. ¿Qué diferencia hay entre un método abstracto y un método concreto dentro de una clase abstracta?
3. ¿Por qué no se puede instanciar una clase que hereda de `ABC` sin implementar todos sus métodos abstractos?
4. ¿Cuándo ocurre el error por no implementar un método abstracto: al definir la subclase o al instanciarla?
5. ¿Cómo se combinan `@property` y `@abstractmethod`? ¿En qué orden deben escribirse los decoradores?
6. ¿Qué es un protocolo (`typing.Protocol`) y en qué se diferencia de una clase abstracta?
7. ¿Qué es el *structural subtyping* y cómo se relaciona con el *duck typing* de Python?
8. Una clase satisface un protocolo, ¿debe heredar de él?
9. ¿En qué situación conviene usar una clase abstracta y en cuál un protocolo?
10. ¿Los protocolos verifican el cumplimiento del contrato en tiempo de ejecución?
11. ¿Qué es el patrón plantilla (*template method*) y cómo se relaciona con las clases abstractas?
12. ¿Cuál es el resultado de este código?
    ```python
    from abc import ABC, abstractmethod

    class Animal(ABC):
        def __init__(self, nombre):
            self.nombre = nombre

        @abstractmethod
        def sonido(self):
            pass

        def presentarse(self):
            return f"{self.nombre} dice {self.sonido()}"

    class Perro(Animal):
        def sonido(self):
            return "guau"

    class Gato(Animal):
        def sonido(self):
            return "miau"

    animales = [Perro("Rex"), Gato("Luna")]
    for a in animales:
        print(a.presentarse())

    try:
        a = Animal("Genérico")
    except TypeError as e:
        print("Error al instanciar Animal")
    ```

---

### R1. ¿Qué es una clase abstracta y para qué sirve?

Una clase abstracta es una clase diseñada para servir como base de otras, pero que no puede instanciarse por sí misma. Declara un conjunto de métodos que las subclases están obligadas a implementar, garantizando que toda la jerarquía comparta una interfaz común.

Su utilidad principal es convertir un olvido de implementación en un error inmediato y explícito. Sin clases abstractas, una subclase incompleta puede crearse sin problemas y el fallo solo aparece cuando el código intenta llamar al método ausente, a veces en condiciones difíciles de reproducir.

---

### R2. ¿Diferencia entre método abstracto y método concreto?

Un método abstracto solo declara su firma (normalmente con `pass` como cuerpo) y está marcado con `@abstractmethod`. Las subclases están obligadas a implementarlo.

Un método concreto tiene una implementación completa y las subclases lo heredan sin modificar. Una clase abstracta puede contener ambos tipos: los abstractos definen los puntos de extensión y los concretos proporcionan lógica común reutilizable. Esta combinación es la base del patrón plantilla.

---

### R3. ¿Por qué no se puede instanciar una subclase incompleta?

Porque la subclase hereda los métodos abstractos de la clase base y mientras no los implemente sigue siendo una clase abstracta. Python detecta que la subclase aún tiene métodos marcados como abstractos y bloquea su instanciación con `TypeError`. Solo cuando todos los métodos abstractos han sido sobrescritos con implementaciones concretas, la subclase deja de considerarse abstracta.

---

### R4. ¿Cuándo ocurre el error?

Al instanciarla, no al definirla. Definir una subclase incompleta es válido y no produce ningún error. El `TypeError` aparece en el momento en que se intenta crear un objeto de esa subclase. Este comportamiento permite, por ejemplo, definir jerarquías intermedias abstractas que nunca se instancian directamente.

---

### R5. ¿Cómo combinar `@property` con `@abstractmethod`?

El orden es importante: `@property` debe ir **encima** de `@abstractmethod`.

```python
class Vehiculo(ABC):
    @property
    @abstractmethod
    def num_ruedas(self):
        pass
```

Las subclases están obligadas a definir la property. Este patrón se usa cuando el contrato incluye valores que conceptualmente son atributos (no acciones), pero se quiere forzar a cada subclase a declararlos explícitamente.

---

### R6. ¿Qué es un protocolo y en qué se diferencia de una clase abstracta?

Un protocolo (`typing.Protocol`) define un contrato basado en la **forma** del objeto, no en su jerarquía de clases. Cualquier clase que tenga los métodos requeridos con la firma correcta satisface el protocolo automáticamente, sin necesidad de heredar de nada.

La diferencia clave con una clase abstracta es el tipo de relación: una clase abstracta establece una relación **nominal** (heredas o no heredas), mientras que un protocolo establece una relación **estructural** (tienes la forma o no la tienes). Además, los protocolos se apoyan en verificación estática con `mypy`, mientras que las clases abstractas verifican en tiempo de ejecución.

---

### R7. ¿Qué es structural subtyping?

Es la idea de que la compatibilidad entre tipos se determina por la **estructura** del objeto (qué métodos y atributos tiene), no por su relación de herencia. Es la formalización del *duck typing* clásico de Python —"si anda como un pato y grazna como un pato, es un pato"— con verificación estática de tipos.

Antes de `typing.Protocol`, Python ya permitía duck typing en tiempo de ejecución pero no había manera de tiparlo. Los protocolos añaden esa capa de seguridad sin romper la flexibilidad que caracteriza al lenguaje.

---

### R8. ¿Una clase debe heredar del protocolo que satisface?

No. Esa es precisamente la ventaja de los protocolos. Una clase satisface un protocolo por tener la forma correcta, no por heredar de él. Esto permite aceptar objetos de clases que no controlamos —por ejemplo, de bibliotecas externas— sin modificarlas.

Heredar explícitamente de un protocolo es opcional y se hace solo cuando se quiere documentar la intención o aprovechar la verificación en tiempo de ejecución con `@runtime_checkable`.

---

### R9. ¿Cuándo usar una clase abstracta y cuándo un protocolo?

Usar una **clase abstracta** cuando se diseña una jerarquía propia y las subclases comparten lógica común. La clase abstracta puede contener métodos concretos que las subclases heredan, evitando duplicación de código. Es también la opción adecuada cuando se necesita verificación en tiempo de ejecución sin depender de herramientas externas.

Usar un **protocolo** cuando el objetivo es aceptar cualquier objeto con una forma determinada, sin imponer una jerarquía. Es la opción adecuada para clases de terceros, para contratos pequeños donde la herencia sería artificial, o para integrar código existente que ya sigue *duck typing*.

---

### R10. ¿Los protocolos verifican en tiempo de ejecución?

Por defecto, no. Los protocolos están pensados para verificación estática con herramientas como `mypy`, que analizan el código antes de ejecutarlo y detectan incompatibilidades. En tiempo de ejecución, un protocolo se comporta como una clase cualquiera y no impide pasar objetos que no cumplen el contrato.

Existe el decorador `@runtime_checkable` que permite usar `isinstance()` con un protocolo, pero esa comprobación solo verifica la presencia de los métodos, no sus firmas ni sus tipos.

---

### R11. ¿Qué es el patrón plantilla?

Es un patrón de diseño en el que una clase base define el esqueleto de un algoritmo invocando métodos abstractos, y las subclases solo rellenan las partes variables. La clase base mantiene el flujo común y las subclases personalizan los pasos concretos.

En Python, las clases abstractas son el mecanismo natural para implementarlo: los métodos concretos de la clase base definen el flujo y los métodos abstractos son los puntos de extensión. Este enfoque evita duplicar la lógica común en cada subclase y garantiza que el flujo sea consistente.

---

### R12. ¿Cuál es el resultado del código?

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def sonido(self):
        pass

    def presentarse(self):
        return f"{self.nombre} dice {self.sonido()}"

class Perro(Animal):
    def sonido(self):
        return "guau"

class Gato(Animal):
    def sonido(self):
        return "miau"

animales = [Perro("Rex"), Gato("Luna")]
for a in animales:
    print(a.presentarse())

try:
    a = Animal("Genérico")
except TypeError as e:
    print("Error al instanciar Animal")
```

Salida:

```
Rex dice guau
Luna dice miau
Error al instanciar Animal
```

- `presentarse` es un método concreto de `Animal` que invoca `self.sonido()` (abstracto). Cada subclase implementa `sonido` a su manera.
- `Perro("Rex").presentarse()` imprime `"Rex dice guau"`.
- `Gato("Luna").presentarse()` imprime `"Luna dice miau"`.
- Intentar crear `Animal("Genérico")` lanza `TypeError` porque `Animal` es una clase abstracta con el método `sonido` sin implementar. El `except` captura el error y imprime el mensaje.
