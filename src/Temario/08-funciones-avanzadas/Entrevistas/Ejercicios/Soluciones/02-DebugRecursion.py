# =====================
# SOLUCIÓN
# =====================
# Error 1: No tiene caso base. La función se llama infinitamente
#   porque nunca deja de llamar a cuenta_atras(n - 1).
#   Corrección: añadir un caso base que detenga la recursión.
#
# Error 2: El caso base es n == 0, pero si n es negativo nunca se
#   alcanza (pasa por -1, -2, -3... sin parar). El caso base debe
#   cubrir también los negativos.
#   Corrección: cambiar if n == 0 por if n <= 0.
#
# ERRORES CORREGIDOS:
# 1. cuenta_atras: falta caso base → añadir if n < 0: return
# 2. suma_hasta: if n == 0 → if n <= 0 (caso base inalcanzable con negativos)


def cuenta_atras(n):
    if n < 0:
        return
    print(n, end=" ")
    cuenta_atras(n - 1)

cuenta_atras(5)
print()

def suma_hasta(n):
    if n <= 0:
        return 0
    return n + suma_hasta(n - 1)

print(f"suma_hasta(5) = {suma_hasta(5)}")
