# 23. Expresiones Regulares

Las expresiones regulares (regex) son un lenguaje pequeño, casi universal, para describir patrones de texto. Aparecen en validaciones de formularios, parseo de logs, scraping, búsqueda y reemplazo en editores, y pipelines de procesamiento de datos. En entrevistas es un tema muy práctico: no se pide recitar la gramática, pero sí leer un regex, explicar qué captura y decidir cuándo usarlo frente a alternativas más simples.

El punto clave es saber cuándo **no** usarlas. Un regex para validar un email estricto pasa de diez líneas; un regex para parsear HTML es un meme en toda la industria del software. Las regex brillan para patrones cortos y estructuras lineales; cuando el problema es estructurado o contextual, hay herramientas mejores (parsers, librerías específicas, `str` con `split`/`startswith`).

## 23.1. Fundamentos de regex

Un regex es una cadena que describe un conjunto de cadenas. Cuando el motor compara el patrón contra un texto, busca trozos del texto que encajen con la descripción. Los caracteres comunes (`a`, `3`, espacio) se interpretan literalmente; ciertos símbolos (`.`, `*`, `+`, `?`, `^`, `$`, `[]`, `()`) tienen significado especial y se llaman **metacaracteres**.

### 23.1.1. Qué son y cuándo usarlas

Las regex son la herramienta correcta cuando el patrón es un formato lineal con variaciones predecibles: un código postal, una marca de tiempo en un log, una dirección IP, una referencia interna tipo `ISSUE-1234`. Se usan también para limpiezas masivas de texto (quitar etiquetas simples, normalizar espacios) y para extraer datos de logs o archivos de configuración.

Para problemas que parecen de texto pero son estructurados — HTML, JSON, XML, CSV con comillas — existen parsers específicos que entienden la gramática del formato. Usar regex sobre HTML funciona en ejemplos simples pero se rompe ante anidamiento, atributos con caracteres especiales o escapes. El criterio habitual en entrevistas: si hay una librería estándar para ese formato, usarla.

La segunda razón para no abusar es la legibilidad. Un regex complejo es difícil de leer, mantener y depurar: cualquier cambio pequeño tiene riesgo de modificar lo que captura sin que salte error. Cuando la lógica se puede expresar con `str.split`, `str.startswith` o `in`, esas opciones son más claras y menos frágiles.

### 23.1.2. Sintaxis básica (caracteres literales, metacaracteres)

Los caracteres alfanuméricos y la mayoría de símbolos se tratan como literales. El patrón `hola` encaja exactamente con el texto `"hola"` y nada más. Los metacaracteres tienen significado especial y hay que **escaparlos** con `\` si se quiere su valor literal.

Los principales metacaracteres son:

- `.` encaja con cualquier carácter (excepto salto de línea, salvo con la flag `DOTALL`).
- `|` es la alternativa: `perro|gato` encaja con `"perro"` o con `"gato"`.
- `()` agrupa subpatrones y crea grupos de captura.
- `[]` define una clase de caracteres.
- `\` escapa un metacarácter o introduce una clase predefinida.

```python
import re

re.search(r"hola", "hola mundo")        # encuentra "hola"
re.search(r"h.la", "hola")              # encaja: . es cualquier carácter
re.search(r"perro|gato", "hay un gato") # encaja: alternativa
re.search(r"3\.14", "pi es 3.14")       # el \. es punto literal
```

El prefijo `r` en los strings (`r"..."`) crea **raw strings**: Python no interpreta los escapes de barra invertida, lo que evita tener que duplicar cada `\`. Es la forma idiomática de escribir regex en Python: sin el prefijo, `"\\d"` sería necesario en lugar de `r"\d"`.

### 23.1.3. Clases de caracteres (\d, \w, \s, [], [^])

Las **clases de caracteres** representan "cualquier carácter de un conjunto". Las predefinidas más usadas son:

- `\d` cualquier dígito (equivalente a `[0-9]`).
- `\w` cualquier carácter alfanumérico o `_` (letras, dígitos, guion bajo).
- `\s` cualquier espacio en blanco (espacio, tabulación, salto de línea).

Cada una tiene su versión "complementaria" en mayúsculas: `\D` cualquier no-dígito, `\W` cualquier no-alfanumérico, `\S` cualquier no-espacio.

Además de las predefinidas, `[]` permite definir una clase ad hoc. Dentro, los guiones indican rangos, y un `^` inicial niega la clase.

```python
re.findall(r"\d+", "pedido 42, envío 103")    # ['42', '103']
re.findall(r"[aeiou]", "murciélago")          # ['u', 'i', 'é'... depende]
re.findall(r"[^0-9]", "abc123")               # ['a', 'b', 'c']
re.findall(r"[A-Z]\w*", "Hola Mundo Cruel")   # ['Hola', 'Mundo', 'Cruel']
```

Con caracteres acentuados (`é`, `ñ`), `\w` los incluye en Python 3 porque `re` trabaja en Unicode por defecto. En versiones antiguas o con la flag `re.ASCII`, `\w` se restringe a `[a-zA-Z0-9_]`.

### 23.1.4. Cuantificadores (*, +, ?, {n}, {n,m})

Los **cuantificadores** controlan cuántas veces se repite el elemento anterior:

- `*` cero o más veces.
- `+` una o más veces.
- `?` cero o una vez (opcional).
- `{n}` exactamente `n` veces.
- `{n,m}` entre `n` y `m` veces.

```python
re.search(r"ho+la", "hooooola")       # 'o' una o más veces → encaja
re.search(r"colou?r", "color")        # 'u' opcional → encaja también con "colour"
re.findall(r"\d{3}", "abc 123 45 678")# ['123', '678']: solo secuencias de exactamente 3
re.findall(r"\d{2,4}", "5 42 1234 99999")  # ['42', '1234', '9999']
```

Por defecto los cuantificadores son **greedy** (codiciosos): intentan capturar lo máximo posible. La sección 23.3.3 trata su contraparte lazy, importante cuando este comportamiento produce resultados inesperados.

### 23.1.5. Anclas (^, $, \b)

Las **anclas** no consumen caracteres: encajan con una posición dentro del texto.

- `^` principio de la cadena (o de línea con `re.MULTILINE`).
- `$` final de la cadena (o de línea con `re.MULTILINE`).
- `\b` frontera de palabra: entre un carácter `\w` y un no-`\w`.

```python
re.search(r"^Hola", "Hola mundo")     # encaja solo si empieza por "Hola"
re.search(r"\.$", "frase final.")     # encaja solo si termina en punto
re.findall(r"\bcat\b", "catalog and cat")  # ['cat']: no encaja "cat" dentro de "catalog"
```

`\b` es la forma correcta de hacer "búsqueda de palabra completa". Sin `\b`, `re.search(r"cat", "catalog")` encontraría el `"cat"` embebido. Esta distinción aparece mucho en búsqueda y reemplazo para no romper palabras más largas.

## 23.2. El módulo re

El módulo `re` de la librería estándar ofrece toda la funcionalidad de regex en Python. Hay dos niveles de uso: funciones de módulo (`re.search`, `re.findall`…) que compilan el patrón cada vez, y patrones precompilados (`re.compile(...)`) que se reutilizan. Para patrones usados una sola vez, las funciones directas son igual de eficientes porque `re` cachea internamente los patrones recientes. Para patrones que se aplican miles de veces en bucle, precompilar es más explícito y evita depender de la caché.

### 23.2.1. re.search(), re.match(), re.fullmatch()

Las tres funciones buscan un patrón en un string pero difieren en dónde comprueban la coincidencia:

- `re.match(patron, texto)` encaja solo si el patrón coincide **desde el principio** del texto. No requiere que encaje hasta el final.
- `re.fullmatch(patron, texto)` requiere que el patrón encaje con **todo** el texto, de principio a fin.
- `re.search(patron, texto)` busca el patrón en **cualquier posición**.

Las tres devuelven un objeto `Match` en caso de encaje y `None` en caso contrario.

```python
re.match(r"\d+", "123 abc")        # encaja: "123"
re.match(r"\d+", "abc 123")        # None: no empieza por dígito
re.fullmatch(r"\d+", "123")        # encaja: todo son dígitos
re.fullmatch(r"\d+", "123 abc")    # None: hay más texto después
re.search(r"\d+", "abc 123")       # encaja: encuentra "123" en medio
```

`search` es la opción por defecto para "encontrar si aparece". `fullmatch` es la elección natural para **validación**: "¿este string entero es un código postal válido?". `match` tiene un uso más específico (parsing secuencial) y su comportamiento "desde el principio pero no hasta el final" sorprende a quienes lo ven por primera vez.

### 23.2.2. re.findall() y re.finditer()

Cuando se quieren todas las coincidencias, no solo la primera:

- `re.findall(patron, texto)` devuelve una lista con todas las coincidencias.
- `re.finditer(patron, texto)` devuelve un iterador de objetos `Match`.

```python
texto = "pedido 42, envío 103, ref 7"
re.findall(r"\d+", texto)          # ['42', '103', '7']

for m in re.finditer(r"\d+", texto):
    print(m.group(), m.start(), m.end())
```

`findall` es más rápido y cómodo cuando solo se necesita el texto de cada coincidencia. `finditer` permite acceder a metadatos — posición, grupos capturados, span — y es preferible cuando el procesamiento de cada coincidencia necesita ese contexto.

Un detalle importante: si el patrón tiene grupos de captura, `findall` devuelve las capturas en lugar de la coincidencia completa. Este comportamiento sorprende: `re.findall(r"(\w+)=(\d+)", "a=1 b=2")` devuelve `[("a", "1"), ("b", "2")]`, no los strings completos `["a=1", "b=2"]`.

### 23.2.3. re.sub() y re.split()

`re.sub(patron, reemplazo, texto)` sustituye cada coincidencia por el reemplazo. Es una de las aplicaciones más prácticas de regex: limpiezas, normalizaciones, transformaciones en masa.

```python
re.sub(r"\s+", " ", "demasiados   espacios\ty\ttabs")
# 'demasiados espacios y tabs'

re.sub(r"\d+", "###", "password: 1234")
# 'password: ###'
```

El reemplazo puede contener referencias a grupos capturados: `\1`, `\2`, etc. (o `\g<nombre>` para grupos con nombre). También acepta una función que recibe cada `Match` y devuelve el reemplazo, útil para transformaciones que dependen del contenido capturado.

`re.split(patron, texto)` divide el texto en los puntos donde encaja el patrón. Más potente que `str.split` porque el separador es un patrón, no un string fijo:

```python
re.split(r"[,;\s]+", "uno, dos;tres   cuatro")
# ['uno', 'dos', 'tres', 'cuatro']
```

Cuando el separador es un único carácter, `str.split` es más simple y eficiente. `re.split` gana cuando el separador tiene variaciones (varios caracteres posibles, cantidad variable de espacios).

### 23.2.4. Grupos de captura y grupos con nombre

Los paréntesis `()` crean **grupos de captura**: partes del patrón cuyo texto encajado queda accesible tras la coincidencia. Un objeto `Match` expone `m.group(0)` para la coincidencia completa, `m.group(1)` para el primer grupo, y así sucesivamente. `m.groups()` devuelve una tupla con todos los grupos.

```python
m = re.search(r"(\w+)@(\w+\.\w+)", "contacto: ana@empresa.com")
m.group(0)   # 'ana@empresa.com' (coincidencia completa)
m.group(1)   # 'ana'
m.group(2)   # 'empresa.com'
m.groups()   # ('ana', 'empresa.com')
```

Los **grupos con nombre** usan la sintaxis `(?P<nombre>...)` y se acceden por nombre. Son mucho más legibles cuando hay varios grupos o el patrón puede cambiar:

```python
m = re.search(r"(?P<usuario>\w+)@(?P<dominio>\w+\.\w+)", "ana@empresa.com")
m.group("usuario")   # 'ana'
m.group("dominio")   # 'empresa.com'
m.groupdict()        # {'usuario': 'ana', 'dominio': 'empresa.com'}
```

Si hay paréntesis que solo sirven para agrupar (por ejemplo, aplicar un cuantificador al subpatrón) pero no interesan como captura, `(?:...)` crea un **grupo no capturador**, que agrupa sin aparecer en `groups()`. Esto mantiene limpias las capturas y suele ser útil en patrones complejos.

### 23.2.5. Flags (re.IGNORECASE, re.MULTILINE, re.DOTALL)

Las **flags** modifican el comportamiento del motor de regex. Las más comunes son:

- `re.IGNORECASE` (`re.I`): la comparación ignora mayúsculas y minúsculas.
- `re.MULTILINE` (`re.M`): `^` y `$` encajan al principio y final de cada línea, no solo del string completo.
- `re.DOTALL` (`re.S`): `.` encaja también con saltos de línea.

```python
re.search(r"error", "ERROR grave", re.IGNORECASE)    # encaja
re.findall(r"^\d+", "1 uno\n2 dos\n3 tres", re.MULTILINE)  # ['1', '2', '3']
re.search(r"inicio.*fin", "inicio\nmedio\nfin", re.DOTALL) # encaja con todo
```

Las flags se combinan con `|`: `re.IGNORECASE | re.MULTILINE`. En patrones precompilados, las flags se pasan a `re.compile`. También existe una sintaxis inline: `(?i)` al principio del patrón equivale a `re.IGNORECASE`.

## 23.3. Patrones comunes

Más allá de la sintaxis, hay un puñado de patrones que aparecen constantemente en código de producción y en entrevistas. Saberlos de memoria — no tener que pensarlos desde cero — es lo que distingue a alguien que ha trabajado con regex de alguien que solo sabe la teoría.

### 23.3.1. Validación (email, teléfono, URL)

Las validaciones con regex suelen dividirse en dos filosofías: **estricta** (el regex acepta exactamente lo que el estándar permite) y **pragmática** (un regex sencillo cubre el 99% de los casos y se delega el resto a otras comprobaciones).

La validación estricta de un email según RFC 5322 requiere un regex de varios cientos de caracteres que nadie escribe a mano. En la práctica se usa un regex pragmático que cubre los casos reales:

```python
EMAIL = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

re.fullmatch(EMAIL, "ana.garcia@empresa.com")   # encaja
re.fullmatch(EMAIL, "contacto+info@x.co.uk")    # encaja
re.fullmatch(EMAIL, "no-es-email")              # None
```

Para validaciones realmente importantes (registro de usuarios, cobros), lo habitual no es confiar solo en el regex: se manda un correo de confirmación. El regex filtra strings manifiestamente incorrectos; la verdad final la da el servidor SMTP.

Para teléfonos y URLs, el enfoque es el mismo: un regex flexible que acepte las variaciones razonables, combinado con validación semántica cuando es crítico. Para URLs, el módulo `urllib.parse` del estándar suele ser más correcto que cualquier regex casero.

### 23.3.2. Extracción de datos de texto

Una de las aplicaciones más útiles de regex es extraer información estructurada de texto semi-estructurado: logs, exportaciones, documentación. El patrón típico es `re.finditer` o `re.findall` con grupos de captura.

```python
log = "[2026-04-22 10:15:32] ERROR: conexión rechazada (intento 3)"

patron = r"\[(?P<fecha>[\d\- :]+)\]\s+(?P<nivel>\w+):\s+(?P<mensaje>.*)"
m = re.search(patron, log)
if m:
    print(m.group("fecha"))    # '2026-04-22 10:15:32'
    print(m.group("nivel"))    # 'ERROR'
    print(m.group("mensaje"))  # 'conexión rechazada (intento 3)'
```

El valor de los grupos con nombre en extracción es enorme: el código que procesa el resultado se lee como prosa, y añadir o reordenar grupos no rompe nada por índices posicionales.

### 23.3.3. Greedy vs lazy (cuantificadores codiciosos y perezosos)

Por defecto, los cuantificadores `*`, `+`, `?`, `{n,m}` son **greedy**: intentan encajar lo máximo posible manteniendo la coincidencia global. Poner un `?` detrás del cuantificador lo convierte en **lazy** (perezoso): encaja lo mínimo posible.

La diferencia se ve claramente en patrones que delimitan con el mismo carácter a ambos lados:

```python
texto = "<b>negrita</b> y <i>cursiva</i>"

re.findall(r"<(.+)>", texto)    # ['b>negrita</b> y <i>cursiva</i']
re.findall(r"<(.+?)>", texto)   # ['b', '/b', 'i', '/i']
```

En el primer caso, `.+` greedy consume todo el texto entre el primer `<` y el último `>`, porque `.` encaja con cualquier cosa y el motor prefiere la coincidencia más larga. En el segundo, `.+?` lazy consume lo mínimo necesario para cerrar con `>`, devolviendo cada etiqueta por separado.

Elegir greedy o lazy es uno de los errores más comunes en regex. Cuando los resultados parezcan "comerse más de la cuenta", la respuesta suele ser cambiar el cuantificador a lazy con `?`. El otro enfoque es ser más específico con el contenido: en lugar de `<.+?>`, usar `<[^>]+>` — "cualquier cosa que no sea `>`", que evita ambigüedad sin depender del modo lazy.
