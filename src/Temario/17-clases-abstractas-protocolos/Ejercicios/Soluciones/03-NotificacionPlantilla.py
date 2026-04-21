from abc import ABC, abstractmethod


class Notificacion(ABC):
    def __init__(self, destinatario, mensaje):
        self.destinatario = destinatario
        self.mensaje = mensaje

    def enviar(self):
        print(f"Preparando envío a {self.destinatario}")
        contenido = self._formatear()
        self._transmitir(contenido)
        print("Envío completado")

    @abstractmethod
    def _formatear(self):
        pass

    @abstractmethod
    def _transmitir(self, contenido):
        pass


class NotificacionEmail(Notificacion):
    def _formatear(self):
        return f"[EMAIL] {self.mensaje}"

    def _transmitir(self, contenido):
        print(f"Enviando por SMTP: {contenido}")


class NotificacionSMS(Notificacion):
    def _formatear(self):
        return self.mensaje.upper()

    def _transmitir(self, contenido):
        print(f"Enviando SMS: {contenido}")


email = NotificacionEmail("ana@example.com", "Bienvenida al sistema")
email.enviar()

sms = NotificacionSMS("+34600123456", "alerta de seguridad")
sms.enviar()
