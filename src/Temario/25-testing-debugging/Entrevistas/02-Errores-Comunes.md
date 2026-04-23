# Errores Comunes: Testing y Debugging

## Error 1. Tests que dependen del orden de ejecución

Cuando el estado global (variables de módulo, archivos, base de datos en memoria) se comparte entre tests, el orden en que pytest los ejecuta influye en el resultado. Un test pasa al correrlo solo y falla al correrlo con los demás.

```python
# MAL: usuarios es global, un test ensucia el estado del siguiente
usuarios = []

def test_agregar():
    usuarios.append("Ana")
    assert len(usuarios) == 1

def test_lista_vacia():
    assert usuarios == []   # falla si se ejecuta después de test_agregar

# BIEN: usar fixtures o inicializar estado dentro de cada test
@pytest.fixture
def usuarios():
    return []

def test_agregar(usuarios):
    usuarios.append("Ana")
    assert len(usuarios) == 1

def test_lista_vacia(usuarios):
    assert usuarios == []
```

Cada test debe ser independiente. La dependencia entre tests es una fuente clásica de "en mi máquina funciona" — distintos sistemas o versiones ejecutan en orden distinto.

---

## Error 2. Mockear donde se define en lugar de donde se usa

`patch` debe apuntar a la ruta desde donde el módulo bajo test importa el objeto, no a su definición original.

```python
# modulo_a.py
from datetime import datetime

def fecha_hora_actual():
    return datetime.now()

# tests.py — MAL: patch donde se define, la función sigue usando el datetime real
with patch("datetime.datetime") as fake:
    ...

# BIEN: patch donde se usa (el modulo_a tiene su propia referencia)
with patch("modulo_a.datetime") as fake:
    ...
```

Es uno de los errores más clásicos con mocks. El test parece configurar el mock pero el código bajo test sigue llamando a la función real.

---

## Error 3. Asserts sin mensaje descriptivo en unittest

En unittest, un `assertEqual` que falla muestra solo los valores. Sin contexto sobre qué se estaba comprobando, diagnosticar en un test grande es más lento.

```python
# MAL: fallo dice solo "5 != 6" sin pista del contexto
self.assertEqual(calcular(x), 6)

# BIEN: mensaje orienta al motivo del test
self.assertEqual(calcular(x), 6, f"fallo con x={x}")
```

pytest no sufre tanto esto porque muestra valores reales y expresión completa. En unittest, el parámetro `msg` del assert vale oro cuando los tests crecen.

---

## Error 4. Testear la implementación, no el comportamiento

Un test que verifica detalles internos (qué métodos privados se llaman, en qué orden) se rompe al refactorizar aunque el comportamiento observable no cambie. El test debería comprobar qué hace la función, no cómo lo hace.

```python
# MAL: verifica que internamente se llama a _validar_formato
def test_guardar():
    with patch.object(Usuario, "_validar_formato") as fake:
        usuario.guardar()
        fake.assert_called_once()

# BIEN: verifica el resultado observable
def test_guardar_lanza_si_formato_invalido():
    with pytest.raises(ValueError):
        Usuario(email="no-es-email").guardar()
```

La regla: si al refactorizar un módulo sin cambiar su API pública los tests tienen que actualizarse, probablemente están testeando la implementación.

---

## Error 5. Usar `time.sleep` para esperar resultados asíncronos en tests

Introducir `sleep` en tests para esperar a que algo ocurra vuelve los tests lentos y flakey (fallan de forma intermitente según la carga del sistema).

```python
# MAL: sleep arbitrario, lento y poco fiable
def test_procesamiento_asincrono():
    lanzar_tarea()
    time.sleep(2)
    assert tarea_completa()

# BIEN: polling con timeout
def test_procesamiento_asincrono():
    lanzar_tarea()
    for _ in range(20):
        if tarea_completa():
            return
        time.sleep(0.1)
    pytest.fail("la tarea no se completó a tiempo")
```

Para tests con `asyncio` se usa `pytest-asyncio` y `await`. Los `sleep` arbitrarios son bandera roja en cualquier test suite.

---

## Error 6. Capturar `Exception` genérica en tests

Capturar `Exception` oculta errores distintos al esperado. El test puede pasar aunque el código lance una excepción no prevista.

```python
# MAL: cualquier error hace pasar el test (incluso uno inesperado)
def test_error():
    try:
        funcion()
    except Exception:
        pass

# BIEN: pytest.raises con la excepción específica
def test_error():
    with pytest.raises(ValueError):
        funcion()
```

Ser específico con la excepción es lo que hace que el test detecte regresiones correctamente.

---

## Error 7. Olvidar quitar los `print` de debug antes de commitear

El print debugging es rápido pero deja rastros que ensucian la salida en CI, complican la lectura de logs y se consideran código sucio en revisiones.

```python
# MAL: prints de debug mezclados en código de producción
def procesar(datos):
    print(f"procesando {datos}")   # olvidado del debug
    resultado = transformar(datos)
    return resultado
```

Dos mitigaciones habituales: usar `logging.debug` en lugar de print (queda silenciado en producción pero disponible si hace falta), o usar linters/pre-commit hooks que detecten prints antes del commit. En entrevistas, dejar prints en un pull request es señal de falta de atención.

---

## Error 8. Comparar floats con `==` en tests

Los floats IEEE 754 no pueden representar ciertos decimales de forma exacta. `0.1 + 0.2 != 0.3` porque el cálculo da `0.30000000000000004`.

```python
# MAL: falla por imprecisión de float
def test_suma_decimales():
    assert 0.1 + 0.2 == 0.3

# BIEN: comparar con tolerancia
import math

def test_suma_decimales():
    assert math.isclose(0.1 + 0.2, 0.3)

# También: pytest.approx
def test_suma_decimales():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

`pytest.approx` y `math.isclose` son las formas idiomáticas. Usar `==` directamente con floats es una trampa clásica que se pregunta en entrevistas.

---

## Error 9. Abusar de `print` cuando un debugger sería más rápido

Para bugs complejos (estado profundo, llamadas encadenadas, bucles), añadir prints y relanzar el programa varias veces es más lento que poner un `breakpoint()` y explorar el estado en una sesión.

```python
# MAL: prints por todas partes para ir acotando
def funcion_compleja(datos):
    print(f"entrada: {datos}")
    paso1 = transformar(datos)
    print(f"paso1: {paso1}")
    paso2 = validar(paso1)
    print(f"paso2: {paso2}")
    ...

# BIEN: un breakpoint inspecciona todo el estado de una vez
def funcion_compleja(datos):
    breakpoint()
    paso1 = transformar(datos)
    paso2 = validar(paso1)
    ...
```

El debugger permite inspeccionar el estado completo, ejecutar código arbitrario, subir por la pila de llamadas. Saber cuándo dejar los prints y abrir un debugger es habilidad de programador con experiencia.

---

## Error 10. No ejecutar los tests antes de subir cambios

Confiar en CI para detectar fallos perjudica al equipo: los builds rotos en main son disruptivos. La disciplina profesional es ejecutar los tests localmente antes de cada push.

```bash
# MAL: commitear y dejar que CI avise si falla algo
git push

# BIEN: verificar antes de subir
pytest && git push
```

Configurar un pre-commit hook con `pytest` garantiza que nadie se lo salte. En entrevistas se pregunta por el flujo de trabajo; la respuesta esperada incluye "corro los tests localmente antes de subir".
