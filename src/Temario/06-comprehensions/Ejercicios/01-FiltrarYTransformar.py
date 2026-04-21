# =============================================================================
# EJERCICIO 1: Filtrar y transformar con list comprehensions
# =============================================================================
# Tienes datos de ventas de una tienda. Usa list comprehensions para procesar
# los datos según las instrucciones.
#
# DATOS:
ventas = [120, 45, 230, 89, 310, 15, 178, 92, 405, 67, 250, 33]
productos = ["camisa", "pantalon", "zapatos", "gorra", "chaqueta", "calcetines"]
descuentos = [0.1, 0.25, 0.05, 0.3, 0.15, 0.2]
#
# TAREAS:
# 1. Crea una lista con las ventas que superan 100 (ventas_altas)
# 2. Crea una lista con cada venta multiplicada por 1.21 (IVA incluido), redondeada a 2 decimales (ventas_con_iva)
# 3. Crea una lista etiquetando cada venta como "alta" si supera 150, "baja" en caso contrario (etiquetas)
# 4. Crea una lista con los productos en mayúsculas cuyo nombre tiene más de 5 letras (productos_largos)
# 5. Crea una lista con los precios finales: producto "zapatos" cuesta 80€, el resto 40€,
#    aplicando el descuento correspondiente a cada uno. Redondea a 2 decimales. (precios_finales)
#
# RESULTADO ESPERADO:
# Ventas altas: [120, 230, 310, 178, 405, 250]
# Ventas con IVA: [145.2, 54.45, 278.3, 107.69, 375.1, 18.15, 215.38, 111.32, 490.05, 81.07, 302.5, 39.93]
# Etiquetas: ['baja', 'baja', 'alta', 'baja', 'alta', 'baja', 'alta', 'baja', 'alta', 'baja', 'alta', 'baja']
# Productos largos: ['CAMISA', 'PANTALON', 'ZAPATOS', 'CHAQUETA', 'CALCETINES']
# Precios finales: [36.0, 30.0, 76.0, 28.0, 34.0, 32.0]
# =============================================================================

# Tu código aquí
