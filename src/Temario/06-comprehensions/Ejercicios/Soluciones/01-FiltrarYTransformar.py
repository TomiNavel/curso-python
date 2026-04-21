ventas = [120, 45, 230, 89, 310, 15, 178, 92, 405, 67, 250, 33]
productos = ["camisa", "pantalon", "zapatos", "gorra", "chaqueta", "calcetines"]
descuentos = [0.1, 0.25, 0.05, 0.3, 0.15, 0.2]

# 1. Ventas que superan 100
ventas_altas = [v for v in ventas if v > 100]
print("Ventas altas:", ventas_altas)

# 2. Ventas con IVA (21%) redondeadas a 2 decimales
ventas_con_iva = [round(v * 1.21, 2) for v in ventas]
print("Ventas con IVA:", ventas_con_iva)

# 3. Etiquetar cada venta
etiquetas = ["alta" if v > 150 else "baja" for v in ventas]
print("Etiquetas:", etiquetas)

# 4. Productos en mayúsculas con más de 5 letras
productos_largos = [p.upper() for p in productos if len(p) > 5]
print("Productos largos:", productos_largos)

# 5. Precio base: zapatos=80€, resto=40€; aplicar descuento correspondiente
precios_finales = [
    round((80 if p == "zapatos" else 40) * (1 - d), 2)
    for p, d in zip(productos, descuentos)
]
print("Precios finales:", precios_finales)
