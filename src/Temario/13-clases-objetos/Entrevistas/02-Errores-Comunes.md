# Errores Comunes: Clases y Objetos

## Error 1: Olvidar `self` en la definición del método

```python
class Calculadora:
    def __init__(self, valor):
        self.valor = valor

    # MAL — falta self como primer parámetro
    def duplicar():
        return self.valor * 2

calc = Calculadora(5)
calc.duplicar()
# TypeError: Calculadora.duplicar() takes 0 positional arguments but 1 was given
```

Python pasa la instancia automáticamente como primer argumento. Si el método no declara `self`, recibe un argumento que no esperaba. La solución es añadir `self` como primer parámetro: `def duplicar(self):`.

---

## Error 2: Olvidar `self.` al asignar atributos en `__init__`

```python
class Usuario:
    def __init__(self, nombre, email):
        nombre = nombre     # crea variable local, NO atributo
        self.email = email

u = Usuario("Ana", "ana@mail.com")
print(u.email)    # ana@mail.com
print(u.nombre)   # AttributeError: 'Usuario' object has no attribute 'nombre'
```

Sin `self.`, la asignación crea una variable local dentro de `__init__` que se pierde al terminar el método. El atributo nunca se crea en el objeto. La solución es `self.nombre = nombre`.

---

## Error 3: Lista mutable como atributo de clase

```python
class Carrito:
    items = []  # compartida entre TODAS las instancias

    def __init__(self, usuario):
        self.usuario = usuario

    def agregar(self, item):
        self.items.append(item)

carrito_ana = Carrito("Ana")
carrito_bob = Carrito("Bob")

carrito_ana.agregar("Laptop")
print(carrito_bob.items)  # ["Laptop"] — ¡Bob ve los items de Ana!
```

La lista `items` es un atributo de clase compartido por todas las instancias. `self.items.append(...)` modifica esa lista compartida sin crear una copia en la instancia. La solución es inicializar la lista en `__init__`:

```python
class Carrito:
    def __init__(self, usuario):
        self.usuario = usuario
        self.items = []  # cada instancia tiene su propia lista
```

---

## Error 4: Confundir atributo de clase con atributo de instancia al asignar

```python
class Config:
    debug = False

c1 = Config()
c2 = Config()

# Esto NO modifica el atributo de clase — crea uno de instancia
c1.debug = True
print(c1.debug)       # True (atributo de instancia)
print(c2.debug)       # False (sigue leyendo el de clase)
print(Config.debug)   # False (el de clase no cambió)
```

La asignación `instancia.atributo = valor` siempre crea un atributo de instancia, nunca modifica el de clase. Para modificar el atributo de clase se debe usar `Config.debug = True`. Esta asimetría entre lectura y escritura es una fuente frecuente de confusión.

---

## Error 5: Llamar al método sin paréntesis

```python
class Sensor:
    def __init__(self, valor):
        self.valor = valor

    def leer(self):
        return self.valor

s = Sensor(42)
print(s.leer)    # <bound method Sensor.leer of <Sensor object ...>>
print(s.leer())  # 42
```

Sin paréntesis, `s.leer` devuelve una referencia al método, no lo ejecuta. Es un error silencioso porque no lanza excepción — simplemente muestra la representación del objeto método. La solución es añadir paréntesis: `s.leer()`.

---

## Error 6: Usar `self` en lugar de `cls` en un `@classmethod`

```python
class Registro:
    total = 0

    def __init__(self, nombre):
        self.nombre = nombre
        Registro.total += 1

    @classmethod
    def obtener_total(self):  # MAL — debería ser cls
        return self.total

Registro.obtener_total()
# TypeError: Registro.obtener_total() missing 1 required positional argument: 'self'
```

Un `@classmethod` recibe la clase como primer argumento, no una instancia. El parámetro debe llamarse `cls` (por convención) y se pasa automáticamente al llamar `Clase.metodo()`. Usar `self` no causa error de sintaxis, pero genera confusión y el mensaje de error es poco claro porque Python intenta pasar la clase como `self`.

---

## Error 7: Usar `@staticmethod` cuando se necesita acceso a la instancia

```python
class Pedido:
    def __init__(self, items):
        self.items = items

    @staticmethod
    def calcular_total():
        # No tiene acceso a self — no puede leer self.items
        return sum(item["precio"] for item in self.items)
        # NameError: name 'self' is not defined

p = Pedido([{"precio": 10}, {"precio": 20}])
p.calcular_total()
```

Un `@staticmethod` no recibe `self`. Si el método necesita acceder a atributos del objeto, debe ser un método de instancia (sin decorador). Solo usar `@staticmethod` para funciones que no necesitan ni la instancia ni la clase.

---

## Error 8: Definir `__str__` pero no `__repr__`

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

p = Producto("Laptop", 999)
print(p)        # Laptop - $999 — funciona
print(repr(p))  # <__main__.Producto object at 0x...> — inútil para debug

# En listas, Python usa __repr__, no __str__
productos = [Producto("Mouse", 25), Producto("Teclado", 75)]
print(productos)  # [<__main__.Producto object at ...>, ...] — ilegible
```

Si solo se define `__str__`, la representación en colecciones y en modo debug sigue siendo ilegible. `__repr__` debería definirse siempre, ya que sirve como fallback de `__str__`.

---

## Error 9: Crear instancias sin paréntesis

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# MAL — sin paréntesis, p es la CLASE, no una instancia
p = Punto
print(type(p))  # <class 'type'> — es la clase misma

# BIEN
p = Punto(3, 5)
print(type(p))  # <class '__main__.Punto'>
```

Sin paréntesis, se asigna la clase a la variable, no se crea una instancia. Es un error silencioso: no lanza excepción, pero `p` es la clase `Punto`, no un objeto de tipo `Punto`.

---

## Error 10: Comparar objetos sin definir `__eq__`

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Punto(3, 5)
p2 = Punto(3, 5)

print(p1 == p2)  # False — compara por identidad (is), no por valor
```

Por defecto, `==` entre objetos compara identidad (si son el mismo objeto en memoria), no igualdad de contenido. Para comparar por valores, se debe definir `__eq__`. Esto se verá en el tema 14 (Dunder Methods), pero es importante saber que el comportamiento por defecto no compara atributos.
