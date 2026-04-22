# Preguntas de Entrevista: Expresiones Regulares

1. ¿Qué diferencia hay entre `re.match`, `re.search` y `re.fullmatch`?
2. ¿Cuándo es preferible `re.findall` y cuándo `re.finditer`?
3. ¿Qué son los cuantificadores greedy y lazy, y cómo se indican?
4. ¿Por qué se usa el prefijo `r"..."` en los patrones?
5. ¿Qué diferencia hay entre `\d+` y `[0-9]+` en Python 3?
6. ¿Para qué sirven los grupos no capturadores `(?:...)`?
7. ¿Cómo funciona `\b` y cuándo es útil?
8. ¿Qué hacen las flags `re.IGNORECASE`, `re.MULTILINE` y `re.DOTALL`?
9. ¿Por qué no es buena idea validar HTML, JSON o emails estrictos solo con regex?
10. ¿Qué ventajas tiene `re.compile` frente a usar las funciones de módulo directamente?

---

### R1. ¿Qué diferencia hay entre `re.match`, `re.search` y `re.fullmatch`?

Las tres buscan un patrón en un string y devuelven un objeto `Match` o `None`, pero difieren en dónde exigen la coincidencia. `re.match` comprueba si el patrón encaja desde el principio del string, sin exigir que llegue al final. `re.search` busca la primera coincidencia en cualquier posición. `re.fullmatch` exige que el patrón cubra el string entero.

Para validación, `fullmatch` es casi siempre lo correcto: se quiere confirmar que todo el input encaja con el formato. `search` es la opción por defecto cuando se busca si aparece algo. `match` tiene un uso más específico y su comportamiento ("desde el principio pero no hasta el final") sorprende a menudo, por lo que en código nuevo suele evitarse salvo que se esté implementando parsing secuencial.

### R2. ¿Cuándo es preferible `re.findall` y cuándo `re.finditer`?

`findall` devuelve una lista con todas las coincidencias y es más cómodo cuando solo se necesitan los strings encontrados. `finditer` devuelve un iterador de objetos `Match`, útil cuando se necesitan metadatos: posición inicial y final de cada coincidencia, grupos capturados, o procesamiento perezoso que evite construir una lista enorme.

Hay que tener cuidado con una sutileza: si el patrón contiene grupos de captura, `findall` devuelve las capturas (como tupla si hay varios grupos) en lugar de la coincidencia completa. Esto rompe expectativas si se esperaba el string entero. `finditer` siempre devuelve `Match` y es más predecible en ese sentido.

### R3. ¿Qué son los cuantificadores greedy y lazy, y cómo se indican?

Los cuantificadores `*`, `+`, `?`, `{n,m}` son greedy por defecto: intentan encajar lo máximo posible manteniendo la coincidencia global. Añadiendo un `?` detrás (`*?`, `+?`, `??`, `{n,m}?`) se convierten en lazy: encajan lo mínimo posible.

La diferencia se ve claramente cuando hay delimitadores similares a ambos lados. `r"<(.+)>"` aplicado a `"<b>texto</b>"` con `.+` greedy captura todo desde el primer `<` hasta el último `>`, dando una coincidencia que engloba todo. Con `.+?` lazy, el motor corta en cuanto encuentra el primer `>`, devolviendo solo `"b"`. Saber cuándo aplicar lazy es uno de los puntos más prácticos de las regex.

### R4. ¿Por qué se usa el prefijo `r"..."` en los patrones?

El prefijo `r` crea un **raw string**: Python no interpreta las barras invertidas como escapes. Sin el prefijo, `"\d"` se interpretaría como `\d` solo si `\d` no es una secuencia de escape conocida (y podría cambiar de comportamiento entre versiones). Para `"\n"` o `"\b"`, Python sí las interpreta, generando un carácter distinto al que el regex espera.

Usar raw strings evita tener que duplicar cada barra (`"\\d"` en lugar de `r"\d"`) y elimina ambigüedades. Es la convención estándar en Python al escribir regex; el código que no las usa suele delatar a alguien poco familiarizado con el módulo.

### R5. ¿Qué diferencia hay entre `\d+` y `[0-9]+` en Python 3?

Semánticamente son distintos. `[0-9]+` siempre encaja solo con dígitos ASCII del 0 al 9. `\d+` en Python 3 por defecto trabaja en modo Unicode y también encaja con dígitos de otros sistemas: números árabes orientales, dígitos devanagari, sufijos chinos que representan números.

En la mayoría de aplicaciones que procesan texto en español o inglés esta diferencia no importa, porque la entrada solo contiene 0-9. Pero en software internacional, `\d` puede aceptar entradas inesperadas. Para garantizar solo dígitos ASCII se usa `[0-9]` o se compila el patrón con la flag `re.ASCII`.

### R6. ¿Para qué sirven los grupos no capturadores `(?:...)`?

Los paréntesis normales `(...)` agrupan y capturan: el texto dentro queda disponible como grupo numerado. Cuando solo se necesita agrupar para aplicar un cuantificador o una alternativa, sin interés en capturar, se usa `(?:...)`, que agrupa sin crear captura.

El beneficio es doble: mantiene limpio el orden de los grupos capturados (si se añaden paréntesis auxiliares no se desplaza la numeración de los grupos reales) y micro-optimiza, aunque la diferencia de rendimiento es insignificante en la práctica. El valor principal es la legibilidad y la estabilidad del código: cambiar un `(?:...)` no rompe referencias como `\1` o `m.group(1)`.

### R7. ¿Cómo funciona `\b` y cuándo es útil?

`\b` es una **frontera de palabra**: una posición (no un carácter) entre un carácter de palabra (`\w`) y algo que no lo sea, o al principio/final del string si empieza/acaba en `\w`. No consume caracteres.

Su uso típico es evitar coincidencias dentro de palabras más largas. Buscar `"cat"` con `re.search(r"cat", "catalog")` encuentra el substring embebido. Con `re.search(r"\bcat\b", "catalog and cat")` solo encaja con el `cat` aislado. En búsqueda y reemplazo es casi imprescindible para no romper palabras por accidente.

### R8. ¿Qué hacen las flags `re.IGNORECASE`, `re.MULTILINE` y `re.DOTALL`?

`re.IGNORECASE` (alias `re.I`) hace la comparación insensible a mayúsculas y minúsculas, útil cuando el patrón busca palabras cuya capitalización puede variar.

`re.MULTILINE` (`re.M`) cambia el significado de `^` y `$` para que encajen al principio y final de cada línea del texto, no solo del string completo. Imprescindible cuando se procesa texto línea a línea con un único `re.findall` sobre varias líneas.

`re.DOTALL` (`re.S`) hace que `.` encaje también con saltos de línea. Sin esta flag, `.` se detiene en `\n`, lo que puede sorprender al intentar capturar bloques multilinea con `.*`. Las flags se combinan con `|` (`re.I | re.M`).

### R9. ¿Por qué no es buena idea validar HTML, JSON o emails estrictos solo con regex?

Son formatos con gramáticas contextuales que requieren más potencia que la que ofrece un autómata finito (que es lo que implementan las regex clásicas). HTML y JSON admiten anidamiento arbitrario; una regex no puede "saber" que un `</div>` cierra el `<div>` correcto si hay `<div>` anidados. Los emails siguen el RFC 5322, que admite comentarios, literales entre corchetes y otras construcciones que hacen que cualquier regex "estricto" sea enorme, ilegible y aún así incompleto.

La práctica recomendada es usar parsers dedicados (`html.parser`, `json`, `email.utils`) que entienden la gramática del formato y manejan correctamente los casos límite. Las regex siguen siendo útiles para casos simples y bien acotados, pero fallan en cuanto el input real incluye anidamiento o características menos comunes del estándar.

### R10. ¿Qué ventajas tiene `re.compile` frente a usar las funciones de módulo directamente?

`re.compile(patron)` crea un objeto `Pattern` reutilizable que expone los mismos métodos (`search`, `match`, `findall`, `sub`…). El patrón se compila una sola vez, así que aplicarlo en bucle a muchos inputs es ligeramente más eficiente que llamar a `re.search(patron, texto)` cada vez.

En la práctica, el módulo `re` ya cachea internamente los últimos patrones usados (alrededor de los 512 más recientes), por lo que la ganancia en velocidad es marginal en la mayoría de casos. La razón principal para usar `re.compile` es la claridad: nombra el patrón, permite pasar flags de forma explícita y separa la construcción del patrón de su uso, lo que facilita tests y mantenimiento.
