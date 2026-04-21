# 16. Encapsulación y Properties

En lenguajes como Java o C#, los atributos de una clase se declaran como `private` y se acceden a través de métodos `getX()` y `setX()`. Python toma un enfoque diferente: no existe una palabra clave que impida el acceso a un atributo. En su lugar, utiliza convenciones de nombrado para indicar la intención del programador, y un mecanismo llamado **properties** que permite interceptar el acceso a un atributo sin cambiar la interfaz de la clase.

La filosofía de Python es "somos todos adultos responsables". No se impide el acceso — se indica qué está pensado para uso externo y qué es un detalle interno. Las properties son el puente entre ambos mundos: permiten empezar con atributos públicos simples y añadir lógica (validación, cálculo, restricciones) más tarde sin romper el código que ya usa la clase.

---

## 16.1. Encapsulación en Python

### 16.1.1. Convención de nombre: público, _protegido, __privado

Python usa el prefijo de guiones bajos para indicar el nivel de acceso previsto de un atributo o método:

**Público** (`atributo`): sin guion bajo. Forma parte de la interfaz de la clase. Cualquier código puede leerlo y modificarlo libremente.

```python
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre  # público

u = Usuario("Ana")
print(u.nombre)      # Ana — acceso libre
u.nombre = "María"   # modificación libre
```

**Protegido** (`_atributo`): un guion bajo al inicio. Es una convención que indica "este atributo es un detalle interno — úsalo bajo tu propia responsabilidad". Python no impide el acceso, pero cualquier programador que lea el código entiende que no debería depender de él:

```python
class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self._saldo = saldo    # protegido — detalle interno
        self._movimientos = []  # protegido

    def depositar(self, monto):
        self._saldo += monto
        self._movimientos.append(f"+{monto}")
```

El guion bajo no es una restricción técnica — `cuenta._saldo` funciona perfectamente. Es una señal para otros programadores: "no uses esto directamente, podría cambiar sin aviso".

**Privado** (`__atributo`): dos guiones bajos al inicio. Python aplica **name mangling**: transforma el nombre internamente para dificultar (no impedir) el acceso desde fuera de la clase.

```python
class Secreto:
    def __init__(self):
        self.__clave = "abc123"

s = Secreto()
# print(s.__clave)  # AttributeError: 'Secreto' has no attribute '__clave'
```

El atributo existe, pero Python lo renombró internamente. La sección siguiente explica cómo.

### 16.1.2. Name mangling (__atributo)

Cuando un atributo empieza con dos guiones bajos y **no** termina con dos guiones bajos (los dunder methods como `__init__` quedan excluidos), Python lo renombra internamente a `_NombreClase__atributo`:

```python
class Secreto:
    def __init__(self):
        self.__clave = "abc123"

    def mostrar(self):
        return self.__clave  # dentro de la clase funciona normalmente

s = Secreto()
print(s.mostrar())           # abc123 — acceso interno funciona

# El nombre real en memoria es _Secreto__clave
print(s._Secreto__clave)     # abc123 — se puede acceder, pero no se debe

# Listar atributos revela el nombre real
print([a for a in dir(s) if "clave" in a])  # ['_Secreto__clave']
```

Name mangling **no es un mecanismo de seguridad** — no impide el acceso, solo lo dificulta. Su propósito real es evitar colisiones de nombres en jerarquías de herencia. Si una clase padre y una subclase definen ambas `__atributo`, el mangling les da nombres internos diferentes, evitando que se sobrescriban accidentalmente:

```python
class Padre:
    def __init__(self):
        self.__valor = "padre"

class Hija(Padre):
    def __init__(self):
        super().__init__()
        self.__valor = "hija"  # no sobrescribe, es _Hija__valor

h = Hija()
print(h._Padre__valor)  # padre — intacto
print(h._Hija__valor)   # hija — atributo separado
```

En la práctica, el doble guion bajo se usa poco. La convención de un solo guion bajo (`_atributo`) es suficiente para la mayoría de los casos. `__atributo` se reserva para situaciones donde realmente se necesita evitar colisiones en herencia.

**Resumen de convenciones:**

| Formato | Nombre | Acceso | Uso |
|---------|--------|--------|-----|
| `atributo` | Público | Libre | Interfaz de la clase |
| `_atributo` | Protegido | Libre (convención) | Detalle interno |
| `__atributo` | Privado (mangling) | Renombrado a `_Clase__atributo` | Evitar colisiones en herencia |
| `__atributo__` | Dunder | Libre | Reservado para Python |

---

## 16.2. Properties

### 16.2.1. El problema: acceso directo vs getters/setters

En muchos lenguajes orientados a objetos, se desaconseja el acceso directo a los atributos. En su lugar, se crean métodos getter y setter para controlar el acceso:

```python
# Estilo Java — NO idiomático en Python
class Temperatura:
    def __init__(self, celsius):
        self._celsius = celsius

    def get_celsius(self):
        return self._celsius

    def set_celsius(self, valor):
        if valor < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        self._celsius = valor

t = Temperatura(25)
print(t.get_celsius())    # 25
t.set_celsius(30)         # OK
# t.set_celsius(-300)     # ValueError
```

Esto funciona, pero es verboso y rompe la naturalidad de Python. El código debería ser `t.celsius = 30`, no `t.set_celsius(30)`. Las properties resuelven exactamente esto.

### 16.2.2. @property (getter)

El decorador `@property` convierte un método en un atributo de solo lectura. Se accede a él como un atributo (sin paréntesis), pero internamente ejecuta el método:

```python
class Circulo:
    def __init__(self, radio):
        self._radio = radio

    @property
    def radio(self):
        return self._radio

    @property
    def area(self):
        import math
        return round(math.pi * self._radio ** 2, 2)

c = Circulo(5)
print(c.radio)   # 5 — parece un atributo, pero ejecuta el método
print(c.area)    # 78.54 — calculado al vuelo

# c.radio = 10  # AttributeError: can't set attribute — solo lectura
```

Sin `@property`, `c.radio` devolvería el método en sí (un objeto `function`), no el valor. Con `@property`, Python intercepta el acceso y ejecuta el método automáticamente.

Una property sin setter es de solo lectura. Intentar asignar un valor lanza `AttributeError`.

### 16.2.3. @atributo.setter

Para permitir la asignación con validación, se define un setter usando `@nombre_property.setter`:

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius  # usa el setter, que valida

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):
        return round(self._celsius * 9 / 5 + 32, 2)


t = Temperatura(25)
print(t.celsius)      # 25
print(t.fahrenheit)   # 77.0

t.celsius = 100       # usa el setter — valida antes de asignar
print(t.celsius)      # 100

# t.celsius = -300    # ValueError: Temperatura por debajo del cero absoluto
```

Nótese que en `__init__`, `self.celsius = celsius` ya pasa por el setter. Esto significa que la validación se aplica desde la creación del objeto — no se puede crear una `Temperatura` con un valor inválido.

El patrón es: el atributo interno es `_celsius` (protegido), y la property `celsius` (sin guion bajo) es la interfaz pública que controla el acceso.

### 16.2.4. @atributo.deleter

Se puede definir un deleter para controlar qué ocurre cuando se usa `del` sobre la property:

```python
class Configuracion:
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        self._valor = nuevo

    @valor.deleter
    def valor(self):
        print("Restaurando valor por defecto")
        self._valor = None

c = Configuracion("produccion")
print(c.valor)      # produccion

del c.valor          # Restaurando valor por defecto
print(c.valor)       # None
```

El deleter se usa raramente. En la práctica, la mayoría de las properties solo necesitan getter y setter.

### 16.2.5. Properties calculadas

Una property calculada no almacena un valor — lo calcula cada vez que se accede a ella. Es útil para valores que dependen de otros atributos y deben estar siempre actualizados:

```python
class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    @property
    def area(self):
        return self.base * self.altura

    @property
    def perimetro(self):
        return 2 * (self.base + self.altura)

    @property
    def es_cuadrado(self):
        return self.base == self.altura


r = Rectangulo(5, 3)
print(r.area)          # 15
print(r.perimetro)     # 16
print(r.es_cuadrado)   # False

r.base = 3
print(r.area)          # 9 — se recalcula automáticamente
print(r.es_cuadrado)   # True
```

`area`, `perimetro` y `es_cuadrado` no se almacenan en ningún sitio. Cada acceso ejecuta el método y devuelve el valor actual. Esto elimina el riesgo de que el área quede desincronizada si se modifica `base` o `altura`.

Otro ejemplo práctico — una clase que valida datos con properties:

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario  # pasa por el setter

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("El salario debe ser numérico")
        if valor < 0:
            raise ValueError("El salario no puede ser negativo")
        self._salario = float(valor)

    @property
    def salario_mensual(self):
        return round(self._salario / 12, 2)


e = Empleado("Ana García", 36000)
print(e.nombre)           # Ana García
print(e.salario)          # 36000.0
print(e.salario_mensual)  # 3000.0

e.salario = 42000
print(e.salario_mensual)  # 3500.0

# e.nombre = ""           # ValueError: El nombre no puede estar vacío
# e.salario = -100        # ValueError: El salario no puede ser negativo
```

Las properties son una de las características más elegantes de Python. Permiten empezar con atributos públicos simples (`self.nombre = nombre`) y, si más tarde se necesita validación o lógica adicional, convertirlos en properties **sin cambiar la interfaz** — todo el código existente que usa `obj.nombre` sigue funcionando exactamente igual.
