# Preguntas de Entrevista: Manejo de Errores y Excepciones

1. ¿Cuál es la diferencia entre `BaseException` y `Exception`? ¿Por qué no se debe capturar `BaseException`?
2. ¿Qué diferencia hay entre un `SyntaxError` y una excepción en tiempo de ejecución?
3. ¿Qué hace el bloque `else` en un `try/except/else`? ¿Por qué no poner ese código dentro del `try`?
4. ¿En qué situaciones se ejecuta el bloque `finally`?
5. ¿Qué ocurre si hay un `return` dentro del `try` y también un `return` dentro del `finally`?
6. ¿Qué significa EAFP y LBYL? ¿Cuál prefiere Python y por qué?
7. ¿Por qué es mala práctica usar `except Exception` o `except` sin tipo?
8. ¿Cuál es la diferencia entre `raise` y `raise ... from ...`?
9. ¿Cuándo se justifica crear una excepción personalizada en lugar de usar las estándar?
10. ¿Por qué importa el orden de los bloques `except` cuando las excepciones tienen relación de herencia?
11. ¿Qué es un `ExceptionGroup` y para qué sirve `except*`?
12. ¿Cuál es el resultado de este código?
    ```python
    def funcion():
        try:
            return 1
        finally:
            return 2

    print(funcion())
    ```

---

### R1. ¿Cuál es la diferencia entre `BaseException` y `Exception`? ¿Por qué no se debe capturar `BaseException`?

`BaseException` es la clase raíz de toda la jerarquía de excepciones. `Exception` hereda de `BaseException` y es la base de todas las excepciones que un programa debería capturar.

`SystemExit`, `KeyboardInterrupt` y `GeneratorExit` heredan directamente de `BaseException`, no de `Exception`. Capturar `BaseException` impediría que `Ctrl+C` cierre el programa o que `sys.exit()` funcione. Por eso se debe capturar `Exception` como máximo, nunca `BaseException`.

---

### R2. ¿Qué diferencia hay entre un `SyntaxError` y una excepción en tiempo de ejecución?

Un `SyntaxError` ocurre cuando Python intenta compilar el código y encuentra sintaxis inválida — el programa ni siquiera llega a ejecutarse. Una excepción en tiempo de ejecución (como `ValueError` o `TypeError`) ocurre durante la ejecución de código sintácticamente correcto.

Un `SyntaxError` no se puede capturar con `try/except` en el mismo bloque de código donde está el error, porque el bloque completo falla al compilarse. Solo se puede capturar si el código con error está en otro módulo importado dinámicamente o se ejecuta con `exec()`.

---

### R3. ¿Qué hace el bloque `else` en un `try/except/else`? ¿Por qué no poner ese código dentro del `try`?

El `else` se ejecuta solo si el bloque `try` se completó sin lanzar ninguna excepción. La ventaja sobre poner más código dentro del `try` es que evita capturar excepciones inesperadas.

Si dentro del `try` hay código que no debería estar protegido por el `except`, una excepción accidental en ese código quedaría atrapada y enmascarada. Con `else`, solo el código que realmente puede fallar está dentro del `try`, y el código que depende de su éxito queda en `else`, fuera de la protección del `except`.

---

### R4. ¿En qué situaciones se ejecuta el bloque `finally`?

El bloque `finally` se ejecuta **siempre**, sin importar lo que ocurra:

- Si el `try` se completa sin error
- Si se captura una excepción en un `except`
- Si hay una excepción no capturada (el `finally` se ejecuta antes de que se propague)
- Si hay un `return`, `break` o `continue` dentro del `try` o del `except`

La única forma de que no se ejecute es una terminación abrupta del proceso (por ejemplo, `os._exit()` o que el sistema operativo mate el proceso).

---

### R5. ¿Qué ocurre si hay un `return` dentro del `try` y también un `return` dentro del `finally`?

El `return` del `finally` sobrescribe al del `try`. El valor devuelto es el del `finally`.

```python
def funcion():
    try:
        return 1
    finally:
        return 2

funcion()  # devuelve 2
```

Esto es una mala práctica — poner `return` en `finally` puede ocultar excepciones (si el `try` lanzó una excepción, el `return` del `finally` la silencia). El `finally` debería usarse solo para limpieza, nunca para devolver valores.

---

### R6. ¿Qué significa EAFP y LBYL? ¿Cuál prefiere Python y por qué?

- **EAFP** (*Easier to Ask Forgiveness than Permission*): intentar la operación y capturar la excepción si falla.
- **LBYL** (*Look Before You Leap*): verificar las condiciones antes de actuar.

Python prefiere EAFP porque:
1. **Evita condiciones de carrera** — entre la verificación y la acción, el estado puede cambiar.
2. **Es más eficiente** cuando el caso exitoso es el más común, porque entrar en un `try` sin excepción tiene un coste casi nulo.
3. **El camino feliz es más legible** — la lógica principal no se fragmenta con verificaciones.

---

### R7. ¿Por qué es mala práctica usar `except Exception` o `except` sin tipo?

Capturar excepciones genéricas oculta errores de programación. Un `TypeError` o `NameError` causado por un bug en el código queda atrapado silenciosamente en lugar de revelarse. Esto convierte errores que serían fáciles de encontrar con un traceback en bugs invisibles que se manifiestan como comportamiento incorrecto.

`except` sin tipo es aún peor: captura incluso `SystemExit` y `KeyboardInterrupt`, impidiendo cerrar el programa con `Ctrl+C` o `sys.exit()`.

Siempre se deben capturar excepciones específicas que se espera que ocurran.

---

### R8. ¿Cuál es la diferencia entre `raise` y `raise ... from ...`?

`raise` solo lanza una excepción. `raise NuevaExcepcion from excepcion_original` lanza la nueva excepción y establece una relación de causa explícita.

Con `from`, el traceback muestra ambas excepciones conectadas por "The above exception was the direct cause of the following exception". Sin `from`, si se lanza una excepción dentro de un `except`, Python muestra ambas pero con "During handling of the above exception, another exception occurred" — un mensaje menos claro que sugiere un error inesperado en el manejo, no una conversión intencional.

---

### R9. ¿Cuándo se justifica crear una excepción personalizada en lugar de usar las estándar?

Se justifica cuando:

1. **El error es específico del dominio** — `SaldoInsuficienteError` comunica más que `ValueError("saldo insuficiente")` y permite capturarlo de forma independiente.
2. **Se necesita distinguir entre errores distintos** — si una función puede fallar por varios motivos, una excepción distinta para cada caso permite que el `except` reaccione de forma específica.

No se justifica si una excepción estándar con un buen mensaje comunica lo mismo. Técnicas más avanzadas, como añadir atributos personalizados a la excepción o construir jerarquías de errores, se verán tras estudiar clases y herencia (temas 13 y 15).

---

### R10. ¿Por qué importa el orden de los bloques `except` cuando las excepciones tienen relación de herencia?

Python usa el primer `except` que coincida. Si una excepción genérica (padre) va antes que una específica (hija), la específica nunca se ejecuta porque el padre ya la captura.

```python
# MAL — FileNotFoundError nunca se alcanza
except OSError: ...
except FileNotFoundError: ...  # nunca se ejecuta

# BIEN — la más específica primero
except FileNotFoundError: ...
except OSError: ...
```

---

### R11. ¿Qué es un `ExceptionGroup` y para qué sirve `except*`?

`ExceptionGroup` (Python 3.11+) es una excepción que agrupa múltiples excepciones que ocurrieron simultáneamente, típicamente en código concurrente donde varias tareas pueden fallar al mismo tiempo.

`except*` permite capturar excepciones específicas dentro del grupo. A diferencia de `except` normal, `except*` puede ejecutar múltiples ramas para el mismo grupo — una para cada tipo de excepción presente.

---

### R12. ¿Cuál es el resultado de este código?

```python
def funcion():
    try:
        return 1
    finally:
        return 2

print(funcion())
```

Imprime `2`. El `finally` siempre se ejecuta, y su `return` sobrescribe el del `try`. Esto es una mala práctica — el `finally` no debería contener `return`.
