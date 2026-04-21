# Preguntas de Entrevista: Comprehensions

1. ¿Cuál es la diferencia entre poner el `if` al final y poner `if/else` al inicio de una list comprehension?
2. ¿Qué diferencia hay entre una list comprehension y una generator expression? ¿Cuándo usarías cada una?
3. ¿Cómo se distingue una set comprehension de una dict comprehension si ambas usan llaves `{}`?
4. ¿Qué significa que un generador usa evaluación diferida (lazy evaluation)?
5. ¿Qué ocurre si intentas recorrer un generador dos veces?
6. ¿Cuál es la diferencia entre `[print(x) for x in lista]` y `for x in lista: print(x)`? ¿Cuál es preferible y por qué?
7. ¿Cómo aplanarías una lista de listas con una comprehension? ¿En qué orden van los `for`?
8. ¿Para qué sirven `any()` y `all()`? ¿Cómo se combinan con generator expressions?
9. ¿Cuándo es mejor usar un bucle `for` tradicional en lugar de una comprehension?
10. ¿Qué produce `{x: x ** 2 for x in range(5) if x % 2 != 0}`? Explica paso a paso.
11. ¿Qué ventaja tiene `sum(n ** 2 for n in range(1000000))` frente a `sum([n ** 2 for n in range(1000000)])`?
12. ¿Por qué `[x for x in range(10) if x > 5 else x + 10]` da un error de sintaxis?

---

### R1. ¿Cuál es la diferencia entre poner el `if` al final y poner `if/else` al inicio de una list comprehension?

Son dos operaciones distintas:

- `if` al final **filtra**: solo los elementos que cumplen la condición se incluyen en el resultado. La lista resultante puede tener menos elementos que el iterable original.
- `if/else` al inicio **transforma**: todos los elementos se incluyen, pero se les aplica una expresión u otra según la condición. La lista resultante siempre tiene la misma cantidad de elementos.

```python
numeros = [1, 2, 3, 4, 5]

# Filtrado — solo pares
[n for n in numeros if n % 2 == 0]          # [2, 4]

# Transformación — todos, etiquetados
["par" if n % 2 == 0 else "impar" for n in numeros]  # ['impar', 'par', 'impar', 'par', 'impar']
```

### R2. ¿Qué diferencia hay entre una list comprehension y una generator expression? ¿Cuándo usarías cada una?

Una list comprehension (`[...]`) crea todos los elementos de golpe y los almacena en una lista en memoria. Una generator expression (`(...)`) no crea nada: devuelve un objeto generador que calcula los valores uno a uno, bajo demanda (evaluación diferida).

Se usa un generador cuando solo se necesita iterar una vez sobre los resultados, especialmente al pasarlo como argumento a funciones como `sum()`, `max()`, `any()` o `all()`. Se usa una lista cuando se necesita acceder a los datos múltiples veces, indexarlos o conocer su longitud.

### R3. ¿Cómo se distingue una set comprehension de una dict comprehension si ambas usan llaves `{}`?

Por la presencia de `:` entre clave y valor:

- `{expresión for x in iterable}` → **set** comprehension (una sola expresión)
- `{clave: valor for x in iterable}` → **dict** comprehension (dos expresiones separadas por `:`)

Además, `{}` vacío crea un diccionario, no un set. Para crear un set vacío se usa `set()`.

### R4. ¿Qué significa que un generador usa evaluación diferida (lazy evaluation)?

Significa que el generador no calcula ningún valor hasta que se le pide explícitamente. Los elementos se producen uno a uno conforme se consumen, en lugar de generarse todos de antemano. Esto tiene dos consecuencias prácticas: el consumo de memoria es constante (no depende del tamaño del iterable) y el cálculo solo se realiza cuando es necesario (por ejemplo, `any()` puede detenerse en el primer `True` sin calcular el resto).

### R5. ¿Qué ocurre si intentas recorrer un generador dos veces?

La segunda vez no produce ningún elemento. Un generador se agota después de ser recorrido una vez: los valores se calculan al vuelo y se descartan, no se almacenan.

```python
gen = (n ** 2 for n in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]
print(list(gen))  # []
```

Si se necesita recorrer los datos más de una vez, hay que usar una list comprehension o convertir el generador a lista con `list()` antes de consumirlo.

### R6. ¿Cuál es la diferencia entre `[print(x) for x in lista]` y `for x in lista: print(x)`? ¿Cuál es preferible y por qué?

Ambos imprimen los elementos, pero la comprehension además crea una lista de valores `None` (el valor de retorno de `print()`) que no se usa para nada. Es un antipatrón porque las comprehensions están diseñadas para **crear colecciones**, no para ejecutar efectos secundarios.

El bucle `for` es la forma correcta. Es más claro en su intención y no desperdicia memoria creando una lista innecesaria.

### R7. ¿Cómo aplanarías una lista de listas con una comprehension? ¿En qué orden van los `for`?

Con dos cláusulas `for`. El primer `for` recorre las sublistas y el segundo recorre los elementos dentro de cada sublista. El orden es el mismo que tendrían los bucles anidados equivalentes:

```python
matriz = [[1, 2], [3, 4], [5, 6]]
plana = [num for fila in matriz for num in fila]
# [1, 2, 3, 4, 5, 6]

# Equivalente con bucles:
# for fila in matriz:
#     for num in fila:
#         plana.append(num)
```

Un error frecuente es invertir el orden de los `for`, lo que provoca un `NameError` porque se intenta usar una variable antes de definirla.

### R8. ¿Para qué sirven `any()` y `all()`? ¿Cómo se combinan con generator expressions?

- `any(iterable)` devuelve `True` si **al menos un** elemento del iterable es truthy.
- `all(iterable)` devuelve `True` si **todos** los elementos son truthy.

Se combinan con generator expressions para comprobar condiciones sobre una colección de forma concisa y eficiente:

```python
edades = [22, 17, 30, 15, 25]

# ¿Hay algún menor de edad?
any(edad < 18 for edad in edades)   # True

# ¿Son todos mayores de edad?
all(edad >= 18 for edad in edades)  # False
```

Además, ambas tienen cortocircuito: `any()` deja de iterar en cuanto encuentra el primer `True`, y `all()` en cuanto encuentra el primer `False`. Con generadores grandes esto supone un ahorro significativo.

### R9. ¿Cuándo es mejor usar un bucle `for` tradicional en lugar de una comprehension?

- Cuando la lógica tiene **múltiples pasos** o requiere variables intermedias.
- Cuando se necesitan **efectos secundarios** (como `print()`, modificar otra estructura, etc.).
- Cuando se anidan **más de dos** `for`.
- Cuando la comprehension supera las ~80 columnas y pierde legibilidad.
- Cuando se necesita **acumular estado** que va cambiando (contadores, flags, totales parciales).

La regla general es: si la comprehension no se entiende de un vistazo, es mejor usar un bucle.

### R10. ¿Qué produce `{x: x ** 2 for x in range(5) if x % 2 != 0}`? Explica paso a paso.

Es una dict comprehension que:

1. Recorre `range(5)` → `0, 1, 2, 3, 4`
2. Filtra solo los impares (`x % 2 != 0`) → `1, 3`
3. Para cada uno, crea una entrada `clave: valor` donde la clave es `x` y el valor es `x ** 2`

Resultado: `{1: 1, 3: 9}`

### R11. ¿Qué ventaja tiene `sum(n ** 2 for n in range(1000000))` frente a `sum([n ** 2 for n in range(1000000)])`?

El primero usa un generador y el segundo una lista. Ambos producen el mismo resultado, pero:

- El generador calcula los cuadrados uno a uno y los pasa a `sum()` sin almacenarlos. Usa una cantidad constante de memoria.
- La lista crea un millón de elementos en memoria antes de que `sum()` empiece a sumarlos.

En términos de resultado son equivalentes, pero el generador es más eficiente en memoria. La diferencia es relevante cuando se trabaja con volúmenes de datos grandes.

### R12. ¿Por qué `[x for x in range(10) if x > 5 else x + 10]` da un error de sintaxis?

Porque mezcla dos sintaxis incompatibles. El `if` al final de una comprehension es para **filtrar** y no admite `else`. Si se quiere usar `if/else` para **transformar**, la expresión condicional debe ir **antes** del `for`:

```python
# MAL — error de sintaxis
[x for x in range(10) if x > 5 else x + 10]

# BIEN — if/else como expresión, antes del for
[x if x > 5 else x + 10 for x in range(10)]
```

Es uno de los errores de sintaxis más comunes con comprehensions y aparece con frecuencia en entrevistas precisamente para comprobar que el candidato entiende la diferencia entre filtrado y transformación condicional.
