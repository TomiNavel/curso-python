# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Late Binding en Closures
# =============================================================================
# El siguiente código tiene 2 errores de late binding. Las funciones creadas
# en los bucles no devuelven lo esperado. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Potencias: [1, 2, 4, 8, 16]
# Saludos: ['Hola, Ana', 'Hola, Pedro', 'Hola, Luis']
# =============================================================================

# Error 1: cada función debería calcular 2 elevado a su índice
potencias = []
for exp in range(5):
    potencias.append(lambda: 2 ** exp)

print(f"Potencias: {[f() for f in potencias]}")


# Error 2: cada función debería saludar con un nombre distinto
nombres = ["Ana", "Pedro", "Luis"]
saludos = []
for nombre in nombres:
    def crear_saludo():
        return f"Hola, {nombre}"
    saludos.append(crear_saludo)

print(f"Saludos: {[f() for f in saludos]}")
