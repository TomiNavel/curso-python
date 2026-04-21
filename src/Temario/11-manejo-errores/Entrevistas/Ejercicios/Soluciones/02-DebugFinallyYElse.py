# =====================
# SOLUCIÓN
# =====================
# Error 1: el return está dentro del finally. Esto hace que SIEMPRE devuelva
#   resultado, incluso si hubo una excepción. En este caso parece funcionar,
#   pero si la excepción no fuera capturada, el return del finally la
#   silenciaría. El return debe estar fuera del finally.
#   Corrección: mover el return fuera del bloque try/except/else/finally.
#
# Error 2: (consecuencia del error 1) si se lanza una excepción NO capturada
#   (por ejemplo, un ValueError), el return del finally la silencia y el
#   caller nunca sabe que hubo un error.
#
# Error 3: (error trampa — el flujo de prints es correcto dado el orden
#   de evaluación). No hay un tercer error real.
#
# ERRORES CORREGIDOS:
# 1-2. Mover return resultado fuera del finally
# 3. (trampa — no hay error)


def procesar_datos(datos):
    resultado = None
    try:
        print("Procesando datos...")
        if not isinstance(datos, list):
            raise TypeError("el argumento no es una lista")
        resultado = datos
    except TypeError as e:
        print(f"Error: {e}")
    else:
        print(f"Datos válidos: {resultado}")
    finally:
        print("Proceso completado")

    return resultado


print(f"Resultado: {procesar_datos([1, 2, 3])}")
print("---")
print(f"Resultado: {procesar_datos('no soy lista')}")
