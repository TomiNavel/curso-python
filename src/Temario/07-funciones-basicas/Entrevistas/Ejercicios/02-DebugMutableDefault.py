# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Valor por defecto mutable
# =============================================================================
# El siguiente código tiene un bug sutil. La función agregar_tarea debería
# crear una lista nueva para cada usuario, pero las tareas se acumulan
# entre llamadas. Encuentra la causa y corrígela.
#
# RESULTADO ESPERADO:
# Tareas de Ana: ['Estudiar', 'Comprar']
# Tareas de Pedro: ['Trabajar']
# =============================================================================

def agregar_tarea(nombre, tareas, lista=[]):
    for tarea in tareas:
        lista.append(tarea)
    return lista

tareas_ana = agregar_tarea("Ana", ["Estudiar", "Comprar"])
print(f"Tareas de Ana: {tareas_ana}")

tareas_pedro = agregar_tarea("Pedro", ["Trabajar"])
print(f"Tareas de Pedro: {tareas_pedro}")
