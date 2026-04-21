# =============================================================================
# EJERCICIO 2: Empleado Abstracto con método concreto
# =============================================================================
# Crea una clase abstracta `Empleado` que combine métodos abstractos y concretos
# (patrón plantilla).
#
# Clase abstracta Empleado:
# - __init__(nombre, horas_trabajadas)
# - Método abstracto tarifa_hora() — cada subclase define su tarifa
# - Método concreto calcular_sueldo() que devuelve horas_trabajadas * tarifa_hora()
# - Método concreto __str__ que devuelve:
#   "{nombre}: ${sueldo:,.2f}"
#
# Subclases:
# - EmpleadoJunior: tarifa_hora = 15
# - EmpleadoSenior: tarifa_hora = 40
# - EmpleadoManager: tarifa_hora = 60
#
# La lógica de calcular_sueldo vive en la clase base. Las subclases solo
# definen la tarifa.
#
# RESULTADO ESPERADO:
# Ana: $2,400.00
# Luis: $6,400.00
# María: $9,600.00
# =============================================================================

# Tu código aquí

# empleados = [
#     EmpleadoJunior("Ana", 160),
#     EmpleadoSenior("Luis", 160),
#     EmpleadoManager("María", 160),
# ]
#
# for e in empleados:
#     print(e)
