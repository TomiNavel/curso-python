# =============================================================================
# EJERCICIO 4: Corregir Late Binding
# =============================================================================
# El siguiente código tiene un bug de late binding. Las funciones creadas
# en el bucle deberían devolver cada una el cuadrado de su índice,
# pero todas devuelven lo mismo.
#
# Corrige el código para que funcione correctamente.
#
# RESULTADO ESPERADO:
# [0, 1, 4, 9, 16]
# =============================================================================

# Código con bug — corrígelo
funciones = []
for i in range(5):
    funciones.append(lambda: i ** 2)

print([f() for f in funciones])  # Debería imprimir [0, 1, 4, 9, 16]
