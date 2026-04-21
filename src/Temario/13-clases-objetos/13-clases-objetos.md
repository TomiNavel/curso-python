# 13. Clases y Objetos

Hasta ahora, los programas que hemos escrito usan funciones para organizar la lógica y estructuras de datos como listas y diccionarios para agrupar información. Esto funciona bien para problemas pequeños, pero cuando los datos y las operaciones que los manipulan están estrechamente relacionados, tiene sentido agruparlos en una unidad coherente. Eso es exactamente lo que hace una clase: define un tipo nuevo que encapsula datos (atributos) y comportamiento (métodos) en un mismo objeto. Python es un lenguaje orientado a objetos — de hecho, todo en Python es un objeto: los enteros, las listas, las funciones, los módulos. Este tema enseña a crear los propios.

---

## 13.1. Conceptos fundamentales

### 13.1.1. Qué es una clase y qué es un objeto

Una **clase** es un molde o plantilla que define la estructura y el comportamiento de un tipo de dato. Un **objeto** (o **instancia**) es una copia concreta creada a partir de esa plantilla, con sus propios datos.

La analogía más directa: una clase es como el plano de una casa. El plano define cuántas habitaciones hay, dónde está la cocina y cómo es la estructura. Pero no se puede vivir en un plano — se necesita construir una casa concreta (un objeto) a partir de él. Se pueden construir muchas casas con el mismo plano, y cada una tendrá su propia dirección, sus propios muebles y su propio color de pared, pero todas comparten la misma estructura.

En términos técnicos:
- La **clase** define qué atributos (datos) y qué métodos (funciones) tendrán los objetos.
- El **objeto** es una instancia concreta con valores específicos para esos atributos.

```python
# int es una clase. El número 42 es un objeto (instancia) de esa clase.
numero = 42
print(type(numero))  # <class 'int'>

# list es una clase. [1, 2, 3] es un objeto de esa clase.
lista = [1, 2, 3]
print(type(lista))   # <class 'list'>

# Cada objeto tiene su propia identidad
otra_lista = [1, 2, 3]
print(lista == otra_lista)   # True — mismo contenido
print(lista is otra_lista)   # False — objetos diferentes en memoria
```

### 13.1.2. Definir una clase y crear instancias

Una clase se define con la palabra clave `class`, seguida del nombre (por convención en PascalCase) y dos puntos:

```python
class Producto:
    pass  # clase vacía por ahora

# Crear instancias (objetos) de la clase
producto1 = Producto()
producto2 = Producto()

print(type(producto1))           # <class '__main__.Producto'>
print(isinstance(producto1, Producto))  # True
print(producto1 is producto2)    # False — dos objetos diferentes
```

Cada vez que se llama a `Producto()` se crea un nuevo objeto en memoria. `producto1` y `producto2` son dos instancias distintas de la misma clase, igual que `[1, 2]` y `[3, 4]` son dos instancias distintas de `list`.

### 13.1.3. El método \_\_init\_\_ y self

Cuando se crea una instancia con `Producto("Laptop", 999)`, Python necesita un lugar donde asignar los valores iniciales del objeto. Ese lugar es `__init__`: un método especial que Python ejecuta automáticamente justo después de crear la instancia. Su único propósito es establecer el estado inicial del objeto asignándole sus atributos.

```python
class Producto:
    def __init__(self, nombre, precio, stock=0):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

laptop = Producto("Laptop", 999, 50)
mouse = Producto("Mouse", 25)       # stock usa el valor por defecto

print(laptop.nombre)  # Laptop
print(laptop.precio)  # 999
print(mouse.stock)    # 0
```

**`self`** es el mecanismo que permite que un método sepa sobre qué objeto está operando. Cuando se escribe `laptop.nombre`, Python necesita saber que `nombre` pertenece a `laptop` y no a `mouse`. `self` es esa referencia: apunta al objeto concreto sobre el que se llama el método.

`self` es siempre el primer parámetro de cualquier método de instancia, y Python lo pasa automáticamente — nunca se escribe al llamar al método:

```python
laptop = Producto("Laptop", 999, 50)
# Python internamente hace:
# Producto.__init__(laptop, "Laptop", 999, 50)
#                   ↑ self = laptop (pasado automáticamente)
```

Por eso `self.nombre = nombre` dentro de `__init__` crea el atributo `nombre` en el objeto específico (`laptop` o `mouse`), no en la clase. Cada instancia tiene su propia copia independiente de los atributos definidos con `self`.

El nombre `self` es una convención fuerte (PEP 8) — técnicamente Python acepta cualquier nombre, pero usar otro se considera una violación de estilo grave.

> **Nota:** `__init__` no crea el objeto — cuando se ejecuta, el objeto ya existe. La creación real la hace `__new__`, un método que raramente se necesita sobreescribir. En la práctica, `__init__` es donde se trabaja siempre.

Python también permite añadir atributos a un objeto de forma dinámica, fuera de la clase, en cualquier momento:

```python
producto1.nombre = "Laptop"
producto1.precio = 999

print(producto1.nombre)          # Laptop
print(producto2.nombre)          # AttributeError — producto2 no tiene ese atributo
```

Esto funciona porque Python almacena los atributos de cada objeto en un diccionario interno (`__dict__`), y se puede añadir entradas a ese diccionario en cualquier momento. Sin embargo, hacerlo rompe la garantía de que todos los objetos de la clase tienen la misma estructura: `producto1` tendría `nombre` y `precio`, pero `producto2` no. Esto hace el código impredecible y propenso a errores difíciles de detectar.

Por eso los atributos siempre deben definirse en `__init__`: garantiza que cada objeto nace con exactamente los mismos atributos, con independencia de cómo o dónde se use.

### 13.1.4. Atributos de instancia vs atributos de clase

Los **atributos de instancia** se definen con `self.atributo` dentro de `__init__` (o cualquier método). Cada objeto tiene su propia copia — modificar uno no afecta a los demás.

Los **atributos de clase** se definen directamente en el cuerpo de la clase, fuera de cualquier método. Son compartidos por todas las instancias.

```python
class Empleado:
    # Atributo de clase — compartido por todos los objetos
    empresa = "TechCorp"
    total_empleados = 0

    def __init__(self, nombre, salario):
        # Atributos de instancia — propios de cada objeto
        self.nombre = nombre
        self.salario = salario
        Empleado.total_empleados += 1

ana = Empleado("Ana", 50000)
bob = Empleado("Bob", 45000)

# Atributos de clase — accesibles desde la clase y desde las instancias
print(Empleado.empresa)         # TechCorp
print(ana.empresa)              # TechCorp
print(Empleado.total_empleados) # 2

# Atributos de instancia — propios de cada objeto
print(ana.nombre)   # Ana
print(bob.nombre)   # Bob
```

Hay una trampa importante con los atributos de clase. Cuando se accede a `instancia.atributo`, Python busca primero en la instancia y luego en la clase. Pero si se asigna `instancia.atributo = valor`, se crea un atributo de instancia que oculta al de clase:

```python
# Leer — busca en la instancia, no lo encuentra, sube a la clase
print(ana.empresa)     # "TechCorp" (del atributo de clase)

# Escribir — crea un atributo de INSTANCIA que oculta al de clase
ana.empresa = "OtraCorp"
print(ana.empresa)     # "OtraCorp" (atributo de instancia)
print(bob.empresa)     # "TechCorp" (sigue leyendo el de clase)
print(Empleado.empresa)  # "TechCorp" (el de clase no cambió)
```

Esta asimetría entre lectura y escritura es una fuente frecuente de bugs. Para modificar un atributo de clase, siempre usar `Clase.atributo = valor`, nunca `instancia.atributo = valor`.

Con tipos mutables (listas, diccionarios) el comportamiento es especialmente peligroso:

```python
class Equipo:
    # MAL — lista compartida como atributo de clase
    miembros = []

    def __init__(self, nombre):
        self.nombre = nombre

equipo_a = Equipo("Frontend")
equipo_b = Equipo("Backend")

equipo_a.miembros.append("Ana")    # modifica la lista compartida
print(equipo_b.miembros)           # ["Ana"] — ¡afectado!
```

La solución es que las listas y diccionarios siempre sean atributos de instancia, inicializados en `__init__`:

```python
class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []  # cada instancia tiene su propia lista
```

### 13.1.5. \_\_slots\_\_

Por defecto, Python almacena los atributos de cada instancia en un diccionario interno llamado `__dict__`. Esto permite añadir atributos dinámicamente, pero consume más memoria.

`__slots__` es una declaración a nivel de clase que restringe los atributos permitidos. Python reemplaza el diccionario dinámico por una estructura fija, más eficiente en memoria:

```python
class Punto:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punto(3, 5)
print(p.x)        # 3

# No se pueden añadir atributos que no estén en __slots__
# p.z = 10        # AttributeError: 'Punto' object has no attribute 'z'

# No existe __dict__
# print(p.__dict__)  # AttributeError
```

Las ventajas de `__slots__`:
- **Menor consumo de memoria** — significativo cuando se crean millones de instancias (por ejemplo, nodos de un árbol, puntos en un gráfico).
- **Acceso ligeramente más rápido** — los atributos se almacenan en posiciones fijas.
- **Previene errores de tipeo** — no se pueden crear atributos por accidente (`self.nomber` en lugar de `self.nombre` lanzaría error).

Las desventajas:
- **Sin atributos dinámicos** — no se pueden añadir atributos que no estén declarados.
- **Sin `__dict__`** — algunas herramientas de introspección no funcionan.

En la práctica, `__slots__` se usa en clases simples con muchas instancias. Para clases normales, el `__dict__` por defecto es suficiente.

---

## 13.2. Métodos

### 13.2.1. Métodos de instancia

Un método de instancia es una función definida dentro de una clase que opera sobre una instancia específica. Recibe `self` como primer parámetro, lo que le da acceso a los atributos y otros métodos del objeto.

```python
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.saldo += monto
        return self.saldo

    def retirar(self, monto):
        if monto > self.saldo:
            raise ValueError(f"Saldo insuficiente: {self.saldo}")
        self.saldo -= monto
        return self.saldo

    def resumen(self):
        return f"Cuenta de {self.titular}: ${self.saldo:,.2f}"


cuenta = CuentaBancaria("Ana", 1000)
cuenta.depositar(500)
cuenta.retirar(200)
print(cuenta.resumen())  # Cuenta de Ana: $1,300.00
```

Cuando se llama `cuenta.depositar(500)`, Python lo traduce automáticamente a `CuentaBancaria.depositar(cuenta, 500)`. El objeto `cuenta` se pasa como `self`.

Los métodos de instancia son, con diferencia, el tipo de método más común. Representan acciones que un objeto puede realizar sobre sí mismo.

### 13.2.2. Métodos de clase (@classmethod)

Un método de clase recibe la clase como primer argumento (por convención `cls`) en lugar de una instancia. Se define con el decorador `@classmethod`.

```python
class Empleado:
    total = 0

    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
        Empleado.total += 1

    @classmethod
    def desde_string(cls, texto):
        """Crea un Empleado a partir de un string 'nombre,salario'"""
        nombre, salario = texto.split(",")
        return cls(nombre, int(salario))

    @classmethod
    def obtener_total(cls):
        return cls.total


# Crear con el constructor normal
ana = Empleado("Ana", 50000)

# Crear con el constructor alternativo (classmethod)
bob = Empleado.desde_string("Bob,45000")

print(bob.nombre)              # Bob
print(bob.salario)             # 45000
print(Empleado.obtener_total())  # 2
```

El uso principal de `@classmethod` es crear **constructores alternativos** — formas diferentes de crear instancias de la clase. El patrón `cls(...)` dentro del classmethod llama al `__init__` de la clase. Se usa `cls(...)` en lugar de `Empleado(...)` directamente porque `cls` hace el código más flexible (la razón se verá en el tema 15, herencia).

Otros usos comunes:
- Acceder o modificar atributos de clase (como `obtener_total`).
- Factory methods que crean instancias a partir de diferentes formatos de datos.

### 13.2.3. Métodos estáticos (@staticmethod)

Un método estático no recibe ni `self` ni `cls`. Es simplemente una función normal que vive dentro de la clase por razones de organización — está lógicamente relacionada con la clase pero no necesita acceder a la instancia ni a la clase.

```python
class Validador:
    def __init__(self, datos):
        self.datos = datos
        self.errores = []

    @staticmethod
    def es_email_valido(email):
        """Verifica si un string tiene formato básico de email"""
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def es_edad_valida(edad):
        return isinstance(edad, int) and 0 <= edad <= 150

    def validar(self):
        if not self.es_email_valido(self.datos.get("email", "")):
            self.errores.append("Email inválido")
        if not self.es_edad_valida(self.datos.get("edad", -1)):
            self.errores.append("Edad inválida")
        return len(self.errores) == 0


# Se puede llamar sin crear una instancia
print(Validador.es_email_valido("ana@mail.com"))  # True
print(Validador.es_email_valido("invalido"))       # False

# También se puede llamar desde una instancia
v = Validador({"email": "bob@mail.com", "edad": 30})
print(v.validar())  # True
```

Un método estático es equivalente a una función normal fuera de la clase. La ventaja de ponerlo dentro es puramente organizativa: si `es_email_valido` solo se usa en el contexto de `Validador`, tiene sentido que viva dentro de esa clase.

### 13.2.4. Cuándo usar cada tipo

| Tipo | Primer argumento | Acceso a instancia | Acceso a clase | Uso principal |
|------|------------------|--------------------|----------------|---------------|
| Instancia | `self` | Sí | Sí (vía `self.__class__` o nombre) | Operaciones sobre el objeto |
| Clase | `cls` | No | Sí | Constructores alternativos, operaciones sobre la clase |
| Estático | ninguno | No | No | Utilidades relacionadas con la clase |

La regla general:

- **Método de instancia** (el más común): cuando el método necesita leer o modificar atributos del objeto.
- **@classmethod**: cuando el método necesita crear instancias (constructores alternativos) o trabajar con atributos de clase, especialmente si debe funcionar correctamente con herencia.
- **@staticmethod**: cuando el método es una utilidad que no necesita ni la instancia ni la clase. Si dudas entre `@staticmethod` y una función libre fuera de la clase, la pregunta es si la función tiene sentido fuera del contexto de la clase. Si sí, es mejor una función libre.

---

## 13.3. Representación de objetos

### 13.3.1. \_\_str\_\_ y \_\_repr\_\_

Por defecto, imprimir un objeto muestra algo como `<__main__.Producto object at 0x7f...>` — la clase y la dirección de memoria. Esto no es útil ni para depuración ni para el usuario. Los métodos `__str__` y `__repr__` permiten definir cómo se muestra el objeto.

**`__repr__`** — representación "oficial" del objeto. Debe ser una cadena no ambigua, idealmente una expresión Python válida que recree el objeto. Es lo que se muestra en el intérprete interactivo y cuando se usa `repr()`.

**`__str__`** — representación "informal", orientada al usuario. Debe ser legible y clara. Es lo que se usa con `print()` y `str()`.

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f"Producto({self.nombre!r}, {self.precio})"

    def __str__(self):
        return f"{self.nombre} - ${self.precio:,.2f}"


laptop = Producto("Laptop", 999.99)

# __str__ — orientado al usuario
print(laptop)         # Laptop - $999.99
print(str(laptop))    # Laptop - $999.99

# __repr__ — orientado al desarrollador
print(repr(laptop))   # Producto('Laptop', 999.99)

# En el intérprete interactivo o en listas, Python usa __repr__
productos = [Producto("Mouse", 25), Producto("Teclado", 75)]
print(productos)      # [Producto('Mouse', 25), Producto('Teclado', 75)]
```

El uso de `!r` en el f-string (`self.nombre!r`) aplica `repr()` al valor, lo que añade comillas a los strings. Esto es importante para que `Producto('Laptop', 999.99)` sea una expresión Python válida que se pueda copiar y ejecutar.

Si solo se define uno de los dos, las reglas son:

- Si solo hay `__repr__`, Python lo usa también para `print()` y `str()`. Es decir, `__repr__` sirve como fallback.
- Si solo hay `__str__`, `repr()` sigue mostrando el formato por defecto (`<Producto object at 0x...>`).

Por eso, si solo se va a definir uno, debe ser `__repr__`. Es el más versátil: sirve para depuración, para logs, como fallback de `__str__` y como representación en colecciones.

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punto({self.x}, {self.y})"

    # Sin __str__ — print() usa __repr__ como fallback
p = Punto(3, 5)
print(p)        # Punto(3, 5) — usa __repr__
print(repr(p))  # Punto(3, 5)
```

Un caso de uso donde ambos se diferencian claramente:

```python
class Fecha:
    def __init__(self, dia, mes, anio):
        self.dia = dia
        self.mes = mes
        self.anio = anio

    def __repr__(self):
        return f"Fecha({self.dia}, {self.mes}, {self.anio})"

    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.anio}"

fecha = Fecha(9, 4, 2026)
print(fecha)        # 09/04/2026 — legible para el usuario
print(repr(fecha))  # Fecha(9, 4, 2026) — útil para el desarrollador
```

## 13.4. Introspección de atributos

Hasta ahora hemos accedido a los atributos de un objeto con la sintaxis de punto (`obj.atributo`). Esto funciona cuando se conoce el nombre del atributo en tiempo de escritura del código. Pero hay situaciones en las que el nombre del atributo no se conoce hasta el tiempo de ejecución: por ejemplo, cuando se lee de un archivo de configuración, de un JSON, o cuando se construyen herramientas genéricas que trabajan con objetos arbitrarios.

Para estos casos, Python ofrece cuatro funciones built-in que permiten manipular atributos a partir de su nombre como cadena: `getattr`, `setattr`, `hasattr` y `delattr`. Forman lo que se conoce como **introspección**: la capacidad de un programa de examinar y modificar su propia estructura en tiempo de ejecución.

### 13.4.1. getattr() y setattr()

`getattr(objeto, "nombre")` devuelve el valor del atributo cuyo nombre se pasa como string. Es el equivalente dinámico a `objeto.nombre`. Su gran ventaja es que acepta un **valor por defecto** opcional como tercer argumento: si el atributo no existe, en lugar de lanzar `AttributeError`, devuelve ese valor por defecto. Esto lo hace mucho más seguro que el acceso directo cuando no se sabe con certeza si el atributo está presente.

`setattr(objeto, "nombre", valor)` asigna un valor a un atributo cuyo nombre se pasa como string. Es el equivalente dinámico a `objeto.nombre = valor`. Permite crear atributos nuevos o modificar los existentes sin tener que escribir el nombre de forma literal en el código.

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

p = Producto("Laptop", 999)

# getattr — acceso dinámico por nombre
print(getattr(p, "nombre"))           # "Laptop" — equivale a p.nombre
print(getattr(p, "stock", 0))         # 0 — atributo no existe, usa el default
print(getattr(p, "stock"))            # AttributeError — sin default, falla

# setattr — asignación dinámica por nombre
setattr(p, "precio", 1099)            # equivale a p.precio = 1099
setattr(p, "categoria", "Electrónica")  # crea un atributo nuevo
print(p.precio)      # 1099
print(p.categoria)   # "Electrónica"

# Caso de uso típico: cargar atributos desde un diccionario
datos = {"nombre": "Mouse", "precio": 25, "color": "negro"}
otro = Producto("temp", 0)
for clave, valor in datos.items():
    setattr(otro, clave, valor)
# otro ahora tiene nombre="Mouse", precio=25, color="negro"
```

### 13.4.2. hasattr() y delattr()

`hasattr(objeto, "nombre")` devuelve `True` si el objeto tiene un atributo con ese nombre, y `False` en caso contrario. Internamente equivale a hacer un `getattr` y comprobar si lanza `AttributeError`. Es la forma estándar de comprobar la existencia de un atributo antes de usarlo.

`delattr(objeto, "nombre")` elimina un atributo del objeto. Es el equivalente dinámico a `del objeto.nombre`. Una vez eliminado, intentar acceder a él lanza `AttributeError`. Se usa con poca frecuencia, pero resulta útil cuando se trabaja con objetos cuya estructura cambia en tiempo de ejecución.

```python
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.email = None

u = Usuario("Ana")

# hasattr — comprobar existencia antes de usar
if hasattr(u, "email"):
    print(f"Email: {u.email}")

if not hasattr(u, "telefono"):
    setattr(u, "telefono", "no especificado")

# delattr — eliminar un atributo
delattr(u, "email")          # equivale a del u.email
print(hasattr(u, "email"))   # False — ya no existe
print(u.email)               # AttributeError
```

Estas cuatro funciones son la base de muchas herramientas avanzadas de Python: serializadores como `json` y `pickle`, ORMs como SQLAlchemy, frameworks de testing y cualquier código que necesite trabajar con objetos sin conocer su estructura de antemano. En el código del día a día se usan menos que el acceso directo con punto, pero saber que existen abre la puerta a soluciones que de otra forma serían imposibles.
