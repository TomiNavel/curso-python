# Preguntas de Entrevista: Clases y Objetos

1. ¿Cuál es la diferencia entre una clase y un objeto (instancia)?
2. ¿Qué es `self` y por qué es necesario como primer parámetro de los métodos de instancia?
3. ¿`__init__` es un constructor? ¿Qué hace exactamente?
4. ¿Cuál es la diferencia entre un atributo de instancia y un atributo de clase? ¿Qué pasa si se usa una lista mutable como atributo de clase?
5. ¿Qué es `__slots__` y cuándo conviene usarlo?
6. ¿Cuál es la diferencia entre un método de instancia, un `@classmethod` y un `@staticmethod`?
7. ¿Para qué se usa `@classmethod` como constructor alternativo? ¿Qué ventaja tiene sobre definir una función normal fuera de la clase?
8. ¿Cuál es la diferencia entre `__str__` y `__repr__`? ¿Cuál debe definirse si solo se define uno?
9. ¿Qué ocurre cuando se accede a un atributo de instancia que no existe pero sí existe como atributo de clase?
10. ¿Qué diferencia hay entre `instancia.atributo_clase = valor` y `Clase.atributo_clase = valor`?
11. ¿Por qué en Python todo es un objeto? Da ejemplos de tipos que normalmente no se consideran objetos en otros lenguajes.
12. ¿Cuál es el resultado de este código?
    ```python
    class Contador:
        cuenta = 0

        def __init__(self):
            self.cuenta = Contador.cuenta
            Contador.cuenta += 1

    a = Contador()
    b = Contador()
    c = Contador()
    print(a.cuenta, b.cuenta, c.cuenta, Contador.cuenta)
    ```

---

### R1. ¿Cuál es la diferencia entre una clase y un objeto (instancia)?

Una clase es una plantilla que define la estructura (atributos) y el comportamiento (métodos) de un tipo de dato. Un objeto es una instancia concreta de esa clase, con valores específicos en sus atributos.

La clase `list` define cómo funcionan las listas en Python. `[1, 2, 3]` es un objeto concreto de esa clase. Se pueden crear múltiples objetos de la misma clase, cada uno con datos diferentes pero compartiendo la misma estructura y comportamiento.

---

### R2. ¿Qué es `self` y por qué es necesario?

`self` es una referencia al objeto sobre el que se está ejecutando el método. Python lo pasa automáticamente como primer argumento cuando se llama un método de instancia.

Es necesario porque los métodos se definen una sola vez en la clase, pero se ejecutan sobre instancias diferentes. Sin `self`, el método no sabría sobre qué objeto operar. Cuando se escribe `objeto.metodo()`, Python lo traduce a `Clase.metodo(objeto)` — `self` es ese `objeto`.

El nombre `self` es una convención fuerte de PEP 8, no una palabra reservada. Pero usar otro nombre se considera una violación grave de estilo.

---

### R3. ¿`__init__` es un constructor?

Estrictamente, no. `__init__` es un **inicializador**. El objeto ya existe cuando `__init__` se ejecuta — su trabajo es establecer el estado inicial (asignar atributos).

El verdadero constructor es `__new__`, que crea el objeto en memoria y lo devuelve. Python llama primero a `__new__` para crear el objeto y luego a `__init__` para inicializarlo. En la práctica, `__new__` casi nunca se sobrescribe (solo en casos como singletons o clases inmutables), así que `__init__` se trata como el "constructor" en el uso cotidiano.

---

### R4. Atributos de instancia vs atributos de clase. ¿Qué pasa con listas mutables?

Los atributos de instancia se definen con `self.atributo` en `__init__` — cada objeto tiene su propia copia. Los atributos de clase se definen en el cuerpo de la clase — son compartidos por todas las instancias.

Con tipos inmutables (int, str) no suele haber problema porque la reasignación crea un atributo de instancia que oculta al de clase. Pero con tipos mutables (listas, diccionarios), todas las instancias comparten el mismo objeto. Modificarlo desde una instancia afecta a todas las demás:

```python
class Grupo:
    miembros = []  # compartida

Grupo().miembros.append("Ana")
print(Grupo().miembros)  # ["Ana"] — todas las instancias afectadas
```

La solución es inicializar listas y diccionarios como atributos de instancia en `__init__`.

---

### R5. ¿Qué es `__slots__` y cuándo conviene usarlo?

`__slots__` es una declaración de clase que restringe los atributos permitidos a una lista fija. Python reemplaza el `__dict__` dinámico por una estructura fija, ahorrando memoria y ganando velocidad de acceso.

Conviene usarlo cuando se crean muchas instancias de una clase simple (millones de objetos con pocos atributos). No conviene cuando se necesitan atributos dinámicos.

La ventaja adicional es que previene errores de tipeo: `self.nomber` en lugar de `self.nombre` lanza `AttributeError` inmediatamente.

---

### R6. Diferencia entre método de instancia, @classmethod y @staticmethod

- **Método de instancia**: recibe `self`, tiene acceso a la instancia y sus atributos. Es el tipo más común.
- **@classmethod**: recibe `cls` (la clase), no tiene acceso a instancias específicas. Se usa para constructores alternativos y operaciones sobre la clase.
- **@staticmethod**: no recibe ni `self` ni `cls`. Es una función normal que vive dentro de la clase por organización.

---

### R7. ¿Qué ventaja tiene `@classmethod` como constructor alternativo sobre una función normal?

Un `@classmethod` vive dentro de la clase, lo que tiene varias ventajas sobre una función libre:

1. **Organización**: el constructor alternativo está junto a la clase que construye, no disperso en el módulo.
2. **Acceso a atributos de clase**: puede leer y modificar atributos de clase directamente a través de `cls`.
3. **Descubrimiento**: al hacer `dir(MiClase)` o leer el código, los constructores alternativos son visibles como parte de la interfaz de la clase.

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    @classmethod
    def desde_string(cls, texto):
        nombre, salario = texto.split(",")
        return cls(nombre, int(salario))

# La creación desde string es parte de la interfaz de Empleado
bob = Empleado.desde_string("Bob,45000")
```

Una función libre `crear_empleado_desde_string()` haría lo mismo, pero no estaría asociada a la clase ni aparecería como parte de su interfaz.

---

### R8. Diferencia entre `__str__` y `__repr__`

`__repr__` es la representación "oficial", orientada al desarrollador. Debe ser no ambigua e idealmente una expresión Python válida que recree el objeto. Se usa en el intérprete, en logs y como fallback de `__str__`.

`__str__` es la representación "informal", orientada al usuario. Debe ser legible. Se usa con `print()` y `str()`.

Si solo se define uno, debe ser `__repr__`, porque Python lo usa como fallback cuando `__str__` no existe. Lo contrario no ocurre: si solo hay `__str__`, `repr()` muestra el formato por defecto.

---

### R9. Acceso a atributo de clase desde la instancia

Python busca atributos en este orden: primero en la instancia, luego en la clase. Si un atributo no existe en la instancia pero sí en la clase, Python devuelve el de la clase.

Esto hace que los atributos de clase parezcan "heredados" por las instancias. Pero es solo lectura — la asignación siempre crea un atributo de instancia.

---

### R10. `instancia.atributo = valor` vs `Clase.atributo = valor`

`instancia.atributo = valor` crea un atributo de instancia que oculta al atributo de clase. El atributo de clase no se modifica; la instancia simplemente tiene ahora su propio atributo con el mismo nombre que le hace "sombra".

`Clase.atributo = valor` modifica el atributo de clase directamente. Todas las instancias que no tengan un atributo de instancia con ese nombre verán el nuevo valor.

Esta asimetría entre lectura y escritura es una fuente frecuente de bugs.

---

### R11. ¿Por qué en Python todo es un objeto?

En Python, absolutamente todo es un objeto: los enteros, los strings, las funciones, las clases, los módulos e incluso `None`. Todos tienen tipo (`type()`), identidad (`id()`) y pueden tener atributos.

```python
def saludar():
    pass

print(type(42))         # <class 'int'>
print(type(saludar))    # <class 'function'>
print(type(int))        # <class 'type'>
saludar.autor = "Ana"   # se pueden añadir atributos a una función
```

En lenguajes como Java o C++, los tipos primitivos (`int`, `boolean`) no son objetos — son valores "planos" sin métodos. En Python, `(42).bit_length()` es válido porque `42` es un objeto de la clase `int` con métodos propios.

---

### R12. ¿Cuál es el resultado del código?

```python
class Contador:
    cuenta = 0

    def __init__(self):
        self.cuenta = Contador.cuenta
        Contador.cuenta += 1

a = Contador()
b = Contador()
c = Contador()
print(a.cuenta, b.cuenta, c.cuenta, Contador.cuenta)
```

Salida:

```
0 1 2 3
```

Cada instancia guarda en `self.cuenta` el valor actual de `Contador.cuenta` y luego incrementa el atributo de clase. `a` se crea cuando `Contador.cuenta` vale 0, `b` cuando vale 1, `c` cuando vale 2. Después de las tres creaciones, `Contador.cuenta` vale 3.

`a.cuenta`, `b.cuenta` y `c.cuenta` son atributos de instancia (creados con `self.cuenta = ...`), no leen el atributo de clase. `Contador.cuenta` es el atributo de clase, que terminó en 3.
