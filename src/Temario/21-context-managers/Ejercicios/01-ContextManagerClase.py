# =============================================================================
# EJERCICIO 1: Context manager con clase
# =============================================================================
# Implementa una clase "Indentador" que funcione como context manager.
# Cada vez que se entra en un bloque with, el nivel de indentación aumenta
# en 1. Al salir del bloque, el nivel disminuye en 1.
# La clase debe tener un método "escribir(texto)" que imprima el texto
# con la indentación correspondiente (usando 4 espacios por nivel).
#
# RESULTADO ESPERADO:
# Inicio
#     Nivel 1
#         Nivel 2
#         Todavía nivel 2
#     De vuelta al nivel 1
# Fin
# =============================================================================

# Tu código aquí


# Pruebas
ind = Indentador()
ind.escribir("Inicio")
with ind:
    ind.escribir("Nivel 1")
    with ind:
        ind.escribir("Nivel 2")
        ind.escribir("Todavía nivel 2")
    ind.escribir("De vuelta al nivel 1")
ind.escribir("Fin")
