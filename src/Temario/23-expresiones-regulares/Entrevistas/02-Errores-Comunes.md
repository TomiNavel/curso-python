# Errores Comunes: Expresiones Regulares

## Error 1. Olvidar el prefijo `r` en los patrones

Sin raw string, Python interpreta las barras invertidas antes de que lleguen al motor de regex, cambiando el significado del patrón o generando `DeprecationWarning` por secuencias de escape desconocidas.

```python
import re

# MAL: "\b" es el carácter de retroceso en Python, no la frontera de palabra
re.search("\bhola\b", "hola mundo")   # None, no encaja

# BIEN: raw string preserva la barra invertida
re.search(r"\bhola\b", "hola mundo")  # encaja
```

El efecto más confuso es que algunos patrones funcionan por casualidad (`"\d"` sobrevive porque `\d` no es un escape estándar de Python), mientras que otros fallan silenciosamente. Usar `r"..."` siempre elimina la clase entera de bugs.

---

## Error 2. Usar `match` cuando se quería `fullmatch`

`re.match` comprueba desde el principio pero no exige que el patrón cubra todo el string. Dar por válido un input "que empieza bien" es un bug de seguridad típico en validaciones.

```python
# MAL: "12345abc" pasa porque los 5 dígitos están al principio
if re.match(r"\d{5}", codigo):
    guardar(codigo)

# BIEN: fullmatch exige que todo el input encaje
if re.fullmatch(r"\d{5}", codigo):
    guardar(codigo)
```

Para validación, `fullmatch` es casi siempre la respuesta correcta. `match` tiene sentido en parsing secuencial donde se procesa el resto después.

---

## Error 3. Cuantificador greedy que devora de más

Los cuantificadores greedy consumen todo lo posible. Con delimitadores iguales a ambos lados (`<...>`, `"..."`), esto captura mucho más de lo esperado.

```python
texto = "<b>negrita</b> y <i>cursiva</i>"

# MAL: .+ greedy se come todo entre el primer < y el último >
re.findall(r"<(.+)>", texto)   # ['b>negrita</b> y <i>cursiva</i']

# BIEN: .+? lazy se detiene en el primer >
re.findall(r"<(.+?)>", texto)  # ['b', '/b', 'i', '/i']

# MEJOR: evitar ambigüedad siendo específico
re.findall(r"<([^>]+)>", texto)  # ['b', '/b', 'i', '/i']
```

El patrón `[^>]+` ("cualquier cosa excepto `>`") es más explícito que depender del modo lazy y no tiene efectos sorpresa si cambia el resto del regex.

---

## Error 4. `findall` con grupos capturadores no devuelve la coincidencia completa

Si el patrón tiene grupos, `findall` devuelve solo las capturas, no la coincidencia entera. Quien lo ve por primera vez espera la coincidencia completa.

```python
# MAL: esperar los strings completos "a=1", "b=2"
re.findall(r"(\w+)=(\d+)", "a=1 b=2")
# Devuelve: [('a', '1'), ('b', '2')]  — solo los grupos, no el match completo

# BIEN: si se necesitan las coincidencias enteras, usar finditer
[m.group() for m in re.finditer(r"(\w+)=(\d+)", "a=1 b=2")]
# Devuelve: ['a=1', 'b=2']
```

La otra opción es envolver el patrón en un grupo no capturador `(?:\w+)=(?:\d+)` si lo único que se quiere es la coincidencia completa sin capturas.

---

## Error 5. Olvidar escapar caracteres literales con significado especial

Los metacaracteres (`.`, `+`, `*`, `?`, `(`, `)`, `[`, `]`, `{`, `}`, `|`, `^`, `$`, `\`) tienen significado especial. Si se quieren como literales, hay que escaparlos con `\`.

```python
# MAL: el . encaja con cualquier carácter
re.search(r"192.168.1.1", "192X168X1X1")   # encaja por error

# BIEN: escapar el punto literal
re.search(r"192\.168\.1\.1", "192X168X1X1")  # None

# Alternativa: re.escape para escapar automáticamente
patron = re.escape("192.168.1.1")
re.search(patron, texto)
```

`re.escape(string)` es especialmente útil cuando el patrón se construye a partir de datos de entrada: evita que caracteres especiales del input modifiquen la semántica del patrón.

---

## Error 6. No usar flags para mayúsculas en lugar de enumerar variantes

Duplicar casos para cubrir mayúsculas y minúsculas infla el patrón y es propenso a errores.

```python
# MAL: intentar cubrir todas las capitalizaciones a mano
re.search(r"error|Error|ERROR", texto)

# BIEN: re.IGNORECASE
re.search(r"error", texto, re.IGNORECASE)
```

Si el patrón tiene muchas partes alfabéticas, añadir la flag es una línea y cubre todas las combinaciones. El patrón queda mucho más legible.

---

## Error 7. Confiar ciegamente en regex para validar emails

Validar emails con regex estrictos es un clásico de preguntas trampa. Los regex casi nunca implementan el RFC completo y fallan con casos válidos (subdominios largos, caracteres `+`, TLDs nuevos).

```python
# MAL: regex demasiado restrictivo
EMAIL = r"^[a-z]+@[a-z]+\.com$"
re.fullmatch(EMAIL, "ana+trabajo@empresa.co.uk")  # None, pero es válido

# BIEN: regex pragmático + validación real
EMAIL = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
if re.fullmatch(EMAIL, email):
    mandar_confirmacion(email)   # la validación real la da el servidor SMTP
```

El regex debería rechazar lo obviamente malformado, no ser la única línea de defensa. Para datos críticos, combinar regex pragmático con verificación del servidor es el enfoque estándar.

---

## Error 8. Construir el patrón con `+` dentro de un bucle

Compilar el mismo patrón en cada iteración desperdicia trabajo y hace el código menos legible.

```python
# MAL: parsea el patrón en cada llamada
for linea in archivo:
    if re.search(r"\bERROR\b.*\d+", linea):
        ...

# BIEN: precompilar fuera del bucle
PATRON = re.compile(r"\bERROR\b.*\d+")
for linea in archivo:
    if PATRON.search(linea):
        ...
```

`re` cachea los últimos patrones internamente, pero depender de esa caché es frágil y menos explícito. En bucles con miles de iteraciones, `re.compile` al principio deja clara la intención y elimina cualquier duda sobre rendimiento.

---

## Error 9. Usar `.` esperando que encaje con saltos de línea

Por defecto, `.` no encaja con `\n`. En textos multilinea esto produce coincidencias parciales inesperadas.

```python
texto = "inicio\nmedio\nfin"

# MAL: . no encaja con \n, así que no captura el texto completo
re.search(r"inicio.*fin", texto)   # None

# BIEN: flag DOTALL hace que . sí encaje con \n
re.search(r"inicio.*fin", texto, re.DOTALL)  # encaja
```

Alternativa sin flag: `[\s\S]` ("cualquier carácter, incluidos saltos") funciona aunque es menos legible. Si el regex opera sobre contenido multilinea, la flag `DOTALL` suele ser la solución natural.

---

## Error 10. Usar regex para problemas que resuelve mejor `str`

No todo texto requiere regex. Para búsquedas simples, `in`, `startswith`, `endswith` y `split` son más rápidos, más legibles y menos propensos a errores.

```python
# MAL: regex para algo trivial
if re.search(r"^http", url):
    ...

# BIEN: método de string
if url.startswith("http"):
    ...

# MAL: regex para un separador simple
partes = re.split(r",", "a,b,c")

# BIEN: str.split es más claro
partes = "a,b,c".split(",")
```

En entrevistas se valora reconocer cuándo una regex no aporta valor. Usarla siempre "porque funciona" es señal de no conocer alternativas más simples.
