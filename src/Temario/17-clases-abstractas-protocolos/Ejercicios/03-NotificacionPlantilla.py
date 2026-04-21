# =============================================================================
# EJERCICIO 3: Notificación con patrón plantilla
# =============================================================================
# Crea una clase abstracta `Notificacion` que defina el flujo común de envío
# y deje abiertas las partes variables a las subclases.
#
# Clase abstracta Notificacion:
# - __init__(destinatario, mensaje)
# - Método concreto enviar() que debe:
#   1. Imprimir: "Preparando envío a {destinatario}"
#   2. Llamar a self._formatear() (abstracto)
#   3. Llamar a self._transmitir(contenido) (abstracto) con el resultado de _formatear
#   4. Imprimir: "Envío completado"
# - Método abstracto _formatear() — devuelve un string con el mensaje formateado
# - Método abstracto _transmitir(contenido) — realiza la transmisión
#
# Subclases:
# - NotificacionEmail:
#   - _formatear: devuelve "[EMAIL] {mensaje}"
#   - _transmitir: imprime "Enviando por SMTP: {contenido}"
# - NotificacionSMS:
#   - _formatear: devuelve mensaje en mayúsculas
#   - _transmitir: imprime "Enviando SMS: {contenido}"
#
# RESULTADO ESPERADO:
# Preparando envío a ana@example.com
# Enviando por SMTP: [EMAIL] Bienvenida al sistema
# Envío completado
# Preparando envío a +34600123456
# Enviando SMS: ALERTA DE SEGURIDAD
# Envío completado
# =============================================================================

# Tu código aquí

# email = NotificacionEmail("ana@example.com", "Bienvenida al sistema")
# email.enviar()
#
# sms = NotificacionSMS("+34600123456", "alerta de seguridad")
# sms.enviar()
