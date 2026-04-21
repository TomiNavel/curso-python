# 1. Fundamentos de Python — Preguntas de Entrevista

## Preguntas

1. ¿Python es compilado o interpretado?
2. ¿Qué es el tipado dinámico?
3. ¿Qué diferencia hay entre `is` y `==`?
4. ¿Qué resultado da `0.1 + 0.2 == 0.3`?
5. ¿Qué valores son falsy en Python?
6. ¿Qué devuelven `and` y `or`?
7. ¿Qué es el small integer caching?
8. ¿Por qué Python no tiene constantes?
9. ¿Qué es PEP 8?
10. ¿Qué diferencia hay entre `/` y `//`?
11. ¿Para qué sirve un entorno virtual?
12. ¿Qué diferencia de rendimiento hay entre `in` en una lista y en un set?

---

## Respuestas

### R1. ¿Python es compilado o interpretado?

Python es interpretado. El código fuente se ejecuta línea a línea a través del intérprete, sin un paso previo de compilación a código máquina como en C o Java. En la práctica, CPython (la implementación estándar) compila a bytecode (archivos `.pyc`) que luego ejecuta una máquina virtual, pero esto es transparente para el programador y no equivale a la compilación tradicional.

### R2. ¿Qué es el tipado dinámico?

Significa que las variables no tienen un tipo fijo — el tipo se determina en tiempo de ejecución según el valor asignado. Una misma variable puede apuntar a un `int` y luego a un `str` sin error. Esto da flexibilidad pero puede introducir bugs que en lenguajes con tipado estático se detectarían en compilación.

```python
x = 10        # x es int
x = "texto"   # ahora x es str — válido, pero desaconsejado
```

### R3. ¿Qué diferencia hay entre `is` y `==`?

`==` compara **valores** — si dos objetos contienen el mismo dato. `is` compara **identidad** — si son el mismo objeto en memoria.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True  — mismo contenido
print(a is b)   # False — objetos distintos
```

El uso principal de `is` es comparar con `None`, porque `None` es un singleton y `is None` es más seguro que `== None` (ya que `==` puede ser sobreescrito por una clase).

### R4. ¿Qué resultado da `0.1 + 0.2 == 0.3`?

`False`. Los floats usan representación IEEE 754 en binario, y `0.1` y `0.2` no pueden representarse de forma exacta. El resultado de `0.1 + 0.2` es `0.30000000000000004`.

Para comparar floats se usa `math.isclose()` o `round()`. Para cálculos financieros, el módulo `decimal`.

### R5. ¿Qué valores son falsy en Python?

`False`, `None`, `0`, `0.0`, y todas las colecciones vacías: `""`, `[]`, `()`, `{}`, `set()`. Todo lo demás es truthy. Esto permite escribir condiciones como `if lista:` en lugar de `if len(lista) > 0`.

### R6. ¿Qué devuelven `and` y `or`?

No devuelven necesariamente `True` o `False` — devuelven el valor que determinó el resultado.

- `and` devuelve el primer valor falsy, o el último si todos son truthy.
- `or` devuelve el primer valor truthy, o el último si todos son falsy.

```python
print(0 or "hola")    # "hola"
print("a" and "b")    # "b"
print(0 and "hola")   # 0
```

Esto se usa habitualmente para valores por defecto: `nombre = input() or "Anónimo"`.

### R7. ¿Qué es el small integer caching?

Python cachea los enteros de -5 a 256 como optimización. Dentro de ese rango, dos variables con el mismo valor apuntan al mismo objeto en memoria, por lo que `is` devuelve `True`. Fuera de ese rango, se crean objetos distintos.

```python
a = 256
b = 256
print(a is b)  # True — mismo objeto cacheado

a = 257
b = 257
print(a is b)  # False — objetos distintos
```

Nunca se debe depender de este comportamiento. Para comparar valores siempre se usa `==`.

### R8. ¿Por qué Python no tiene constantes?

Python no tiene un mecanismo para hacer que una variable sea inmutable a nivel de lenguaje. No existe `const` ni `final`. La convención es usar `MAYÚSCULAS_CON_GUIONES` para señalar que un valor no debe modificarse, pero nada impide reasignarlo. Es una decisión de diseño coherente con la filosofía de Python: confiar en el programador en lugar de restringirlo.

### R9. ¿Qué es PEP 8?

Es la guía de estilo oficial de Python. Define convenciones como `snake_case` para variables y funciones, `PascalCase` para clases, `UPPER_SNAKE_CASE` para constantes, y 4 espacios de indentación. No es obligatoria a nivel de intérprete, pero se considera estándar en la industria y la mayoría de equipos la aplican con herramientas como `flake8` o `black`.

### R10. ¿Qué diferencia hay entre `/` y `//`?

`/` es la división real — siempre devuelve `float`, incluso entre enteros (`10 / 2 → 5.0`). `//` es la división entera (floor division) — redondea hacia abajo al entero más cercano. Con negativos, `//` redondea hacia abajo, no hacia cero: `-7 // 2` es `-4`, no `-3`.

### R11. ¿Para qué sirve un entorno virtual?

Para aislar las dependencias de cada proyecto. Sin entorno virtual, todos los proyectos comparten las mismas librerías instaladas globalmente, lo que genera conflictos de versiones. Con `python -m venv .venv` se crea una instalación de Python aislada donde cada proyecto tiene sus propios paquetes.

### R12. ¿Qué diferencia de rendimiento hay entre `in` en una lista y en un set?

Sobre una lista, `in` recorre los elementos secuencialmente hasta encontrar una coincidencia — O(n). Sobre un set, `in` calcula el hash del valor y accede directamente a su posición — O(1). Para búsquedas frecuentes sobre colecciones grandes, un set es significativamente más rápido.
