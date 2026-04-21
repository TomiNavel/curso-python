# 2. Strings — Errores Comunes

## E1. Olvidar que los métodos de string no modifican el original

```python
# MAL — el método se ejecuta pero el resultado se descarta
nombre = "ana garcía"
nombre.title()
print(nombre)  # "ana garcía" — sin cambios

# BIEN — reasignar el resultado
nombre = "ana garcía"
nombre = nombre.title()
print(nombre)  # "Ana García"
```

Los strings son inmutables. Cada método devuelve un **nuevo** string — si no se asigna a una variable, se pierde. Este error es especialmente silencioso porque no lanza ninguna excepción; simplemente no pasa nada.

## E2. Usar `+` en un bucle para construir strings

```python
# MAL — O(n²), crea un nuevo string en cada iteración
resultado = ""
for palabra in ["hola", "mundo", "cruel"]:
    resultado += " " + palabra

# BIEN — O(n), construye el resultado de una sola vez
resultado = " ".join(["hola", "mundo", "cruel"])
```

Cada `+=` crea un nuevo objeto string en memoria, copia el contenido anterior y le añade el nuevo fragmento. Con muchas iteraciones, el rendimiento se degrada cuadráticamente. `join()` reserva la memoria necesaria una sola vez.

## E3. Confundir `find()` con `index()` y no manejar la ausencia

```python
# MAL — index() lanza ValueError si no encuentra
texto = "hola mundo"
pos = texto.index("python")  # ValueError: substring not found

# BIEN — find() devuelve -1, permite comprobar sin excepción
pos = texto.find("python")
if pos == -1:
    print("No encontrado")
```

Usar `index()` cuando el substring podría no existir provoca excepciones no controladas. `find()` es la opción segura para búsquedas donde la ausencia es un resultado normal, no un error.

## E4. No especificar encoding al abrir archivos

```python
# MAL — usa el encoding del sistema operativo (cp1252 en Windows)
with open("datos.txt") as f:
    contenido = f.read()  # puede corromper caracteres como ñ, á, ü

# BIEN — encoding explícito
with open("datos.txt", encoding="utf-8") as f:
    contenido = f.read()
```

Sin encoding explícito, Python usa el del sistema operativo. En Windows suele ser `cp1252`, no `utf-8`. Un archivo creado en Linux (utf-8) se lee mal en Windows si no se especifica el encoding. Esto causa errores silenciosos: el programa no falla, pero los caracteres especiales se corrompen.

## E5. Usar `split()` y `split(" ")` como si fueran iguales

```python
texto = "  hola   mundo  "

# split() sin argumentos: elimina espacios múltiples y extremos
print(texto.split())       # ["hola", "mundo"]

# split(" "): divide por CADA espacio individual, incluyendo vacíos
print(texto.split(" "))    # ["", "", "hola", "", "", "mundo", "", ""]
```

`split()` sin argumentos es mucho más inteligente: trata cualquier cantidad de espacios en blanco (espacios, tabs, saltos de línea) como un solo separador, y además ignora los extremos. `split(" ")` divide literalmente por cada espacio, lo que genera strings vacíos cuando hay espacios múltiples o al inicio/final.

## E6. Comparar strings sin normalizar

```python
# MAL — falla porque las mayúsculas difieren
usuario = input("¿Aceptas? (si/no): ")
if usuario == "si":
    print("Aceptado")  # no se ejecuta si el usuario escribe "Si", "SI", "sI"

# BIEN — normalizar antes de comparar
usuario = input("¿Aceptas? (si/no): ")
if usuario.strip().lower() == "si":
    print("Aceptado")  # funciona con "Si", " si ", "SI", etc.
```

El input del usuario es impredecible: puede incluir mayúsculas, espacios al inicio/final, o ambas cosas. Siempre normalizar con `strip()` y `lower()` antes de comparar.

## E7. Usar slicing negativo sin entender la indexación

```python
texto = "Python"

# MAL — esperar que [-3:-1] incluya el último carácter
print(texto[-3:-1])  # "ho", no "hon" — el índice final no se incluye

# BIEN — omitir el final para llegar hasta el último carácter
print(texto[-3:])    # "hon"
```

El índice final del slicing nunca se incluye en el resultado. Esto confunde especialmente con índices negativos, donde `-1` es el último carácter pero `texto[-3:-1]` no lo incluye. Para llegar hasta el final, omitir el segundo índice.

## E8. Creer que `isdigit()` valida números en general

```python
# isdigit() NO reconoce negativos, decimales ni notación científica
print("-5".isdigit())      # False
print("3.14".isdigit())    # False
print("1e10".isdigit())    # False
print("123".isdigit())     # True — solo dígitos puros

# Para validar si un string es un número válido:
def es_numero(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
```

`isdigit()` comprueba si todos los caracteres son dígitos (0-9), nada más. No sirve para validar números con signo, decimales o notación científica. Para eso hay que intentar la conversión con `float()` y capturar la excepción.

## E9. Decodificar bytes con un encoding incorrecto

```python
# MAL — no falla pero produce texto corrupto
datos = "año".encode("utf-8")       # b'a\xc3\xb1o'
texto = datos.decode("latin-1")     # "aÃ±o" — corrupto, sin error

# BIEN — usar el mismo encoding
datos = "año".encode("utf-8")
texto = datos.decode("utf-8")       # "año" — correcto
```

Este error es traicionero porque muchas veces no lanza excepción — simplemente produce texto con caracteres extraños. Si un fichero o una API devuelve texto corrupto con caracteres como `Ã±` o `Ã©`, casi siempre es un problema de encoding: los bytes están en utf-8 pero se están leyendo como latin-1 o cp1252.
