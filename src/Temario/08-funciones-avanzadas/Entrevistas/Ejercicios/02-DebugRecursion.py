# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Recursión
# =============================================================================
# El siguiente código tiene 2 funciones recursivas con errores.
# Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# cuenta_atras: 5 4 3 2 1 0
# suma_hasta(5) = 15
# suma_hasta(-3) = 0
# =============================================================================

# Error 1: la función no se detiene nunca
def cuenta_atras(n):
    print(n, end=" ")
    cuenta_atras(n - 1)

# Descomentar para probar (CUIDADO: provoca RecursionError):
# cuenta_atras(5)

# Error 2: la función devuelve resultados incorrectos para negativos
def suma_hasta(n):
    if n == 0:
        return 0
    return n + suma_hasta(n - 1)

# Descomentar para probar:
# print(f"suma_hasta(5) = {suma_hasta(5)}")
# print(f"suma_hasta(-3) = {suma_hasta(-3)}")  # RecursionError
