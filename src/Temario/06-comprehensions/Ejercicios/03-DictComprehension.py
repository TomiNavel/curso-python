# =============================================================================
# EJERCICIO 3: Dict comprehensions
# =============================================================================
# Tienes datos de empleados de una empresa. Usa dict comprehensions para
# construir y transformar diccionarios.
#
# DATOS:
empleados = ["Marta", "Jorge", "Sara", "David", "Elena"]
salarios = [2800, 3500, 2200, 4100, 3000]
departamentos = ["RRHH", "IT", "RRHH", "IT", "Ventas"]
antiguedad = [3, 7, 1, 10, 5]  # años en la empresa
#
# TAREAS:
# 1. Crea un diccionario {nombre: salario} para todos los empleados (salario_por_empleado)
# 2. Crea un diccionario {nombre: salario_con_bonus} donde el bonus es 10% del salario
#    si la antigüedad >= 5 años, 0 en caso contrario. Redondea a 2 decimales. (salario_con_bonus)
# 3. Crea un diccionario solo con los empleados del departamento "IT" {nombre: salario} (empleados_it)
# 4. Crea un diccionario {nombre: departamento} invirtiendo la búsqueda: dado que puede haber
#    varios empleados por departamento, guarda una lista con los nombres de cada depto.
#    Pista: esto no es invertir claves/valores directamente; construye el dict con los deptos únicos
#    como clave y los nombres filtrados como valor. (empleados_por_depto)
# 5. Crea un diccionario {nombre: "senior" | "junior"} donde senior = antigüedad >= 5 (nivel)
#
# RESULTADO ESPERADO:
# Salario por empleado: {'Marta': 2800, 'Jorge': 3500, 'Sara': 2200, 'David': 4100, 'Elena': 3000}
# Salario con bonus: {'Marta': 2800, 'Jorge': 3850.0, 'Sara': 2200, 'David': 4510.0, 'Elena': 3300.0}
# Empleados IT: {'Jorge': 3500, 'David': 4100}
# Empleados por depto: {'RRHH': ['Marta', 'Sara'], 'IT': ['Jorge', 'David'], 'Ventas': ['Elena']}
# Nivel: {'Marta': 'junior', 'Jorge': 'senior', 'Sara': 'junior', 'David': 'senior', 'Elena': 'senior'}
# =============================================================================

# Tu código aquí
