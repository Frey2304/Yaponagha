import random


class Caballo:
    def __init__(self, nombre, imagen, descripcion):
        self.nombre = nombre
        self.imagen = imagen
        self.descripcion = descripcion

        self.padre = "Padre Elite"
        self.madre = "Madre Campeona"
        self.criador = "Criador Yaponagha"
        self.contacto = "WhatsApp: +54 11 3512047142"
        self.nivel = round(random.uniform(7, 10), 2)


caballos = []