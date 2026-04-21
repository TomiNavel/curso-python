# 2. Strings — Preguntas de Entrevista

## Preguntas

1. ¿Qué significa que los strings en Python sean inmutables?
2. ¿Qué diferencia hay entre `find()` e `index()`?
3. ¿Cómo invertir un string en Python?
4. ¿Qué diferencia hay entre `split()` sin argumentos y `split(" ")`?
5. ¿Por qué `join()` es un método del separador y no de la lista?
6. ¿Qué es un f-string y por qué se prefiere sobre `format()` y `%`?
7. ¿Qué es un raw string y cuándo se usa?
8. ¿Qué devuelve `"hola"[1:3]`? ¿Y `"hola"[-2:]`?
9. ¿Cómo comprobar si un string contiene solo dígitos? ¿Es suficiente `isdigit()`?
10. ¿Qué diferencia hay entre `replace()` y `translate()`?
11. ¿Qué es el encoding y por qué es importante especificarlo al abrir archivos?
12. ¿Cómo comparar dos strings ignorando mayúsculas y espacios extra?
13. ¿Por qué concatenar strings con `+=` en un bucle es ineficiente?
14. ¿Qué hace `partition()` y en qué se diferencia de `split()`?

---

### R1. ¿Qué significa que los strings en Python sean inmutables?

Significa que una vez creado un string, no se puede modificar su contenido. Ningún método de string altera el objeto original — todos devuelven un nuevo string. Si se llama a `saludo.upper()` sin asignar el resultado, el string original no cambia y el nuevo se descarta.

```python
s = "hola"
s.upper()       # devuelve "HOLA", pero s sigue siendo "hola"
s = s.upper()   # ahora sí, s apunta al nuevo string "HOLA"
```

Esto tiene implicaciones de rendimiento: cada operación que "modifica" un string en realidad crea uno nuevo en memoria. Por eso concatenar con `+=` en un bucle es O(n²).

### R2. ¿Qué diferencia hay entre `find()` e `index()`?

Ambos buscan la primera ocurrencia de un substring y devuelven su posición. La diferencia está en qué ocurre cuando no lo encuentran: `find()` devuelve `-1`, mientras que `index()` lanza `ValueError`.

Se usa `find()` cuando la ausencia del substring es un resultado normal que se quiere manejar con un condicional. Se usa `index()` cuando la ausencia sería un bug — así la excepción hace visible el problema.

### R3. ¿Cómo invertir un string en Python?

Con slicing: `s[::-1]`. El paso negativo recorre el string de derecha a izquierda.

```python
print("Python"[::-1])  # "nohtyP"
```

No existe un método `.reverse()` en strings (sí en listas) precisamente porque los strings son inmutables.

### R4. ¿Qué diferencia hay entre `split()` sin argumentos y `split(" ")`?

`split()` sin argumentos trata cualquier secuencia de espacios en blanco (espacios, tabs, saltos de línea) como un solo separador, y además ignora los espacios al inicio y final. `split(" ")` divide literalmente por cada espacio individual, generando strings vacíos cuando hay espacios múltiples o en los extremos.

```python
texto = "  hola   mundo  "
texto.split()       # ["hola", "mundo"]
texto.split(" ")    # ["", "", "hola", "", "", "mundo", "", ""]
```

En la mayoría de casos, `split()` sin argumentos es lo que se necesita.

### R5. ¿Por qué `join()` es un método del separador y no de la lista?

Porque `join()` es una operación de strings, no de listas. El separador determina el tipo del resultado (un string), y la lista es solo el input. Además, las listas pueden contener cualquier tipo de dato, pero `join()` solo tiene sentido con strings. Ponerlo como método del separador deja claro que es una operación sobre texto.

```python
", ".join(["ana", "pedro", "luis"])  # "ana, pedro, luis"
```

### R6. ¿Qué es un f-string y por qué se prefiere sobre `format()` y `%`?

Un f-string es un string con el prefijo `f` que permite incluir expresiones Python directamente dentro de `{}`. Se evalúan en tiempo de ejecución.

Se prefieren por tres razones: son más legibles (el valor aparece donde se inserta, no separado al final), más concisos (menos código), y más rápidos (Python los optimiza internamente mejor que `format()` o `%`).

```python
nombre = "Ana"
edad = 28
f"Hola, {nombre}. Tienes {edad} años."
```

### R7. ¿Qué es un raw string y cuándo se usa?

Un raw string (prefijo `r`) trata las barras invertidas como caracteres literales, sin interpretar secuencias de escape como `\n` o `\t`.

Se usa en dos contextos principales: **expresiones regulares** (donde `\d`, `\w`, `\s` son patrones, no secuencias de escape) y **rutas de Windows** (donde `\` es el separador de directorios).

```python
# Sin raw string hay que escapar cada barra
patron = "\\d{3}-\\d{4}"
# Con raw string es legible
patron = r"\d{3}-\d{4}"
```

### R8. ¿Qué devuelve `"hola"[1:3]`? ¿Y `"hola"[-2:]`?

`"hola"[1:3]` devuelve `"ol"` — desde el índice 1 hasta el 2 (el índice final no se incluye).

`"hola"[-2:]` devuelve `"la"` — desde el penúltimo carácter hasta el final.

```python
#  h  o  l  a
#  0  1  2  3   → índices positivos
# -4 -3 -2 -1   → índices negativos
```

### R9. ¿Cómo comprobar si un string contiene solo dígitos? ¿Es suficiente `isdigit()`?

`isdigit()` comprueba si todos los caracteres son dígitos (0-9), pero no reconoce negativos (`"-5"`), decimales (`"3.14"`), ni notación científica (`"1e10"`). Devuelve `False` en strings vacíos.

Para validar si un string representa un número en general, la forma más fiable es intentar la conversión y capturar la excepción:

```python
try:
    float(valor)
    es_numero = True
except ValueError:
    es_numero = False
```

### R10. ¿Qué diferencia hay entre `replace()` y `translate()`?

`replace()` sustituye substrings completos: busca una secuencia de caracteres y la reemplaza por otra. `translate()` trabaja carácter a carácter: cada carácter se mapea individualmente a otro (o se elimina).

`replace()` es más simple y se usa en la mayoría de casos. `translate()` es más eficiente cuando se necesitan muchas sustituciones de caracteres individuales a la vez, porque hace todo en una sola pasada en lugar de encadenar múltiples `replace()`.

```python
# replace: sustituye substrings
"el gato y el perro".replace("el", "un")  # "un gato y un perro"

# translate: sustituye carácter a carácter
tabla = str.maketrans("aeiou", "AEIOU")
"hola mundo".translate(tabla)              # "hOlA mUndO"
```

### R11. ¿Qué es el encoding y por qué es importante especificarlo al abrir archivos?

Un encoding es una tabla que define cómo convertir caracteres en bytes y viceversa. Dentro de Python, los strings son texto abstracto (Unicode). Pero cuando se leen o escriben archivos, ese texto debe convertirse en bytes, y para eso se necesita un encoding.

Si no se especifica, Python usa el del sistema operativo (en Windows suele ser `cp1252`, no `utf-8`). Esto causa que archivos creados en Linux con utf-8 se lean con caracteres corruptos en Windows. La solución: siempre especificar `encoding="utf-8"` al abrir archivos.

### R12. ¿Cómo comparar dos strings ignorando mayúsculas y espacios extra?

Aplicar `strip()` para eliminar espacios en los extremos y `lower()` para normalizar a minúsculas antes de comparar.

```python
input_usuario = "  Hola Mundo  "
if input_usuario.strip().lower() == "hola mundo":
    print("Coincide")
```

Es una práctica estándar al manejar input de usuario, donde las mayúsculas y los espacios son impredecibles.

### R13. ¿Por qué concatenar strings con `+=` en un bucle es ineficiente?

Porque los strings son inmutables. Cada `+=` crea un nuevo objeto string en memoria, copia todo el contenido acumulado y le añade el fragmento nuevo. Con n iteraciones, el coste total es O(n²) porque cada copia es más grande que la anterior.

`join()` es O(n): calcula la longitud total, reserva la memoria necesaria una sola vez y copia cada fragmento una única vez.

```python
# O(n²)
resultado = ""
for p in palabras:
    resultado += p

# O(n)
resultado = "".join(palabras)
```

### R14. ¿Qué hace `partition()` y en qué se diferencia de `split()`?

`partition()` divide un string en exactamente tres partes: lo que hay antes del separador, el separador mismo, y lo que hay después. Siempre devuelve una tupla de tres elementos, incluso si el separador no existe (en ese caso devuelve el string original y dos strings vacíos).

`split()` divide en todas las ocurrencias y devuelve una lista de longitud variable. `partition()` es útil cuando solo se necesita la primera división y se quiere preservar la estructura.

```python
"ana@empresa.com".partition("@")   # ("ana", "@", "empresa.com")
"sin-arroba".partition("@")        # ("sin-arroba", "", "")
```
