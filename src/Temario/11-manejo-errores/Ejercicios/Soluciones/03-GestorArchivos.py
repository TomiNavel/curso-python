def leer_archivo(ruta):
    contenido = None
    try:
        archivo = open(ruta)
        contenido = archivo.read()
        archivo.close()
    except FileNotFoundError:
        print(f"Error: el archivo '{ruta}' no existe")
    except PermissionError:
        print(f"Error: sin permisos para '{ruta}'")
    else:
        print(f"Leídos {len(contenido)} caracteres de '{ruta}'")
    finally:
        print("Operación de lectura finalizada")

    return contenido


resultado = leer_archivo("datos.txt")
print(f"Resultado: {resultado}")
resultado = leer_archivo("config.json")
print(f"Resultado: {resultado}")
