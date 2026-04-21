# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Múltiples errores
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Cociente: 3, Resto: 2
# Perfil: Ana, 28 años, Madrid
# Números: 6, 15
# =============================================================================

# Error 1: algo va mal con el retorno
def dividir_con_resto(a, b):
    cociente = a // b
    resto = a % b
    return cociente, resto
    print("División completada")

c, r = dividir_con_resto(17, 5)
print(f"Cociente: {c}, Resto: {r}")

# Error 2: algo va mal con los argumentos
def crear_perfil(nombre, edad, ciudad):
    return f"{nombre}, {edad} años, {ciudad}"

perfil = crear_perfil(nombre="Ana", 28, "Madrid")
print(f"Perfil: {perfil}")

# Error 3: algo va mal con el desempaquetado
def calcular(a, b):
    return a * 2, b * 3

x, y, z = calcular(3, 5)
print(f"Números: {x}, {y}")
