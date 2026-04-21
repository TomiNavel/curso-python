while True:
    print("--- Menú ---")
    print("1. Saludar")
    print("2. Despedir")
    print("3. Salir")
    opcion = input("Opción: ")

    if opcion == "1":
        print("¡Hola!")
    elif opcion == "2":
        print("¡Hasta luego!")
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida")
        continue
