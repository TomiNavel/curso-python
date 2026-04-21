# Preguntas de Entrevista: Scope y Closures

1. ¿Cuáles son los cuatro scopes de Python y en qué orden se buscan las variables?
2. ¿Qué ocurre si una función tiene un `print(x)` seguido de `x = 5`? ¿Por qué?
3. ¿Cuál es la diferencia entre `global` y `nonlocal`?
4. ¿Por qué se desaconseja el uso de `global` en la mayoría de casos?
5. ¿Qué es un closure y qué condiciones deben cumplirse para que se forme uno?
6. ¿Qué significa que los closures capturan referencias y no valores?
7. ¿Cuál es el resultado de este código y por qué?
   ```python
   funciones = []
   for i in range(3):
       funciones.append(lambda: i)
   print([f() for f in funciones])
   ```
8. ¿Cómo se soluciona el problema de late binding en closures dentro de bucles?
9. ¿Cuál es la relación entre closures y decoradores?
10. ¿Cómo se puede inspeccionar qué variables ha capturado un closure?
11. ¿Qué diferencia hay entre una función anidada y un closure?
12. ¿Puedes dar un ejemplo de uso práctico de closures que no sea un decorador?

---

### R1. ¿Cuáles son los cuatro scopes de Python y en qué orden se buscan las variables?

La regla **LEGB**:

1. **Local** — variables definidas dentro de la función actual
2. **Enclosing** — variables de funciones externas que contienen a la actual (funciones anidadas)
3. **Global** — variables definidas al nivel superior del módulo
4. **Built-in** — nombres predefinidos de Python (`print`, `len`, `range`, etc.)

Python busca en este orden y se detiene en el primer scope donde encuentra el nombre. Si no lo encuentra en ninguno, lanza `NameError`.

### R2. ¿Qué ocurre si una función tiene un `print(x)` seguido de `x = 5`? ¿Por qué?

Lanza `UnboundLocalError`. Python determina el scope de las variables **en tiempo de compilación**, no en tiempo de ejecución. Al ver la asignación `x = 5` en cualquier parte de la función, marca `x` como local en toda la función. Cuando `print(x)` se ejecuta antes de la asignación, la variable local `x` existe pero no tiene valor asignado.

```python
x = 10

def funcion():
    print(x)  # UnboundLocalError — x es local por la asignación de abajo
    x = 5

funcion()
```

Es un error frecuente que confunde a programadores de otros lenguajes donde el scope se resuelve en ejecución.

### R3. ¿Cuál es la diferencia entre `global` y `nonlocal`?

- `global` indica que la variable hace referencia al **scope del módulo** (nivel superior del archivo)
- `nonlocal` indica que la variable hace referencia al **scope de la función que contiene a la actual** (scope Enclosing)

```python
x = "global"

def externa():
    x = "enclosing"

    def con_global():
        global x
        x = "cambiado"  # modifica la x del módulo

    def con_nonlocal():
        nonlocal x
        x = "cambiado"  # modifica la x de externa()
```

`nonlocal` solo funciona dentro de funciones anidadas. Usarla en una función que no esté anidada lanza `SyntaxError`.

### R4. ¿Por qué se desaconseja el uso de `global` en la mayoría de casos?

Las funciones que dependen de estado global son difíciles de testear, de razonar y de mantener. Introducen dependencias ocultas: para entender qué hace la función hay que conocer el estado de variables que no aparecen en sus parámetros.

La alternativa es diseñar funciones que reciban lo que necesitan como argumentos y devuelvan resultados:

```python
# Mal — dependencia oculta del estado global
contador = 0
def incrementar():
    global contador
    contador += 1

# Bien — explícito, testeable, sin efectos secundarios
def incrementar(contador):
    return contador + 1
```

### R5. ¿Qué es un closure y qué condiciones deben cumplirse para que se forme uno?

Un closure es una función que recuerda las variables del scope en el que fue definida, incluso después de que ese scope haya terminado de ejecutarse.

Se necesitan dos condiciones:

1. Una función interna **referencia variables** del scope de la función externa
2. La función interna **sobrevive** más allá de la ejecución de la función externa (normalmente porque se devuelve con `return`)

```python
def crear_multiplicador(factor):
    def multiplicar(n):
        return n * factor  # referencia a 'factor' del scope externo
    return multiplicar     # la función interna sobrevive

doble = crear_multiplicador(2)
doble(5)  # 10 — factor=2 sigue accesible
```

### R6. ¿Qué significa que los closures capturan referencias y no valores?

El closure no almacena una copia del valor de la variable en el momento de la definición. Almacena una referencia a la variable en sí, y lee su valor **en el momento de la llamada**. Si la variable cambia entre la definición y la llamada, el closure ve el valor actualizado.

```python
def crear():
    x = 1
    def leer():
        return x
    x = 99  # se modifica DESPUÉS de definir leer()
    return leer

print(crear()())  # 99 — no 1
```

### R7. ¿Cuál es el resultado de este código y por qué?

```python
funciones = []
for i in range(3):
    funciones.append(lambda: i)
print([f() for f in funciones])
```

El resultado es `[2, 2, 2]`, no `[0, 1, 2]`.

Las tres lambdas capturan una **referencia** a la misma variable `i`. Cuando el bucle termina, `i` vale 2. Al llamar a cualquiera de las funciones, todas leen el valor actual de `i`, que es 2.

### R8. ¿Cómo se soluciona el problema de late binding en closures dentro de bucles?

La solución estándar es capturar el valor actual como **argumento por defecto**. Los argumentos por defecto se evalúan en el momento de la definición, no en el de la llamada:

```python
funciones = []
for i in range(3):
    funciones.append(lambda i=i: i)  # i=i captura el valor actual

print([f() for f in funciones])  # [0, 1, 2]
```

El parámetro `i=i` crea una copia del valor de `i` en cada iteración, aislando cada lambda del cambio posterior de la variable del bucle.

### R9. ¿Cuál es la relación entre closures y decoradores?

Un decorador es un caso específico de closure. El patrón consiste en una función que recibe otra función como argumento, define una función interna (wrapper) que captura la función original en su closure, y devuelve esa función interna:

```python
def decorador(func):        # recibe la función original
    def wrapper(*args):     # captura func en el closure
        print("antes")
        resultado = func(*args)  # llama a la función original
        print("después")
        return resultado
    return wrapper          # devuelve el wrapper
```

Sin entender closures, no se puede entender cómo el wrapper mantiene acceso a `func` después de que `decorador()` haya terminado de ejecutarse.

### R10. ¿Cómo se puede inspeccionar qué variables ha capturado un closure?

A través del atributo `__closure__`, que contiene una tupla de objetos `cell`. Cada celda tiene un atributo `cell_contents` con el valor capturado:

```python
def crear(x):
    def interna():
        return x
    return interna

f = crear(42)
print(f.__closure__)                    # (<cell at 0x...>,)
print(f.__closure__[0].cell_contents)   # 42
```

Si la función no es un closure, `__closure__` es `None`.

### R11. ¿Qué diferencia hay entre una función anidada y un closure?

Toda función anidada está definida dentro de otra función, pero no toda función anidada es un closure. Un closure se forma solo cuando la función interna **referencia variables del scope de la función externa** y sobrevive más allá de ella:

```python
# Función anidada, pero NO closure — no captura nada
def externa():
    def interna():
        return 42
    return interna

f = externa()
print(f.__closure__)  # None

# Closure — captura 'x' del scope externo
def externa(x):
    def interna():
        return x
    return interna

f = externa(10)
print(f.__closure__[0].cell_contents)  # 10
```

### R12. ¿Puedes dar un ejemplo de uso práctico de closures que no sea un decorador?

**Función fábrica** — crear variantes de una función con configuración preestablecida:

```python
def crear_formateador(moneda, decimales):
    def formatear(cantidad):
        return f"{cantidad:.{decimales}f} {moneda}"
    return formatear

formato_eur = crear_formateador("€", 2)
formato_btc = crear_formateador("BTC", 8)

print(formato_eur(19.5))       # "19.50 €"
print(formato_btc(0.00045))   # "0.00045000 BTC"
```

Cada formateador captura su propia `moneda` y `decimales` en el closure, evitando pasar esos valores en cada llamada. Esto es más ligero que crear una clase cuando solo se necesita una función configurable.
