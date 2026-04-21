# =============================================================================
# EJERCICIO 5: IntEnum Prioridad
# =============================================================================
# Crea un IntEnum "Prioridad" con tres miembros: BAJA=1, MEDIA=2, ALTA=3.
#
# Crea una dataclass "Tarea" con los campos:
#   - titulo: str
#   - prioridad: Prioridad (por defecto Prioridad.MEDIA)
#
# Dada una lista de tareas, ordénalas por prioridad descendente (ALTA primero)
# aprovechando que IntEnum permite comparar sus miembros como enteros.
#
# RESULTADO ESPERADO:
# Tarea(titulo='Deploy', prioridad=<Prioridad.ALTA: 3>)
# Tarea(titulo='Documentar', prioridad=<Prioridad.MEDIA: 2>)
# Tarea(titulo='Limpiar logs', prioridad=<Prioridad.BAJA: 1>)
# =============================================================================

# Tu código aquí


# Pruebas
tareas = [
    Tarea("Limpiar logs", Prioridad.BAJA),
    Tarea("Deploy", Prioridad.ALTA),
    Tarea("Documentar"),
]

for tarea in sorted(tareas, key=lambda t: t.prioridad, reverse=True):
    print(tarea)
