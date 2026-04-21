# =============================================================================
# EJERCICIO 2: Context manager con @contextmanager
# =============================================================================
# Implementa un context manager "etiqueta_html" usando @contextmanager.
# Recibe el nombre de una etiqueta HTML, imprime la etiqueta de apertura
# al entrar, y la etiqueta de cierre al salir.
#
# RESULTADO ESPERADO:
# <html>
# <body>
# <p>
# Hola mundo
# </p>
# </body>
# </html>
# =============================================================================

from contextlib import contextmanager

# Tu código aquí


# Pruebas
with etiqueta_html("html"):
    with etiqueta_html("body"):
        with etiqueta_html("p"):
            print("Hola mundo")
