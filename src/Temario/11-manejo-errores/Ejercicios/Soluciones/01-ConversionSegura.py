def convertir_a_entero(valor, por_defecto=0):
    try:
        resultado = int(valor)
    except (ValueError, TypeError) as e:
        print(f"No se pudo convertir '{valor}': {e}")
        return por_defecto
    else:
        print(f"Convertido: {resultado}")
        return resultado


print(convertir_a_entero("42"))
print(convertir_a_entero("3.7"))
print(convertir_a_entero("abc"))
print(convertir_a_entero(None, -1))
