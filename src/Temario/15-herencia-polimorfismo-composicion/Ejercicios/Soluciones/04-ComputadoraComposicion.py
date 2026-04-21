class CPU:
    def __init__(self, marca, nucleos, ghz):
        self.marca = marca
        self.nucleos = nucleos
        self.ghz = ghz

    def __str__(self):
        return f"{self.marca} {self.nucleos} núcleos @ {self.ghz}GHz"


class RAM:
    def __init__(self, capacidad_gb, tipo):
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo

    def __str__(self):
        return f"{self.capacidad_gb}GB {self.tipo}"


class Disco:
    def __init__(self, capacidad_gb, tipo):
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo

    def __str__(self):
        return f"{self.capacidad_gb}GB {self.tipo}"


class Computadora:
    def __init__(self, nombre, cpu, ram, disco):
        self.nombre = nombre
        self.cpu = cpu
        self.ram = ram
        self.disco = disco

    def especificaciones(self):
        return (
            f"=== {self.nombre} ===\n"
            f"CPU: {self.cpu}\n"
            f"RAM: {self.ram}\n"
            f"Disco: {self.disco}"
        )

    def upgrade_ram(self, nueva_ram):
        self.ram = nueva_ram

    def upgrade_disco(self, nuevo_disco):
        self.disco = nuevo_disco

    def __str__(self):
        return self.nombre


pc = Computadora(
    "PC Gaming",
    CPU("AMD", 12, 4.2),
    RAM(16, "DDR5"),
    Disco(512, "SSD"),
)
print(pc.especificaciones())

pc.upgrade_ram(RAM(32, "DDR5"))
pc.upgrade_disco(Disco(1000, "SSD"))
print()
print("Después del upgrade:")
print(pc.especificaciones())
