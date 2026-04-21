# Preguntas de Entrevista: Encapsulación y Properties

1. ¿Python tiene atributos privados como Java o C#? ¿Cómo se controla el acceso a los atributos?
2. ¿Cuál es la diferencia entre `_atributo` y `__atributo`?
3. ¿Qué es name mangling y cuál es su propósito real?
4. ¿Qué es una property y qué problema resuelve?
5. ¿Por qué se desaconsejan los métodos `get_x()` y `set_x()` explícitos en Python?
6. ¿Qué ocurre si se define `@property` sin setter e intentas asignar un valor?
7. ¿Cómo se aplica la validación desde `__init__` si el atributo usa una property con setter?
8. ¿Qué es una property calculada y cuándo conviene usarla?
9. ¿Se puede acceder a un atributo con name mangling desde fuera de la clase?
10. ¿Cuál es la ventaja principal de las properties respecto a la compatibilidad hacia atrás?
11. ¿Cuándo se usa `__atributo` (doble guion bajo) en la práctica?
12. ¿Cuál es el resultado de este código?
    ```python
    class Producto:
        def __init__(self, nombre, precio):
            self.nombre = nombre
            self.precio = precio

        @property
        def precio(self):
            return self._precio

        @precio.setter
        def precio(self, valor):
            if valor < 0:
                self._precio = 0
            else:
                self._precio = valor

        @property
        def con_iva(self):
            return round(self._precio * 1.21, 2)

    p = Producto("Laptop", -50)
    print(p.precio)
    print(p.con_iva)
    p.precio = 100
    print(p.precio)
    print(p.con_iva)
    ```

---

### R1. ¿Python tiene atributos privados?

No en el sentido de Java o C#. Python no tiene una palabra clave `private` que impida el acceso. En su lugar, usa convenciones de nombrado: `_atributo` indica "detalle interno" y `__atributo` aplica name mangling que dificulta el acceso. Pero ninguno de los dos impide realmente el acceso — la filosofía de Python es "somos todos adultos responsables".

---

### R2. Diferencia entre `_atributo` y `__atributo`

`_atributo` (un guion bajo): convención pura. Indica que el atributo es un detalle interno, pero Python no hace nada especial con él. Es accesible normalmente.

`__atributo` (dos guiones bajos): Python aplica name mangling, renombrándolo a `_NombreClase__atributo`. Esto dificulta (no impide) el acceso externo y evita colisiones de nombres en herencia.

---

### R3. ¿Qué es name mangling y cuál es su propósito?

Name mangling es la transformación automática de `__atributo` a `_NombreClase__atributo`. Python lo hace cuando el nombre empieza con dos guiones bajos pero no termina con dos (los dunder methods quedan excluidos).

Su propósito **no es la seguridad** sino evitar colisiones de nombres en jerarquías de herencia. Si una clase padre y una subclase definen ambas `__valor`, el mangling les da nombres internos diferentes (`_Padre__valor` y `_Hija__valor`), evitando que se sobrescriban.

---

### R4. ¿Qué es una property y qué problema resuelve?

Una property permite interceptar el acceso a un atributo (lectura, escritura, eliminación) ejecutando código personalizado, sin cambiar la sintaxis de acceso. Se escribe `obj.atributo` como siempre, pero internamente se ejecuta un método.

Resuelve el problema de añadir validación o lógica a un atributo sin romper el código existente. Si una clase empieza con `self.nombre = nombre` y luego necesita validar el nombre, puede convertirlo en property sin que el código que usa `obj.nombre` tenga que cambiar.

---

### R5. ¿Por qué se desaconsejan getters/setters explícitos?

Porque Python tiene properties. Escribir `t.get_celsius()` y `t.set_celsius(30)` es verboso e innecesario cuando se puede escribir `t.celsius` y `t.celsius = 30`. Las properties proporcionan la misma funcionalidad (validación, lógica personalizada) con una sintaxis natural.

Además, los getters/setters explícitos obligan a decidir desde el inicio si un atributo necesita control de acceso. Con properties, se puede empezar con atributos simples y añadir lógica después sin cambiar la interfaz.

---

### R6. ¿Qué ocurre si no hay setter y se intenta asignar?

`AttributeError: can't set attribute`. Una property con solo `@property` (getter) es de solo lectura. Para permitir la asignación, se debe definir un setter con `@nombre.setter`.

---

### R7. ¿Cómo se aplica validación desde `__init__`?

Si `__init__` usa `self.atributo = valor` y existe una property llamada `atributo` con setter, la asignación pasa por el setter automáticamente. Esto significa que la validación se aplica desde la creación del objeto:

```python
def __init__(self, precio):
    self.precio = precio  # llama al setter → valida
```

Es importante no usar `self._precio = precio` en `__init__` si se quiere que la validación del setter se aplique al construir el objeto.

---

### R8. ¿Qué es una property calculada?

Una property que no almacena un valor sino que lo calcula cada vez que se accede a ella, a partir de otros atributos. Ejemplos: `area` calculada desde `base` y `altura`, `salario_mensual` desde `salario_anual`.

Conviene usarla cuando el valor depende de otros atributos y debe estar siempre actualizado. No conviene cuando el cálculo es costoso y el valor se consulta frecuentemente (en ese caso, considerar cachear el resultado).

---

### R9. ¿Se puede acceder a un atributo con name mangling desde fuera?

Sí, usando el nombre transformado: `obj._NombreClase__atributo`. Name mangling dificulta el acceso accidental pero no lo impide. Es intencionalmente débil — no es un mecanismo de seguridad.

---

### R10. Ventaja de properties para compatibilidad

La ventaja principal es que se puede evolucionar una clase sin romper su interfaz. Si una clase tiene `self.precio = precio` como atributo público y, meses después, necesita validar que el precio sea positivo, se puede convertir en property. Todo el código que usa `obj.precio` sigue funcionando sin cambios — la property intercepta el acceso de forma transparente.

---

### R11. ¿Cuándo se usa `__atributo` en la práctica?

Raramente. Se usa cuando existe un riesgo real de colisión de nombres en una jerarquía de herencia — por ejemplo, en frameworks o librerías donde la clase padre define atributos que las subclases no deben sobrescribir accidentalmente.

Para la mayoría de los casos, `_atributo` (un guion bajo) es suficiente. Usar `__atributo` por defecto "por seguridad" es un error frecuente de programadores que vienen de Java.

---

### R12. ¿Cuál es el resultado del código?

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            self._precio = 0
        else:
            self._precio = valor

    @property
    def con_iva(self):
        return round(self._precio * 1.21, 2)

p = Producto("Laptop", -50)
print(p.precio)
print(p.con_iva)
p.precio = 100
print(p.precio)
print(p.con_iva)
```

Salida:

```
0
0.0
100
121.0
```

- `Producto("Laptop", -50)`: en `__init__`, `self.precio = -50` pasa por el setter. Como -50 < 0, se asigna `self._precio = 0`.
- `p.precio` → 0 (el setter guardó 0).
- `p.con_iva` → `0 * 1.21 = 0.0`.
- `p.precio = 100` → el setter asigna `self._precio = 100` (es >= 0).
- `p.precio` → 100.
- `p.con_iva` → `100 * 1.21 = 121.0`.
