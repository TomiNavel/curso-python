# =====================
# SOLUCIÓN
# =====================
# Error 1: saldo += cantidad es una asignación, marca saldo como local.
#   Corrección: añadir "nonlocal saldo" al inicio de operacion().
#
# Error 2: registros = registros + [valor] es una reasignación, marca registros
#   como local. La solución más simple es usar .append() que muta la lista
#   sin reasignar la variable.
#   Corrección: cambiar "registros = registros + [valor]" por
#   "registros.append(valor)" y "return registros" después.
#
# Error 3: no es un error de scope sino de orden. El closure captura una
#   REFERENCIA a prefijo. La línea prefijo = prefijo.upper() se ejecuta
#   DESPUÉS de definir formatear(), pero ANTES de devolver la función.
#   Como el closure lee el valor en el momento de la llamada, sí ve "URGENTE".
#   Sin embargo, si el orden cambiara, dejaría de funcionar.
#   Para hacerlo robusto: mover prefijo = prefijo.upper() ANTES de definir
#   formatear().
#
# ERRORES CORREGIDOS:
# 1. Añadir "nonlocal saldo" en operacion()
# 2. Cambiar "registros = registros + [valor]" por "registros.append(valor)"
# 3. Mover "prefijo = prefijo.upper()" antes de la definición de formatear()


def crear_cuenta(saldo_inicial):
    saldo = saldo_inicial

    def operacion(cantidad):
        nonlocal saldo
        saldo += cantidad
        return saldo

    return operacion

cuenta = crear_cuenta(1000)
print(f"Saldo: {cuenta(-100)}")
print(f"Saldo: {cuenta(500)}")


def crear_historial():
    registros = []

    def agregar(valor):
        registros.append(valor)
        return registros

    def ultimo():
        return registros[-1]

    return agregar, ultimo

agregar, ultimo = crear_historial()
agregar(100)
agregar(200)
print(f"Historial: {agregar(300)}")
print(f"Último: {ultimo()}")


def crear_formateador(prefijo):
    prefijo = prefijo.upper()

    def formatear(mensaje):
        return f"[{prefijo}] {mensaje}"

    return formatear

fmt = crear_formateador("urgente")
print(f"Mensaje: {fmt('Error en el servidor')}")
