# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Finally y Else
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Procesando datos...
# Datos válidos: [1, 2, 3]
# Proceso completado
# Resultado: [1, 2, 3]
# ---
# Procesando datos...
# Error: el argumento no es una lista
# Proceso completado
# Resultado: None
# =============================================================================

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
