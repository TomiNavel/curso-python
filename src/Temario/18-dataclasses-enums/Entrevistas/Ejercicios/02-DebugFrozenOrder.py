# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Frozen y order mal configurados
# =============================================================================
# El siguiente código intenta definir una dataclass "Evento" inmutable,
# comparable por fecha y utilizable como clave de diccionario. Tiene 3
# errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# [Evento(fecha='2024-01-10', nombre='Inicio'), Evento(fecha='2024-03-15', nombre='Revisión'), Evento(fecha='2024-06-01', nombre='Cierre')]
# Reunión importante
# =============================================================================

from dataclasses import dataclass


@dataclass
class Evento:
    nombre: str
    fecha: str


e1 = Evento("Cierre", "2024-06-01")
e2 = Evento("Inicio", "2024-01-10")
e3 = Evento("Revisión", "2024-03-15")

eventos = [e1, e2, e3]
print(sorted(eventos))

e1.nombre = "No se debería poder cambiar"

agenda = {e2: "Reunión importante"}
print(agenda[Evento("Inicio", "2024-01-10")])
