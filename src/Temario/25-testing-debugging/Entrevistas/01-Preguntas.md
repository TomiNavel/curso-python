# Preguntas de Entrevista: Testing y Debugging

1. ¿Cuál es la diferencia entre `pytest` y `unittest` y cuándo elegir cada uno?
2. ¿Qué es una fixture en pytest y qué ventajas tiene sobre `setUp` de unittest?
3. ¿Qué hace `@pytest.mark.parametrize` y por qué es preferible a escribir varios tests casi iguales?
4. ¿Cómo se testea que una función lanza una excepción?
5. ¿Qué es un mock y en qué situaciones es apropiado usarlo?
6. ¿Qué significa "patchear donde se usa, no donde se define"?
7. ¿Qué es la cobertura de tests y por qué no hay que obsesionarse con llegar al 100%?
8. ¿Qué es `breakpoint()` y en qué mejora a `import pdb; pdb.set_trace()`?
9. ¿Cuál es la diferencia entre un test unitario y un test de integración?
10. ¿Qué problemas puede ocultar el abuso de mocks?

---

### R1. ¿Cuál es la diferencia entre `pytest` y `unittest` y cuándo elegir cada uno?

`unittest` está en la biblioteca estándar de Python, inspirado en JUnit. Sus tests se escriben como clases que heredan de `TestCase` y usan métodos como `assertEqual` o `assertRaises`. `pytest` es una librería externa con sintaxis más ligera: funciones con `assert` plano, fixtures por inyección de parámetros y parametrización integrada. Su reporte de errores muestra los valores reales y esperados con detalle sin configuración adicional.

En proyectos nuevos `pytest` es la elección estándar por su ergonomía y ecosistema (plugins para cobertura, paralelización, captura de salida, mocks). `unittest` sigue siendo útil cuando no se puede añadir dependencias externas (scripts restringidos, Lambdas pequeñas) y es la elección en parte de la propia biblioteca estándar. `pytest` ejecuta tests escritos con `unittest` sin cambios, así que conviven sin fricción en bases grandes.

### R2. ¿Qué es una fixture en pytest y qué ventajas tiene sobre `setUp` de unittest?

Una fixture es una función decorada con `@pytest.fixture` que produce datos o recursos para los tests. pytest la inyecta como argumento en cualquier test que la declare, y gestiona su ciclo de vida. Si la fixture usa `yield`, el código después del yield se ejecuta como teardown.

Frente a `setUp` de unittest, las fixtures tienen tres ventajas: son **declarativas** (solo los tests que las piden por parámetro las reciben, no se aplican a toda la clase), son **componibles** (una fixture puede usar otra como dependencia), y tienen **alcances flexibles** (`function`, `class`, `module`, `session`) para controlar con qué frecuencia se crea el recurso. `setUp` se ejecuta antes de cada test de la clase sin distinción.

### R3. ¿Qué hace `@pytest.mark.parametrize` y por qué es preferible a escribir varios tests casi iguales?

El decorador ejecuta el mismo test con varios conjuntos de valores. Recibe los nombres de los parámetros y una lista de tuplas con los valores. pytest ejecuta una vez por tupla y muestra cada caso por separado en el reporte.

Las ventajas son tres. **Menos código**: un test cubre múltiples casos. **Mejor diagnóstico**: si falla un caso concreto, el reporte indica exactamente cuál. **Más casos añadidos con menos esfuerzo**: cubrir un caso nuevo es añadir una tupla, no copiar un test. Frente a un bucle dentro de un único test, la parametrización mantiene cada caso aislado: si falla uno, el resto se sigue ejecutando, y el reporte individual facilita encontrar el problema.

### R4. ¿Cómo se testea que una función lanza una excepción?

En pytest se usa `pytest.raises` como context manager: el bloque `with` ejecuta el código y, si la excepción esperada se lanza, el test pasa. Si se lanza otra o no se lanza ninguna, el test falla. Admite `match` para verificar que el mensaje coincide con un regex.

```python
with pytest.raises(ValueError, match="edad negativa"):
    crear_usuario(edad=-1)
```

En unittest existe el equivalente `self.assertRaises(Excepción)`, también como context manager. Ambos patrones sustituyen al `try/except` manual, que es más largo y menos claro.

### R5. ¿Qué es un mock y en qué situaciones es apropiado usarlo?

Un mock es un objeto sustituto que simula una dependencia real durante los tests, permitiendo ejecutar el código bajo test sin necesidad de la dependencia auténtica. `unittest.mock` ofrece `Mock` para objetos por parámetro y `patch` para sustituir referencias globales temporalmente.

Son apropiados cuando la dependencia es **externa, costosa o no determinista**: una API HTTP, una base de datos, el sistema de archivos, la hora actual, generadores aleatorios. Para código propio rápido y determinista, mockear añade complejidad sin beneficio: es mejor testear el sistema real. Un test que mockea todo acaba verificando llamadas en lugar de comportamiento.

### R6. ¿Qué significa "patchear donde se usa, no donde se define"?

Cuando se parchea una función o clase con `patch`, el argumento debe ser la ruta **desde donde se importa en el módulo bajo test**, no donde está definida originalmente. Si `modulo_a.py` hace `from datetime import datetime`, el patch correcto es `patch("modulo_a.datetime")`, no `patch("datetime.datetime")`.

La razón es que cuando el módulo A importa `datetime`, crea una referencia local en su namespace. Parchear la definición original no afecta a esa referencia local que ya existe. Este error es uno de los más comunes con mocks y es una pregunta clásica de entrevista para ver si la persona ha usado `patch` en profundidad, no solo copiado ejemplos.

### R7. ¿Qué es la cobertura de tests y por qué no hay que obsesionarse con llegar al 100%?

La cobertura mide qué porcentaje del código se ejecuta al correr los tests. Herramientas como `coverage` o `pytest-cov` producen reportes con líneas cubiertas y no cubiertas. Es una métrica orientativa: cobertura alta no garantiza tests buenos (se puede ejecutar código sin comprobar su resultado), pero cobertura baja suele indicar zonas sin testear.

Perseguir el 100% lleva a tests triviales (testear getters, testear que una asignación hace lo que dice) que no aportan confianza y sí mantenimiento. El umbral profesional pragmático está en 80–90%, con tests centrados en el comportamiento importante y los casos límite. En entrevistas, la respuesta correcta es "importa qué se testea, no cuánto".

### R8. ¿Qué es `breakpoint()` y en qué mejora a `import pdb; pdb.set_trace()`?

`breakpoint()` es una función integrada desde Python 3.7 que pausa la ejecución y abre el debugger. Sustituye al antiguo patrón `import pdb; pdb.set_trace()` con varias ventajas: una sola palabra, sin import manual, y **configurable mediante la variable de entorno `PYTHONBREAKPOINT`**.

Esa configurabilidad es la mejora real: se puede definir `PYTHONBREAKPOINT=ipdb.set_trace` para usar `ipdb` (debugger mejorado) sin tocar el código, o `PYTHONBREAKPOINT=0` para deshabilitar todos los breakpoints en producción sin tener que eliminarlos. Con el patrón antiguo hay que editar cada archivo para cambiar el debugger.

### R9. ¿Cuál es la diferencia entre un test unitario y un test de integración?

Un **test unitario** prueba una unidad aislada — normalmente una función o una clase — sustituyendo sus dependencias por mocks o por objetos simples. Es rápido (milisegundos), determinista y se ejecuta en cada cambio de código. Detecta errores de lógica local.

Un **test de integración** prueba cómo colaboran varias unidades reales, o la integración con sistemas externos (base de datos real, API HTTP real con un servidor de prueba). Es más lento, más frágil y menos frecuente, pero detecta errores que los unitarios no ven: serialización, contratos entre módulos, conexiones, configuración. La pirámide de tests recomienda muchos unitarios en la base, menos de integración en el medio y pocos end-to-end arriba.

### R10. ¿Qué problemas puede ocultar el abuso de mocks?

El abuso más común es mockear tanto que el test deja de verificar el **comportamiento** y solo verifica la **interacción**: "la función llama a X antes que a Y con estos argumentos". Ese tipo de test se rompe al refactorizar internamente aunque el comportamiento observable no cambie, y no da confianza real — puede pasar cuando el código está roto si las llamadas siguen siendo correctas.

Otro problema es el **acoplamiento al diseño actual**: los mocks fijan la forma concreta de las dependencias. Cambiar una firma de función o reorganizar módulos obliga a tocar todos los tests, lo que penaliza el refactoring. Un indicio de abuso es que el test tenga más líneas de configuración de mocks que de ejecución del código bajo test; suele significar que la lógica debería extraerse a una función pura testeable sin mocks.
