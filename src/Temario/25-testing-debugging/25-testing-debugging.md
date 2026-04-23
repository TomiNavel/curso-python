# 25. Testing y Debugging

Escribir tests es una de las habilidades que más separa a un programador profesional de un aficionado. No porque sea difícil técnicamente — la API de pytest es trivial — sino porque requiere disciplina: estructurar el código para que sea testable, decidir qué merece test y qué no, y aceptar que el tiempo invertido en escribir tests se recupera con intereses al refactorizar.

El debugging es su complemento natural: cuando algo falla (y algo siempre falla), saber usar el debugger, leer tracebacks y aislar el problema ahorra horas. En entrevistas se valoran ambas habilidades; prácticamente cualquier empresa pide "experiencia con pytest" o equivalente en sus ofertas de Python.

## 25.1. Testing con pytest

`pytest` es el framework de testing más usado en Python. Es una librería externa (no viene con Python) que se ha convertido en el estándar de facto por su sintaxis mínima: no hay que heredar de una clase ni recordar métodos especiales — basta con escribir funciones que empiecen por `test_` y usar `assert`.

La clave de pytest es reducir la ceremonia al mínimo. Un test típico cabe en dos líneas:

```python
def test_suma():
    assert 2 + 3 == 5
```

Esta simplicidad es deliberada: cuanto menor sea la fricción para escribir un test, más tests se escriben. El resto del framework (fixtures, parametrización, plugins) está construido sobre este núcleo minimalista.

### 25.1.1. Instalación y convenciones (test_, assert)

pytest se instala como cualquier paquete: `pip install pytest`. En proyectos profesionales suele ir en un `requirements-dev.txt` o como dependencia opcional en `pyproject.toml`, separado de las dependencias de producción.

pytest descubre tests automáticamente siguiendo convenciones de nombres:

- Archivos que empiezan por `test_` o terminan en `_test.py`.
- Funciones que empiezan por `test_`.
- Clases que empiezan por `Test` (sin herencia especial).

No hace falta `main` ni registrar nada: al ejecutar `pytest` en la raíz del proyecto, recorre recursivamente, encuentra los archivos que cumplen la convención y ejecuta todas sus funciones `test_`. Este descubrimiento automático es una de las razones de su adopción: escribir un test nuevo es tan simple como crear el archivo.

La convención es colocar los tests en un directorio paralelo al código fuente, habitualmente `tests/` en la raíz del proyecto, con nombres que reflejan el módulo que testean: `src/usuarios.py` tiene su contraparte en `tests/test_usuarios.py`. Esta separación mantiene el código de producción limpio.

### 25.1.2. Escribir y ejecutar tests

Un test en pytest es una función que usa `assert` para verificar expectativas. Si cualquier `assert` falla, el test falla; si todos pasan sin excepciones, el test pasa.

```python
from calculadora import sumar, dividir

def test_sumar_positivos():
    assert sumar(2, 3) == 5

def test_sumar_negativos():
    assert sumar(-1, -1) == -2

def test_dividir_por_cero_lanza():
    try:
        dividir(10, 0)
        assert False, "debería haber lanzado"
    except ZeroDivisionError:
        pass
```

Ejecutar `pytest` en la raíz del proyecto corre todos los tests descubiertos. Opciones útiles en el día a día:

- `pytest -v` muestra cada test con su resultado (útil al depurar fallos).
- `pytest -x` para tras el primer fallo.
- `pytest archivo.py::test_funcion` ejecuta un test concreto.
- `pytest -k "palabra"` ejecuta solo los tests cuyo nombre contiene la palabra.

Cuando un `assert` falla, pytest muestra el valor real y el esperado, haciendo muy claro qué se esperaba y qué se obtuvo. Este reporte detallado es otra razón de su popularidad: frente a otros frameworks, el feedback es inmediato y preciso.

### 25.1.3. Fixtures

Una **fixture** en pytest es una función decorada con `@pytest.fixture` que prepara datos o recursos para los tests. pytest inyecta la fixture como argumento en cualquier test que la declare, gestionando su ciclo de vida.

```python
import pytest

@pytest.fixture
def usuario_de_prueba():
    return {"nombre": "Ana", "edad": 30, "activo": True}

def test_nombre(usuario_de_prueba):
    assert usuario_de_prueba["nombre"] == "Ana"

def test_edad(usuario_de_prueba):
    assert usuario_de_prueba["edad"] >= 18
```

Las fixtures evitan duplicar código de preparación entre tests. Si varios tests necesitan el mismo objeto de partida, se define una fixture y cada test la pide como parámetro. pytest crea una nueva instancia para cada test por defecto, garantizando aislamiento.

Las fixtures pueden tener `yield` para separar setup y teardown, como un context manager:

```python
@pytest.fixture
def archivo_temporal(tmp_path):
    ruta = tmp_path / "test.txt"
    ruta.write_text("contenido inicial")
    yield ruta
    # Código tras yield se ejecuta al terminar el test (limpieza).
    # tmp_path ya limpia su directorio, así que aquí no hace falta más.
```

pytest trae fixtures integradas muy útiles: `tmp_path` (directorio temporal), `capsys` (capturar stdout/stderr), `monkeypatch` (modificar variables/entorno de forma reversible). Conocer esta librería de fixtures es parte del "saber usar pytest" esperado en una entrevista senior.

### 25.1.4. Parametrización (@pytest.mark.parametrize)

Cuando una misma función se debe testear con varios inputs/outputs, la parametrización evita duplicar el código del test. El decorador `@pytest.mark.parametrize` recibe los nombres de los parámetros y una lista de tuplas con los valores.

```python
import pytest

@pytest.mark.parametrize("entrada,esperado", [
    (2, 4),
    (3, 9),
    (10, 100),
    (-5, 25),
])
def test_cuadrado(entrada, esperado):
    assert entrada ** 2 == esperado
```

pytest ejecuta este test cuatro veces, una por cada tupla, y muestra cada caso por separado en el reporte. Si un caso falla, se ve exactamente cuál — no se oculta detrás de un único test que "falla con alguno de estos inputs".

La parametrización es una de las mejores herramientas para convertir tests repetitivos en código limpio. En entrevistas, mostrar este patrón en lugar de copiar-pegar tests demuestra soltura con pytest.

### 25.1.5. Testear excepciones (pytest.raises)

Cuando se quiere verificar que una función **lanza** una excepción concreta, `pytest.raises` es el patrón idiomático. Se usa como context manager:

```python
import pytest

def test_dividir_por_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0)

def test_mensaje_de_error():
    with pytest.raises(ValueError, match="edad negativa"):
        crear_usuario(edad=-1)
```

El bloque `with` ejecuta el código; si la excepción esperada se lanza, el test pasa. Si se lanza otra excepción o no se lanza ninguna, el test falla. El parámetro `match` permite verificar que el mensaje de la excepción contiene una expresión regular concreta, útil cuando la misma excepción se lanza por motivos distintos.

Este patrón reemplaza el `try/except` manual que suele verse en código menos idiomático. `pytest.raises` es más corto y deja más clara la intención.

### 25.1.6. Cobertura de tests (coverage, pytest-cov)

La **cobertura de tests** mide qué porcentaje del código es ejecutado por los tests. El plugin `pytest-cov` integra la herramienta `coverage` con pytest:

```bash
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

Este comando muestra qué líneas están cubiertas y cuáles no. Cobertura alta no implica tests buenos — se puede ejecutar código sin verificar su resultado — pero cobertura baja suele indicar zonas sin testear. El umbral pragmático en proyectos profesionales es **80–90%**, con la consciencia de que el último 10% suele ser código de error o casos límite poco frecuentes.

En entrevistas se valora entender que la cobertura es una métrica **orientativa**, no un fin en sí mismo. Perseguir el 100% lleva a tests triviales que no aportan valor. La pregunta correcta es "¿cubre los casos que importan?", no "¿qué porcentaje hay?".

## 25.2. unittest

`unittest` es la librería de testing **de la biblioteca estándar**, inspirada en JUnit de Java. No hay que instalar nada: está disponible en cualquier instalación de Python. En proyectos que no pueden añadir dependencias externas (sistemas restringidos, scripts en AWS Lambda, etc.), `unittest` es la opción por defecto.

En proyectos donde se puede usar pytest, es la elección preferida por su sintaxis más ligera. Pero conocer `unittest` sigue siendo útil porque sigue apareciendo en código existente y en entrevistas.

### 25.2.1. TestCase y métodos assert

Los tests de `unittest` se agrupan en clases que heredan de `unittest.TestCase`. Cada método que empiece por `test_` es un test individual. En lugar del `assert` plano de pytest, se usan métodos específicos del objeto `TestCase`:

```python
import unittest

class TestCalculadora(unittest.TestCase):
    def test_sumar(self):
        self.assertEqual(sumar(2, 3), 5)

    def test_dividir_por_cero(self):
        with self.assertRaises(ZeroDivisionError):
            dividir(10, 0)
```

Los métodos assert más usados son `assertEqual`, `assertTrue`, `assertFalse`, `assertIn`, `assertIsNone`, `assertRaises`. La ventaja es que dan mensajes de error descriptivos sin configuración adicional; la desventaja es que hay que recordarlos todos.

Los tests se ejecutan con `python -m unittest` desde la raíz del proyecto, o con `python archivo.py` si el archivo termina en `unittest.main()`.

### 25.2.2. setUp y tearDown

Los métodos `setUp` y `tearDown` se ejecutan automáticamente antes y después de cada test de la clase, respectivamente. Son el equivalente a las fixtures de pytest pero con acoplamiento más rígido — son métodos de la clase, no inyección explícita.

```python
class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario(nombre="Ana", edad=30)

    def tearDown(self):
        self.usuario.cerrar_conexion()

    def test_nombre(self):
        self.assertEqual(self.usuario.nombre, "Ana")
```

Cada método `test_` recibe un `self.usuario` recién creado gracias a `setUp`, y al terminar se ejecuta `tearDown` para limpiar. Para setup/teardown a nivel de clase (una vez antes de todos los tests), existen `setUpClass` y `tearDownClass`.

El mecanismo funciona, pero es más rígido que las fixtures de pytest: todos los tests de la clase comparten el setup, aunque solo algunos lo necesiten. Con fixtures, cada test declara explícitamente qué necesita.

### 25.2.3. pytest vs unittest

En proyectos modernos, pytest es la opción recomendada por varias razones:

- **Sintaxis más limpia**: funciones con `assert` plano, sin heredar de ninguna clase.
- **Fixtures más flexibles**: inyección explícita por parámetros, reutilizables entre archivos, con distintos niveles de alcance (`function`, `class`, `module`, `session`).
- **Plugins**: cobertura, paralelización, mocks, capturas — todo disponible como plugins pytest.
- **Mejores mensajes de error**: muestra valores reales y esperados con detalle sin configuración.
- **Parametrización integrada**: `@pytest.mark.parametrize` no tiene equivalente directo en unittest.

Ventajas de unittest:

- Viene con Python, no requiere instalar nada.
- Es el estándar en partes de la propia biblioteca de Python y algunos proyectos legacy.

pytest puede ejecutar tests escritos con `unittest` sin cambios, así que migrar gradualmente es sencillo. En una entrevista, saber que ambos existen y poder justificar pytest para proyectos nuevos es la respuesta esperada.

## 25.3. Mocking

A veces el código bajo test depende de algo incómodo: una API externa, una base de datos, la hora del sistema, un archivo. Los **mocks** son objetos sustitutos que simulan estas dependencias durante los tests, permitiendo verificar el comportamiento del código sin necesidad de infraestructura real.

El módulo `unittest.mock` (incluido en la librería estándar) es la herramienta estándar, tanto para tests con pytest como con unittest.

### 25.3.1. unittest.mock (Mock, patch)

Las dos construcciones más usadas son `Mock` y `patch`.

`Mock` crea un objeto que responde a cualquier atributo o llamada devolviendo otro Mock, registrando qué se le llamó y con qué argumentos. Se usa para sustituir dependencias pasadas por parámetro:

```python
from unittest.mock import Mock

def saludar(servicio, nombre):
    servicio.registrar_visita(nombre)
    return servicio.generar_saludo(nombre)

def test_saludar_llama_a_registrar():
    servicio = Mock()
    servicio.generar_saludo.return_value = "Hola, Ana"

    resultado = saludar(servicio, "Ana")

    assert resultado == "Hola, Ana"
    servicio.registrar_visita.assert_called_once_with("Ana")
```

`patch` reemplaza un objeto (función, clase, atributo de módulo) temporalmente durante el test, útil cuando no se puede pasar la dependencia como parámetro. Se usa como context manager o decorador:

```python
from unittest.mock import patch

def obtener_hora_saludo():
    from datetime import datetime
    hora = datetime.now().hour
    return "buenos días" if hora < 12 else "buenas tardes"

def test_hora_saludo_manana():
    with patch("modulo.datetime") as fake_dt:
        fake_dt.now.return_value.hour = 9
        assert obtener_hora_saludo() == "buenos días"
```

El detalle clave de `patch` es **qué ruta se parchea**: se parchea en el módulo donde se **usa**, no donde está definido. Este error ("patch donde se usa, no donde se define") es uno de los bugs más típicos con mocks y se explica en muchas entrevistas.

### 25.3.2. Cuándo usar mocks y cuándo no

Los mocks son potentes pero se abusan con facilidad. La heurística profesional:

- **Usar mock cuando**: la dependencia es externa, costosa o no determinista (API HTTP, base de datos, sistema de archivos, hora actual, generador aleatorio).
- **No usar mock cuando**: la dependencia es código propio rápido y determinista. Mejor testar el sistema real.

Un test que mockea todo acaba verificando "la función llama a los métodos en este orden" en lugar de "la función produce el resultado correcto". Ese tipo de test se rompe al refactorizar sin que el comportamiento cambie, y no aporta confianza real.

Una señal de abuso: si al escribir el test hay más líneas configurando mocks que ejecutando código. Normalmente significa que el diseño está acoplado — extraer la lógica pura a una función testeable sin mocks suele ser mejor que mockear más.

## 25.4. Debugging

Debuggear es arte y ciencia. Hay técnicas que se aplican casi siempre: leer el traceback completo, reproducir el fallo de forma aislada, reducir el caso mínimo. Python ofrece herramientas desde las más básicas (print) hasta debuggers completos (pdb, IDE).

### 25.4.1. print debugging y f-strings

El print debugging es la técnica más usada del mundo porque es inmediata: no hace falta configurar nada, solo añadir un print y ejecutar. Para que sea efectivo, los prints deben ser informativos.

Los f-strings tienen una característica poco conocida pero muy útil para debug: el operador `=` dentro de la expresión muestra el nombre y el valor.

```python
def calcular_descuento(precio, porcentaje):
    # MAL: print sin contexto
    # print(precio)

    # BIEN: nombre y valor claros
    print(f"{precio=}, {porcentaje=}")
    descuento = precio * porcentaje / 100
    print(f"{descuento=}")
    return precio - descuento
```

El `=` dentro del f-string produce `"precio=100, porcentaje=15"` sin tener que escribir el nombre dos veces. Es el patrón idiomático para prints de debug desde Python 3.8.

Hay que recordar quitar los prints antes de comitear. Una forma común de evitar dejar prints olvidados es usar el módulo `logging` con nivel DEBUG desde el principio; así los mensajes siguen existiendo pero no salen por defecto en producción (tema del siguiente bloque).

### 25.4.2. breakpoint() y pdb

`breakpoint()` (desde Python 3.7) pausa la ejecución y abre una sesión de debugger interactivo. Por defecto lanza `pdb`, el debugger de la librería estándar, pero puede configurarse (mediante la variable de entorno `PYTHONBREAKPOINT`) para abrir otros debuggers como `ipdb` o el del IDE.

```python
def procesar(datos):
    resultado = transformar(datos)
    breakpoint()   # se pausa aquí; prompt (Pdb)
    return validar(resultado)
```

Los comandos más útiles dentro de pdb:

- `n` (next): ejecuta la línea actual y pasa a la siguiente.
- `s` (step): entra dentro de llamadas de función.
- `c` (continue): continúa hasta el siguiente breakpoint.
- `l` (list): muestra el código alrededor de la línea actual.
- `p variable` (print): imprime el valor de una variable.
- `pp variable` (pretty print): imprime de forma legible estructuras complejas.
- `q` (quit): sale del debugger (y del programa).

pdb es más que "print con más pasos": permite inspeccionar el estado completo en ese punto, ejecutar código arbitrario, subir/bajar por la pila de llamadas. Para bugs complejos es mucho más eficiente que distribuir prints.

### 25.4.3. El debugger del IDE

Los IDEs modernos (VS Code, PyCharm) ofrecen debuggers gráficos con puntos de interrupción, inspección visual de variables, expresiones watch, y step into/over/out con un clic. Son la forma más productiva de debuggear en el día a día.

Los conceptos son los mismos que en pdb: poner breakpoints, avanzar paso a paso, inspeccionar. La diferencia es la interfaz: ver todas las variables locales en un panel, el call stack lateral, y la posibilidad de marcar condiciones en los breakpoints (detener solo cuando `x > 100`).

Saber usar el debugger del IDE bien es una habilidad que se nota en entrevistas técnicas y en el día a día. El print debugging es el primer paso; el debugger interactivo es la herramienta que se usa cuando el problema es realmente complejo.
