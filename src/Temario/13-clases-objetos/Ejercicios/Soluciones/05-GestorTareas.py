class Tarea:
    _siguiente_id = 1

    def __init__(self, titulo, prioridad=3):
        if not 1 <= prioridad <= 5:
            raise ValueError(f"La prioridad debe estar entre 1 y 5, se recibió: {prioridad}")
        self.id = Tarea._siguiente_id
        Tarea._siguiente_id += 1
        self.titulo = titulo
        self.prioridad = prioridad
        self.completada = False

    def completar(self):
        self.completada = True

    def __repr__(self):
        return (
            f"Tarea({self.id}, {self.titulo!r}, "
            f"prioridad={self.prioridad}, completada={self.completada})"
        )

    def __str__(self):
        marca = "X" if self.completada else " "
        return f"[{marca}] #{self.id} {self.titulo} (P{self.prioridad})"


class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar(self, titulo, prioridad=3):
        tarea = Tarea(titulo, prioridad)
        self.tareas.append(tarea)
        return tarea

    def completar(self, id_tarea):
        for tarea in self.tareas:
            if tarea.id == id_tarea:
                tarea.completar()
                return
        raise ValueError(f"No existe tarea con id {id_tarea}")

    def pendientes(self):
        return sorted(
            [t for t in self.tareas if not t.completada],
            key=lambda t: t.prioridad,
            reverse=True,
        )

    def completadas(self):
        return [t for t in self.tareas if t.completada]

    def resumen(self):
        lineas = ["=== Tareas ==="]
        pend = self.pendientes()
        comp = self.completadas()
        lineas.append(f"Pendientes ({len(pend)}):")
        for t in pend:
            lineas.append(f"  {t}")
        lineas.append(f"Completadas ({len(comp)}):")
        for t in comp:
            lineas.append(f"  {t}")
        return "\n".join(lineas)

    @staticmethod
    def prioridad_texto(prioridad):
        textos = {5: "Crítica", 4: "Alta", 3: "Media", 2: "Baja", 1: "Mínima"}
        return textos.get(prioridad, "Desconocida")


gestor = GestorTareas()
gestor.agregar("Estudiar Python", 3)
gestor.agregar("Hacer ejercicios", 4)
gestor.agregar("Desplegar", 5)
gestor.agregar("Leer docs", 2)
gestor.completar(2)
print(gestor.resumen())
print(f"Prioridad de tarea 3: {GestorTareas.prioridad_texto(5)}")
