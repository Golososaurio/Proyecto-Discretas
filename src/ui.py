from tkinter import ttk
from tkinter import *
import tkinter as tk
from src.mapaInundacion import MapaInundacion
from src.productos import Productos

class UserInterface:

    def __init__(self, ventana):
        '''Inicialización de atributos'''
        self.ventana = ventana
        self.ventana.geometry("1600x900")
        self.ventana.resizable(width = False, height = False)
        self.ventana.title("PROYECTO: ARES")
        self.centra(self.ventana, 1600, 900)
        self.estilos()

        #Iniciación de Estados en la aplicación
        productos = Productos()
        self.productos = productos.cargarProductos()
        self.carrito = {}
        self.tienda = (24, 5)
        self.filas = 30
        self.columnas = 30
        self.mapa = self.crearMapa()
        self.entrega = None
        self.anim_idx = 0
        self.anim_camino_idx = 0
        self.anim_job = None

        #Construcción de las ventanas
        self.contenedor = ttk.Frame(self.ventana, style="Fondo.TFrame")
        self.contenedor.place(x=0, y=0, width=1600, height=900)

        self.pantallaPrincipal = ttk.Frame(self.contenedor, style="Fondo.TFrame")
        self.pantallaPrincipal.place(x=0, y=0, width=1600, height=900)
        self.pantallaMapa = ttk.Frame(self.contenedor, style="Fondo.TFrame")
        self.pantallaMapa.place(x=0, y=0, width=1600, height=900)

        self.iniciarPantallaPrincipal(self.pantallaPrincipal)
        self.iniciarPantallaMapa(self.pantallaMapa)

        self.mostrarPantallaPrincipal()

    def estilos(self):
        '''Sirve para inicializar los estilos del texto'''
        estilo = ttk.Style(self.ventana)
        estilo.theme_use("clam")

        #Fondos
        estilo.configure("Fondo.TFrame", background = "#EEF0F5")
        estilo.configure("Tarjeta.TFrame", background="#FFFFFF")

        #Textos
        estilo.configure("Fondo.TLabel", background="#EEF0F5", foreground="#19191C", font=("Space Grotesk", 11))
        estilo.configure("Titulo.TLabel", background="#EEF0F5", foreground="#19191C", font=("Space Grotesk", 24, "bold"))
        estilo.configure("Subtitulo.TLabel", background="#EEF0F5", foreground="#64666C", font=("Space Grotesk", 11))
        estilo.configure("Tarjeta.TLabel", background="#FFFFFF", foreground="#19191C", font=("Space Grotesk", 11))
        estilo.configure("TarjetaNombre.TLabel", background="#FFFFFF", foreground="#19191C", font=("Space Grotesk", 13, "bold"))
        estilo.configure("TarjetaPrecio.TLabel", background="#FFFFFF", foreground="#64666C", font=("Space Grotesk", 10))
        estilo.configure("TarjetaCantidad.TLabel", background="#FFFFFF", foreground="#19191C", font=("Space Grotesk", 13, "bold"))
        estilo.configure("TotalGrande.TLabel", background="#FFFFFF", foreground="#19191C", font=("Space Grotesk", 15, "bold"))

        #Botones
        estilo.configure("Aceptar.TButton", background="#3478F6", foreground="white", font=("Space Grotesk", 11, "bold"), borderwidth=0, focusthickness=0, padding=8)
        estilo.map("Aceptar.TButton", background=[("disabled", "#AEB0B8"), ("active", "#2054BE")], foreground=[("disabled", "#F0F0F0")])
        estilo.configure("Añadir.TButton", background="#2EC46A", foreground="white", font=("Space Grotesk", 11, "bold"), borderwidth=0, focusthickness=0, padding=8)
        estilo.map("Añadir.TButton", background=[("disabled", "#AEB0B8"), ("active", "#1C9650")], foreground=[("disabled", "#F0F0F0")])
        estilo.configure("Quitar.TButton", background="#E6394A", foreground="white", font=("Space Grotesk", 11, "bold"), borderwidth=0, focusthickness=0, padding=8)
        estilo.map("Quitar.TButton", background=[("disabled", "#AEB0B8"), ("active", "#B42832")], foreground=[("disabled", "#F0F0F0")])
        
    def iniciarPantallaPrincipal(self, ventana):
        '''Método que inicia el menú de inicio'''
        ttk.Label(ventana, text="Mani Manitas S.A.", style="Titulo.TLabel").place(x=40, y=28)
        ttk.Label(ventana, text="Arma tu pedido y confirma para elegir el punto de entrega en el mapa", style="Subtitulo.TLabel").place(x=40, y=70)

        #Panel de Productos

        self.cantidadLabels = {}
        y = 120
        for prod in self.productos:
            tarjeta = tk.Frame(ventana, bg="#FFFFFF", highlightthickness=0)
            tarjeta.place(x=40, y=y, width=680, height=70)

            ttk.Label(tarjeta, text=prod["Nombre"], style="TarjetaNombre.TLabel").place(x=20, y=10)
            ttk.Label(tarjeta, text=self.formatoPrecio(prod["Precio"]), style="TarjetaPrecio.TLabel").place(x=20, y=38)

            botonQuitar = ttk.Button(tarjeta, text="-", style="Quitar.TButton", width=2, command=lambda n=prod["Nombre"]: self.actualizarCantidad(n, -1))
            botonQuitar.place(x=520, y=15, width=36, height=36)

            labelCantidad = tk.Label(tarjeta, text="0", bg="#FFFFFF", fg="#19191C", font=("Space Grotesk", 13, "bold"))
            labelCantidad.place(x=568, y=15, width=40, height=36)
            self.cantidadLabels[prod["Nombre"]] = labelCantidad

            botonAñadir = ttk.Button(tarjeta, text="+", style="Añadir.TButton", width=2, command=lambda n=prod["Nombre"]: self.actualizarCantidad(n, +1))
            botonAñadir.place(x=618, y=15, width=36, height=36)

            y += 86

        #Panel de Pedidos

        panel = tk.Frame(ventana, bg="#FFFFFF")
        panel.place(x=780, y=120, width=460, height=500)

        ttk.Label(panel, text="Resumen del pedido", style="TarjetaNombre.TLabel").place(x=20, y=16)

        self.resumen = tk.Text(panel, bg="#FFFFFF", fg="#19191C", bd=0, font=("Space Grotesk", 11), highlightthickness=0, wrap="word", state="disabled")
        self.resumen.place(x=20, y=60, width=420, height=340)

        self.totalPrecio = ttk.Label(panel, text="Total: $ 0", style="TotalGrande.TLabel")
        self.totalPrecio.place(x=20, y=415)

        self.botonAceptar = ttk.Button(ventana, text="Confirmar pedido y elegir lugar de entrega", style="Aceptar.TButton", state="disabled", command=self.confirmarPedido)
        self.botonAceptar.place(x=780, y=640, width=460, height=50)

        self.actualizarTotal()
        
    def actualizarCantidad(self, nombre, delta):
        '''Actualiza la cantidad de productos en lista'''
        nueva = max(0, self.carrito.get(nombre, 0) + delta)
        self.carrito[nombre] = nueva
        self.cantidadLabels[nombre].config(text=str(nueva))
        self.actualizarTotal()

    def actualizarTotal(self):
        '''Actualiza el total de dinero'''
        self.resumen.config(state="normal")
        self.resumen.delete("1.0", "end")
        items = 0
        for prod in self.productos:
            cant = self.carrito.get(prod["Nombre"], 0)
            if cant > 0:
                items += cant
                subtotal = cant * prod["Precio"]
                linea = f"{cant} x {prod['Nombre']:<22} {self.formatoPrecio(subtotal):>12}\n"
                self.resumen.insert("end", linea)
        if items == 0:
            self.resumen.insert("end", "Tu carrito esta vacio")
        self.resumen.config(state="disabled")

        total = self.totalCarrito(self.carrito)
        self.totalPrecio.config(text="Total: " + self.formatoPrecio(total))
        self.botonAceptar.config(state=("normal" if items > 0 else "disabled"))

    def confirmarPedido(self):
        '''Confirma el pedido y envia al mapa'''
        if self.totalCarrito(self.carrito) <= 0:
            return
        self.mostrarMapa()

    def totalCarrito(self, carrito):
        '''Suma el total de productos'''
        return sum(carrito.get(prod["Nombre"], 0) * prod["Precio"] for prod in self.productos)

    def iniciarPantallaMapa(self, ventana):
        '''Inicia la pantalla del mapa'''
        self.tituloMapa = ttk.Label(ventana, text="Elige el punto de entrega", style="Titulo.TLabel")
        self.tituloMapa.place(x=40, y=28)
        self.subtituloMapa = ttk.Label(ventana, text="Haz click en un cuadrado libre del mapa", style="Subtitulo.TLabel")
        self.subtituloMapa.place(x=40, y=72)

        anchoCanvas = 30 * 27
        altoCanvas = 30 * 27
        self.xCanvas, self.yCanvas = 40, 110

        self.canvas = tk.Canvas(ventana, width=anchoCanvas, height=altoCanvas, bg="#FFFFFF", highlightthickness=0)
        self.canvas.place(x=self.xCanvas, y=self.yCanvas)
        self.canvas.bind("<Button-1>", self.clickMapa)

        #Panel de Leyenda
        px = self.xCanvas + anchoCanvas + 40
        panel = tk.Frame(ventana, bg="#FFFFFF")
        panel.place(x=px, y=self.yCanvas, width=460, height=500)
        self.panel_ancho = 460

        ttk.Label(panel, text="Leyenda", style="TarjetaNombre.TLabel").place(x=20, y=16)
        leyenda = [
            ("#2EC46A", "Ferreteria (inicio)"),
            ("#FF9500", "Punto de entrega"),
            ("#96C8FF", "Ola de exploracion"),
            ("#E6394A", "Ruta calculada"),
            ("#232328", "Construcción / Edificio"),
        ]
        ly = 56
        for color, texto in leyenda:
            tk.Label(panel, bg=color, width=2, height=1).place(x=20, y=ly, width=22, height=22)
            ttk.Label(panel, text=texto, style="Tarjeta.TLabel").place(x=54, y=ly)
            ly += 32

        #Paneles de información
        ttk.Separator(panel, orient="horizontal").place(x=20, y=ly + 8, width=420)
        ly += 24
        ttk.Label(panel, text="Tu pedido", style="TarjetaNombre.TLabel").place(x=20, y=ly)
        ly += 34
        self.pedidoMapa = tk.Text(panel, bg="#FFFFFF", fg="#64666C", bd=0, font=("Space Grotesk", 10), highlightthickness=0, wrap="word", state="disabled", height=6)
        self.pedidoMapa.place(x=20, y=ly, width=420, height=110)
        ly += 120

        self.totalMapa = ttk.Label(panel, text="Total: $ 0", style="TarjetaNombre.TLabel")
        self.totalMapa.place(x=20, y=ly)
        ly += 34

        ttk.Separator(panel, orient="horizontal").place(x=20, y=ly, width=420)
        ly += 16
        self.distancia = ttk.Label(panel, text="", style="Tarjeta.TLabel")
        self.distancia.place(x=20, y=ly)
        ly += 26
        self.tiempo = ttk.Label(panel, text="", style="Tarjeta.TLabel")
        self.tiempo.place(x=20, y=ly)

        self.botonNuevoPedido = ttk.Button(ventana, text="Nuevo pedido", style="Accent.TButton", command=self.nuevoPedido)
        self.botonNuevoPedido.place(x=px + (self.panel_ancho - 260) // 2, y=630, width=260, height=50)
        self.botonNuevoPedido.place_forget()

    def celdaDesdePixel(self, x, y):
        '''Ayuda con la selección de la celda desde el pixel que se oprime'''
        col = x // 27
        fila = y // 27
        if 0 <= fila < 30 and 0 <= col < 30:
            return (int(fila), int(col))
        return None

    def obstaculo(self, celda):
        '''Ayuda con la creación de los obstaculos en la cuadricula'''
        f, c = celda
        x0, y0 = c * 27, f * 27
        return x0, y0, x0 + 27, y0 + 27

    def centroCelda(self, celda):
        '''Ayuda con el centro de la celda para los puntos de tienda y entrega'''
        f, c = celda
        return c * 27 + 27 / 2, f * 27 + 27 / 2

    def cuadricula(self):
        '''Construye la cuadricula'''
        self.canvas.delete("all")
        for f in range(30):
            for c in range(30):
                x0, y0, x1, y1 = self.obstaculo((f, c))
                color = "#232328" if self.mapa.grid[f][c] == 1 else "#FFFFFF"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#DCDCE1")

        tx, ty = self.centroCelda(self.tienda)
        self.canvas.create_oval(tx - 9, ty - 9, tx + 9, ty + 9, fill="#2EC46A", outline="#19191C", width=2)
        self.canvas.create_text(tx, ty - 18, text="Ferreteria", fill="#1C9650", font=("Space Grotesk", 9, "bold"))

    def actualizarPedidoMapa(self):
        '''Actualiza los pedidos y el total en la información del mapa'''
        self.pedidoMapa.config(state="normal")
        self.pedidoMapa.delete("1.0", "end")
        for prod in self.productos:
            cant = self.carrito.get(prod["Nombre"], 0)
            if cant > 0:
                self.pedidoMapa.insert("end", f"{cant} x {prod['Nombre']}\n")
        self.pedidoMapa.config(state="disabled")
        self.totalMapa.config(text="Total: " + self.formatoPrecio(self.totalCarrito(self.carrito)))

    def clickMapa(self, event):
        '''Espera el click en el mapa para empezar con la simulación'''
        if self.entrega is not None:
            return

        celda = self.celdaDesdePixel(event.x, event.y)
        if celda is None or celda == self.tienda or self.mapa.grid[celda[0]][celda[1]] == 1:
            return

        self.entrega = celda
        self.mapa.inundar(self.tienda, self.entrega)

        fx, fy = self.centroCelda(self.entrega)
        self.canvas.create_oval(fx - 9, fy - 9, fx + 9, fy + 9, fill="#FF9500", outline="#19191C", width=2)
        self.canvas.create_text(fx, fy - 18, text="Entrega", fill="#B46400", font=("Space Grotesk", 9, "bold"))

        self.tituloMapa.config(text="Calculando la ruta...")
        self.subtituloMapa.config(text="Simulando la exploracion del mapa (metodo de inundacion)")

        self.anim_idx = 0
        self.anim_camino_idx = 0
        self.animacionInundacion()

    def animacionInundacion(self):
        '''Realiza la animación de ola en la cuadricula'''
        # revelar varias celdas de la onda por frame
        lote = self.mapa.ordenVisita[self.anim_idx: self.anim_idx + 4]
        for celda in lote:
            if celda == self.tienda or celda == self.entrega:
                continue
            x0, y0, x1, y1 = self.obstaculo(celda)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#96C8FF", outline="#DCDCE1")
        self.anim_idx += len(lote)

        if self.anim_idx < len(self.mapa.ordenVisita):
            self.anim_job = self.ventana.after(20, self.animacionInundacion)
            return

        # luego, revelar el camino final paso a paso
        if self.anim_camino_idx < len(self.mapa.camino) - 1:
            a = self.mapa.camino[self.anim_camino_idx]
            b = self.mapa.camino[self.anim_camino_idx + 1]
            xa, ya = self.centroCelda(a)
            xb, yb = self.centroCelda(b)
            self.canvas.create_line(xa, ya, xb, yb, fill="#E6394A", width=5, capstyle="round", joinstyle="round")
            self.anim_camino_idx += 1
            self.anim_job = self.ventana.after(35, self.animacionInundacion)
            return

        self.anim_job = None
        self.resultadoAnimacion()

    def resultadoAnimacion(self):
        '''Luego de terminar la animación se llama a esta función para
        que se actualice la información de tiempo y distancia'''
        self.tituloMapa.config(text="Pedido en camino")
        self.subtituloMapa.config(text="Esta es la ruta mas corta calculada para tu domicilio")

        distancia = len(self.mapa.camino) - 1
        tiempoEstimado = max(5, distancia * 0.75)
        self.distancia.config(text=f"Distancia: {distancia} cuadras")
        self.tiempo.config(text=f"Tiempo estimado: {tiempoEstimado} min")

        px = self.xCanvas + self.columnas * 27 + 40
        self.botonNuevoPedido.place(x=px + (self.panel_ancho - 260) // 2, y=630, width=260, height=50)

    def nuevoPedido(self):
        '''Devuelve a la pantalla principal dejándola en default'''
        self.carrito = {}
        for nombre, lbl in self.cantidadLabels.items():
            lbl.config(text="0")
        self.actualizarTotal()
        self.mostrarPantallaPrincipal()

    def formatoPrecio(self, valor):
        '''Pone en formato los precios traídos del .json'''
        return "$ " + f"{valor:,.0f}".replace(",", ".")

    def centra(self, ventana, ancho, alto): 
        '''centra las ventanas en la pantalla'''
        x = ventana.winfo_screenwidth() // 2 - ancho // 2 
        y = ventana.winfo_screenheight() // 2 - alto // 2 
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        return ventana

    def mostrarPantallaPrincipal(self):
        '''Muestra la Pantalla Principal'''
        self.pantallaPrincipal.tkraise()
    
    def mostrarMapa(self):
        '''Restablece el mapa a default y muestra la pantalla de Mapa'''
        self.entrega = None
        self.anim_idx = 0
        self.anim_camino_idx = 0
        if self.anim_job is not None:
            self.ventana.after_cancel(self.anim_job)
            self.anim_job = None

        self.tituloMapa.config(text="Elige el punto de entrega")
        self.subtituloMapa.config(text="Haz click en una celda libre del mapa")
        self.distancia.config(text="")
        self.tiempo.config(text="")
        self.botonNuevoPedido.place_forget()

        self.cuadricula()
        self.actualizarPedidoMapa()
        self.pantallaMapa.tkraise()

    def crearMapa(self):
        '''Crea el mapa lógico que analiza el computador con los obstaculos
        que se quieran'''
        mapa = MapaInundacion(30, 30)
        #Bordes
        mapa.crearObstaculoGrande(0, 0, 0, 29)
        mapa.crearObstaculoGrande(1, 0, 29, 0)
        mapa.crearObstaculoGrande(1, 29, 29, 29)
        mapa.crearObstaculoGrande(29, 1, 29, 28)
    
        #Casas / Construcciones
        mapa.crearObstaculoGrande(2, 2, 5, 3)
        mapa.crearObstaculoGrande(7, 2, 9, 3)
        mapa.crearObstaculoGrande(11, 2, 13, 3)
        mapa.crearObstaculoGrande(2, 5, 5, 6)
        mapa.crearObstaculoGrande(7, 5, 9, 6)
        mapa.crearObstaculoGrande(11, 5, 13, 6)
        mapa.crearObstaculoGrande(15, 2, 16, 6)
        mapa.crearObstaculoGrande(18, 2, 21, 3)
        mapa.crearObstaculoGrande(18, 5, 21, 6)
        mapa.crearObstaculoGrande(23, 2, 27, 3)
        mapa.crearObstaculoGrande(26, 4, 27, 6)
    
        mapa.crearObstaculoGrande(2, 8, 3, 12)
        mapa.crearObstaculoGrande(4, 9, 5, 11)
        mapa.crearObstaculoGrande(7, 8, 9, 12)
        mapa.crearObstaculoGrande(11, 8, 12, 12)
        mapa.crearObstaculoGrande(13, 8, 14, 9)
        mapa.crearObstaculo(14,12)
        mapa.crearObstaculoGrande(15, 11, 15, 12)
        mapa.crearObstaculoGrande(16, 10, 16, 11)
        mapa.crearObstaculoGrande(17, 9, 17, 10)
        mapa.crearObstaculoGrande(18, 8, 18, 9)
        mapa.crearObstaculo(18,12)
        mapa.crearObstaculoGrande(20, 8, 21, 12)
        mapa.crearObstaculoGrande(23, 8, 24, 12)
        mapa.crearObstaculoGrande(26, 8, 27, 12)
    
        mapa.crearObstaculoGrande(2, 14, 5, 15)
        mapa.crearObstaculoGrande(2, 17, 3, 20)
        mapa.crearObstaculoGrande(5, 17, 5, 20)
        mapa.crearObstaculoGrande(2, 22, 5, 22)
        mapa.crearObstaculoGrande(2, 24, 5, 24)
        mapa.crearObstaculoGrande(5, 25, 5, 27)
        mapa.crearObstaculo(1,28)
        mapa.crearObstaculoGrande(2, 26, 2, 27)
        mapa.crearObstaculo(3,27)
    
        mapa.crearObstaculoGrande(7, 14, 7, 15)
        mapa.crearObstaculoGrande(9, 14, 11, 15)
        mapa.crearObstaculoGrande(13, 14, 13, 15)
        mapa.crearObstaculoGrande(8, 16, 12, 17)
        mapa.crearObstaculoGrande(7, 18, 13, 19)
        mapa.crearObstaculoGrande(8, 20, 12, 21)
        mapa.crearObstaculoGrande(7, 22, 7, 23)
        mapa.crearObstaculoGrande(9, 22, 11, 23)
        mapa.crearObstaculoGrande(13, 22, 13, 23)
        mapa.crearObstaculoGrande(7, 25, 13, 25)
        mapa.crearObstaculoGrande(7, 27, 13, 27)
    
        mapa.crearObstaculoGrande(15, 14, 16, 23)
        mapa.crearObstaculoGrande(15, 25, 16, 27)
        mapa.crearObstaculoGrande(17, 26, 19, 27)
        mapa.crearObstaculoGrande(18, 14, 19, 15)
        mapa.crearObstaculoGrande(18, 17, 19, 18)
        mapa.crearObstaculoGrande(18, 20, 19, 21)
        mapa.crearObstaculoGrande(18, 23, 19, 24)
    
        mapa.crearObstaculoGrande(21, 14, 22, 18)
        mapa.crearObstaculoGrande(23, 17, 27, 18)
        mapa.crearObstaculoGrande(24, 14, 27, 15)
        mapa.crearObstaculoGrande(21, 20, 23, 21)
        mapa.crearObstaculoGrande(25, 20, 27, 21)
        mapa.crearObstaculoGrande(21, 23, 22, 25)
        mapa.crearObstaculoGrande(24, 23, 25, 25)
        mapa.crearObstaculoGrande(27, 23, 27, 27)
        mapa.crearObstaculoGrande(21, 27, 25, 27)
        return mapa