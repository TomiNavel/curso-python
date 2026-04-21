# Errores Comunes: Módulos, Paquetes y Entornos Virtuales

## Error 1: Nombrar un archivo igual que un módulo de la librería estándar

```python
# archivo: random.py (¡mismo nombre que el módulo estándar!)
import random

print(random.randint(1, 10))
# ImportError: cannot import name 'randint' from 'random'
# Python importa el PROPIO archivo random.py en lugar del módulo estándar
```

Python busca módulos primero en el directorio actual. Si un archivo se llama `random.py`, `math.py`, `os.py` o igual que cualquier módulo estándar, Python lo importa a él en lugar del módulo de la librería estándar. La solución es renombrar el archivo.

Nombres problemáticos frecuentes: `random.py`, `math.py`, `email.py`, `test.py`, `string.py`, `collections.py`.

---

## Error 2: Código suelto fuera de `if __name__ == "__main__"`

```python
# archivo: utilidades.py
def procesar(datos):
    return [d.upper() for d in datos]

# Código de prueba suelto — se ejecuta AL IMPORTAR
datos_prueba = ["hola", "mundo"]
resultado = procesar(datos_prueba)
print(f"Prueba: {resultado}")

# Otro archivo que importa utilidades:
# import utilidades  ← imprime "Prueba: ['HOLA', 'MUNDO']" como efecto secundario
```

Todo código de ejecución (prints, llamadas a funciones, pruebas) debe ir dentro de `if __name__ == "__main__"`. Sin este guard, importar el módulo tiene efectos secundarios no deseados.

---

## Error 3: Modificar `sys.path` para resolver imports

```python
# MAL — hack frágil que depende de la estructura de directorios
import sys
sys.path.append("../mi_paquete")
sys.path.insert(0, "/ruta/absoluta/al/proyecto")

from modulo import funcion
```

Modificar `sys.path` en el código es una mala práctica que indica un problema de organización del proyecto. Las soluciones correctas son: estructurar el proyecto como un paquete instalable con `pyproject.toml`, o usar `pip install -e .` para instalar el paquete en modo editable.

---

## Error 4: `from modulo import *` en código de producción

```python
from os import *
from json import *

# ¿De dónde viene 'open'? ¿Es os.open o el built-in open?
# ¿De dónde viene 'load'? Imposible saberlo sin revisar los módulos
resultado = load(open("datos.json"))  # ambiguo y propenso a errores
```

`import *` contamina el espacio de nombres y puede sobrescribir nombres existentes sin aviso. En este ejemplo, `os.open` sobrescribe el `open` built-in de Python, causando errores difíciles de diagnosticar. Siempre importar nombres explícitos.

---

## Error 5: Import circular entre módulos

```python
# archivo: modelos.py
from servicios import procesar_usuario  # importa de servicios

class Usuario:
    pass

# archivo: servicios.py
from modelos import Usuario  # importa de modelos ← CIRCULAR

def procesar_usuario(user):
    return isinstance(user, Usuario)
```

`modelos.py` importa de `servicios.py` y `servicios.py` importa de `modelos.py`. Python no puede completar ninguna de las dos importaciones. La solución correcta es reorganizar: mover lo compartido a un tercer módulo, o replantearse si la dependencia bidireccional es realmente necesaria.

---

## Error 6: No usar entorno virtual

```bash
# MAL — instala en la instalación global de Python
pip install requests flask sqlalchemy pandas numpy

# Semanas después, en otro proyecto:
pip install requests==2.25  # downgradea requests y rompe el primer proyecto
```

Sin entorno virtual, todos los proyectos comparten los mismos paquetes. Instalar o actualizar una dependencia para un proyecto puede romper otro. La práctica profesional es crear un entorno virtual para cada proyecto: `python -m venv .venv`.

---

## Error 7: Subir el directorio del entorno virtual a git

```
# MAL — .venv en el repositorio
mi_proyecto/
├── .venv/          # ← cientos de MB de paquetes binarios en git
├── src/
└── requirements.txt
```

El directorio `.venv` contiene binarios específicos de la plataforma y el sistema operativo. No es portable y ocupa cientos de megabytes. Debe añadirse al `.gitignore`. Lo que se sube es el archivo de dependencias (`requirements.txt` o `pyproject.toml`) para que cualquiera pueda recrear el entorno.

```gitignore
# .gitignore
.venv/
__pycache__/
*.pyc
```

---

## Error 8: `pip freeze` sin entorno virtual activo

```bash
# Sin entorno virtual activo
pip freeze > requirements.txt
# Genera una lista con TODOS los paquetes del sistema — docenas de paquetes
# que no tienen nada que ver con el proyecto
```

`pip freeze` lista todos los paquetes instalados en el Python activo. Si no hay entorno virtual, lista los paquetes del sistema, que incluyen herramientas globales y dependencias de otros proyectos. Siempre activar el entorno virtual antes de ejecutar `pip freeze`.

---

## Error 9: Confundir `os.path.join` con concatenación de strings

```python
import os

# MAL — falla en Windows (usa \ en lugar de /)
ruta = "proyecto" + "/" + "src" + "/" + "main.py"

# MAL — no maneja separadores del sistema operativo
ruta = f"proyecto/src/main.py"

# BIEN — usa el separador correcto del sistema operativo
ruta = os.path.join("proyecto", "src", "main.py")

# MEJOR — pathlib es más legible y moderno
from pathlib import Path
ruta = Path("proyecto") / "src" / "main.py"
```

Concatenar rutas con strings hardcodeando `/` falla en Windows (que usa `\`). `os.path.join` y `pathlib` manejan automáticamente el separador correcto del sistema operativo.

---

## Error 10: Asumir que un import relativo funciona al ejecutar directamente

```python
# archivo: mi_paquete/servicios.py
from .modelos import Usuario  # import relativo

def crear_usuario():
    return Usuario("Ana")
```

```bash
# Ejecutar directamente — FALLA
python mi_paquete/servicios.py
# ImportError: attempted relative import with no known parent package

# Ejecutar como módulo del paquete — FUNCIONA
python -m mi_paquete.servicios
```

Los imports relativos solo funcionan dentro de un paquete. Si se ejecuta un archivo directamente con `python archivo.py`, Python no sabe que el archivo pertenece a un paquete y los imports relativos fallan. La solución es ejecutar con `-m` (que activa el sistema de paquetes) o usar imports absolutos.
