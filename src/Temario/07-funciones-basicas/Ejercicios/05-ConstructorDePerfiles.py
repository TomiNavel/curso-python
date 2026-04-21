# =============================================================================
# EJERCICIO 5: Constructor de Perfiles
# =============================================================================
# Practica *args, **kwargs y desempaquetado de argumentos.
#
# Completa cada paso en orden. Después de cada operación, imprime el resultado
# indicado para verificar que funciona correctamente.
#
# RESULTADO ESPERADO:
# Total: 150
# Total: 0
# nombre: Ana
# edad: 28
# ciudad: Madrid
# profesion: Ingeniera
# Ana (28) - Madrid, Ingeniera
# Pedro (35)
# =============================================================================

# PASO 1: Define una función "sumar_todos" que use *args para aceptar
# cualquier cantidad de números y devuelva su suma.
# Imprime: sumar_todos(10, 20, 30, 40, 50) y sumar_todos().

# Tu código aquí

# PASO 2: Define una función "mostrar_datos" que use **kwargs.
# Debe recorrer kwargs.items() e imprimir "clave: valor" por cada entrada.
# Llama a: mostrar_datos(nombre="Ana", edad=28, ciudad="Madrid", profesion="Ingeniera")

# Tu código aquí

# PASO 3: Define una función "crear_perfil" que reciba nombre, edad,
# y **kwargs para datos opcionales. Debe devolver un string con formato:
# - Si hay kwargs: "nombre (edad) - valor1, valor2, ..."
#   (los valores de kwargs separados por ", ")
# - Si no hay kwargs: "nombre (edad)"
# Imprime: crear_perfil("Ana", 28, ciudad="Madrid", profesion="Ingeniera")
# y crear_perfil("Pedro", 35).

# Tu código aquí

