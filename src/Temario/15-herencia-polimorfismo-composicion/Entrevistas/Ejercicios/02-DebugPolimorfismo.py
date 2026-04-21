# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Polimorfismo y override
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# [Envío email] Reunión mañana -> ana@mail.com
# [Envío SMS] Código: 5678 -> +34600111222
# [Envío push] Actualización disponible
# Total enviados: 3
# =============================================================================

class Notificacion:
    enviados = 0

    def __init__(self, mensaje):
        self.mensaje = mensaje

    def enviar(self):
        raise NotImplementedError

    def registrar_envio(self):
        Notificacion.enviados += 1


class Email(Notificacion):
    def __init__(self, mensaje, destinatario):
        self.destinatario = destinatario

    def enviar(self):
        self.registrar_envio()
        return f"[Envío email] {self.mensaje} -> {self.destinatario}"


class SMS(Notificacion):
    def __init__(self, mensaje, telefono):
        super().__init__(mensaje)
        self.telefono = telefono

    def enviar(self):
        self.registrar_envio()
        return f"[Envío SMS] {self.mensaje} -> {self.telefono}"


class Push(Notificacion):
    def enviar(self):
        return f"[Envío push] {self.mensaje}"


notificaciones = [
    Email("Reunión mañana", "ana@mail.com"),
    SMS("Código: 5678", "+34600111222"),
    Push("Actualización disponible"),
]

for n in notificaciones:
    print(n.enviar())

print(f"Total enviados: {Notificacion.enviados}")
