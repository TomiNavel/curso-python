# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Closure vs Variable Local
# =============================================================================
# El siguiente código tiene 3 errores. Las funciones intentan usar closures
# para mantener estado, pero fallan. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Saldo: 900
# Saldo: 1400
# Historial: [100, 200, 300]
# Último: 300
# Mensaje: [URGENTE] Error en el servidor
# =============================================================================

# Error 1: el closure debería mantener un saldo que se modifica con cada operación
def crear_cuenta(saldo_inicial):
    saldo = saldo_inicial

    def operacion(cantidad):
        saldo += cantidad
        return saldo

    return operacion

cuenta = crear_cuenta(1000)
print(f"Saldo: {cuenta(-100)}")
print(f"Saldo: {cuenta(500)}")


# Error 2: el closure debería acumular valores en una lista
def crear_historial():
    registros = []

    def agregar(valor):
        registros = registros + [valor]
        return registros

    def ultimo():
        return registros[-1]

    return agregar, ultimo

agregar, ultimo = crear_historial()
agregar(100)
agregar(200)
print(f"Historial: {agregar(300)}")
print(f"Último: {ultimo()}")


# Error 3: el closure debería recordar el prefijo configurado
def crear_formateador(prefijo):
    def formatear(mensaje):
        return f"[{prefijo}] {mensaje}"

    prefijo = prefijo.upper()
    return formatear

fmt = crear_formateador("urgente")
print(f"Mensaje: {fmt('Error en el servidor')}")
