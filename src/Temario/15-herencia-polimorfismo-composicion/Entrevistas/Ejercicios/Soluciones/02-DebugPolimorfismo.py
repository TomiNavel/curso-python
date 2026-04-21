# =====================
# SOLUCIÓN
# =====================
# Error 1: Email.__init__ no llama a super().__init__(mensaje).
#   self.mensaje nunca se inicializa. Al llamar enviar(), self.mensaje
#   no existe → AttributeError.
#   Solución: añadir super().__init__(mensaje)
#
# Error 2: Push.enviar() no llama a self.registrar_envio().
#   Los push no se cuentan en el total de enviados.
#   Solución: añadir self.registrar_envio() en Push.enviar()
#
# Error 3: total_libros() llama a e.cantidad sin paréntesis.
#   cantidad es un método, no una propiedad. Sin () devuelve el objeto
#   método, y sum() no puede sumar objetos método.
#   (Nota: este error está en el ejercicio 03, no aquí. El error real aquí
#   es que el total esperado es 3 pero solo Email y SMS registran envío = 2)
#   Solución del Error 2 corrige el conteo.
#
# ERRORES CORREGIDOS:
# 1. Email.__init__: añadir super().__init__(mensaje)
# 2. Push.enviar(): añadir self.registrar_envio()


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
        super().__init__(mensaje)
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
        self.registrar_envio()
        return f"[Envío push] {self.mensaje}"


notificaciones = [
    Email("Reunión mañana", "ana@mail.com"),
    SMS("Código: 5678", "+34600111222"),
    Push("Actualización disponible"),
]

for n in notificaciones:
    print(n.enviar())

print(f"Total enviados: {Notificacion.enviados}")
