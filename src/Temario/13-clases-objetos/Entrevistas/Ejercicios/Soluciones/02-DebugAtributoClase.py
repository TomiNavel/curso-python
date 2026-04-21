# =====================
# SOLUCIÓN
# =====================
# Error 1: "miembros = []" es un atributo de clase. Todas las instancias
#   comparten la misma lista. Agregar un miembro a frontend también lo añade
#   a backend. Solución: mover miembros a __init__ como atributo de instancia.
#
# Error 2: "self.total_equipos += 1" no modifica el atributo de clase. Lo que
#   hace Python es: leer Equipo.total_equipos (0), sumar 1, y asignar el
#   resultado como atributo de INSTANCIA self.total_equipos = 1. El atributo
#   de clase nunca cambia.
#   Solución: Equipo.total_equipos += 1
#
# Error 3: (Consecuencia del Error 1) __str__ muestra self.miembros que, al
#   ser atributo de clase, contiene los miembros de TODOS los equipos.
#   Se resuelve al corregir Error 1.
#
# ERRORES CORREGIDOS:
# 1. miembros = [] (clase) → self.miembros = [] (en __init__)
# 2. self.total_equipos += 1 → Equipo.total_equipos += 1


class Equipo:
    total_equipos = 0

    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []
        Equipo.total_equipos += 1

    def agregar(self, miembro):
        self.miembros.append(miembro)

    def __str__(self):
        return f"Equipo {self.nombre}: {self.miembros}"


frontend = Equipo("Frontend")
frontend.agregar("Ana")
frontend.agregar("Bob")

backend = Equipo("Backend")
backend.agregar("Carlos")

print(frontend)
print(backend)
print(f"Total equipos creados: {Equipo.total_equipos}")
