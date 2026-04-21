# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Atributo de clase mutable
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Equipo Frontend: ['Ana', 'Bob']
# Equipo Backend: ['Carlos']
# Total equipos creados: 2
# =============================================================================

class Equipo:
    total_equipos = 0
    miembros = []

    def __init__(self, nombre):
        self.nombre = nombre
        Equipo.total_equipos += 1

    def agregar(self, miembro):
        Equipo.miembros.append(miembro)

    def __str__(self):
        return f"Equipo {self.nombre}: {Equipo.miembros}"


frontend = Equipo("Frontend")
frontend.agregar("Ana")
frontend.agregar("Bob")

backend = Equipo("Backend")
backend.agregar("Carlos")

print(frontend)
print(backend)
print(f"Total equipos creados: {Equipo.total_equipos}")
