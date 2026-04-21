# =============================================================================
# EJERCICIO 2: Sistema de Empleados
# =============================================================================
# Crea una jerarquía de empleados con herencia y uso de super().
#
# Clase base Empleado:
# - Atributos: nombre (str), salario_base (float)
# - Método salario_total(): devuelve salario_base
# - Método resumen(): "Ana - Empleado: $3,000.00"
# - __repr__: Empleado('Ana', 3000)
#
# Subclase Gerente(Empleado):
# - Atributo extra: bono (float)
# - salario_total(): salario_base + bono (usa super() + bono)
# - resumen(): extiende el resumen del padre con " [Gerente, bono: $500.00]"
#
# Subclase Desarrollador(Empleado):
# - Atributo extra: lenguaje (str)
# - resumen(): extiende el resumen del padre con " [Dev: Python]"
#
# Subclase TechLead(Desarrollador, Gerente):
#   (herencia múltiple: es desarrollador Y gerente)
# - salario_total(): usa super() (sigue el MRO, sumará bono de Gerente)
# - resumen(): extiende el resumen de Desarrollador con " + TechLead"
#
# RESULTADO ESPERADO:
# Ana - Empleado: $3,000.00
# Bob - Empleado: $6,000.00 [Gerente, bono: $1,000.00]
# Carlos - Empleado: $4,000.00 [Dev: Python]
# Diana - Empleado: $6,000.00 [Gerente, bono: $1,500.00] [Dev: Go] + TechLead
# MRO de TechLead: TechLead -> Desarrollador -> Gerente -> Empleado -> object
# =============================================================================

# Tu código aquí

# ana = Empleado("Ana", 3000)
# bob = Gerente("Bob", 5000, 1000)
# carlos = Desarrollador("Carlos", 4000, "Python")
# diana = TechLead("Diana", 4500, 1500, "Go")
#
# for emp in [ana, bob, carlos, diana]:
#     print(emp.resumen())
#
# mro = " -> ".join(c.__name__ for c in TechLead.__mro__)
# print(f"MRO de TechLead: {mro}")
