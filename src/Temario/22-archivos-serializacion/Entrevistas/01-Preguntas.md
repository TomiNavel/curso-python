# Preguntas de Entrevista: Archivos y Serialización

1. ¿Por qué conviene usar `with open(...)` en lugar de `open()` seguido de `close()`?
2. ¿Qué hace el parámetro `encoding` de `open()` y qué ocurre si no lo especificamos?
3. ¿Cuál es la diferencia entre los modos `"w"` y `"x"` al abrir un archivo?
4. ¿Por qué iterar directamente sobre el objeto de archivo es preferible a `readlines()` para archivos grandes?
5. ¿Cuál es la diferencia entre `json.dump` y `json.dumps`?
6. ¿Qué tipos de Python no son serializables a JSON directamente y cómo se manejan?
7. ¿Por qué hay que pasar `newline=""` al abrir archivos para leer o escribir CSV?
8. ¿Qué ventajas tiene `csv.DictReader` sobre `csv.reader`?
9. ¿Cuáles son las principales limitaciones y riesgos de `pickle`?
10. ¿Qué ventajas ofrece `pathlib` sobre `os.path`?
11. ¿Cuándo se prefiere `Path.rglob` frente a `os.walk`?
12. ¿Por qué `f.writelines(lista)` no añade saltos de línea entre los elementos?

---

### R1. ¿Por qué conviene usar `with open(...)` en lugar de `open()` seguido de `close()`?

`with` garantiza que el archivo se cierre al salir del bloque incluso si ocurre una excepción. Con `close()` manual, cualquier error entre la apertura y el cierre deja el descriptor abierto hasta que el recolector de basura lo libere, lo que puede tardar o no ocurrir en implementaciones distintas a CPython.

Además de liberar el descriptor, cerrar un archivo abierto en modo escritura fuerza el flush de cualquier buffer pendiente. Sin cierre, los últimos datos escritos pueden no llegar al disco. Este detalle provoca bugs sutiles en los que "los datos están ahí casi siempre" pero se pierden cuando el programa termina abruptamente.

### R2. ¿Qué hace el parámetro `encoding` de `open()` y qué ocurre si no lo especificamos?

`encoding` indica cómo convertir entre los bytes del disco y los `str` de Python. Sin especificarlo, Python usa el encoding por defecto del sistema operativo, que varía: en Windows suele ser `cp1252`, en macOS y Linux modernos suele ser `utf-8`. Esto provoca bugs que solo aparecen al pasar un archivo entre sistemas o al desplegar en servidores con locale distinto.

La práctica recomendada es siempre especificar `encoding`, habitualmente `"utf-8"`. En aplicaciones que leen archivos de terceros con encoding desconocido, a veces se combina con `errors="replace"` para no fallar ante bytes inválidos. En modo binario (`"rb"`, `"wb"`) el parámetro no aplica porque se trabaja con `bytes` directamente.

### R3. ¿Cuál es la diferencia entre los modos `"w"` y `"x"` al abrir un archivo?

Ambos abren para escritura, pero se comportan de forma distinta si el archivo ya existe. `"w"` lo trunca silenciosamente: borra el contenido anterior sin previo aviso. `"x"` lanza `FileExistsError`, evitando que se sobrescriba por accidente.

`"x"` es útil en procesos batch o generación de artefactos donde sobrescribir un resultado previo sería un error (por ejemplo, al escribir una exportación con fecha en el nombre). `"w"` es el modo normal cuando sí se quiere reemplazar el contenido, como al actualizar un archivo de configuración.

### R4. ¿Por qué iterar directamente sobre el objeto de archivo es preferible a `readlines()` para archivos grandes?

`readlines()` carga todas las líneas en una lista en memoria, por lo que un archivo de 10 GB requiere alrededor de 10 GB de RAM. Iterar directamente sobre el objeto de archivo (`for linea in f:`) lee una línea cada vez, manteniendo un uso de memoria prácticamente constante independientemente del tamaño del archivo.

Python implementa esta iteración con un buffer interno, así que el rendimiento es comparable o superior al de `readlines()`. La forma idiomática en código profesional es iterar directamente; `readlines()` solo es razonable cuando se sabe que el archivo es pequeño y se necesita indexar aleatoriamente sobre las líneas.

### R5. ¿Cuál es la diferencia entre `json.dump` y `json.dumps`?

`json.dumps` (con `s` al final) devuelve un string con la representación JSON. `json.dump` (sin `s`) escribe directamente sobre un objeto de archivo. La regla mnemotécnica es que la `s` final significa "string".

Lo mismo aplica a la deserialización: `json.loads` parsea un string y `json.load` lee un archivo. Saber cuándo cada variante es más apropiada es importante: `dumps`/`loads` son útiles cuando los datos viajan por red (API responses) o se almacenan en bases de datos como texto. `dump`/`load` evitan pasos intermedios cuando el destino u origen ya es un archivo.

### R6. ¿Qué tipos de Python no son serializables a JSON directamente y cómo se manejan?

JSON solo soporta `dict`, `list`, `str`, `int`, `float`, `bool` y `None`. No soporta `datetime`, `set`, `tuple` (las tuplas se convierten a listas al round-trip), `bytes`, ni instancias de clases personalizadas. Intentar serializar uno de estos lanza `TypeError`.

La solución habitual es convertir manualmente antes de serializar: `datetime.isoformat()` para fechas, `list(mi_set)` para conjuntos, `base64.b64encode` para bytes. Otra opción es pasar `default=` a `dumps`, una función que Python llama cuando encuentra un tipo no serializable; allí se implementa la conversión. Para casos complejos, se suele escribir un `json.JSONEncoder` personalizado o usar una librería como `pydantic` que encapsula el mapeo.

### R7. ¿Por qué hay que pasar `newline=""` al abrir archivos para leer o escribir CSV?

El módulo `csv` gestiona los saltos de línea internamente porque la convención CSV permite saltos de línea dentro de campos entrecomillados (`"nombre\ncon salto"`), que no deben tratarse como fin de registro. Si se abre el archivo sin `newline=""`, Python aplica su traducción de saltos de línea normal, que puede interferir con la lógica de `csv` y corromper los datos al escribir o leer.

Este detalle está marcado como obligatorio en la documentación oficial. Es uno de los errores más típicos al trabajar con CSV por primera vez porque el archivo "parece" correcto pero genera líneas extra en Windows o trunca campos multilinea.

### R8. ¿Qué ventajas tiene `csv.DictReader` sobre `csv.reader`?

`DictReader` devuelve cada fila como un diccionario con las columnas como claves, mientras que `reader` devuelve listas con índices posicionales. El código resultante con `DictReader` es auto-documentado (`fila["precio"]` frente a `fila[2]`) y resistente a cambios de orden de columnas en el archivo.

La misma ventaja se aplica a `DictWriter`: las filas se escriben pasando diccionarios, y el mapeo a columnas lo gestiona el writer con el parámetro `fieldnames`. En código profesional, la versión con diccionarios es la opción por defecto salvo para archivos muy específicos donde el orden posicional es estable y obvio.

### R9. ¿Cuáles son las principales limitaciones y riesgos de `pickle`?

Pickle tiene tres limitaciones importantes. **Específico de Python**: los archivos solo son legibles desde Python, así que no sirve para intercambiar datos con otros lenguajes. **Frágil ante cambios de código**: si renombras una clase o mueves un módulo, los pickle generados previamente dejan de cargarse. **Inseguro**: `pickle.load` puede ejecutar código arbitrario si el archivo ha sido manipulado, porque el formato incluye instrucciones que se evalúan durante la deserialización.

Por el riesgo de seguridad, **nunca** cargar pickle de fuentes no confiables (uploads de usuarios, downloads externos, mensajes por red). El caso de uso legítimo es cachear resultados costosos dentro de un proceso controlado, donde el archivo no sale del sistema. Para intercambio de datos, JSON o formatos binarios como MessagePack son alternativas seguras y portables.

### R10. ¿Qué ventajas ofrece `pathlib` sobre `os.path`?

`pathlib` presenta una API orientada a objetos: un `Path` es un objeto con métodos descubribles (`exists()`, `is_file()`, `parent`, `name`, `stem`, `suffix`), mientras que `os.path` es un conjunto de funciones que operan sobre strings dispersas entre varios módulos (`os`, `os.path`, `shutil`).

La composición de rutas es más legible con el operador `/` (`base / "config" / "app.toml"`) que con `os.path.join(base, "config", "app.toml")`. `pathlib` normaliza separadores automáticamente entre Windows y Unix. Desde Python 3.6, cualquier función de stdlib que acepte un path también acepta un `Path`, por lo que no hay fricción al interoperar con librerías existentes. En código moderno es la opción recomendada; `os.path` sigue siendo válido para mantener compatibilidad con código legacy.

### R11. ¿Cuándo se prefiere `Path.rglob` frente a `os.walk`?

`Path.rglob(patron)` es más conciso cuando basta con filtrar por un patrón glob sobre todo el árbol (`Path("src").rglob("*.py")`). Devuelve directamente un iterador de paths, evitando las tuplas y bucles anidados de `os.walk`.

`os.walk` se prefiere cuando se necesita control sobre la estructura del recorrido: por ejemplo, saltar subdirectorios enteros modificando la lista `dirnames` in-place, o procesar directorios y archivos de forma distinta en cada nivel. Para la mayoría de scripts que simplemente "buscan archivos que cumplen X", `rglob` es más idiomático.

### R12. ¿Por qué `f.writelines(lista)` no añade saltos de línea entre los elementos?

El nombre es engañoso: `writelines` no interpreta sus argumentos como "líneas", solo los escribe concatenados sin separador. El motivo histórico es que es la contraparte simétrica de `readlines()`, que devuelve las líneas con el `\n` incluido — así, `f.writelines(f.readlines())` reproduce el archivo original.

Si los datos no incluyen saltos de línea, hay que añadirlos explícitamente antes de pasarlos, por ejemplo con una comprensión (`[linea + "\n" for linea in items]`). En la práctica, construir el texto completo con `"\n".join(...)` y escribirlo con `f.write(...)` suele ser más claro que preparar una lista para `writelines`.
