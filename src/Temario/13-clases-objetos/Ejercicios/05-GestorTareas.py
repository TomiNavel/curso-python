# =============================================================================
# EJERCICIO 5: Gestor de Tareas
# =============================================================================
# Crea dos clases: `Tarea` y `GestorTareas`.
#
# Clase Tarea:
# - Atributos: titulo (str), prioridad (int, 1-5, por defecto 3), completada (bool, False)
# - Atributo de clase: _siguiente_id = 1 (autoincremental)
# - En __init__, asignar self.id = Tarea._siguiente_id e incrementar _siguiente_id
# - Validar que prioridad esté entre 1 y 5 (lanzar ValueError si no)
# - completar(): marca la tarea como completada
# - __repr__: Tarea(1, 'Estudiar', prioridad=3, completada=False)
# - __str__: "[  ] #1 Estudiar (P3)" o "[✓] #1 Estudiar (P3)" si completada
#   (usar "X" en lugar de "✓" para compatibilidad)
#
# Clase GestorTareas:
# - Atributos: tareas (lista vacía)
# - agregar(titulo, prioridad=3): crea y añade una Tarea, devuelve la tarea creada
# - completar(id_tarea): marca como completada la tarea con ese id.
#   Lanzar ValueError si no existe.
# - pendientes(): devuelve lista de tareas no completadas, ordenadas por prioridad (mayor primero)
# - completadas(): devuelve lista de tareas completadas
# - resumen(): devuelve string con formato mostrado abajo
#
# @staticmethod
# - prioridad_texto(prioridad): devuelve "Crítica" (5), "Alta" (4),
#   "Media" (3), "Baja" (2), "Mínima" (1)
#
# RESULTADO ESPERADO:
# === Tareas ===
# Pendientes (3):
#   [  ] #3 Desplegar (P5)
#   [  ] #1 Estudiar Python (P3)
#   [  ] #4 Leer docs (P2)
# Completadas (1):
#   [X] #2 Hacer ejercicios (P4)
#
# Prioridad de tarea 3: Crítica
# =============================================================================

# Tu código aquí

# gestor = GestorTareas()
# gestor.agregar("Estudiar Python", 3)
# gestor.agregar("Hacer ejercicios", 4)
# gestor.agregar("Desplegar", 5)
# gestor.agregar("Leer docs", 2)
# gestor.completar(2)
# print(gestor.resumen())
# print(f"Prioridad de tarea 3: {GestorTareas.prioridad_texto(5)}")
