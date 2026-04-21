# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — print() vs return
# =============================================================================
# Encuentra y corrige los errores.
#
# RESULTADO ESPERADO:
# Precio final: 45.0
# Es mayor de edad: True
# Mensaje: HOLA MUNDO
# =============================================================================

def calcular_descuento(precio, porcentaje):
    precio_final = precio * (1 - porcentaje / 100)
    print(precio_final)

def es_mayor_de_edad(edad):
    print(edad >= 18)

def convertir_a_mayusculas(texto):
    print(texto.upper())

precio = calcular_descuento(50, 10)
print(f"Precio final: {precio}")

mayor = es_mayor_de_edad(25)
print(f"Es mayor de edad: {mayor}")

mensaje = convertir_a_mayusculas("hola mundo")
print(f"Mensaje: {mensaje}")
