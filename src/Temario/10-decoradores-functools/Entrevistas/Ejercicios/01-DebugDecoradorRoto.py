# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Decorador Roto
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Llamando a sumar
# 8
# sumar
# Suma dos números.
# =============================================================================

# Error 1 y 2: el decorador tiene dos problemas
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__}")
        func(*args, **kwargs)
    return wrapper

@mi_decorador
def sumar(a, b):
    """Suma dos números."""
    return a + b

resultado = sumar(3, 5)
print(resultado)

# Error 3: los metadatos se perdieron
print(sumar.__name__)
print(sumar.__doc__)
