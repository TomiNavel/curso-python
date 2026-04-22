# Errores Comunes: Archivos y Serialización

## Error 1. No especificar `encoding` al abrir archivos de texto

Sin `encoding`, Python usa el del sistema operativo, que varía entre Windows, macOS y Linux. El mismo archivo puede leerse correctamente en un portátil y fallar en el servidor con `UnicodeDecodeError`.

```python
# MAL: depende del locale del sistema
with open("datos.txt") as f:
    contenido = f.read()

# BIEN: explícito y portable
with open("datos.txt", encoding="utf-8") as f:
    contenido = f.read()
```

En la práctica, casi todos los proyectos modernos usan `utf-8` como estándar. Especificarlo siempre evita sorpresas al desplegar.

---

## Error 2. Usar `open()` sin `with` y olvidar `close()`

Si `open()` no va dentro de un `with`, el archivo queda abierto hasta que el recolector de basura lo libere — y en escritura, los datos pueden perderse si no se hace flush.

```python
# MAL: si algo falla antes del close, el archivo queda abierto
f = open("salida.txt", "w")
f.write("datos")
procesar(datos)  # si lanza excepción, el archivo no se cierra
f.close()

# BIEN: garantiza el cierre incluso ante excepciones
with open("salida.txt", "w", encoding="utf-8") as f:
    f.write("datos")
    procesar(datos)
```

En entrevistas, usar `with` es la respuesta esperada; escribir `open` sin context manager es señal de código no idiomático.

---

## Error 3. Usar `readlines()` con archivos grandes

`readlines()` carga todas las líneas en una lista en memoria. Con un archivo de varios gigabytes, el proceso se queda sin RAM aunque solo se quiera contar líneas.

```python
# MAL: carga todo el archivo en memoria
with open("logs.txt", encoding="utf-8") as f:
    for linea in f.readlines():
        procesar(linea)

# BIEN: itera línea a línea, memoria constante
with open("logs.txt", encoding="utf-8") as f:
    for linea in f:
        procesar(linea)
```

Iterar directamente sobre el objeto de archivo es igual de cómodo y escala a archivos de cualquier tamaño.

---

## Error 4. Serializar `datetime` o `set` con JSON sin convertir

JSON no conoce tipos como `datetime`, `set`, `bytes` o clases personalizadas. Intentar serializarlos lanza `TypeError` con un mensaje críptico.

```python
import json
from datetime import datetime

datos = {"creado": datetime.now()}

# MAL: TypeError: Object of type datetime is not JSON serializable
json.dumps(datos)

# BIEN: convertir antes de serializar
datos = {"creado": datetime.now().isoformat()}
json.dumps(datos)
```

Alternativas: pasar `default=str` para un casting rápido, o escribir un `JSONEncoder` personalizado cuando la conversión necesita lógica.

---

## Error 5. Abrir CSV sin `newline=""`

El módulo `csv` gestiona los saltos de línea internamente. Abrir sin `newline=""` hace que Python traduzca los saltos al escribir y al leer, lo que provoca líneas en blanco extra en Windows o campos multilinea rotos.

```python
# MAL: genera líneas en blanco entre registros en Windows
with open("datos.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b"])

# BIEN: deja que csv gestione los saltos de línea
with open("datos.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b"])
```

Es uno de los detalles más fáciles de olvidar porque el código funciona en Linux pero genera basura en Windows.

---

## Error 6. Olvidar que CSV lee todo como string

`csv.reader` y `csv.DictReader` devuelven siempre strings, incluso si la columna contenía un número. Comparar con `int` o sumar directamente da resultados inesperados.

```python
# MAL: comparación alfabética, no numérica
with open("productos.csv", encoding="utf-8", newline="") as f:
    for fila in csv.DictReader(f):
        if fila["precio"] > 100:  # "95" > 100 es True (string > int comparación lexicográfica falla)
            ...

# BIEN: convertir explícitamente
with open("productos.csv", encoding="utf-8", newline="") as f:
    for fila in csv.DictReader(f):
        if float(fila["precio"]) > 100:
            ...
```

Cuando el CSV puede estar mal formado, conviene envolver la conversión en `try/except` para no fallar ante filas corruptas.

---

## Error 7. Cargar pickle de fuentes no confiables

`pickle.load` puede ejecutar código arbitrario al deserializar. Un archivo pickle manipulado puede comprometer el proceso al cargarlo. Nunca aceptar pickle desde internet, uploads de usuarios o mensajes de red.

```python
# MAL: permite ejecución de código arbitrario
datos_del_usuario = request.body
objeto = pickle.loads(datos_del_usuario)

# BIEN: usar un formato seguro para datos externos
objeto = json.loads(datos_del_usuario)
```

Pickle es apropiado solo para intercambio interno dentro de un proceso controlado (caches, checkpoints). Para cualquier comunicación entre sistemas o con usuarios, usar JSON u otro formato sin ejecución implícita.

---

## Error 8. Concatenar rutas con strings en lugar de `pathlib`

Concatenar rutas a mano con `+` o barras literales produce código que falla entre sistemas operativos y es frágil ante separadores duplicados.

```python
# MAL: separadores hardcoded, no cross-platform
ruta = base + "/config/" + archivo

# BIEN: pathlib normaliza y compone limpiamente
from pathlib import Path
ruta = Path(base) / "config" / archivo
```

`Path` usa el separador correcto del sistema automáticamente y evita errores como `/config//app.toml` cuando alguno de los fragmentos ya termina en `/`.

---

## Error 9. Usar `w` cuando se quería `a`

Abrir en modo `w` un archivo existente borra el contenido previo sin aviso. Es un error especialmente doloroso en scripts que anotan resultados incrementales: al relanzar el script, se pierde todo lo anterior.

```python
# MAL: borra los logs anteriores cada ejecución
with open("registro.log", "w", encoding="utf-8") as f:
    f.write(nueva_entrada + "\n")

# BIEN: añade al final
with open("registro.log", "a", encoding="utf-8") as f:
    f.write(nueva_entrada + "\n")
```

Cuando el objetivo es "no sobrescribir nunca", usar `x` en lugar de `w` hace que el programa falle explícitamente si el archivo ya existe, en vez de borrar datos silenciosamente.

---

## Error 10. Escribir JSON sin `ensure_ascii=False` y con caracteres no ASCII

Por defecto, `json.dumps` escapa los caracteres no ASCII como `\uXXXX`. El JSON es válido pero ilegible: un nombre como "García" se guarda como `"García"`.

```python
import json

# MAL: archivo ilegible para humanos
json.dumps({"nombre": "García"})  # '{"nombre": "Garc\\u00eda"}'

# BIEN: caracteres no ASCII tal cual
json.dumps({"nombre": "García"}, ensure_ascii=False)  # '{"nombre": "García"}'
```

El significado es idéntico — cualquier parser JSON descodifica ambas formas al mismo string — pero cuando el archivo se abre en un editor, la versión sin escapar es mucho más útil.
