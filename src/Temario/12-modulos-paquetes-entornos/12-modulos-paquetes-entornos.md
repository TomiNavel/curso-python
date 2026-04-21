# 12. Módulos, Paquetes y Entornos Virtuales

Cuando un programa crece más allá de un solo archivo, necesita organizarse en partes reutilizables. Python resuelve esto con módulos (archivos `.py` individuales) y paquetes (directorios que agrupan módulos). Además, la librería estándar incluye decenas de módulos listos para usar — desde manipulación de rutas hasta generación de números aleatorios. Y para gestionar dependencias de terceros sin conflictos entre proyectos, Python ofrece entornos virtuales. Este tema cubre toda esa cadena: cómo importar, cómo organizar y cómo aislar.

---

## 12.1. Módulos

### 12.1.1. Qué es un módulo

Un módulo es simplemente un archivo `.py`. Cualquier archivo Python es un módulo que puede ser importado por otro. Cuando se importa un módulo, Python ejecuta todo el código del archivo de arriba a abajo (una sola vez) y crea un objeto módulo con todo lo que se definió: funciones, clases, variables.

```python
# archivo: matematicas.py
PI = 3.14159

def area_circulo(radio):
    return PI * radio ** 2

def perimetro_circulo(radio):
    return 2 * PI * radio
```

Este archivo define un módulo llamado `matematicas`. Las funciones y variables que contiene están disponibles para cualquier otro archivo que lo importe.

El hecho de que Python ejecute el archivo al importarlo tiene una consecuencia importante: si el módulo contiene código "suelto" (llamadas a funciones, prints, etc.), ese código se ejecutará en el momento de la importación, no cuando se llame a una función del módulo. Por eso es fundamental separar las definiciones del código de ejecución (ver sección 12.1.3).

### 12.1.2. import, from...import, alias (as)

Hay varias formas de importar un módulo o partes de él:

**`import modulo`** — importa el módulo completo. Se accede a su contenido con notación de punto:

```python
import matematicas

print(matematicas.PI)                    # 3.14159
print(matematicas.area_circulo(5))       # 78.53975
```

Esta forma es la más explícita: cada vez que se usa algo del módulo, queda claro de dónde viene. Es la forma preferida para módulos grandes o cuando se usan pocos elementos.

**`from modulo import nombre`** — importa elementos específicos directamente al espacio de nombres actual:

```python
from matematicas import area_circulo, PI

print(PI)                # 3.14159
print(area_circulo(5))   # 78.53975 — sin prefijo "matematicas."
```

Es más cómodo cuando se usan pocos elementos del módulo con frecuencia. La desventaja es que pierde claridad sobre el origen: si el archivo importa `area_circulo` de un módulo y `area_rectangulo` de otro, no queda claro a simple vista de dónde viene cada uno.

**`from modulo import *`** — importa todo lo que el módulo expone al espacio de nombres actual:

```python
from matematicas import *

print(PI)                # funciona, pero ¿de dónde viene PI?
```

Esta forma es mala práctica en código de producción. Contamina el espacio de nombres, hace imposible saber de dónde viene cada nombre y puede sobrescribir variables existentes sin aviso. Solo es aceptable en sesiones interactivas del intérprete para explorar un módulo rápidamente.

**`as`** — crea un alias para el módulo o el nombre importado:

```python
import matematicas as mat

print(mat.area_circulo(5))

from matematicas import area_circulo as area

print(area(5))
```

Los alias son útiles cuando el nombre del módulo es largo o cuando hay conflictos de nombres. Algunos alias son convenciones establecidas en la comunidad Python: `import numpy as np`, `import pandas as pd`.

### 12.1.3. El módulo \_\_main\_\_ y if \_\_name\_\_ == "\_\_main\_\_"

Cada módulo tiene un atributo especial `__name__` que Python establece automáticamente. Cuando un archivo se ejecuta directamente (por ejemplo, `python mi_script.py`), su `__name__` vale `"__main__"`. Cuando se importa desde otro archivo, `__name__` vale el nombre del módulo (por ejemplo, `"mi_script"`).

Este mecanismo permite que un archivo se comporte de forma diferente según se ejecute directamente o se importe:

```python
# archivo: utilidades.py
def saludar(nombre):
    return f"Hola, {nombre}"

# Este bloque SOLO se ejecuta si el archivo se ejecuta directamente
# NO se ejecuta cuando otro archivo hace "import utilidades"
if __name__ == "__main__":
    print(saludar("Mundo"))
    print("Ejecutando pruebas...")
```

Sin el guard `if __name__ == "__main__"`, el `print` se ejecutaría cada vez que alguien hiciera `import utilidades`, lo cual es un efecto secundario no deseado.

Este patrón es fundamental por dos razones:

1. **Reutilización** — permite que un archivo funcione tanto como módulo importable como script ejecutable.
2. **Testing** — permite incluir código de prueba rápida en el mismo archivo sin que interfiera cuando se importa el módulo.

```python
# archivo: calculadora.py
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

if __name__ == "__main__":
    # Pruebas rápidas — solo se ejecutan al lanzar el archivo directamente
    assert sumar(2, 3) == 5
    assert restar(10, 4) == 6
    print("Todas las pruebas pasaron")
```

### 12.1.4. La variable \_\_all\_\_

Cuando alguien hace `from modulo import *`, Python busca la variable `__all__` en el módulo para decidir qué nombres exportar. Si `__all__` no existe, se exportan todos los nombres que no empiezan con guion bajo.

```python
# archivo: utilidades.py
__all__ = ["funcion_publica", "CONSTANTE"]

CONSTANTE = 42

def funcion_publica():
    return "pública"

def _funcion_interna():
    return "interna"

def funcion_auxiliar():
    return "auxiliar"
```

Con `from utilidades import *`, solo se importan `funcion_publica` y `CONSTANTE`. Tanto `_funcion_interna` como `funcion_auxiliar` quedan excluidas por la misma razón: no están en `__all__`. Cuando `__all__` existe, es el **único** criterio que determina qué se exporta con `import *`; la convención del guion bajo deja de ser relevante. Si `_funcion_interna` estuviera en `__all__`, se importaría con `import *` a pesar del guion bajo.

Sin `__all__`, Python recurre al mecanismo por defecto: exportar todos los nombres que **no** empiecen con guion bajo. Los dos mecanismos nunca actúan a la vez: si `__all__` existe, tiene prioridad absoluta.

`__all__` no impide el acceso directo — `import utilidades` seguido de `utilidades.funcion_auxiliar()` sigue funcionando. Solo controla el comportamiento de `import *`.

En la práctica, `__all__` se usa sobre todo en paquetes (en el `__init__.py`) para definir la API pública del paquete. En módulos simples, la convención del guion bajo (`_nombre`) suele ser suficiente para señalar lo que es privado.

---

## 12.2. Paquetes

### 12.2.1. Estructura de un paquete (\_\_init\_\_.py)

Un paquete es un directorio que contiene módulos Python y un archivo especial `__init__.py`. Este archivo marca el directorio como un paquete Python y se ejecuta automáticamente cuando se importa el paquete.

```
mi_proyecto/
├── __init__.py          # hace de mi_proyecto un paquete
├── modelos.py
├── servicios.py
└── utilidades/
    ├── __init__.py      # hace de utilidades un subpaquete
    ├── texto.py
    └── numeros.py
```

El `__init__.py` puede estar vacío (es suficiente para que Python reconozca el directorio como paquete) o puede contener código de inicialización y definir la API pública del paquete:

```python
# mi_proyecto/__init__.py
from .modelos import Usuario, Producto
from .servicios import procesar_pedido

__all__ = ["Usuario", "Producto", "procesar_pedido"]
```

Con esto, quien importe el paquete puede escribir:

```python
from mi_proyecto import Usuario, procesar_pedido
```

En lugar de:

```python
from mi_proyecto.modelos import Usuario
from mi_proyecto.servicios import procesar_pedido
```

Desde Python 3.3 existen los **namespace packages** — paquetes sin `__init__.py`. Se crearon para casos avanzados donde un paquete se distribuye en varios directorios. En la práctica, siempre se recomienda incluir `__init__.py`: es explícito, evita ambigüedades y permite control sobre lo que se exporta.

### 12.2.2. Imports absolutos y relativos

Dentro de un paquete, hay dos formas de importar módulos hermanos:

**Imports absolutos** — usan la ruta completa desde la raíz del paquete:

```python
# Desde mi_proyecto/servicios.py
from mi_proyecto.modelos import Usuario
from mi_proyecto.utilidades.texto import limpiar
```

Son explícitos y claros: siempre se sabe exactamente de dónde viene cada import. Son la forma recomendada por PEP 8.

**Imports relativos** — usan puntos para indicar la posición relativa dentro del paquete:

```python
# Desde mi_proyecto/servicios.py
from .modelos import Usuario          # . = mismo directorio (mi_proyecto/)
from .utilidades.texto import limpiar # subpaquete del mismo nivel

# Desde mi_proyecto/utilidades/texto.py
from .. import servicios              # .. = directorio padre (mi_proyecto/)
from ..modelos import Usuario         # módulo en el directorio padre
```

Un punto (`.`) significa "mismo paquete", dos puntos (`..`) significan "paquete padre", tres puntos (`...`) "dos niveles arriba", y así sucesivamente.

Los imports relativos solo funcionan dentro de paquetes — no se pueden usar en scripts ejecutados directamente. Si se intenta ejecutar `python mi_proyecto/servicios.py` directamente, los imports relativos fallan con `ImportError`. Para que funcionen, el archivo debe importarse como parte del paquete: `python -m mi_proyecto.servicios`.

### 12.2.3. Organización de un proyecto

Un proyecto Python bien organizado separa el código fuente, los tests, la configuración y la documentación:

```
mi_proyecto/
├── src/
│   └── mi_proyecto/        # paquete principal
│       ├── __init__.py
│       ├── modelos.py
│       ├── servicios.py
│       └── utilidades/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── test_modelos.py
│   └── test_servicios.py
├── pyproject.toml           # configuración del proyecto
├── requirements.txt         # dependencias
└── README.md
```

Algunas convenciones importantes:

- **Un paquete por responsabilidad** — no meter todo en un solo archivo de 2000 líneas. Dividir por funcionalidad: modelos, servicios, utilidades.
- **Imports al inicio del archivo** — PEP 8 establece que los imports van al principio, agrupados en tres bloques separados por una línea en blanco: (1) librería estándar, (2) terceros, (3) locales.
- **Evitar imports circulares** — si `modelos.py` importa de `servicios.py` y `servicios.py` importa de `modelos.py`, Python entra en un ciclo. La solución suele ser reorganizar el código para romper la dependencia circular, o mover el import dentro de la función que lo necesita.

```python
# Orden correcto de imports según PEP 8
import os                          # librería estándar
import sys
from pathlib import Path

import requests                    # terceros (pip install)
from flask import Flask

from .modelos import Usuario       # locales (del propio proyecto)
from .utilidades import limpiar
```

---

## 12.3. Módulos de la librería estándar

Python incluye una librería estándar extensa — módulos listos para usar sin instalar nada. Conocer los más comunes ahorra tiempo y evita reinventar la rueda.

### 12.3.1. os y pathlib

**`os`** proporciona funciones para interactuar con el sistema operativo: variables de entorno, información del sistema, manipulación de rutas (en su submódulo `os.path`).

```python
import os

# Variables de entorno
home = os.environ.get("HOME", "/default")
api_key = os.getenv("API_KEY", "sin_clave")

# Información del sistema
print(os.getcwd())       # directorio actual de trabajo
print(os.name)           # 'posix' (Linux/Mac) o 'nt' (Windows)

# Manipulación de directorios
os.makedirs("ruta/a/directorio", exist_ok=True)  # crea directorios anidados
os.listdir(".")          # lista archivos del directorio actual
```

**`pathlib`** (Python 3.4+) ofrece una interfaz orientada a objetos para manipular rutas del sistema de archivos. Es la alternativa moderna y recomendada a `os.path`:

```python
from pathlib import Path

# Crear rutas — el operador / une segmentos
ruta = Path("proyecto") / "src" / "main.py"
print(ruta)              # proyecto/src/main.py

# Información de la ruta
print(ruta.name)         # main.py
print(ruta.stem)         # main (sin extensión)
print(ruta.suffix)       # .py
print(ruta.parent)       # proyecto/src

# Operaciones con archivos
ruta.exists()            # ¿existe el archivo?
ruta.is_file()           # ¿es un archivo?
ruta.is_dir()            # ¿es un directorio?

# Leer y escribir archivos directamente
contenido = ruta.read_text(encoding="utf-8")
ruta.write_text("nuevo contenido", encoding="utf-8")

# Buscar archivos con patrones glob
for py_file in Path("src").glob("**/*.py"):  # recursivo
    print(py_file)

# Directorio actual y home del usuario
print(Path.cwd())        # equivalente a os.getcwd()
print(Path.home())       # directorio home del usuario
```

`pathlib` es preferible a `os.path` porque produce código más legible y menos propenso a errores. La unión de rutas con `/` es más intuitiva que `os.path.join()`, y los métodos como `.read_text()` simplifican operaciones comunes.

### 12.3.2. sys

El módulo `sys` proporciona acceso a variables y funciones específicas del intérprete de Python:

```python
import sys

# Argumentos de línea de comandos
# python script.py argumento1 argumento2
print(sys.argv)          # ['script.py', 'argumento1', 'argumento2']
print(sys.argv[0])       # nombre del script
print(sys.argv[1:])      # argumentos (sin el nombre del script)

# Versión de Python
print(sys.version)       # '3.12.0 (main, Oct  2 2023, ...)'
print(sys.version_info)  # sys.version_info(major=3, minor=12, micro=0, ...)

# Ruta de búsqueda de módulos
print(sys.path)          # lista de directorios donde Python busca módulos

# Salir del programa con un código de estado
sys.exit(0)              # 0 = éxito, cualquier otro = error
sys.exit("Mensaje de error")  # imprime el mensaje y sale con código 1
```

`sys.path` es especialmente importante para entender cómo Python encuentra los módulos. Cuando se hace `import modulo`, Python busca `modulo.py` en cada directorio de `sys.path`, en orden. Si el módulo no está en ninguno de esos directorios, se obtiene un `ModuleNotFoundError`.

`sys.argv` es la forma más básica de recibir argumentos por línea de comandos. Para scripts con argumentos complejos, el módulo `argparse` de la librería estándar ofrece parsing más robusto con validación, ayuda automática y valores por defecto.

### 12.3.3. math y random

**`math`** proporciona funciones matemáticas implementadas en C (más rápidas que su equivalente en Python puro):

```python
import math

# Constantes
print(math.pi)           # 3.141592653589793
print(math.e)            # 2.718281828459045
print(math.inf)          # infinito positivo

# Redondeo
math.ceil(3.2)           # 4 — redondea hacia arriba
math.floor(3.8)          # 3 — redondea hacia abajo
math.trunc(3.8)          # 3 — elimina decimales (similar a int())

# Potencias y raíces
math.sqrt(16)            # 4.0
math.pow(2, 10)          # 1024.0

# Logaritmos
math.log(100, 10)        # 2.0 (log base 10 de 100)
math.log2(8)             # 3.0

# Trigonometría (ángulos en radianes)
math.sin(math.pi / 2)   # 1.0
math.degrees(math.pi)   # 180.0 — radianes a grados
math.radians(180)        # 3.14159... — grados a radianes

# Utilidades
math.factorial(5)        # 120
math.gcd(12, 8)          # 4 — máximo común divisor
math.isclose(0.1 + 0.2, 0.3)  # True — comparación con tolerancia
```

**`random`** genera números pseudoaleatorios. No es criptográficamente seguro — para seguridad usar el módulo `secrets`.

```python
import random

# Números aleatorios
random.random()              # float entre 0.0 y 1.0
random.uniform(1.5, 5.5)    # float entre 1.5 y 5.5
random.randint(1, 10)       # entero entre 1 y 10 (ambos incluidos)
random.randrange(0, 100, 5) # entero entre 0 y 99, en pasos de 5

# Selección aleatoria de secuencias
colores = ["rojo", "verde", "azul", "amarillo"]
random.choice(colores)       # un elemento aleatorio
random.choices(colores, k=3) # 3 elementos con reposición (pueden repetirse)
random.sample(colores, k=2)  # 2 elementos sin reposición (no se repiten)

# Mezclar una lista in-place
random.shuffle(colores)
print(colores)               # orden aleatorio

# Semilla para reproducibilidad
random.seed(42)              # misma semilla = mismos resultados
print(random.randint(1, 100))  # siempre el mismo número con seed(42)
```

La semilla (`seed`) es útil en testing y desarrollo: permite obtener resultados "aleatorios" pero reproducibles, facilitando la depuración.

### 12.3.4. collections, functools e itertools (ya vistos)

Estos módulos ya se cubrieron en temas anteriores, pero vale la pena recordar dónde:

- **`collections`** (tema 4) — `Counter`, `defaultdict`, `deque`, `OrderedDict`. Estructuras de datos especializadas que resuelven problemas comunes de forma eficiente.
- **`functools`** (tema 10) — `partial`, `reduce`, `lru_cache`, `@cache`, `@wraps`. Herramientas para trabajar con funciones: cacheo, aplicación parcial, decoradores.
- **`itertools`** (tema 6, mencionado) — `chain`, `islice`, `groupby`, `product`, `combinations`, `permutations`. Generadores eficientes para combinaciones, agrupaciones y transformaciones de iterables.

### 12.3.5. copy, operator y string

**`copy`** — copia superficial y profunda de objetos (visto brevemente en el tema 3):

```python
import copy

original = [[1, 2], [3, 4]]

# Copia superficial — copia la lista exterior, pero las listas internas
# siguen siendo las mismas referencias
superficial = copy.copy(original)
superficial[0].append(99)
print(original)      # [[1, 2, 99], [3, 4]] — ¡afectado!

# Copia profunda — copia TODO recursivamente
original = [[1, 2], [3, 4]]
profunda = copy.deepcopy(original)
profunda[0].append(99)
print(original)      # [[1, 2], [3, 4]] — no afectado
```

**`operator`** — funciones que corresponden a los operadores de Python. Son útiles como argumentos para `sorted`, `map`, `reduce`, etc.:

```python
import operator

# En lugar de lambda x, y: x + y
operator.add(3, 5)       # 8
operator.mul(4, 6)       # 24

# En lugar de lambda x: x["nombre"]
personas = [{"nombre": "Ana", "edad": 30}, {"nombre": "Bob", "edad": 25}]
por_nombre = sorted(personas, key=operator.itemgetter("nombre"))
por_edad = sorted(personas, key=operator.itemgetter("edad"))

# En lugar de lambda obj: obj.nombre
from operator import attrgetter
por_atributo = sorted(objetos, key=attrgetter("nombre"))
```

`operator.itemgetter` y `operator.attrgetter` son más rápidos que lambdas equivalentes y producen código más legible en contextos funcionales.

**`string`** — constantes y utilidades de strings:

```python
import string

print(string.ascii_lowercase)   # 'abcdefghijklmnopqrstuvwxyz'
print(string.ascii_uppercase)   # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print(string.digits)            # '0123456789'
print(string.punctuation)       # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
print(string.ascii_letters)     # letras minúsculas + mayúsculas

# Útil para validaciones y generación de datos
caracteres_validos = string.ascii_letters + string.digits
```

---

## 12.4. Entornos virtuales y pip

### 12.4.1. Qué es un entorno virtual y por qué usarlo

Un entorno virtual es una instalación aislada de Python que tiene su propia copia del intérprete, su propio `pip` y su propio directorio de paquetes. Los paquetes instalados en un entorno virtual no afectan al Python del sistema ni a otros entornos virtuales.

El problema que resuelven es el conflicto de dependencias. Si el proyecto A necesita `requests==2.25` y el proyecto B necesita `requests==2.31`, no pueden compartir la misma instalación de Python. Con entornos virtuales, cada proyecto tiene su propio `requests` en la versión que necesite.

Usar entornos virtuales es una práctica obligatoria en Python profesional. Sin ellos:
- Instalar un paquete para un proyecto puede romper otro.
- No se puede saber qué paquetes necesita un proyecto específico.
- Se contamina la instalación global de Python con decenas de paquetes innecesarios.
- Se dificulta reproducir el entorno de desarrollo en otra máquina.

### 12.4.2. venv: crear y activar

El módulo `venv` viene incluido en Python 3.3+ y es la herramienta estándar para crear entornos virtuales:

```bash
# Crear un entorno virtual en el directorio ".venv"
python -m venv .venv

# Activar el entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows (CMD):
.venv\Scripts\activate

# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

Cuando el entorno está activo, el prompt del terminal muestra el nombre del entorno entre paréntesis:

```bash
(.venv) $ python --version    # usa el Python del entorno virtual
(.venv) $ pip install requests  # instala en el entorno virtual, no globalmente
```

Para desactivar el entorno:

```bash
(.venv) $ deactivate
$ python --version             # vuelve al Python del sistema
```

El directorio `.venv` contiene el intérprete, pip y todos los paquetes instalados. Nunca se sube a control de versiones — se añade al `.gitignore`. Lo que sí se sube es el archivo de dependencias (`requirements.txt` o `pyproject.toml`) para que cualquiera pueda recrear el entorno.

Convenciones comunes para el nombre del directorio: `.venv`, `venv`, `.env`. El más habitual y recomendado es `.venv` (con punto, para que quede oculto en sistemas Unix).

### 12.4.3. pip: instalar y gestionar dependencias

`pip` es el gestor de paquetes de Python. Descarga e instala paquetes desde PyPI (Python Package Index), el repositorio público de paquetes Python.

```bash
# Instalar un paquete
pip install requests

# Instalar una versión específica
pip install requests==2.31.0

# Instalar con restricción de versión
pip install "requests>=2.28,<3.0"

# Actualizar un paquete
pip install --upgrade requests

# Desinstalar un paquete
pip uninstall requests

# Ver paquetes instalados
pip list

# Ver información de un paquete
pip show requests

# Buscar paquetes desactualizados
pip list --outdated
```

Cuando se instala un paquete, pip también instala sus dependencias transitivas (los paquetes que ese paquete necesita). Por ejemplo, `pip install flask` instala Flask y todas sus dependencias.

### 12.4.4. requirements.txt y pyproject.toml

**`requirements.txt`** es la forma tradicional de declarar las dependencias de un proyecto. Es un archivo de texto plano con un paquete por línea:

```
requests==2.31.0
flask==3.0.0
sqlalchemy>=2.0,<3.0
python-dotenv~=1.0.0
```

```bash
# Generar requirements.txt desde el entorno actual
pip freeze > requirements.txt

# Instalar todas las dependencias de un requirements.txt
pip install -r requirements.txt
```

`pip freeze` lista todos los paquetes instalados con sus versiones exactas. Esto garantiza que cualquiera que ejecute `pip install -r requirements.txt` obtenga exactamente las mismas versiones.

Los operadores de versión más comunes:

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `==` | Versión exacta | `requests==2.31.0` |
| `>=` | Versión mínima | `requests>=2.28` |
| `<` | Versión máxima (excluida) | `requests<3.0` |
| `~=` | Compatible (~= 1.4 equivale a >=1.4, <2.0) | `requests~=2.31` |

**`pyproject.toml`** es el formato moderno (PEP 621) para configurar proyectos Python. Reemplaza a `setup.py`, `setup.cfg` y en muchos casos a `requirements.txt`:

```toml
[project]
name = "mi-proyecto"
version = "1.0.0"
description = "Descripción del proyecto"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
    "flask>=3.0",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "mypy>=1.0",
]
```

La diferencia clave es que `requirements.txt` lista versiones exactas (lo que está instalado ahora), mientras que `pyproject.toml` declara rangos de versiones compatibles (lo que el proyecto necesita). En la práctica, muchos proyectos usan ambos: `pyproject.toml` para la declaración formal y `requirements.txt` (generado con `pip freeze`) para reproducir el entorno exacto.
