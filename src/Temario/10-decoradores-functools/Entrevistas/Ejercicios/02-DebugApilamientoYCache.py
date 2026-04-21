# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Apilamiento y Cache
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# === RESULTADO FINAL ===
# === resultado final ===
# 832040
# 832040
# =============================================================================

from functools import wraps, lru_cache

# Error 1: el orden de los decoradores produce el resultado incorrecto
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

@mayusculas
@entre_signos
def formatear(texto):
    return texto

# Debería imprimir "=== RESULTADO FINAL ===" (primero mayúsculas, luego signos)
print(formatear("resultado final"))

# Y también debería funcionar al revés:
# "=== resultado final ===" (primero signos, luego... no, solo signos sin mayúsculas)
# Imprime el resultado de aplicar SOLO entre_signos (sin mayusculas)
@entre_signos
def formatear_simple(texto):
    return texto

print(formatear_simple("resultado final"))


# Error 2: la caché no funciona con este tipo de argumento
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(30))


# Error 3: se intenta usar lru_cache pero falla
@lru_cache
def buscar_en_datos(datos, clave):
    for item in datos:
        if item["id"] == clave:
            return item
    return None

datos = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Pedro"}]
# print(buscar_en_datos(datos, 1))  # esto falla — ¿por qué y cómo se arregla?

# Descomenta la línea y corrígela para que funcione:
# print(buscar_en_datos(???, 1))
