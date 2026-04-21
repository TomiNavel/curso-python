# 15. Herencia, Polimorfismo y Composición

Hasta ahora, cada clase que hemos creado ha sido independiente — definía toda su estructura y comportamiento desde cero. Pero en la realidad, los tipos de datos suelen tener relaciones entre sí. Un empleado es una persona. Un cuadrado es una figura geométrica. Un coche eléctrico es un coche. Estas relaciones de "es un" son exactamente lo que modela la herencia: un mecanismo que permite crear nuevas clases a partir de clases existentes, heredando sus atributos y métodos.

La herencia es una herramienta poderosa pero fácil de abusar. Este tema cubre no solo cómo funciona, sino cuándo usarla — y cuándo la composición es una alternativa mejor.

---

## 15.1. Herencia

### 15.1.1. Concepto y sintaxis

La herencia permite crear una clase nueva (clase **hija** o **subclase**) que hereda atributos y métodos de una clase existente (clase **padre** o **superclase**). La subclase puede usar todo lo que tiene la clase padre sin redefinirlo, y puede añadir atributos y métodos propios o modificar los heredados.

La sintaxis es simple: se pone el nombre de la clase padre entre paréntesis al definir la subclase.

```python
class Animal:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie

    def describir(self):
        return f"{self.nombre} es un {self.especie}"


class Perro(Animal):
    def ladrar(self):
        return f"{self.nombre} dice: ¡Guau!"


rex = Perro("Rex", "perro")
print(rex.describir())  # Rex es un perro — heredado de Animal
print(rex.ladrar())     # Rex dice: ¡Guau! — propio de Perro
```

`Perro` no define `__init__` ni `describir`, pero los tiene porque los hereda de `Animal`. Cuando se crea `Perro("Rex", "perro")`, Python busca `__init__` en `Perro`, no lo encuentra, y sube a `Animal`.

La herencia establece una relación **"es un"**: un `Perro` es un `Animal`. Esto tiene implicaciones prácticas — un `Perro` puede usarse en cualquier lugar donde se espere un `Animal`:

```python
print(isinstance(rex, Perro))    # True
print(isinstance(rex, Animal))   # True — un Perro ES un Animal
```

En Python, todas las clases heredan de `object` implícitamente. `class Perro(Animal)` y `class Animal:` (equivalente a `class Animal(object):`) forman una cadena: `Perro` → `Animal` → `object`. Esto significa que todo objeto en Python tiene los métodos de `object` (`__str__`, `__repr__`, `__eq__`, etc.), aunque sean las versiones por defecto.

### 15.1.2. super() y el MRO (Method Resolution Order)

Esta sección cubre dos conceptos que aparecen siempre que se trabaja con herencia. **`super()`** es la función que permite a una subclase acceder a los métodos de su clase padre, y es imprescindible para reutilizar su lógica — en especial dentro de `__init__`. **El MRO (Method Resolution Order)** es el orden en que Python decide qué método se ejecuta cuando hay varias clases en la jerarquía que definen el mismo nombre.

El punto de partida es un problema concreto. Una subclase hereda automáticamente todos los métodos del padre, pero en cuanto define su propio `__init__`, lo sobreescribe — y el `__init__` del padre deja de ejecutarse. Este es uno de los errores más frecuentes: la subclase nunca inicializa los atributos que el padre esperaba establecer.

```python
class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo


class Coche(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        # Se ha olvidado llamar al __init__ del padre
        self.puertas = puertas


c = Coche("Toyota", "Corolla", 4)
print(c.puertas)  # 4 — funciona
print(c.marca)    # AttributeError: 'Coche' object has no attribute 'marca'
```

La solución es **`super()`**: una función incorporada que da acceso a los métodos de la clase padre. Llamar a `super().__init__(...)` ejecuta el `__init__` del padre para que inicialice sus atributos, y después la subclase añade los suyos.

```python
class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def info(self):
        return f"{self.marca} {self.modelo}"


class Coche(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)  # el padre inicializa marca y modelo
        self.puertas = puertas           # la subclase añade lo suyo

    def info(self):
        # super().info() llama a la versión del padre, sin duplicar código
        return f"{super().info()} - {self.puertas} puertas"


c = Coche("Toyota", "Corolla", 4)
print(c.info())  # Toyota Corolla - 4 puertas
```

`super()` también sirve para **extender** (no solo reemplazar) un método heredado: se llama a `super().metodo()` para obtener el comportamiento del padre, y luego se añade lo específico de la subclase. Esto evita duplicar código y mantiene la coherencia si el método del padre cambia en el futuro.

**El MRO (Method Resolution Order)** es la lista ordenada de clases donde Python busca un método cuando se invoca sobre un objeto. Cada clase tiene su propio MRO, calculado automáticamente en el momento de su definición a partir de sus clases padre.

Cuando se escribe `c.info()`, Python no puede saber automáticamente dónde está definido `info`. Lo que hace es recorrer el MRO de la clase del objeto, en orden, y ejecutar el primer método con ese nombre que encuentre. Esto es lo que hace que la herencia funcione: un `Coche` no define `info` directamente, pero cuando se invoca, Python sube por el MRO hasta encontrarla en `Vehiculo`.

El MRO se puede consultar con `Clase.__mro__`:

```python
print(Coche.__mro__)
# (<class 'Coche'>, <class 'Vehiculo'>, <class 'object'>)
```

Este MRO se lee así: "cuando busques un método en un `Coche`, mira primero en `Coche`, luego en `Vehiculo`, luego en `object`". Por eso `c.info()` ejecuta la versión de `Coche` (es la primera que encuentra), mientras que `c.__init__` del padre se encuentra en `Vehiculo` si `Coche` no lo define.

`super()` y el MRO están directamente conectados: `super()` no llama al "padre" de forma literal, sino al **siguiente nivel en el MRO**. En herencia simple esto es equivalente — el siguiente nivel siempre es el padre directo — y por eso el MRO parece trivial. Su importancia real aparece en herencia múltiple, donde una clase tiene varios padres y el MRO define cuál se considera "el siguiente". Ese caso se ve en la sección 15.1.4.

### 15.1.3. Sobreescribir métodos

Sobreescribir (override) un método significa redefinirlo en la subclase. Cuando se llama al método en una instancia de la subclase, se ejecuta la versión de la subclase, no la del padre:

```python
class Figura:
    def __init__(self, nombre):
        self.nombre = nombre

    def area(self):
        raise NotImplementedError("Las subclases deben implementar area()")

    def __str__(self):
        return f"{self.nombre}: área = {self.area()}"


class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura


class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.radio = radio

    def area(self):
        import math
        return round(math.pi * self.radio ** 2, 2)


r = Rectangulo(5, 3)
c = Circulo(4)

print(r)  # Rectángulo: área = 15
print(c)  # Círculo: área = 50.27
```

La clase padre `Figura` define `area()` lanzando `NotImplementedError`. Esto obliga a cada subclase a proporcionar su propia implementación. El método `__str__` del padre llama a `self.area()`, y como `self` es un `Rectangulo` o un `Circulo`, ejecuta la versión correcta. Este patrón se verá formalizado en el tema 17 con clases abstractas.

Un aspecto importante: `super()` permite **extender** un método en lugar de reemplazarlo completamente. Llamar a `super().metodo()` ejecuta la versión del padre, y la subclase añade lógica adicional antes o después:

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def resumen(self):
        return f"{self.nombre} - ${self.salario:,.0f}"


class Gerente(Empleado):
    def __init__(self, nombre, salario, departamento):
        super().__init__(nombre, salario)
        self.departamento = departamento

    def resumen(self):
        # Extiende el resumen del padre en lugar de reemplazarlo
        return f"{super().resumen()} (Gerente de {self.departamento})"


g = Gerente("Ana", 80000, "IT")
print(g.resumen())  # Ana - $80,000 (Gerente de IT)
```

### 15.1.4. Herencia múltiple y el problema del diamante

Python permite que una clase herede de múltiples clases padre:

```python
class Volador:
    def volar(self):
        return "Volando"

class Nadador:
    def nadar(self):
        return "Nadando"

class Pato(Volador, Nadador):
    def describir(self):
        return f"Puedo: {self.volar()} y {self.nadar()}"

p = Pato()
print(p.describir())  # Puedo: Volando y Nadando
```

Esto funciona bien cuando las clases padre no tienen métodos en común. El problema aparece cuando dos clases padre heredan de la misma clase base — formando un "diamante":

```python
class Base:
    def __init__(self):
        print("Base.__init__")

class A(Base):
    def __init__(self):
        super().__init__()
        print("A.__init__")

class B(Base):
    def __init__(self):
        super().__init__()
        print("B.__init__")

class C(A, B):
    def __init__(self):
        super().__init__()
        print("C.__init__")

c = C()
# Salida:
# Base.__init__
# B.__init__
# A.__init__
# C.__init__
```

El MRO de `C` es `C → A → B → Base → object`. Python usa el algoritmo **C3 linearization** para determinar un orden lineal que respete la jerarquía. Lo importante es que `Base.__init__` se llama **una sola vez**, no dos, gracias a que `super()` sigue el MRO en lugar de llamar directamente al padre.

```python
print(C.__mro__)
# (<class 'C'>, <class 'A'>, <class 'B'>, <class 'Base'>, <class 'object'>)
```

La herencia múltiple es una herramienta legítima en Python, pero puede generar jerarquías difíciles de entender. Se usa habitualmente con **mixins** — clases pequeñas que añaden una funcionalidad específica sin pretender ser una clase base completa:

```python
class SerializableMixin:
    def to_dict(self):
        return vars(self)

class Producto(SerializableMixin):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

p = Producto("Laptop", 999)
print(p.to_dict())  # {'nombre': 'Laptop', 'precio': 999}
```

Un mixin no tiene `__init__` propio (o tiene uno trivial) y añade métodos utilitarios. Por convención, su nombre termina en `Mixin`.

---

## 15.2. Polimorfismo

### 15.2.1. Duck typing

El polimorfismo es la capacidad de tratar objetos de tipos diferentes de forma uniforme, siempre que compartan la misma interfaz (los mismos métodos). En Python, el polimorfismo es natural gracias al **duck typing**: "si camina como un pato y grazna como un pato, es un pato".

Python no verifica el tipo de un objeto antes de llamar a un método — simplemente intenta llamarlo. Si el método existe, funciona. Si no, lanza `AttributeError`. Esto significa que no se necesita herencia para que dos clases sean polimórficas — basta con que tengan los mismos métodos:

```python
class Archivo:
    def __init__(self, nombre, tamano):
        self.nombre = nombre
        self.tamano = tamano

    def describir(self):
        return f"Archivo: {self.nombre} ({self.tamano} KB)"


class Carpeta:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def describir(self):
        return f"Carpeta: {self.nombre} ({self.cantidad} elementos)"


# Ambos tienen describir() — se pueden tratar de forma uniforme
elementos = [Archivo("foto.jpg", 2048), Carpeta("Documentos", 15)]

for elem in elementos:
    print(elem.describir())
# Archivo: foto.jpg (2048 KB)
# Carpeta: Documentos (15 elementos)
```

`Archivo` y `Carpeta` no comparten ninguna clase padre (más allá de `object`), pero como ambos tienen `describir()`, el bucle `for` funciona. Esto es duck typing en acción.

### 15.2.2. Polimorfismo con herencia

La herencia hace el polimorfismo más formal: la clase padre define la interfaz y las subclases la implementan. Esto garantiza que todas las subclases tienen los métodos esperados:

```python
class Notificacion:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def enviar(self):
        raise NotImplementedError("Las subclases deben implementar enviar()")


class Email(Notificacion):
    def __init__(self, mensaje, destinatario):
        super().__init__(mensaje)
        self.destinatario = destinatario

    def enviar(self):
        return f"Email a {self.destinatario}: {self.mensaje}"


class SMS(Notificacion):
    def __init__(self, mensaje, telefono):
        super().__init__(mensaje)
        self.telefono = telefono

    def enviar(self):
        return f"SMS a {self.telefono}: {self.mensaje}"


class Push(Notificacion):
    def enviar(self):
        return f"Push: {self.mensaje}"


# Todas se tratan como Notificacion
notificaciones = [
    Email("Hola", "ana@mail.com"),
    SMS("Código: 1234", "+34600000000"),
    Push("Nueva actualización"),
]

for n in notificaciones:
    print(n.enviar())
```

El código que recorre la lista no necesita saber si es un `Email`, un `SMS` o un `Push`. Solo necesita saber que tiene `enviar()`. Si mañana se añade un nuevo tipo de notificación (`Slack`, `Telegram`), el bucle funciona sin cambios.

### 15.2.3. isinstance() e issubclass() en contexto de herencia

`isinstance(obj, Clase)` comprueba si un objeto es instancia de una clase **o de cualquiera de sus subclases**. `issubclass(Hija, Padre)` comprueba si una clase es subclase de otra.

```python
email = Email("Hola", "ana@mail.com")

print(isinstance(email, Email))         # True
print(isinstance(email, Notificacion))  # True — Email hereda de Notificacion
print(isinstance(email, object))        # True — todo hereda de object

print(issubclass(Email, Notificacion))  # True
print(issubclass(Email, SMS))           # False — no hay relación
```

Ambas funciones aceptan tuplas para comprobar contra varios tipos:

```python
print(isinstance(email, (Email, SMS)))  # True — es al menos uno de ellos
```

En la práctica, **el uso excesivo de `isinstance()` es un indicador de mal diseño**. Si el código necesita comprobar constantemente el tipo de un objeto para decidir qué hacer, probablemente debería usar polimorfismo en su lugar — dejar que cada clase defina su propio comportamiento:

```python
# MAL — comprobación de tipo manual
def procesar(notificacion):
    if isinstance(notificacion, Email):
        return f"Enviando email a {notificacion.destinatario}"
    elif isinstance(notificacion, SMS):
        return f"Enviando SMS a {notificacion.telefono}"

# BIEN — polimorfismo
def procesar(notificacion):
    return notificacion.enviar()
```

---

## 15.3. Composición vs herencia

### 15.3.1. Qué es composición

La composición es una alternativa a la herencia donde, en lugar de heredar comportamiento de una clase padre, un objeto **contiene** instancias de otras clases como atributos. La relación es **"tiene un"** en lugar de **"es un"**.

```python
class Motor:
    def __init__(self, cilindrada, combustible):
        self.cilindrada = cilindrada
        self.combustible = combustible

    def arrancar(self):
        return f"Motor {self.cilindrada}cc arrancado ({self.combustible})"


class GPS:
    def __init__(self, modelo):
        self.modelo = modelo

    def localizar(self):
        return f"GPS {self.modelo}: posición obtenida"


class Coche:
    def __init__(self, marca, modelo, motor, gps=None):
        self.marca = marca
        self.modelo = modelo
        self.motor = motor      # Composición: Coche TIENE un Motor
        self.gps = gps          # Composición: Coche TIENE un GPS (opcional)

    def arrancar(self):
        resultado = self.motor.arrancar()
        if self.gps:
            resultado += f"\n{self.gps.localizar()}"
        return resultado

    def __str__(self):
        return f"{self.marca} {self.modelo}"


motor = Motor(2000, "gasolina")
gps = GPS("TomTom")
coche = Coche("Toyota", "Corolla", motor, gps)

print(coche)
print(coche.arrancar())
# Toyota Corolla
# Motor 2000cc arrancado (gasolina)
# GPS TomTom: posición obtenida
```

`Coche` no hereda de `Motor` ni de `GPS` — no sería correcto decir que un coche "es un" motor. Un coche **tiene** un motor. La composición modela esta relación de forma natural.

### 15.3.2. Cuándo usar herencia y cuándo composición

La regla general es: **preferir composición sobre herencia**. La composición es más flexible, más fácil de cambiar y genera menos acoplamiento. La herencia debe reservarse para relaciones genuinas de "es un".

**Usar herencia cuando:**
- Existe una relación clara de "es un" (un `Perro` es un `Animal`, un `Email` es una `Notificacion`).
- Se quiere garantizar que todas las subclases implementen la misma interfaz.
- Se necesita que las subclases sean sustituibles por la clase padre (principio de Liskov).

**Usar composición cuando:**
- La relación es "tiene un" (un `Coche` tiene un `Motor`).
- Se necesita combinar funcionalidades de varias clases sin crear jerarquías complejas.
- El comportamiento puede cambiar en tiempo de ejecución (intercambiar componentes).
- La herencia crearía una jerarquía demasiado profunda o frágil.

**Ejemplo de herencia mal usada:**

```python
# MAL — un Stack no ES una lista
class Stack(list):
    def push(self, item):
        self.append(item)

s = Stack()
s.push(1)
s.push(2)
# Pero también se puede hacer esto, rompiendo la abstracción:
s.insert(0, "oops")  # insert() viene de list — no debería ser accesible
```

Al heredar de `list`, el `Stack` expone todos los métodos de lista (`insert`, `remove`, `sort`...) que no tienen sentido para una pila. La composición resuelve esto:

```python
# BIEN — un Stack TIENE una lista interna
class Stack:
    def __init__(self):
        self._datos = []

    def push(self, item):
        self._datos.append(item)

    def pop(self):
        if not self._datos:
            raise IndexError("pop from empty stack")
        return self._datos.pop()

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"Stack({self._datos})"
```

Ahora el `Stack` solo expone `push`, `pop` y `len` — exactamente la interfaz de una pila, nada más.

**Resumen:**

| Criterio | Herencia | Composición |
|----------|----------|-------------|
| Relación | "es un" | "tiene un" |
| Acoplamiento | Alto (la subclase depende del padre) | Bajo (los componentes son independientes) |
| Flexibilidad | Fija en tiempo de definición | Intercambiable en tiempo de ejecución |
| Reutilización | Hereda toda la interfaz del padre | Solo usa lo que necesita |
| Complejidad | Crece con la profundidad de la jerarquía | Se mantiene plana |
