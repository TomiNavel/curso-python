# =====================
# SOLUCIÓN
# =====================
# Error 1: dividir_seguro usa bare except (except sin tipo). Esto captura
#   todo, incluyendo KeyboardInterrupt. Debe capturar ZeroDivisionError.
#   Corrección: except ZeroDivisionError as e
#
# Error 2: dividir_seguro imprime un mensaje genérico "Algo salió mal" en
#   lugar del mensaje de la excepción. No permite saber qué falló.
#   Corrección: usar "as e" y mostrar el mensaje del error.
#
# Error 3: convertir_y_dividir captura Exception genérica. Debería capturar
#   ValueError específicamente para el caso de int() fallido. Además, el
#   mensaje de error no indica qué texto falló.
#   Corrección: except ValueError y mensaje descriptivo con el texto original.
#
# ERRORES CORREGIDOS:
# 1. Cambiar bare except por except ZeroDivisionError as e
# 2. Imprimir f"Error: {e}" en dividir_seguro
# 3. Cambiar except Exception por except ValueError con mensaje descriptivo


def dividir_seguro(a, b):
    try:
        resultado = a / b
        return resultado
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None

def convertir_y_dividir(texto, divisor):
    try:
        numero = int(texto)
        resultado = dividir_seguro(numero, divisor)
        print(f"Resultado: {resultado}")
    except ValueError:
        print(f"Error: No se pudo convertir '{texto}' a número")


convertir_y_dividir("10", 2)
convertir_y_dividir("10", 0)
convertir_y_dividir("abc", 1)
