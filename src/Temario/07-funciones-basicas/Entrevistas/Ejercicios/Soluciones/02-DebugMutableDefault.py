# =====================
# SOLUCIÓN
# =====================
# El parámetro lista=[] se evalúa UNA sola vez (al definir la función).
# Todas las llamadas que no pasen una lista explícita comparten el mismo
# objeto lista. Por eso las tareas de Pedro incluyen también las de Ana.
#
# ERRORES CORREGIDOS:
# 1. lista=[] → lista=None, con creación de lista nueva dentro de la función


def agregar_tarea(nombre, tareas, lista=None):
    if lista is None:
        lista = []
    for tarea in tareas:
        lista.append(tarea)
    return lista

tareas_ana = agregar_tarea("Ana", ["Estudiar", "Comprar"])
print(f"Tareas de Ana: {tareas_ana}")

tareas_pedro = agregar_tarea("Pedro", ["Trabajar"])
print(f"Tareas de Pedro: {tareas_pedro}")
