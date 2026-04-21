# Preguntas de Entrevista: Herencia, Polimorfismo y Composición

1. ¿Qué es la herencia en Python y qué relación modela?
2. ¿Qué ocurre si una subclase define `__init__` pero no llama a `super().__init__()`?
3. ¿Qué es el MRO y cómo se puede consultar?
4. ¿Cuál es la diferencia entre sobreescribir y extender un método?
5. ¿Qué es el problema del diamante y cómo lo resuelve Python?
6. ¿Qué es duck typing y por qué es relevante en Python?
7. ¿Por qué el uso excesivo de `isinstance()` suele indicar mal diseño?
8. ¿Cuál es la diferencia entre composición y herencia? ¿Cuándo usar cada una?
9. ¿Por qué heredar de `list` para crear un `Stack` es un antipatrón?
10. ¿Qué es un mixin y cómo se diferencia de la herencia normal?
11. ¿`isinstance(obj, ClasePadre)` devuelve True si `obj` es instancia de una subclase?
12. ¿Cuál es el resultado de este código?
    ```python
    class A:
        def saludar(self):
            return "Hola desde A"

    class B(A):
        pass

    class C(A):
        def saludar(self):
            return "Hola desde C"

    class D(B, C):
        pass

    d = D()
    print(d.saludar())
    print(D.__mro__)
    ```

---

### R1. ¿Qué es la herencia y qué relación modela?

La herencia permite crear una clase nueva (subclase) que recibe atributos y métodos de una clase existente (superclase). Modela una relación **"es un"**: un `Perro` es un `Animal`, un `Email` es una `Notificacion`.

La subclase puede usar todo lo heredado, añadir atributos y métodos propios, o sobreescribir los existentes. En Python, todas las clases heredan implícitamente de `object`.

---

### R2. ¿Qué ocurre si la subclase no llama a `super().__init__()`?

Los atributos que el padre inicializa en su `__init__` no se crean. Si la subclase o algún método heredado intenta acceder a esos atributos, se obtiene `AttributeError`.

Es un error silencioso porque Python no obliga a llamar a `super().__init__()`. El código no falla al crear la instancia, sino más tarde cuando se intenta usar un atributo que nunca se inicializó.

---

### R3. ¿Qué es el MRO y cómo se consulta?

El MRO (Method Resolution Order) es el orden en que Python busca métodos al invocarlos en un objeto. Recorre la clase del objeto, sus padres, los padres de los padres, hasta `object`.

Se consulta con `Clase.__mro__` (tupla) o `Clase.mro()` (lista). Python usa el algoritmo C3 linearization para calcular un orden lineal que respeta la jerarquía de herencia.

---

### R4. Sobreescribir vs extender un método

**Sobreescribir** (override): la subclase redefine el método completamente, reemplazando la versión del padre.

**Extender**: la subclase llama a `super().metodo()` para ejecutar la versión del padre y añade lógica adicional antes o después. Esto permite reutilizar el comportamiento existente en lugar de duplicarlo.

```python
# Sobreescribir — reemplaza completamente
def resumen(self):
    return f"{self.nombre} - Gerente"

# Extender — reutiliza y amplía
def resumen(self):
    return f"{super().resumen()} - Gerente"
```

---

### R5. El problema del diamante

Ocurre cuando una clase hereda de dos clases que a su vez heredan de la misma base, formando un diamante. El riesgo es que el `__init__` de la base se ejecute dos veces.

Python lo resuelve con el MRO (C3 linearization): establece un orden lineal único donde cada clase aparece una sola vez. `super()` sigue este orden, garantizando que la base solo se inicializa una vez.

---

### R6. ¿Qué es duck typing?

Es el principio de que el tipo de un objeto importa menos que los métodos que soporta: "si camina como un pato y grazna como un pato, es un pato". Python no verifica tipos antes de llamar a un método — simplemente lo intenta.

Esto significa que dos clases sin ninguna relación de herencia pueden ser tratadas de forma idéntica si tienen los mismos métodos. Es la base del polimorfismo en Python y hace que el lenguaje sea más flexible que los lenguajes con tipado estricto.

---

### R7. ¿Por qué el uso excesivo de `isinstance()` indica mal diseño?

Porque suele significar que el código está tomando decisiones basándose en el tipo del objeto en lugar de delegar en el objeto mismo. Eso es exactamente lo que el polimorfismo resuelve: cada clase define su propio comportamiento y el código que la usa no necesita saber el tipo concreto.

Cadenas de `if isinstance(x, A) ... elif isinstance(x, B)` son frágiles: si se añade un nuevo tipo, hay que modificar cada punto donde aparece esa cadena.

---

### R8. Composición vs herencia

**Herencia** modela "es un" (un `Email` es una `Notificacion`). La subclase hereda toda la interfaz del padre. El acoplamiento es alto.

**Composición** modela "tiene un" (un `Coche` tiene un `Motor`). El objeto contiene instancias de otras clases como atributos. El acoplamiento es bajo y los componentes son intercambiables.

Regla general: **preferir composición sobre herencia**. Usar herencia solo cuando la relación "es un" es genuina y la subclase puede sustituir al padre en cualquier contexto.

---

### R9. ¿Por qué heredar de `list` para un `Stack` es un antipatrón?

Porque un `Stack` no "es una" lista. Un stack solo debe exponer `push`, `pop` y consulta de tamaño. Al heredar de `list`, el stack hereda `insert`, `remove`, `sort`, `reverse` y decenas de métodos que rompen la abstracción de pila.

La composición es la solución correcta: el stack **tiene** una lista interna pero solo expone los métodos de pila. Esto encapsula la implementación y protege la interfaz.

---

### R10. ¿Qué es un mixin?

Un mixin es una clase pequeña diseñada para ser combinada con otras mediante herencia múltiple. Añade una funcionalidad específica (serialización, logging, validación) sin pretender ser una clase base completa.

Características:
- No tiene `__init__` propio (o tiene uno trivial).
- Añade uno o pocos métodos utilitarios.
- Su nombre termina en `Mixin` por convención.
- No se instancia directamente.

---

### R11. ¿`isinstance` con subclases?

Sí. `isinstance(obj, ClasePadre)` devuelve `True` si `obj` es instancia de `ClasePadre` o de **cualquier subclase** de ella. Esto es coherente con la relación "es un": si un `Perro` es un `Animal`, `isinstance(perro, Animal)` debe ser `True`.

Lo mismo aplica a `issubclass(Hija, Padre)` — devuelve `True` si `Hija` hereda de `Padre` directa o indirectamente.

---

### R12. ¿Cuál es el resultado del código?

```python
class A:
    def saludar(self):
        return "Hola desde A"

class B(A):
    pass

class C(A):
    def saludar(self):
        return "Hola desde C"

class D(B, C):
    pass

d = D()
print(d.saludar())
print(D.__mro__)
```

Salida:

```
Hola desde C
(<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

El MRO de `D` es `D → B → C → A → object`. Cuando se llama `d.saludar()`, Python busca en `D` (no lo tiene), luego en `B` (no lo tiene), luego en `C` (lo tiene) y ejecuta esa versión. Aunque `B` hereda de `A` que tiene `saludar`, `C` está antes en el MRO que `A`.
