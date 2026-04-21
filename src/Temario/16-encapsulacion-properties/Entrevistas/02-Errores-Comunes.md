# Errores Comunes: Encapsulación y Properties

## Error 1: Usar `__atributo` creyendo que es privado de verdad

```python
class Secreto:
    def __init__(self, clave):
        self.__clave = clave

s = Secreto("abc123")
# "Es privado, nadie puede acceder"
print(s._Secreto__clave)  # abc123 — accesible vía name mangling
```

El doble guion bajo no es un mecanismo de seguridad. Cualquiera puede acceder al atributo usando `_NombreClase__atributo`. Su propósito real es evitar colisiones en herencia, no proteger datos. Para indicar que algo es interno, basta con `_atributo` (un guion bajo).

---

## Error 2: Property y atributo con el mismo nombre (recursión infinita)

```python
class Producto:
    def __init__(self, precio):
        self.precio = precio

    @property
    def precio(self):
        return self.precio  # MAL — se llama a sí mismo infinitamente

    @precio.setter
    def precio(self, valor):
        self.precio = valor  # MAL — se llama a sí mismo infinitamente
```

Si la property `precio` accede a `self.precio`, vuelve a invocar la property, creando una recursión infinita (`RecursionError`). La solución es usar un atributo interno con nombre diferente (`self._precio`):

```python
@property
def precio(self):
    return self._precio

@precio.setter
def precio(self, valor):
    self._precio = valor
```

---

## Error 3: Asignar al atributo interno en `__init__` saltándose la validación del setter

```python
class Edad:
    def __init__(self, valor):
        self._valor = valor  # MAL — asigna directamente, sin pasar por el setter

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        if nuevo < 0 or nuevo > 150:
            raise ValueError("Edad inválida")
        self._valor = nuevo

e = Edad(-5)           # No lanza error — la validación se saltó
print(e.valor)          # -5
```

En `__init__`, hay que usar `self.valor = valor` (sin guion bajo) para que la asignación pase por el setter y se valide. `self._valor = valor` asigna directamente al atributo interno.

---

## Error 4: Definir el setter sin el getter

```python
class Config:
    @Config.nivel.setter  # NameError — Config.nivel no existe aún
    def nivel(self, valor):
        self._nivel = valor
```

La property (getter) debe definirse primero con `@property`. El setter se define después usando `@nombre.setter`. No se puede crear un setter sin que exista previamente el getter.

```python
# Correcto: primero getter, luego setter
@property
def nivel(self):
    return self._nivel

@nivel.setter
def nivel(self, valor):
    self._nivel = valor
```

---

## Error 5: Usar name mangling accidentalmente con nombres que terminan en __

```python
class Ejemplo:
    def __init__(self):
        self.__datos__ = []  # Esto NO tiene name mangling

e = Ejemplo()
print(e.__datos__)  # [] — accesible directamente
```

Name mangling solo se aplica a nombres que empiezan con dos guiones bajos y **no** terminan con dos guiones bajos. `__datos__` es un nombre estilo dunder y no se renombra. `__datos` (sin guiones al final) sí se renombraría.

---

## Error 6: Property calculada costosa sin caché

```python
class Informe:
    def __init__(self, datos):
        self._datos = datos

    @property
    def analisis(self):
        # Recalcula CADA vez que se accede
        import time
        time.sleep(2)  # simula cálculo costoso
        return sum(self._datos) / len(self._datos)

i = Informe(list(range(1000000)))
print(i.analisis)  # espera 2 segundos
print(i.analisis)  # espera otros 2 segundos — recalcula innecesariamente
```

Una property se ejecuta cada vez que se accede a ella. Si el cálculo es costoso y los datos no cambian frecuentemente, se debería cachear el resultado en un atributo interno e invalidar la caché cuando los datos cambien. Otra opción es usar `@functools.cached_property` (Python 3.8+), que calcula el valor una sola vez.

---

## Error 7: Confundir property con método (olvidar paréntesis o añadir de más)

```python
class Circulo:
    def __init__(self, radio):
        self._radio = radio

    @property
    def area(self):
        import math
        return round(math.pi * self._radio ** 2, 2)

c = Circulo(5)
print(c.area())    # TypeError: 'float' object is not callable
# area es una property, se accede sin paréntesis:
print(c.area)      # 78.54
```

Las properties se acceden como atributos (`c.area`), no como métodos (`c.area()`). Llamar a `c.area()` ejecuta la property (que devuelve un float) y luego intenta "llamar" al float, causando `TypeError`.

---

## Error 8: Crear una property en una clase hija que no sabe del atributo del padre

```python
class Base:
    def __init__(self, valor):
        self.valor = valor

class Hija(Base):
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        self._valor = nuevo * 2

h = Hija(5)
print(h.valor)  # 10 — funciona, pero el __init__ del padre usa self.valor
                 # que ahora pasa por el setter de Hija
```

Esto no es un error en sí — funciona correctamente. Pero puede sorprender: `Base.__init__` asigna `self.valor = valor`, que en `Hija` pasa por el setter de la property (multiplicando por 2). Hay que ser consciente de que las properties de la subclase interceptan las asignaciones del padre.

---

## Error 9: Usar `__atributo` por defecto (sobreuso de name mangling)

```python
# MAL — name mangling en todas partes, sin necesidad
class Usuario:
    def __init__(self, nombre, email, edad):
        self.__nombre = nombre
        self.__email = email
        self.__edad = edad

    def get_nombre(self):
        return self.__nombre
    def set_nombre(self, valor):
        self.__nombre = valor
    # ... getters/setters para todo
```

Esto es código Java escrito en Python. El doble guion bajo hace el código más difícil de depurar (los atributos no aparecen con su nombre esperado en `vars()` o el debugger) y los getters/setters explícitos son innecesarios con properties. La forma Pythónica es usar atributos públicos o `_atributo` con properties si se necesita validación.

---

## Error 10: Olvidar que `del` en una property requiere un deleter explícito

```python
class Sesion:
    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, valor):
        self._token = valor

s = Sesion("abc123")
del s.token  # AttributeError: can't delete attribute
```

Sin un deleter definido con `@token.deleter`, `del s.token` lanza `AttributeError`. Si se necesita soportar `del`, hay que definir el deleter explícitamente.
