# Preguntas de Entrevista: Context Managers

1. ¿Qué es un context manager y qué problema resuelve?
2. ¿Qué métodos debe implementar un objeto para funcionar como context manager?
3. ¿Qué ocurre exactamente cuando Python ejecuta una sentencia `with`?
4. ¿Qué significan los tres parámetros de `__exit__` y cuándo son `None`?
5. ¿Qué efecto tiene que `__exit__` devuelva `True`?
6. ¿Cómo funciona `@contextmanager` de `contextlib` y qué relación tiene el `yield` con `__enter__` y `__exit__`?
7. ¿Por qué es necesario envolver el `yield` en un bloque `try/finally` dentro de un `@contextmanager`?
8. ¿Cuál es la diferencia entre crear un context manager con clase y con `@contextmanager`?
9. ¿Qué hace `suppress` de `contextlib` y cuándo es apropiado usarlo?
10. ¿Qué es `ExitStack` y en qué situaciones resulta útil?
11. ¿La variable definida con `as` en un `with` deja de existir al salir del bloque?
12. ¿Puede un mismo objeto usarse como context manager varias veces?

---

### R1. ¿Qué es un context manager y qué problema resuelve?

Un context manager es un objeto que gestiona la adquisición y liberación de un recurso de forma automática. Resuelve el problema de garantizar que la limpieza de un recurso —cerrar un archivo, liberar una conexión, soltar un bloqueo— se ejecute siempre, incluso si se produce una excepción durante su uso.

Sin context managers, esta garantía requiere bloques `try/finally` manuales, que son verbosos y dependen de que el programador los escriba correctamente cada vez. La sentencia `with` encapsula este patrón: la liberación del recurso está garantizada por la sintaxis, no por la disciplina del programador.

### R2. ¿Qué métodos debe implementar un objeto para funcionar como context manager?

Debe implementar `__enter__` y `__exit__`. El método `__enter__` se ejecuta al entrar en el bloque `with` y su valor de retorno se asigna a la variable tras `as`. El método `__exit__` se ejecuta al salir del bloque, recibiendo tres argumentos que describen la excepción en curso (o `None` si no hubo excepción).

Es habitual que `__enter__` devuelva `self` para que el bloque `with` tenga acceso al propio objeto, pero puede devolver cualquier cosa. Por ejemplo, `open()` devuelve el objeto archivo desde `__enter__`, que es el propio objeto `self`.

### R3. ¿Qué ocurre exactamente cuando Python ejecuta una sentencia `with`?

Python evalúa la expresión tras `with` para obtener el context manager. Llama a su método `__enter__` y asigna el resultado a la variable `as` (si la hay). A continuación ejecuta el cuerpo del bloque. Al terminar —ya sea normalmente o por una excepción—, Python llama a `__exit__`. Si hubo excepción, `__exit__` recibe el tipo, la instancia y el traceback; si no hubo, recibe `None` en los tres argumentos. Si `__exit__` devuelve un valor truthy, la excepción se suprime; en caso contrario, se propaga.

### R4. ¿Qué significan los tres parámetros de `__exit__` y cuándo son `None`?

Los tres parámetros son `exc_type` (la clase de la excepción), `exc_val` (la instancia de la excepción) y `exc_tb` (el traceback). Cuando el bloque `with` termina sin error, los tres son `None`. Cuando se produce una excepción, los tres contienen información sobre ella: `exc_type` permite saber qué tipo de error ocurrió, `exc_val` da acceso al mensaje y datos de la excepción, y `exc_tb` contiene la traza de la pila.

Esto permite que `__exit__` tome decisiones informadas: registrar el error, realizar limpieza específica según el tipo de excepción, o decidir si suprimir la excepción o propagarla.

### R5. ¿Qué efecto tiene que `__exit__` devuelva `True`?

Si `__exit__` devuelve un valor truthy (como `True`), la excepción se suprime: el programa continúa después del bloque `with` como si no hubiera ocurrido ningún error. Si devuelve un valor falsy (`False`, `None`, o no devuelve nada), la excepción se propaga normalmente.

Suprimir excepciones es una operación delicada. Solo debe hacerse cuando ignorar el error es la acción correcta y deliberada. Suprimir excepciones silenciosamente como práctica general puede ocultar errores reales y dificultar la depuración. La convención es no devolver `True` a menos que haya una razón explícita y documentada.

### R6. ¿Cómo funciona `@contextmanager` de `contextlib` y qué relación tiene el `yield` con `__enter__` y `__exit__`?

El decorador `@contextmanager` convierte una función generadora en un context manager. La función debe contener exactamente un `yield`. Todo el código antes del `yield` se ejecuta como `__enter__`, el valor que produce el `yield` es lo que se asigna a la variable `as`, y todo el código después del `yield` se ejecuta como `__exit__`.

Internamente, `@contextmanager` crea un objeto que implementa `__enter__` y `__exit__` invocando la función generadora y avanzándola hasta el `yield` y luego más allá. El resultado es equivalente a una clase con ambos métodos, pero con menos código.

### R7. ¿Por qué es necesario envolver el `yield` en un bloque `try/finally` dentro de un `@contextmanager`?

Porque si se produce una excepción dentro del bloque `with`, esa excepción se inyecta en el generador en el punto del `yield`. Sin un `try/finally`, el código posterior al `yield` nunca se ejecutaría, lo que significa que la limpieza del recurso no ocurriría. El bloque `finally` garantiza que el código de limpieza se ejecute independientemente de si hubo excepción.

Esto es análogo a lo que ocurre con `__exit__` en una clase: ese método se llama siempre, haya o no excepción. El `try/finally` en un `@contextmanager` replica esa garantía.

### R8. ¿Cuál es la diferencia entre crear un context manager con clase y con `@contextmanager`?

Con clase se tiene control total: se pueden mantener atributos, exponer métodos adicionales y escribir lógica compleja en `__exit__` (inspeccionar la excepción, decidir si suprimirla). Con `@contextmanager` se escribe menos código, pero la lógica queda confinada a una función y no hay un objeto con estado propio más allá de variables locales.

En la práctica, `@contextmanager` es suficiente para la mayoría de casos simples (envolver adquisición/liberación de un recurso). Las clases se prefieren cuando el context manager necesita ser también un objeto con identidad, atributos accesibles y métodos propios.

### R9. ¿Qué hace `suppress` de `contextlib` y cuándo es apropiado usarlo?

`suppress` crea un context manager que captura y silencia las excepciones de los tipos indicados. Es una alternativa más limpia a un bloque `try/except` con `pass` cuando la única acción ante la excepción es ignorarla.

Es apropiado cuando ignorar la excepción es la acción correcta y completa: por ejemplo, intentar borrar un archivo que puede no existir (`suppress(FileNotFoundError)`). No es apropiado cuando la excepción requiere alguna acción adicional como registrar un log, reintentar la operación o notificar al usuario.

### R10. ¿Qué es `ExitStack` y en qué situaciones resulta útil?

`ExitStack` es un context manager que gestiona una pila dinámica de otros context managers y funciones de limpieza. Es útil cuando el número de recursos a gestionar no se conoce de antemano —por ejemplo, abrir una lista variable de archivos— o cuando los recursos se adquieren condicionalmente durante la ejecución.

Cada recurso se registra con `enter_context()` y `ExitStack` garantiza que todos se liberen al salir, en orden inverso al de registro (LIFO). También permite registrar funciones de limpieza arbitrarias con `callback()`.

### R11. ¿La variable definida con `as` en un `with` deja de existir al salir del bloque?

No. La variable sigue existiendo en el ámbito actual después del bloque `with`, como cualquier otra variable definida dentro de un bloque. Lo que cambia es el estado del recurso: un archivo seguirá existiendo como objeto Python, pero estará cerrado. Se puede inspeccionar la variable (por ejemplo, comprobar `f.closed`), pero operar con el recurso cerrado lanzará una excepción.

Python no tiene scope de bloque como otros lenguajes: `if`, `for`, `with` y `try` no crean ámbitos nuevos. Solo las funciones y las clases crean ámbitos.

### R12. ¿Puede un mismo objeto usarse como context manager varias veces?

Depende de la implementación. Algunos context managers son reutilizables: si `__enter__` puede reiniciar el estado y `__exit__` puede dejarlo limpio, el mismo objeto puede usarse en múltiples sentencias `with`. Un ejemplo es `suppress()`, que puede usarse repetidamente.

Otros no son reutilizables: una vez que `__exit__` libera el recurso, intentar llamar a `__enter__` de nuevo puede fallar o producir resultados inesperados. Los generadores creados con `@contextmanager` no son reutilizables, porque un generador solo puede recorrerse una vez. Cada llamada a la función decorada crea un context manager nuevo, pero un mismo objeto generador no puede reentrarse.
