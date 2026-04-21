# Errores Comunes: Herencia, Polimorfismo y Composición

## Error 1: No llamar a `super().__init__()` en la subclase

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        # MAL — no llama a super().__init__()
        self.carrera = carrera

e = Estudiante("Ana", 22, "Informática")
print(e.carrera)   # Informática
print(e.nombre)    # AttributeError: 'Estudiante' has no attribute 'nombre'
```

Si la subclase define `__init__`, el del padre no se ejecuta automáticamente. Se debe llamar `super().__init__(nombre, edad)` para que se inicialicen los atributos del padre.

---

## Error 2: Llamar a la clase padre directamente en lugar de usar `super()`

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

class Perro(Animal):
    def __init__(self, nombre, raza):
        # Funciona, pero es frágil
        Animal.__init__(self, nombre)
        self.raza = raza
```

Llamar a `Animal.__init__(self, nombre)` funciona en herencia simple, pero falla con herencia múltiple porque no sigue el MRO. Si `Perro` participa en un diamante, la clase base podría inicializarse dos veces o en orden incorrecto. `super().__init__(nombre)` siempre sigue el MRO correcto.

---

## Error 3: Usar herencia cuando la relación es "tiene un"

```python
# MAL — un Pedido no ES una lista
class Pedido(list):
    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente

p = Pedido("Ana")
p.append({"producto": "Laptop", "precio": 999})
p.sort()        # ¿Ordenar un pedido? No tiene sentido
p.reverse()     # ¿Invertir un pedido? Tampoco
p.insert(0, "basura")  # Rompe la abstracción
```

Un pedido **tiene** una lista de items, no **es** una lista. La composición es correcta:

```python
class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self._items = []

    def agregar(self, item):
        self._items.append(item)
```

---

## Error 4: Olvidar que `super()` sigue el MRO, no el padre directo

```python
class A:
    def metodo(self):
        print("A")

class B(A):
    def metodo(self):
        print("B")
        super().metodo()

class C(A):
    def metodo(self):
        print("C")
        super().metodo()

class D(B, C):
    def metodo(self):
        print("D")
        super().metodo()

D().metodo()
# D
# B
# C  ← super() en B llama a C, no a A (¡sorpresa!)
# A
```

En `B.metodo()`, `super().metodo()` no llama a `A.metodo()` sino a `C.metodo()`, porque el MRO de `D` es `D → B → C → A`. Es correcto, pero puede sorprender si se asume que `super()` siempre va al padre directo.

---

## Error 5: Sobreescribir un método sin llamar a `super()` cuando se necesita

```python
class Registro:
    def __init__(self, datos):
        self.datos = datos
        self.validado = False

    def validar(self):
        if not self.datos:
            raise ValueError("Datos vacíos")
        self.validado = True
        return True

class RegistroEmail(Registro):
    def validar(self):
        # MAL — sobreescribe completamente, no ejecuta la validación base
        if "@" not in self.datos.get("email", ""):
            raise ValueError("Email inválido")
        return True

r = RegistroEmail({"email": "ana@mail.com"})
r.validar()
print(r.validado)  # False — nunca se ejecutó Registro.validar()
```

La subclase reemplazó `validar()` completamente en lugar de extenderlo. Debería llamar a `super().validar()` para ejecutar la validación base y luego añadir la suya.

---

## Error 6: Cadenas de `isinstance()` en lugar de polimorfismo

```python
# MAL — se debe modificar cada vez que se añade un tipo nuevo
def calcular_precio(item):
    if isinstance(item, Libro):
        return item.precio * 0.96  # 4% IVA reducido
    elif isinstance(item, Electronica):
        return item.precio * 1.21  # 21% IVA
    elif isinstance(item, Alimento):
        return item.precio * 1.10  # 10% IVA
    else:
        raise TypeError(f"Tipo desconocido: {type(item)}")
```

Cada nuevo tipo obliga a modificar esta función. La solución es que cada clase defina su propio método:

```python
# BIEN — cada clase sabe calcular su precio
class Libro:
    def precio_final(self):
        return self.precio * 0.96

class Electronica:
    def precio_final(self):
        return self.precio * 1.21
```

---

## Error 7: Jerarquías de herencia demasiado profundas

```python
class Base: pass
class A(Base): pass
class B(A): pass
class C(B): pass
class D(C): pass
class E(D): pass  # 5 niveles de profundidad
```

Las jerarquías profundas son difíciles de entender, depurar y modificar. Un cambio en `Base` puede tener efectos inesperados en `E`. En general, más de 2-3 niveles de herencia es señal de que la composición sería más apropiada.

---

## Error 8: Modificar atributos mutables del padre sin copia

```python
class ConfigBase:
    DEFAULTS = {"debug": False, "verbose": False, "timeout": 30}

    def __init__(self):
        self.config = self.DEFAULTS

class ConfigDev(ConfigBase):
    def __init__(self):
        super().__init__()
        self.config["debug"] = True  # ¡Modifica DEFAULTS de la clase base!

dev = ConfigDev()
prod = ConfigBase()
print(prod.config["debug"])  # True — ¡contaminado!
```

`self.config = self.DEFAULTS` no copia el diccionario — asigna una referencia al mismo objeto. Modificarlo en la subclase afecta a la clase base. La solución es copiar: `self.config = dict(self.DEFAULTS)`.

---

## Error 9: Asumir que `isinstance()` solo comprueba el tipo exacto

```python
class Animal:
    pass

class Perro(Animal):
    pass

p = Perro()

# Sorpresa para quien no sabe de herencia:
print(isinstance(p, Animal))  # True — Perro ES un Animal
print(type(p) == Animal)      # False — el tipo exacto es Perro
```

`isinstance()` recorre toda la cadena de herencia. Si se necesita comprobar el tipo exacto (rara vez necesario), se usa `type(obj) is Clase`. Pero en la inmensa mayoría de los casos, `isinstance()` es lo correcto.

---

## Error 10: Crear un mixin que depende de atributos que no define

```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.datos)  # ¿de dónde sale self.datos?

class Reporte(JsonMixin):
    def __init__(self, titulo):
        self.titulo = titulo

r = Reporte("Ventas Q1")
r.to_json()  # AttributeError: 'Reporte' has no attribute 'datos'
```

El mixin asume que la clase que lo use tiene un atributo `datos`, pero nada lo garantiza. Un mixin debe usar mecanismos genéricos como `vars(self)` o documentar claramente qué atributos espera:

```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(vars(self))
```
