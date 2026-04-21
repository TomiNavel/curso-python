empleados = ["Marta", "Jorge", "Sara", "David", "Elena"]
salarios = [2800, 3500, 2200, 4100, 3000]
departamentos = ["RRHH", "IT", "RRHH", "IT", "Ventas"]
antiguedad = [3, 7, 1, 10, 5]

# 1. Diccionario {nombre: salario}
salario_por_empleado = {nombre: salario for nombre, salario in zip(empleados, salarios)}
print("Salario por empleado:", salario_por_empleado)

# 2. Salario con bonus del 10% si antigüedad >= 5 años
salario_con_bonus = {
    nombre: round(salario * 1.1, 2) if anios >= 5 else salario
    for nombre, salario, anios in zip(empleados, salarios, antiguedad)
}
print("Salario con bonus:", salario_con_bonus)

# 3. Solo empleados del departamento IT
empleados_it = {
    nombre: salario
    for nombre, salario, depto in zip(empleados, salarios, departamentos)
    if depto == "IT"
}
print("Empleados IT:", empleados_it)

# 4. Empleados agrupados por departamento
deptos_unicos = set(departamentos)
empleados_por_depto = {
    depto: [nombre for nombre, d in zip(empleados, departamentos) if d == depto]
    for depto in deptos_unicos
}
print("Empleados por depto:", empleados_por_depto)

# 5. Nivel senior/junior según antigüedad
nivel = {
    nombre: "senior" if anios >= 5 else "junior"
    for nombre, anios in zip(empleados, antiguedad)
}
print("Nivel:", nivel)
