# Preguntas de Entrevista: Módulos, Paquetes y Entornos Virtuales

1. ¿Qué ocurre internamente cuando Python ejecuta `import modulo`? ¿Cuántas veces se ejecuta el código del módulo si se importa desde varios archivos?
2. ¿Cuál es la diferencia entre `import modulo` y `from modulo import nombre`? ¿Cuándo usar cada uno?
3. ¿Por qué `from modulo import *` es mala práctica en código de producción?
4. ¿Qué es `if __name__ == "__main__"` y qué problema resuelve?
5. ¿Qué es `__all__` y qué controla?
6. ¿Cuál es la diferencia entre un módulo y un paquete? ¿Qué papel cumple `__init__.py`?
7. ¿Cuál es la diferencia entre imports absolutos y relativos? ¿Cuál recomienda PEP 8?
8. ¿Qué es un import circular y cómo se resuelve?
9. ¿Cómo encuentra Python los módulos cuando se hace `import`? ¿Qué es `sys.path`?
10. ¿Qué diferencia hay entre `os.path` y `pathlib`? ¿Cuál se recomienda en Python moderno?
11. ¿Para qué sirve un entorno virtual y qué problema resuelve?
12. ¿Cuál es la diferencia entre `requirements.txt` y `pyproject.toml`?

---

### R1. ¿Qué ocurre internamente cuando Python ejecuta `import modulo`?

Python sigue estos pasos:

1. Busca el módulo en `sys.modules` (caché de módulos ya importados). Si ya está, devuelve la referencia existente sin ejecutar nada.
2. Si no está en caché, busca el archivo en los directorios de `sys.path`.
3. Crea un objeto módulo nuevo y lo añade a `sys.modules`.
4. Ejecuta todo el código del archivo de arriba a abajo dentro del contexto del objeto módulo.

El código del módulo se ejecuta solo una vez, la primera vez que se importa. Las importaciones posteriores desde cualquier otro archivo simplemente obtienen la referencia del caché en `sys.modules`. Esto es cierto incluso si varios archivos hacen `import modulo` — todos comparten el mismo objeto módulo.

---

### R2. ¿Cuál es la diferencia entre `import modulo` y `from modulo import nombre`?

`import modulo` importa el módulo completo como un objeto. Se accede a su contenido con notación de punto: `modulo.funcion()`. Cada uso deja claro de dónde viene la función.

`from modulo import nombre` importa un nombre específico directamente al espacio de nombres actual. Se usa sin prefijo: `funcion()`. Es más cómodo pero pierde la trazabilidad del origen.

`import modulo` es preferible cuando se usan muchos elementos del módulo o cuando la claridad del origen es importante. `from modulo import nombre` es preferible cuando se usa un solo elemento con mucha frecuencia y su origen es evidente por contexto.

---

### R3. ¿Por qué `from modulo import *` es mala práctica?

Tres razones:

1. **Contamina el espacio de nombres** — importa todo al ámbito actual, incluyendo nombres que podrían colisionar con variables o funciones existentes.
2. **Pierde trazabilidad** — hace imposible saber de dónde viene cada nombre sin revisar manualmente el módulo importado.
3. **Sobrescritura silenciosa** — si dos módulos definen una función con el mismo nombre, el segundo `import *` sobrescribe el primero sin aviso ni error.

Solo es aceptable en sesiones interactivas del intérprete para explorar módulos rápidamente. En código de producción, siempre se deben importar nombres explícitos.

---

### R4. ¿Qué es `if __name__ == "__main__"` y qué problema resuelve?

Cada módulo tiene un atributo `__name__`. Cuando el archivo se ejecuta directamente (`python script.py`), `__name__` vale `"__main__"`. Cuando se importa desde otro archivo, `__name__` vale el nombre del módulo.

El guard `if __name__ == "__main__"` permite que el código dentro de ese bloque solo se ejecute al lanzar el archivo directamente, no al importarlo. Resuelve el problema de que un módulo tenga código de ejecución (prints, llamadas a funciones, pruebas) que no debería ejecutarse cuando otro módulo lo importa.

Sin este guard, al hacer `import utilidades`, cualquier `print()` o llamada a función suelta en el archivo se ejecutaría como efecto secundario de la importación.

---

### R5. ¿Qué es `__all__` y qué controla?

`__all__` es una lista de strings que define qué nombres se exportan cuando alguien hace `from modulo import *`. Si `__all__` existe, solo los nombres listados se importan con `import *`. Si no existe, se importan todos los nombres que no empiezan con guion bajo.

`__all__` no restringe el acceso directo — `import modulo` seguido de `modulo.funcion_interna()` sigue funcionando. Solo controla el comportamiento de `import *`.

Se usa sobre todo en paquetes (en `__init__.py`) para definir la API pública.

---

### R6. ¿Cuál es la diferencia entre un módulo y un paquete?

Un módulo es un archivo `.py` individual. Un paquete es un directorio que contiene módulos y un archivo `__init__.py`.

`__init__.py` tiene dos funciones: marca el directorio como paquete Python (para que se pueda importar) y se ejecuta automáticamente cuando se importa el paquete. Puede estar vacío o contener código de inicialización y re-exportaciones que definan la API pública del paquete.

Desde Python 3.3 existen namespace packages sin `__init__.py`, pero en la práctica siempre se recomienda incluirlo para mayor claridad y control.

---

### R7. ¿Cuál es la diferencia entre imports absolutos y relativos?

Los imports absolutos usan la ruta completa desde la raíz del paquete: `from mi_proyecto.modelos import Usuario`. Los imports relativos usan puntos para indicar posición relativa: `from .modelos import Usuario` (`.` = mismo paquete, `..` = paquete padre).

PEP 8 recomienda imports absolutos porque son más claros y menos propensos a confusión. Los imports relativos son aceptables en paquetes con muchos niveles de anidamiento donde la ruta absoluta sería excesivamente larga.

Los imports relativos solo funcionan dentro de paquetes — no se pueden usar en scripts ejecutados directamente con `python script.py`.

---

### R8. ¿Qué es un import circular y cómo se resuelve?

Un import circular ocurre cuando el módulo A importa del módulo B y el módulo B importa del módulo A. Python no puede completar la importación porque cada módulo depende del otro para terminar de cargarse.

Soluciones, ordenadas de mejor a peor:

1. **Reorganizar el código** — mover las definiciones compartidas a un tercer módulo que ambos importen. Esta es la solución correcta en la mayoría de casos.
2. **Mover el import dentro de la función** — retrasar la importación al momento de uso. Funciona pero oculta dependencias.
3. **Usar `TYPE_CHECKING`** — para imports que solo se necesitan en type hints: `from __future__ import annotations` junto con `if TYPE_CHECKING: import modulo`.

---

### R9. ¿Cómo encuentra Python los módulos cuando se hace `import`?

Python busca módulos en este orden:

1. **`sys.modules`** — caché de módulos ya importados. Si está aquí, no busca más.
2. **`sys.path`** — lista de directorios donde Python busca archivos `.py`. Incluye:
   - El directorio del script que se ejecutó.
   - Los directorios de la variable de entorno `PYTHONPATH` (si existe).
   - Los directorios de instalación de la librería estándar.
   - Los directorios `site-packages` (paquetes de terceros).

Si el módulo no se encuentra en ningún directorio de `sys.path`, Python lanza `ModuleNotFoundError`.

Se puede modificar `sys.path` en tiempo de ejecución (`sys.path.append("ruta")`), pero es una mala práctica en producción. La forma correcta es instalar el paquete con pip o configurar el proyecto con `pyproject.toml`.

---

### R10. ¿Qué diferencia hay entre `os.path` y `pathlib`?

`os.path` trabaja con strings — las rutas son cadenas de texto y las funciones son procedurales: `os.path.join("a", "b")`, `os.path.exists(ruta)`.

`pathlib` (Python 3.4+) trabaja con objetos `Path` — las rutas son objetos con métodos: `Path("a") / "b"`, `ruta.exists()`. Además, `Path` ofrece métodos directos como `.read_text()`, `.write_text()`, `.glob()` que simplifican operaciones comunes.

`pathlib` es la forma recomendada en Python moderno. Produce código más legible, más conciso y menos propenso a errores de concatenación de rutas.

---

### R11. ¿Para qué sirve un entorno virtual y qué problema resuelve?

Un entorno virtual es una instalación aislada de Python con su propio directorio de paquetes. Resuelve el problema de conflictos de dependencias entre proyectos: si el proyecto A necesita `requests==2.25` y el proyecto B necesita `requests==2.31`, cada uno tiene su entorno virtual con su propia versión.

Sin entornos virtuales, todos los proyectos comparten la misma instalación de Python y los mismos paquetes. Instalar o actualizar un paquete para un proyecto puede romper otro. Usar entornos virtuales es práctica obligatoria en desarrollo profesional con Python.

Se crean con `python -m venv .venv`, se activan con `source .venv/bin/activate` (Linux/Mac) o `.venv\Scripts\activate` (Windows), y el directorio `.venv` nunca se sube a control de versiones.

---

### R12. ¿Cuál es la diferencia entre `requirements.txt` y `pyproject.toml`?

`requirements.txt` lista versiones exactas de paquetes instalados. Se genera con `pip freeze > requirements.txt` y refleja el estado actual del entorno. Es útil para reproducir un entorno exacto.

`pyproject.toml` (PEP 621) declara rangos de versiones compatibles que el proyecto necesita. Es la configuración formal del proyecto e incluye también metadatos (nombre, versión, descripción).

La diferencia conceptual es: `requirements.txt` dice "qué hay instalado ahora" y `pyproject.toml` dice "qué necesita el proyecto". Muchos proyectos usan ambos: `pyproject.toml` para la declaración formal y `requirements.txt` para reproducibilidad exacta.
