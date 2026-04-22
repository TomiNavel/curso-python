# 22. Trabajo con Archivos y Serialización

Casi cualquier aplicación real necesita persistir datos: configuraciones, logs, exportaciones, resultados de procesamiento, estado entre ejecuciones. Python ofrece dos capas complementarias: una capa de **entrada/salida** sobre archivos (abrir, leer, escribir) y una capa de **serialización** que convierte estructuras de datos en bytes reversibles. Dominar ambas es habitual en entrevistas porque aparecen en cualquier proyecto no trivial y los errores suelen ser silenciosos (encoding mal detectado, archivos abiertos sin cerrar, JSON que no round-trip correctamente).

## 22.1. Lectura y escritura de archivos

Trabajar con archivos en Python siempre pasa por la función `open()`, que devuelve un objeto de archivo. Ese objeto expone métodos para leer y escribir, y debe cerrarse al terminar para liberar el descriptor del sistema operativo y asegurar que los datos escritos lleguen a disco. En código productivo, `open()` se usa casi siempre como context manager (`with open(...) as f:`) — ya introducido en el tema 21 — porque garantiza el cierre incluso si salta una excepción.

### 22.1.1. open() y modos de apertura (r, w, a, x, b)

El primer argumento de `open()` es la ruta y el segundo es el modo, un string corto que indica la intención: leer, escribir, añadir, en texto o en binario. El modo por defecto es `"r"` (lectura en texto).

Los modos básicos son combinaciones de dos ejes:

- **Qué hacer**: `r` leer, `w` escribir sobreescribiendo, `a` añadir al final, `x` crear fallando si existe.
- **Cómo interpretar los bytes**: sin sufijo (texto, con decodificación) o con `b` (binario, bytes crudos).

```python
with open("config.txt", "r") as f:      # leer texto
    texto = f.read()

with open("salida.txt", "w") as f:      # crea o sobreescribe
    f.write("hola\n")

with open("log.txt", "a") as f:         # añade al final
    f.write("nueva línea\n")

with open("nuevo.txt", "x") as f:       # error si ya existe
    f.write("primera versión")

with open("imagen.png", "rb") as f:     # binario: devuelve bytes
    datos = f.read()
```

La diferencia entre `w` y `x` es importante en trabajos batch: `w` borra silenciosamente el archivo previo, mientras que `x` lanza `FileExistsError` — útil para evitar sobrescribir resultados por accidente. El modo `a` nunca trunca; simplemente coloca el cursor al final antes de escribir.

Hay un tercer eje, `+`, que añade lectura/escritura simultánea (`r+`, `w+`, `a+`). Se usa poco en código profesional porque mezcla responsabilidades y el posicionamiento del cursor es confuso. Si necesitas leer y después reescribir, casi siempre es más claro abrir el archivo dos veces.

### 22.1.2. El parámetro encoding

En modo texto, Python decodifica los bytes del disco a `str` usando un encoding. Si no se especifica, usa el del sistema (`locale.getpreferredencoding()`), que varía entre Windows (`cp1252`), macOS y Linux (`utf-8`). Este detalle provoca bugs que solo se ven en producción: un archivo que abre bien en el portátil del desarrollador falla en el servidor con `UnicodeDecodeError`.

La regla práctica es: **siempre especificar `encoding` cuando se trabaja con texto**. En 99% de los casos, `"utf-8"`.

```python
with open("datos.csv", "r", encoding="utf-8") as f:
    contenido = f.read()
```

Para archivos que pueden tener caracteres problemáticos (exportaciones de sistemas antiguos, correos), `errors="replace"` sustituye bytes inválidos por `?` en lugar de fallar:

```python
with open("legacy.txt", "r", encoding="utf-8", errors="replace") as f:
    texto = f.read()
```

En modo binario (`"rb"`, `"wb"`) no hay encoding porque se trabaja con `bytes` directamente — es responsabilidad del programador decodificarlos si lo necesita.

### 22.1.3. Leer archivos (read, readline, readlines)

El objeto de archivo ofrece tres formas de leer, con trade-offs distintos:

- `f.read()`: devuelve todo el contenido como un único string. Cómodo para archivos pequeños (configuración, un JSON). Peligroso con archivos grandes: carga todo en memoria.
- `f.readline()`: lee una línea, incluyendo el `\n` final. Útil cuando el procesamiento depende de leer cabeceras antes que el resto.
- `f.readlines()`: devuelve una lista con todas las líneas. Tiene el mismo problema de memoria que `read()` y además el coste extra del objeto lista.

```python
with open("articulo.md", "r", encoding="utf-8") as f:
    cabecera = f.readline()          # primera línea
    cuerpo = f.read()                # el resto
```

Para archivos grandes, el patrón idiomático es iterar directamente sobre el objeto de archivo — lo veremos en el siguiente apartado.

### 22.1.4. Escribir archivos (write, writelines)

La escritura es más simple que la lectura: `f.write(string)` añade el string tal cual (no pone `\n` automáticamente) y `f.writelines(iterable)` escribe cada elemento sin separadores. El nombre `writelines` despista porque **no añade saltos de línea** — si los datos no los incluyen ya, hay que concatenarlos a mano.

```python
lineas = ["nombre,edad\n", "Ana,30\n", "Luis,25\n"]

with open("personas.csv", "w", encoding="utf-8") as f:
    f.writelines(lineas)
```

Cuando se escribe mucho contenido dinámico, construir las líneas con `"\n".join(...)` suele ser más claro que acumular strings con `\n` en cada elemento.

En modo texto, Python traduce `\n` al separador de línea del sistema operativo al escribir (en Windows, eso significa escribir `\r\n`). En modo binario, los bytes van a disco exactamente como se pasan.

### 22.1.5. Archivos como iteradores (lectura línea a línea)

Un objeto de archivo en modo texto es iterable: cada iteración devuelve una línea. Esto es la forma correcta de procesar archivos grandes porque solo carga una línea en memoria a la vez, independientemente del tamaño total.

```python
with open("logs.txt", "r", encoding="utf-8") as f:
    for linea in f:
        if "ERROR" in linea:
            print(linea.rstrip())
```

`rstrip()` quita el `\n` final, que Python conserva al iterar. Este patrón procesa archivos de gigabytes sin problema, a diferencia de `readlines()` o `read().splitlines()`.

En entrevistas se valora distinguir cuándo una solución fallará con archivos grandes. Si la pregunta implica "contar/filtrar/transformar líneas de un archivo", la respuesta esperada casi siempre es iterar directamente, no leer todo en memoria primero.

## 22.2. pathlib

Durante años, el manejo de rutas en Python se hacía con el módulo `os.path`, una colección de funciones que operan sobre strings. Era funcional pero verboso: concatenar rutas, separarlas, comprobar existencia y listar directorios requerían cada una una función distinta. `pathlib` (introducido en Python 3.4) agrupa todo esto en un objeto `Path` con métodos descubribles y una API más uniforme. Es el enfoque recomendado en proyectos nuevos.

### 22.2.1. Path: crear y manipular rutas

Un `Path` representa una ruta del sistema de archivos. Se crea a partir de uno o varios segmentos, y se compone usando el operador `/` — más legible que las llamadas anidadas a `os.path.join`.

```python
from pathlib import Path

proyecto = Path("/home/usuario/proyectos/miapp")
config = proyecto / "config" / "settings.toml"

print(config.name)        # "settings.toml"
print(config.stem)        # "settings"
print(config.suffix)      # ".toml"
print(config.parent)      # "/home/usuario/proyectos/miapp/config"
```

`Path` normaliza el separador según el sistema operativo (en Windows usa `\`, en Unix `/`), así que el mismo código funciona en ambos sin `if platform.system() ==`. El operador `/` funciona también cuando el lado derecho es un string, lo que evita construir sub-paths manualmente.

Los atributos más usados son `name` (nombre con extensión), `stem` (nombre sin extensión), `suffix` (extensión con el punto) y `parent` (directorio contenedor).

### 22.2.2. Operaciones con archivos y directorios

`Path` trae métodos para las operaciones de sistema de archivos más comunes, evitando tener que importar `os` para cada una:

```python
ruta = Path("datos/informe.txt")

ruta.exists()              # True/False
ruta.is_file()             # True si es archivo regular
ruta.is_dir()              # True si es directorio
ruta.stat().st_size        # tamaño en bytes

ruta.parent.mkdir(parents=True, exist_ok=True)   # crea directorios intermedios
ruta.write_text("contenido", encoding="utf-8")   # abre, escribe y cierra
texto = ruta.read_text(encoding="utf-8")         # abre, lee y cierra
ruta.unlink()                                    # borra el archivo
```

`mkdir(parents=True, exist_ok=True)` es el equivalente a `mkdir -p` de Unix: crea la ruta entera sin fallar si ya existe. Sin estas banderas, mkdir lanza `FileNotFoundError` si falta un directorio intermedio y `FileExistsError` si el destino ya existe.

Los helpers `read_text`/`write_text` son atajos muy útiles para archivos pequeños — abren, operan y cierran en una sola línea. Para archivos grandes sigue siendo preferible `open()` con iteración para no cargar todo en memoria.

### 22.2.3. pathlib vs os.path

En código nuevo, `pathlib` es la opción recomendada por varias razones:

- API más compacta: `ruta.exists()` frente a `os.path.exists(ruta)`.
- Composición con `/` en lugar de `os.path.join(a, b, c)`.
- Métodos agrupados en el mismo objeto en vez de repartidos entre `os`, `os.path` y `shutil`.
- Tipado más claro: un `Path` es un `Path`, no un string que podría contener cualquier cosa.

La razón principal para seguir viendo `os.path` es compatibilidad con código antiguo o APIs externas que esperan strings. Si una librería quiere un string, se convierte con `str(ruta)` sin fricción. En sentido inverso, todo lo que acepte una ruta en stdlib desde Python 3.6 acepta también `Path` directamente.

En entrevistas, usar `pathlib` demuestra familiaridad con código Python moderno. Mencionar que `os.path` sigue siendo válido para interoperar con código legacy también muestra criterio.

### 22.2.4. Recorrer directorios (os.walk y Path.rglob)

Cuando hay que procesar todos los archivos de un árbol de directorios — por ejemplo, para encontrar todos los `.py` de un proyecto o mover todas las imágenes — hay dos herramientas principales: `os.walk` y `Path.rglob`.

`os.walk` recorre recursivamente y devuelve, por cada directorio, una tupla con `(dirpath, dirnames, filenames)`. Da control fino pero es verboso:

```python
import os

for dirpath, _, filenames in os.walk("src"):
    for nombre in filenames:
        if nombre.endswith(".py"):
            print(os.path.join(dirpath, nombre))
```

`Path.rglob(pattern)` devuelve directamente un iterador con todos los paths que encajan con el patrón glob, recorriendo subdirectorios. Mucho más conciso para el caso habitual:

```python
from pathlib import Path

for archivo in Path("src").rglob("*.py"):
    print(archivo)
```

`rglob` es preferible cuando basta con un patrón glob. `os.walk` sigue siendo útil cuando se necesita conocer o modificar la estructura de directorios durante el recorrido (por ejemplo, saltar un subdirectorio entero modificando `dirnames` in-place).

## 22.3. Serialización

Serializar es convertir una estructura de datos en memoria en una secuencia de bytes que se pueda guardar o transmitir, y deserializar es el proceso inverso. Python ofrece tres formatos integrados con casos de uso distintos: **JSON** para intercambio con otros sistemas, **CSV** para datos tabulares legibles, y **pickle** para guardar objetos Python específicos. Elegir el formato correcto es parte del diseño.

### 22.3.1. JSON (json.dumps, json.loads, json.dump, json.load)

JSON es el formato estándar de intercambio de datos en la web y APIs. Es texto legible por humanos, soportado por prácticamente cualquier lenguaje, y mapea de forma natural a tipos básicos de Python: `dict`, `list`, `str`, `int`, `float`, `bool`, `None`.

El módulo `json` ofrece cuatro funciones principales, combinación de "trabajar con string" vs "trabajar con archivo" y "serializar vs deserializar":

| Operación | A/desde string | A/desde archivo |
|-----------|---------------|-----------------|
| Python → JSON | `json.dumps(obj)` | `json.dump(obj, f)` |
| JSON → Python | `json.loads(texto)` | `json.load(f)` |

La regla mnemotécnica: la `s` al final ("dumps", "loads") significa "string". Sin la `s`, trabajan con un objeto de archivo.

```python
import json

datos = {"usuario": "ana", "edad": 30, "activo": True}

# A string
texto = json.dumps(datos, indent=2, ensure_ascii=False)

# A archivo
with open("usuario.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)

# Desde archivo
with open("usuario.json", "r", encoding="utf-8") as f:
    recuperado = json.load(f)
```

Dos parámetros son casi siempre necesarios en código real:

- `indent=2` formatea el JSON con saltos de línea y sangría para que sea legible por humanos. En producción, a veces se omite para minimizar el tamaño transmitido.
- `ensure_ascii=False` permite escribir caracteres no ASCII (acentos, ñ, emojis) tal cual en lugar de como escapes `\uXXXX`. Mejor legibilidad, mismo significado.

JSON no soporta todos los tipos de Python: `datetime`, `set`, `bytes`, clases personalizadas y tuplas (las tuplas se convierten en listas). Intentar serializar uno de estos provoca `TypeError`. La solución habitual es convertir a un tipo compatible antes de serializar (`datetime.isoformat()` → string) o pasar un `default=` que sepa manejarlo.

### 22.3.2. CSV (csv.reader, csv.writer, csv.DictReader, csv.DictWriter)

CSV ("comma-separated values") es el formato natural para datos tabulares: hojas de cálculo, exportaciones de bases de datos, dumps de logs estructurados. El módulo `csv` ofrece dos pares de API: uno basado en listas (`reader`/`writer`) y otro basado en diccionarios (`DictReader`/`DictWriter`).

La versión con diccionarios es preferible en casi todos los casos porque cada fila queda auto-documentada por los nombres de columna, en vez de depender de índices posicionales frágiles.

```python
import csv

# Escribir con DictWriter
personas = [
    {"nombre": "Ana", "edad": 30},
    {"nombre": "Luis", "edad": 25},
]

with open("personas.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "edad"])
    writer.writeheader()
    writer.writerows(personas)

# Leer con DictReader
with open("personas.csv", "r", encoding="utf-8", newline="") as f:
    for fila in csv.DictReader(f):
        print(fila["nombre"], fila["edad"])
```

El detalle de `newline=""` al abrir el archivo es una de las trampas más típicas de CSV. El módulo `csv` gestiona los saltos de línea internamente según la convención del formato (que puede mezclar `\r\n` dentro de campos entrecomillados). Si no se pasa `newline=""`, Python convierte esos saltos de línea al leer/escribir y corrompe los datos. En la documentación oficial este detalle está marcado como obligatorio.

CSV no conoce tipos: todo lo que lee son strings, incluso si originalmente era un número. Convertir a `int`/`float` es responsabilidad del código que lee, y conviene validar que el input tiene el formato esperado porque CSV malformado (comillas sin cerrar, número de columnas irregular) no siempre salta como error.

### 22.3.3. pickle (serialización binaria de objetos Python)

`pickle` serializa casi cualquier objeto Python (listas, diccionarios, instancias de clases personalizadas, funciones) a bytes, y los deserializa reconstruyendo el objeto original. Su principal ventaja es que "simplemente funciona" con tipos Python: no hay que transformar `datetime` ni definir un mapeo como con JSON.

```python
import pickle

datos = {"usuarios": ["ana", "luis"], "activos": True, "creado": 42}

with open("cache.pkl", "wb") as f:           # modo binario
    pickle.dump(datos, f)

with open("cache.pkl", "rb") as f:
    recuperado = pickle.load(f)
```

Limitaciones importantes:

- **Específico de Python**: los archivos pickle solo se leen desde Python. Inútil para intercambiar datos con sistemas en otros lenguajes.
- **Riesgo de seguridad**: `pickle.load` ejecuta código arbitrario si el archivo ha sido manipulado. **Nunca** cargar pickle de fuentes no confiables (downloads, uploads de usuarios, red). En entrevistas, mencionar esto al hablar de pickle marca la diferencia entre alguien que lo ha usado y alguien que entiende sus implicaciones.
- **Sensible a cambios de código**: si renombras una clase o cambias su módulo, los pickle existentes dejan de cargarse.

El caso de uso legítimo es cachear resultados costosos de computación entre ejecuciones del mismo programa — por ejemplo, el resultado de un entrenamiento de modelo o un grafo ya procesado — donde el archivo nunca sale del propio sistema controlado.

Para cualquier intercambio de datos entre procesos o sistemas distintos, JSON (o formatos binarios como MessagePack o Protocol Buffers) son alternativas más seguras y portables.
