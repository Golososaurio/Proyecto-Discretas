import json
import os

class Productos:
    def existenciaArchivo(self):
        archivo = 'Proyecto Discretas\\data\\productos.json' 
        
        if os.path.exists(archivo):
            with open(archivo, 'r') as file:
                self.data = json.load(file)
        else:
            productos = {
            "Nombre": "Caja Tornillos 3mm",
            "Precio": "5000"
            }

            self.data = {"Productos": [productos]}

            with open(archivo, 'w') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)

    def cargarProductos(self):
        self.existenciaArchivo()
        try:
            with open('Proyecto Discretas\\data\\productos.json', 'r') as file:  #Carga pedidos.json
                self.productos = json.load(file)
                productos = self.productos["Productos"]
                return productos
        except:
            return "0"