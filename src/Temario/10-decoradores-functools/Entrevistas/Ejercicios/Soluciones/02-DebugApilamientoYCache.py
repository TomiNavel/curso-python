# =====================
# SOLUCIÓN
# =====================
# Error 1: el orden de decoradores está invertido. Con @mayusculas arriba
#   y @entre_signos abajo, se ejecuta entre_signos primero ("=== resultado final ===")
#   y luego mayusculas ("=== RESULTADO FINAL ==="). Si se quiere que las mayúsculas
#   se apliquen primero y luego se envuelva en signos, el orden debe ser:
#   @entre_signos (exterior) / @mayusculas (interior, más cerca de la función).
#   Corrección: invertir el orden → @entre_signos arriba, @mayusculas abajo.
#
# Error 2: no hay error real en fibonacci — funciona correctamente.
#   Es una trampa: el código es correcto tal cual.
#
# Error 3: datos es una lista (mutable, no hashable). lru_cache necesita
#   argumentos hashables. Se debe convertir la lista a tupla de tuplas
#   o pasar los datos de otra forma.
#   Corrección: convertir cada dict a tupla de items antes de pasar, o
#   usar una tupla de tuplas. La forma más práctica es no cachear esta función
#   o reestructurar para que datos no sea un argumento.
#
# ERRORES CORREGIDOS:
# 1. Invertir el orden: @entre_signos / @mayusculas
# 2. (no hay error — trampa para el candidato)
# 3. No usar lru_cache con argumentos mutables, o convertir a hashable


from functools import wraps, lru_cache

def mayusculas(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def entre_signos(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        return f"=== {resultado} ==="
    return wrapper

@entre_signos
@mayusculas
def formatear(texto):
    return texto

print(formatear("resultado final"))

@entre_signos
def formatear_simple(texto):
    return texto

print(formatear_simple("resultado final"))


@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(30))


@lru_cache
def buscar_en_datos(datos, clave):
    for item in datos:
        if item[1] == clave:
            return dict(item)
    return None

datos = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Pedro"}]
datos_hashable = tuple(tuple(d.items()) for d in datos)
print(buscar_en_datos(datos_hashable, 1))
