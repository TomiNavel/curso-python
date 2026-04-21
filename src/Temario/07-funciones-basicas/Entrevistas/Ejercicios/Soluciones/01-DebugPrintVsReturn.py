# =====================
# SOLUCIÓN
# =====================
# Error en las tres funciones: usan print() en lugar de return.
# print() muestra el valor en consola pero devuelve None.
# Al asignar el resultado a una variable, se obtiene None.
#
# ERRORES CORREGIDOS:
# 1. calcular_descuento: print(precio_final) → return precio_final
# 2. es_mayor_de_edad: print(edad >= 18) → return edad >= 18
# 3. convertir_a_mayusculas: print(texto.upper()) → return texto.upper()


def calcular_descuento(precio, porcentaje):
    precio_final = precio * (1 - porcentaje / 100)
    return precio_final

def es_mayor_de_edad(edad):
    return edad >= 18

def convertir_a_mayusculas(texto):
    return texto.upper()

precio = calcular_descuento(50, 10)
print(f"Precio final: {precio}")

mayor = es_mayor_de_edad(25)
print(f"Es mayor de edad: {mayor}")

mensaje = convertir_a_mayusculas("hola mundo")
print(f"Mensaje: {mensaje}")
