# =============================================================================
# SOLUCIÓN
# =============================================================================

from contextlib import contextmanager


@contextmanager
def etiqueta_html(nombre: str):
    print(f"<{nombre}>")
    try:
        yield
    finally:
        print(f"</{nombre}>")


# Pruebas
with etiqueta_html("html"):
    with etiqueta_html("body"):
        with etiqueta_html("p"):
            print("Hola mundo")
