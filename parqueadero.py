import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime
import os
from typing import Dict, List, Optional
import math
import threading
import time

class Vehiculo:
    def __init__(self, tipo_vehiculo: str, color: str, placa: str, tiene_seguro: bool):
        self.id = f"v-{datetime.now().timestamp()}"
        self.tipo = tipo_vehiculo
        self.color = color
        self.placa = placa
        self.hora_entrada = datetime.now()
        self.tiene_seguro = tiene_seguro
        self.id_espacio_estacionamiento: Optional[int] = None
        self.id_casillero: Optional[int] = None
        # Posición del vehículo en el mapa
        self.x = 50  # Posición inicial X para conducir
        self.y = 475 # Posición inicial Y en la carretera principal
        self.angulo = 0 # Ángulo inicial (hacia la derecha)
        self.velocidad = 0
        self.max_velocidad = 3

class EspacioEstacionamiento:
    def __init__(self, id_espacio: int, tipo_espacio: str, x: int, y: int):
        self.id = id_espacio
        self.tipo = tipo_espacio # "regular" o "motocicleta"
        self.esta_ocupado = False
        self.id_vehiculo: Optional[str] = None
        self.x = x
        self.y = y

class SimuladorEstacionamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Estacionamiento Premium")
        self.root.geometry("1400x900")
        
        self.colores = {
            'fondo': '#1a1a2e',
            'secundario': '#16213e',
            'acento': '#e94560',
            'oro': '#f39c12',
            'verde': '#27ae60',
            'azul': '#3498db',
            'purpura': '#9b59b6',
            'carretera': '#34495e',
            'linea_carretera': '#ecf0f1',
            'cesped': '#2d5016', 
            'texto': '#ecf0f1'
        }
        
        self.root.configure(bg=self.colores['fondo'])

        self.modo_conduccion = False
        self.vehiculo_actual: Optional[Vehiculo] = None
        
        self.teclas_presionadas = set()

        self.vehiculos: Dict[str, Vehiculo] = {}
        self.espacios_estacionamiento: List[EspacioEstacionamiento] = []
        self.casilleros = [{"id": i, "ocupado": False} for i in range(15)] 
        self.historial_salidas: List[Dict] = []
        
        # Tarifas por minuto (COP)
        self.tarifas_minuto = { 
            "carro": 110, 
            "deportivo": 180, 
            "motocicleta": 85 
        }

        self.crear_espacios_estacionamiento() 
        self.cargar_imagenes_vehiculos()
        self.crear_diseño() # Aquí se llamará a crear_panel_tarifas
        self.iniciar_reloj()
        self.configurar_controles()
        self.actualizar_juego() 

    def crear_espacios_estacionamiento(self):
        self.espacios_estacionamiento.clear() 
        
        centro_x_canvas = 500 
        
        espacios_por_fila_bloque = 6
        filas_por_bloque = 3
        espacio_width = 80
        # espacio_height = 60 # No se usa aquí directamente
        separacion_x = 90
        separacion_y = 70
        
        inicio_y_bloque1 = 50 
        total_width_bloque = (espacios_por_fila_bloque - 1) * separacion_x + espacio_width
        inicio_x_bloques = centro_x_canvas - total_width_bloque // 2

        id_actual = 0
        for fila in range(filas_por_bloque):
            for columna in range(espacios_por_fila_bloque):
                x = inicio_x_bloques + columna * separacion_x
                y = inicio_y_bloque1 + fila * separacion_y
                self.espacios_estacionamiento.append(
                    EspacioEstacionamiento(id_actual, "regular", x, y)
                )
                id_actual += 1
        
        inicio_y_bloque2 = inicio_y_bloque1 + filas_por_bloque * separacion_y + 120 

        for fila in range(filas_por_bloque):
            for columna in range(espacios_por_fila_bloque):
                x = inicio_x_bloques + columna * separacion_x
                y = inicio_y_bloque2 + fila * separacion_y
                self.espacios_estacionamiento.append(
                    EspacioEstacionamiento(id_actual, "regular", x, y)
                )
                id_actual += 1
        
        motos_por_fila = 10
        moto_width = 50
        moto_separacion_x = 60
        
        motos_y_pos = self.canvas.winfo_height() - 80 if hasattr(self, 'canvas') and self.canvas.winfo_exists() else 620
        
        total_width_motos = (motos_por_fila - 1) * moto_separacion_x + moto_width
        motos_inicio_x = centro_x_canvas - total_width_motos // 2
        
        for i in range(motos_por_fila):
            x = motos_inicio_x + i * moto_separacion_x
            self.espacios_estacionamiento.append(
                EspacioEstacionamiento(id_actual, "motocicleta", x, motos_y_pos)
            )
            id_actual += 1
        
        print(f"Creados {len(self.espacios_estacionamiento)} espacios de estacionamiento.")


    def cargar_imagenes_vehiculos(self):
        self.imagenes_vehiculos = {}
        directorio_imagenes = "images" 
        
        if not os.path.exists(directorio_imagenes):
            print(f"Advertencia: No se encontró el directorio '{directorio_imagenes}'. Creando imágenes por defecto.")
            self.crear_imagenes_por_defecto()
            return
        
        colores_img = ['rojo', 'azul', 'verde', 'negro', 'blanco', 'amarillo', 'gris']
        tipos_vehiculos_img = ['carro', 'deportivo']
        
        for tipo in tipos_vehiculos_img:
            for color in colores_img:
                ruta_imagen = os.path.join(directorio_imagenes, f"{tipo}_{color}.png")
                if os.path.exists(ruta_imagen):
                    try:
                        img = Image.open(ruta_imagen)
                        img = img.resize((60, 35), Image.Resampling.LANCZOS) 
                        self.imagenes_vehiculos[f"{tipo}_{color}"] = ImageTk.PhotoImage(img)
                    except Exception as e:
                        print(f"Error cargando imagen {ruta_imagen}: {e}")
                else:
                     print(f"Imagen no encontrada, se usará color por defecto: {ruta_imagen}")


        ruta_moto = os.path.join(directorio_imagenes, "moto.png")
        if os.path.exists(ruta_moto):
            try:
                img = Image.open(ruta_moto)
                img = img.resize((40, 25), Image.Resampling.LANCZOS) 
                self.imagenes_vehiculos["motocicleta"] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando imagen de motocicleta: {e}")
        else:
            print(f"Imagen de motocicleta no encontrada ({ruta_moto}), se usará color por defecto.")
            
        if not self.imagenes_vehiculos: 
            self.crear_imagenes_por_defecto()

    def crear_imagenes_por_defecto(self):
        colores_rgb_defecto = {
            'rojo': self.colores['acento'], 'azul': self.colores['azul'], 
            'verde': self.colores['verde'], 'negro': '#2c3e50',
            'blanco': '#ecf0f1', 'amarillo': '#f1c40f', 'gris': '#95a5a6'
        }
        tipos_vehiculos_defecto = ['carro', 'deportivo']
        
        for tipo in tipos_vehiculos_defecto:
            for color_nombre, color_hex in colores_rgb_defecto.items():
                if f"{tipo}_{color_nombre}" not in self.imagenes_vehiculos: 
                    img = Image.new('RGB', (60, 35), color_hex)
                    self.imagenes_vehiculos[f"{tipo}_{color_nombre}"] = ImageTk.PhotoImage(img)
        
        if "motocicleta" not in self.imagenes_vehiculos: 
            img_moto = Image.new('RGB', (40, 25), self.colores['oro'])
            self.imagenes_vehiculos["motocicleta"] = ImageTk.PhotoImage(img_moto)
        print("Imágenes por defecto creadas/asignadas.")

    def crear_diseño(self):
        self.marco_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        self.marco_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.marco_control = tk.Frame(self.root, bg=self.colores['secundario'], width=300)
        self.marco_control.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.marco_control.pack_propagate(False)

        self.canvas = tk.Canvas(
            self.marco_principal,
            width=1000,
            height=700,
            bg=self.colores['cesped'],
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.crear_panel_info()
        self.crear_panel_control()
        self.crear_panel_tarifas() # Añadido aquí

    def crear_panel_info(self):
        info_frame = tk.Frame(self.marco_control, bg=self.colores['secundario'])
        info_frame.pack(fill=tk.X, pady=(10,0), padx=10) # Reducir pady inferior
        
        self.label_reloj = tk.Label(
            info_frame, text="00:00:00", font=('Arial', 18, 'bold'),
            bg=self.colores['secundario'], fg=self.colores['oro']
        )
        self.label_reloj.pack(pady=(0,5)) # Reducir pady inferior
        
        self.label_estado = tk.Label(
            info_frame, text="Modo: Vista General", font=('Arial', 12),
            bg=self.colores['secundario'], fg=self.colores['texto']
        )
        self.label_estado.pack(pady=3) # Reducir pady
        
        controles_frame = tk.LabelFrame(info_frame, text="CONTROLES", 
                                        font=('Arial', 10, 'bold'), 
                                        bg=self.colores['secundario'], 
                                        fg=self.colores['acento'], labelanchor="n", bd=2)
        controles_frame.pack(pady=(5,10), fill=tk.X) # Ajustar pady
        
        tk.Label(
            controles_frame,
            text="W/S: Acelerar/Frenar\nA/D: Girar\nESPACIO: Estacionar",
            font=('Arial', 9), bg=self.colores['secundario'], fg=self.colores['texto'], justify=tk.LEFT
        ).pack(padx=5, pady=5)

    def crear_panel_control(self):
        # Botones principales
        tk.Button(
            self.marco_control, text="🚗 Nuevo Vehículo", command=self.mostrar_dialogo_entrada,
            bg=self.colores['verde'], fg='white', font=('Arial', 12, 'bold'), height=2
        ).pack(fill=tk.X, pady=3, padx=10) # Reducir pady

        tk.Button(
            self.marco_control, text="🚪 Salida de Vehículo", command=self.mostrar_dialogo_salida,
            bg=self.colores['acento'], fg='white', font=('Arial', 12, 'bold'), height=2
        ).pack(fill=tk.X, pady=3, padx=10) # Reducir pady

        tk.Button(
            self.marco_control, text="📊 Historial", command=self.mostrar_historial,
            bg=self.colores['azul'], fg='white', font=('Arial', 12, 'bold'), height=2
        ).pack(fill=tk.X, pady=3, padx=10) # Reducir pady
        
        # Estadísticas
        stats_frame = tk.LabelFrame(self.marco_control, text="ESTADÍSTICAS",
                                   font=('Arial', 10, 'bold'),
                                   bg=self.colores['secundario'], fg=self.colores['oro'], labelanchor="n", bd=2)
        stats_frame.pack(fill=tk.X, pady=(10,5), padx=10) # Ajustar pady
        
        self.label_ocupados = tk.Label(
            stats_frame, text="Ocupados: 0/0", font=('Arial', 10),
            bg=self.colores['secundario'], fg=self.colores['texto']
        )
        self.label_ocupados.pack(pady=2)
        
        self.label_ingresos = tk.Label(
            stats_frame, text="Ingresos: $0 COP", font=('Arial', 10),
            bg=self.colores['secundario'], fg=self.colores['verde']
        )
        self.label_ingresos.pack(pady=2)
    
    def crear_panel_tarifas(self):
        tarifas_frame = tk.LabelFrame(self.marco_control, text="TARIFAS (COP)",
                                   font=('Arial', 10, 'bold'),
                                   bg=self.colores['secundario'], fg=self.colores['oro'], labelanchor="n", bd=2)
        tarifas_frame.pack(fill=tk.X, pady=5, padx=10)

        for tipo, tarifa_minuto in self.tarifas_minuto.items():
            tarifa_hora = tarifa_minuto * 60
            texto_tarifa = f"{tipo.title()}: ${tarifa_minuto:,}/min - ${tarifa_hora:,}/hora"
            tk.Label(
                tarifas_frame, text=texto_tarifa, font=('Arial', 9),
                bg=self.colores['secundario'], fg=self.colores['texto'], anchor="w"
            ).pack(fill=tk.X, padx=5)

        # Botón de Reseteo al final del panel de control, después de tarifas
        tk.Button(
            self.marco_control,
            text="🔄 Reseteo Completo",
            command=self.reseteo_completo, 
            bg=self.colores['purpura'], 
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2
        ).pack(fill=tk.X, pady=(10,5) , padx=10, side=tk.BOTTOM)


    def iniciar_reloj(self):
        def actualizar():
            self.label_reloj.config(text=datetime.now().strftime("%H:%M:%S"))
            self.root.after(1000, actualizar) 
        actualizar()

    def configurar_controles(self):
        self.root.bind("<KeyPress>", self.tecla_presionada)
        self.root.bind("<KeyRelease>", self.tecla_liberada)
        self.canvas.bind("<Button-1>", self.click_en_canvas) 
        self.root.focus_set()

    def tecla_presionada(self, event):
        self.teclas_presionadas.add(event.keysym.lower())

    def tecla_liberada(self, event):
        self.teclas_presionadas.discard(event.keysym.lower())
        if event.keysym.lower() == 'space' and self.vehiculo_actual and self.modo_conduccion:
            self.intentar_estacionar()
    
    def click_en_canvas(self, event):
        if not self.modo_conduccion:
            print(f"Click en canvas: ({event.x}, {event.y})")
            for vehiculo in self.vehiculos.values():
                if vehiculo.id_espacio_estacionamiento is not None:
                    # Asegurarse de que el ID del espacio es un índice válido
                    if 0 <= vehiculo.id_espacio_estacionamiento < len(self.espacios_estacionamiento):
                        espacio = self.espacios_estacionamiento[vehiculo.id_espacio_estacionamiento]
                        ancho_dibujo, alto_dibujo = (40,25) if vehiculo.tipo == "motocicleta" else (60,35)
                        ex, ey = espacio.x + (50 if espacio.tipo == "motocicleta" else 80)//2, espacio.y + (30 if espacio.tipo == "motocicleta" else 60)//2
                        if abs(event.x - ex) < ancho_dibujo/2 and abs(event.y - ey) < alto_dibujo/2:
                            messagebox.showinfo("Info Vehículo", f"Placa: {vehiculo.placa}\nTipo: {vehiculo.tipo}\nColor: {vehiculo.color}\nEntrada: {vehiculo.hora_entrada.strftime('%H:%M')}", parent=self.root)
                            break
                    else:
                        print(f"Advertencia: Vehículo {vehiculo.placa} tiene un id_espacio_estacionamiento inválido: {vehiculo.id_espacio_estacionamiento}")


    def actualizar_juego(self):
        if self.vehiculo_actual and self.modo_conduccion:
            self.actualizar_movimiento_vehiculo()
        
        self.dibujar_estacionamiento() 
        self.actualizar_estadisticas()
        
        self.root.after(30, self.actualizar_juego) 

    def actualizar_movimiento_vehiculo(self):
        vehiculo = self.vehiculo_actual
        if not vehiculo: return

        if 'w' in self.teclas_presionadas:
            vehiculo.velocidad = min(vehiculo.velocidad + 0.15, vehiculo.max_velocidad)
        elif 's' in self.teclas_presionadas:
            vehiculo.velocidad = max(vehiculo.velocidad - 0.25, -vehiculo.max_velocidad / 2)
        else:
            if vehiculo.velocidad > 0:
                vehiculo.velocidad = max(0, vehiculo.velocidad - 0.05)
            elif vehiculo.velocidad < 0:
                vehiculo.velocidad = min(0, vehiculo.velocidad + 0.05)

        if abs(vehiculo.velocidad) > 0.05:
            # Ajuste de factor de giro: menos giro a mayor velocidad para más control
            factor_giro_base = 3.5 
            velocidad_relativa = abs(vehiculo.velocidad) / vehiculo.max_velocidad
            factor_giro = factor_giro_base * (1 - velocidad_relativa * 0.7) # Reduce el giro hasta un 70% a max vel.

            if 'a' in self.teclas_presionadas:
                vehiculo.angulo -= factor_giro
            if 'd' in self.teclas_presionadas:
                vehiculo.angulo += factor_giro
        
        vehiculo.angulo %= 360 

        rad = math.radians(vehiculo.angulo)
        vehiculo.x += math.cos(rad) * vehiculo.velocidad
        vehiculo.y += math.sin(rad) * vehiculo.velocidad
            
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_exists() else 1000
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_exists() else 700
        vehiculo.x = max(20, min(canvas_width - 20, vehiculo.x))
        vehiculo.y = max(20, min(canvas_height - 20, vehiculo.y))

    def intentar_estacionar(self):
        if not self.vehiculo_actual: return
            
        vehiculo = self.vehiculo_actual
        espacio_ideal = None
        distancia_minima_ideal = 60 

        for espacio in self.espacios_estacionamiento:
            if espacio.esta_ocupado: continue
                
            tipo_compatible = (vehiculo.tipo == "motocicleta" and espacio.tipo == "motocicleta") or \
                              (vehiculo.tipo != "motocicleta" and espacio.tipo == "regular")
            if not tipo_compatible: continue
                
            centro_espacio_x = espacio.x + (50 if espacio.tipo == "motocicleta" else 80) / 2
            centro_espacio_y = espacio.y + (30 if espacio.tipo == "motocicleta" else 60) / 2
            
            distancia = math.hypot(vehiculo.x - centro_espacio_x, vehiculo.y - centro_espacio_y)
            
            if distancia < distancia_minima_ideal:
                espacio_ideal = espacio
                distancia_minima_ideal = distancia 
        
        if espacio_ideal:
            self.estacionar_vehiculo_en_espacio(vehiculo, espacio_ideal)
        else:
            messagebox.showwarning("Estacionamiento", "No estás lo suficientemente cerca de un espacio compatible o está ocupado.", parent=self.root)

    def estacionar_vehiculo_en_espacio(self, vehiculo: Vehiculo, espacio: EspacioEstacionamiento):
        vehiculo.id_espacio_estacionamiento = espacio.id
        espacio.esta_ocupado = True
        espacio.id_vehiculo = vehiculo.id
        
        msg_casillero = ""
        if vehiculo.tipo == "motocicleta":
            casillero_disponible = next((c for c in self.casilleros if not c["ocupado"]), None)
            if casillero_disponible:
                vehiculo.id_casillero = casillero_disponible["id"]
                casillero_disponible["ocupado"] = True
                msg_casillero = f" y se le asignó el casillero {casillero_disponible['id'] + 1}"
            else:
                msg_casillero = ", pero no hay casilleros disponibles."
        
        self.modo_conduccion = False
        self.vehiculo_actual = None 
        self.label_estado.config(text="Modo: Vista General")
        
        messagebox.showinfo("Éxito", f"Vehículo {vehiculo.placa} estacionado en el espacio {espacio.id + 1}{msg_casillero}.", parent=self.root)
        self.dibujar_estacionamiento() 

    def dibujar_estacionamiento(self):
        self.canvas.delete("all")
        self.dibujar_carreteras()
        self.dibujar_espacios()
        self.dibujar_vehiculos_estacionados()
        if self.vehiculo_actual and self.modo_conduccion:
            self.dibujar_vehiculo_en_movimiento(self.vehiculo_actual)

    def dibujar_carreteras(self):
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_exists() else 1000
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_exists() else 700

        y_carretera_central = canvas_height / 2 
        alto_carretera = 100
        self.canvas.create_rectangle(
            0, y_carretera_central - alto_carretera/2, 
            canvas_width, y_carretera_central + alto_carretera/2,
            fill=self.colores['carretera'], outline=""
        )
        for x_linea in range(0, canvas_width, 40):
            self.canvas.create_line(
                x_linea, y_carretera_central, x_linea + 20, y_carretera_central,
                fill=self.colores['linea_carretera'], width=2, dash=(4,4)
            )
        
    def dibujar_espacios(self):
        if not self.espacios_estacionamiento:
            print("DEBUG: No hay espacios para dibujar.") 
            return

        for espacio in self.espacios_estacionamiento:
            color_borde = self.colores['acento'] if espacio.esta_ocupado else self.colores['verde']
            color_fondo = self.colores['secundario'] if not espacio.esta_ocupado else '#404040' 
            
            ancho_esp = 50 if espacio.tipo == "motocicleta" else 80
            alto_esp = 30 if espacio.tipo == "motocicleta" else 60
            
            self.canvas.create_rectangle(
                espacio.x, espacio.y, espacio.x + ancho_esp, espacio.y + alto_esp,
                fill=color_fondo, outline=color_borde, width=2
            )
            self.canvas.create_text(
                espacio.x + ancho_esp / 2, espacio.y + alto_esp / 2,
                text=str(espacio.id + 1), fill=self.colores['texto'], font=('Arial', 8, 'bold')
            )

    def dibujar_vehiculos_estacionados(self):
        for vehiculo_id, vehiculo in self.vehiculos.items():
            if vehiculo.id_espacio_estacionamiento is not None:
                espacio_obj = next((e for e in self.espacios_estacionamiento if e.id == vehiculo.id_espacio_estacionamiento), None)
                if espacio_obj:
                    self.dibujar_vehiculo_en_espacio(vehiculo, espacio_obj)


    def dibujar_vehiculo_en_espacio(self, vehiculo: Vehiculo, espacio: EspacioEstacionamiento):
        ancho_base_esp = 80 if espacio.tipo == "regular" else 50
        alto_base_esp = 60 if espacio.tipo == "regular" else 30

        centro_x_esp = espacio.x + ancho_base_esp / 2
        centro_y_esp = espacio.y + alto_base_esp / 2
        
        clave_imagen = "motocicleta" if vehiculo.tipo == "motocicleta" else f"{vehiculo.tipo}_{vehiculo.color}"
        imagen_tk = self.imagenes_vehiculos.get(clave_imagen)

        if imagen_tk:
            self.canvas.create_image(centro_x_esp, centro_y_esp, image=imagen_tk, anchor=tk.CENTER)
        else: 
            ancho_veh, alto_veh = (40,25) if vehiculo.tipo == "motocicleta" else (60,35)
            colores_rgb_defecto = {
                'rojo': self.colores['acento'], 'azul': self.colores['azul'], 
                'verde': self.colores['verde'], 'negro': '#2c3e50',
                'blanco': '#ecf0f1', 'amarillo': '#f1c40f', 'gris': '#95a5a6'
            }
            color_fill = colores_rgb_defecto.get(vehiculo.color, '#808080')
            self.canvas.create_rectangle(
                centro_x_esp - ancho_veh/2, centro_y_esp - alto_veh/2,
                centro_x_esp + ancho_veh/2, centro_y_esp + alto_veh/2,
                fill=color_fill, outline=self.colores['texto'], width=1
            )

    def dibujar_vehiculo_en_movimiento(self, vehiculo: Vehiculo):
        ancho_veh, alto_veh = (40,25) if vehiculo.tipo == "motocicleta" else (60,35)
        colores_rgb_defecto = {
            'rojo': self.colores['acento'], 'azul': self.colores['azul'], 
            'verde': self.colores['verde'], 'negro': '#2c3e50',
            'blanco': '#ecf0f1', 'amarillo': '#f1c40f', 'gris': '#95a5a6'
        }
        color_fill = colores_rgb_defecto.get(vehiculo.color, '#808080')

        puntos = [
            (-ancho_veh/2, -alto_veh/2), (ancho_veh/2, -alto_veh/2),
            (ancho_veh/2, alto_veh/2), (-ancho_veh/2, alto_veh/2)
        ]
        puntos_rotados = []
        rad = math.radians(-vehiculo.angulo) 
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        for x, y in puntos:
            xr = x * cos_a - y * sin_a + vehiculo.x
            yr = x * sin_a + y * cos_a + vehiculo.y
            puntos_rotados.extend([xr, yr])
        
        self.canvas.create_polygon(puntos_rotados, fill=color_fill, outline=self.colores['oro'], width=2)


    def actualizar_estadisticas(self):
        ocupados = len([e for e in self.espacios_estacionamiento if e.esta_ocupado])
        total_espacios = len(self.espacios_estacionamiento)
        self.label_ocupados.config(text=f"Ocupados: {ocupados}/{total_espacios}")
        
        ingresos_total = sum(entrada['costo'] for entrada in self.historial_salidas)
        self.label_ingresos.config(text=f"Ingresos: ${ingresos_total:,.0f} COP")

    def mostrar_dialogo_entrada(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Nuevo Vehículo")
        dialogo.geometry("350x380") 
        dialogo.configure(bg=self.colores['secundario'])
        dialogo.transient(self.root) 
        dialogo.grab_set() 

        tk.Label(dialogo, text="Tipo de Vehículo:", bg=self.colores['secundario'], fg=self.colores['texto'], font=('Arial', 10, 'bold')).pack(pady=(10,2))
        tipo_vehiculo_var = tk.StringVar(value="carro")
        combo_tipo = ttk.Combobox(dialogo, textvariable=tipo_vehiculo_var, values=["carro", "deportivo", "motocicleta"], state="readonly")
        combo_tipo.pack(pady=2, padx=20, fill=tk.X)

        tk.Label(dialogo, text="Color:", bg=self.colores['secundario'], fg=self.colores['texto'], font=('Arial', 10, 'bold')).pack(pady=(10,2))
        color_var = tk.StringVar(value="rojo")
        combo_color = ttk.Combobox(dialogo, textvariable=color_var, values=["rojo", "azul", "verde", "negro", "blanco", "amarillo", "gris"], state="readonly")
        combo_color.pack(pady=2, padx=20, fill=tk.X)

        tk.Label(dialogo, text="Placa:", bg=self.colores['secundario'], fg=self.colores['texto'], font=('Arial', 10, 'bold')).pack(pady=(10,2))
        placa_entry = tk.Entry(dialogo, font=('Arial', 10))
        placa_entry.pack(pady=2, padx=20, fill=tk.X)
        placa_entry.focus_set() 

        tiene_seguro_var = tk.BooleanVar()
        check_seguro = tk.Checkbutton(
            dialogo, text="Seguro Adicional", variable=tiene_seguro_var,
            bg=self.colores['secundario'], fg=self.colores['texto'], selectcolor=self.colores['fondo'],
            font=('Arial', 10), activebackground=self.colores['secundario'], activeforeground=self.colores['texto']
        )
        check_seguro.pack(pady=10)
        
        def actualizar_texto_seguro(*args):
            costo_s = 15000 if tipo_vehiculo_var.get() == 'deportivo' else 5000
            check_seguro.config(text=f"Seguro Adicional (+${costo_s:,})")
        tipo_vehiculo_var.trace_add("write", actualizar_texto_seguro)
        actualizar_texto_seguro() 

        def enviar_vehiculo():
            if self.agregar_vehiculo(tipo_vehiculo_var.get(), color_var.get(), placa_entry.get(), tiene_seguro_var.get()):
                dialogo.destroy()
        
        tk.Button(
            dialogo, text="🚗 Ingresar y Conducir", command=enviar_vehiculo,
            bg=self.colores['verde'], fg='white', font=('Arial', 12, 'bold'), height=2
        ).pack(pady=20, padx=20, fill=tk.X)
        
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.destroy)


    def agregar_vehiculo(self, tipo_vehiculo: str, color: str, placa: str, tiene_seguro: bool):
        if not placa.strip():
            messagebox.showerror("Error de Entrada", "La placa no puede estar vacía.", parent=self.root)
            return False

        if any(v.placa == placa.upper() for v in self.vehiculos.values()):
             messagebox.showerror("Error de Entrada", f"El vehículo con placa {placa.upper()} ya se encuentra registrado.", parent=self.root)
             return False
        
        nuevo_vehiculo = Vehiculo(tipo_vehiculo, color, placa.upper(), tiene_seguro)
        self.vehiculos[nuevo_vehiculo.id] = nuevo_vehiculo

        self.vehiculo_actual = nuevo_vehiculo
        self.modo_conduccion = True
        self.label_estado.config(text=f"Modo: Conduciendo {nuevo_vehiculo.placa}")
        self.root.focus_set() 

        messagebox.showinfo("Vehículo Ingresado", 
                            f"Vehículo {placa.upper()} listo para conducir.\nUse WASD para moverse y ESPACIO para estacionar.",
                            parent=self.root)
        return True

    def mostrar_dialogo_salida(self):
        vehiculos_estacionados = [v for v in self.vehiculos.values() if v.id_espacio_estacionamiento is not None]
        if not vehiculos_estacionados:
            messagebox.showinfo("Información", "No hay vehículos estacionados para retirar.", parent=self.root)
            return

        dialogo = tk.Toplevel(self.root)
        dialogo.title("Salida de Vehículo")
        dialogo.geometry("350x200") 
        dialogo.configure(bg=self.colores['secundario'])
        dialogo.transient(self.root)
        dialogo.grab_set()

        tk.Label(dialogo, text="Seleccionar Vehículo a Retirar:", 
                bg=self.colores['secundario'], fg=self.colores['texto'],
                font=('Arial', 11, 'bold')).pack(pady=(10,5))
        
        opciones_vehiculos = []
        for v in vehiculos_estacionados:
            id_esp = v.id_espacio_estacionamiento
            nombre_esp = "N/A"
            if id_esp is not None and 0 <= id_esp < len(self.espacios_estacionamiento):
                nombre_esp = str(self.espacios_estacionamiento[id_esp].id + 1)
            opciones_vehiculos.append(f"{v.placa} (Esp. {nombre_esp})")

        vehiculo_seleccionado_var = tk.StringVar()
        if opciones_vehiculos:
            vehiculo_seleccionado_var.set(opciones_vehiculos[0])

        combo_vehiculos = ttk.Combobox(dialogo, textvariable=vehiculo_seleccionado_var, values=opciones_vehiculos, state="readonly", width=30)
        combo_vehiculos.pack(pady=5, padx=20, fill=tk.X)

        def confirmar_salida():
            if not vehiculo_seleccionado_var.get():
                messagebox.showwarning("Selección Vacía", "Debe seleccionar un vehículo.", parent=dialogo)
                return
            
            placa_seleccionada = vehiculo_seleccionado_var.get().split(" (")[0]
            vehiculo_a_retirar = next((v for v in vehiculos_estacionados if v.placa == placa_seleccionada), None)
            
            if vehiculo_a_retirar:
                self.retirar_vehiculo(vehiculo_a_retirar.id)
                dialogo.destroy()
            else:
                messagebox.showerror("Error", "No se pudo encontrar el vehículo seleccionado.", parent=dialogo)

        tk.Button(
            dialogo, text="🚪 Retirar y Pagar", command=confirmar_salida,
            bg=self.colores['acento'], fg='white', font=('Arial', 12, 'bold'), height=2
        ).pack(pady=20, padx=20, fill=tk.X)
        
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.destroy)


    def retirar_vehiculo(self, id_vehiculo: str):
        vehiculo = self.vehiculos.get(id_vehiculo)
        if not vehiculo:
            messagebox.showerror("Error Interno", "No se encontró el vehículo para retirar.", parent=self.root)
            return

        hora_salida = datetime.now()
        duracion_timedelta = hora_salida - vehiculo.hora_entrada
        total_minutos_estadia = duracion_timedelta.total_seconds() / 60.0
        
        tarifa_minuto_vehiculo = self.tarifas_minuto.get(vehiculo.tipo, self.tarifas_minuto["carro"]) # Default a carro
        tarifa_hora_vehiculo = tarifa_minuto_vehiculo * 60

        costo_estadia = 0
        detalle_calculo_factura = ""
        minutos_cobrados_fraccion = 0
        horas_cobradas_completas = 0

        if total_minutos_estadia < 60:
            minutos_a_cobrar = math.ceil(max(1, total_minutos_estadia)) # Mínimo 1 minuto
            costo_estadia = minutos_a_cobrar * tarifa_minuto_vehiculo
            minutos_cobrados_fraccion = minutos_a_cobrar
            detalle_calculo_factura = f"  {minutos_a_cobrar} Minutos: {minutos_a_cobrar} x ${tarifa_minuto_vehiculo:,} = ${costo_estadia:,}\n"
        else:
            horas_completas = int(total_minutos_estadia // 60)
            minutos_restantes = total_minutos_estadia % 60
            
            costo_horas = horas_completas * tarifa_hora_vehiculo
            horas_cobradas_completas = horas_completas
            detalle_calculo_factura = f"  {horas_completas} Hora(s): {horas_completas} x ${tarifa_hora_vehiculo:,} = ${costo_horas:,}\n"
            costo_estadia += costo_horas

            if minutos_restantes > 0:
                minutos_adicionales_a_cobrar = math.ceil(minutos_restantes)
                costo_minutos_adicionales = minutos_adicionales_a_cobrar * tarifa_minuto_vehiculo
                minutos_cobrados_fraccion = minutos_adicionales_a_cobrar
                detalle_calculo_factura += f"  {minutos_adicionales_a_cobrar} Min. Adic: {minutos_adicionales_a_cobrar} x ${tarifa_minuto_vehiculo:,} = ${costo_minutos_adicionales:,}\n"
                costo_estadia += costo_minutos_adicionales
        
        costo_final = costo_estadia
        costo_seguro_aplicado = 0
        descuento_valor = 0

        if vehiculo.tiene_seguro:
            costo_seguro_aplicado = 15000 if vehiculo.tipo == "deportivo" else 5000
            costo_final += costo_seguro_aplicado
        
        if total_minutos_estadia / 60.0 > 8: # Descuento si más de 8 horas
            descuento_valor = int(costo_final * 0.15) # 15% de descuento sobre (estadia + seguro)
            costo_final -= descuento_valor
        
        self.historial_salidas.append({
            "placa": vehiculo.placa, "tipo": vehiculo.tipo, "color": vehiculo.color,
            "hora_entrada": vehiculo.hora_entrada, "hora_salida": hora_salida,
            "duracion": f"{int(total_minutos_estadia // 60)}h {int(total_minutos_estadia % 60)}m",
            "costo": costo_final,
            "tuvo_seguro": vehiculo.tiene_seguro,
            "costo_seguro_aplicado": costo_seguro_aplicado,
            "descuento_aplicado": descuento_valor
        })

        if vehiculo.id_espacio_estacionamiento is not None:
            espacio = next((e for e in self.espacios_estacionamiento if e.id == vehiculo.id_espacio_estacionamiento), None)
            if espacio:
                espacio.esta_ocupado = False
                espacio.id_vehiculo = None
        if vehiculo.id_casillero is not None:
            if 0 <= vehiculo.id_casillero < len(self.casilleros):
                 self.casilleros[vehiculo.id_casillero]["ocupado"] = False
            else:
                print(f"Error: id_casillero {vehiculo.id_casillero} fuera de rango para vehículo {vehiculo.placa}")


        del self.vehiculos[id_vehiculo]

        factura_str = (
            f"🚗 FACTURA DE SALIDA 🚗\n══════════════════════\n"
            f"Placa: {vehiculo.placa}\nTipo: {vehiculo.tipo.title()} {vehiculo.color.title()}\n"
            f"Entrada: {vehiculo.hora_entrada.strftime('%d/%m/%Y %H:%M')}\n"
            f"Salida: {hora_salida.strftime('%d/%m/%Y %H:%M')}\n"
            f"Duración Total: {int(total_minutos_estadia // 60)}h {int(total_minutos_estadia % 60)}m ({total_minutos_estadia:.2f} mins)\n"
            f"══════════════════════\n"
            f"Tarifa {vehiculo.tipo.title()}: ${tarifa_minuto_vehiculo:,}/min - ${tarifa_hora_vehiculo:,}/hora\n"
            f"Cálculo de Estadía:\n"
            f"{detalle_calculo_factura}"
            f"Subtotal Estadía: ${costo_estadia:,.0f} COP\n"
        )
        if vehiculo.tiene_seguro:
            factura_str += f"Seguro Adicional: +${costo_seguro_aplicado:,} COP\n"
        if descuento_valor > 0:
            factura_str += f"Descuento Larga Estadía (15%): -${descuento_valor:,} COP\n"
        factura_str += (
            f"══════════════════════\nTOTAL A PAGAR: ${costo_final:,.0f} COP\n"
            f"══════════════════════\n¡Gracias por su visita!"
        )
        messagebox.showinfo("💰 Factura de Salida", factura_str, parent=self.root)
        self.dibujar_estacionamiento() 

    def mostrar_historial(self):
        if not self.historial_salidas:
            messagebox.showinfo("Historial Vacío", "Aún no hay registros de salidas.", parent=self.root)
            return

        dialogo = tk.Toplevel(self.root)
        dialogo.title("📊 Historial Completo de Salidas")
        dialogo.geometry("750x600")
        dialogo.configure(bg=self.colores['secundario'])
        dialogo.transient(self.root)
        dialogo.grab_set()

        frame_principal = tk.Frame(dialogo, bg=self.colores['secundario'])
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        texto_historial = tk.Text(
            frame_principal, bg=self.colores['fondo'], fg=self.colores['texto'],
            wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10,
            borderwidth=0, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(frame_principal, command=texto_historial.yview, style="Vertical.TScrollbar")
        texto_historial.configure(yscrollcommand=scrollbar.set)
        
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", troughcolor=self.colores['fondo'], bordercolor=self.colores['secundario'], background=self.colores['azul'], arrowcolor=self.colores['texto'])


        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        texto_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        texto_historial.tag_configure('titulo', justify='center', font=('Consolas', 14, 'bold'), foreground=self.colores['oro'])
        texto_historial.tag_configure('subtitulo', font=('Consolas', 11, 'bold'), foreground=self.colores['azul'])
        texto_historial.tag_configure('bold', font=('Consolas', 10, 'bold'))

        texto_historial.insert(tk.END, "HISTORIAL DETALLADO DE SALIDAS\n\n", 'titulo')

        total_ingresos_general = 0
        conteo_tipos = {'carro': 0, 'deportivo': 0, 'motocicleta': 0}
        ingresos_tipos = {'carro': 0, 'deportivo': 0, 'motocicleta': 0}

        for i, entrada in enumerate(reversed(self.historial_salidas)): 
            total_ingresos_general += entrada['costo']
            conteo_tipos[entrada['tipo']] += 1
            ingresos_tipos[entrada['tipo']] += entrada['costo']

            texto_historial.insert(tk.END, f"--- Registro #{len(self.historial_salidas) - i} ---\n", 'subtitulo')
            texto_historial.insert(tk.END, f"  Fecha Salida: {entrada['hora_salida'].strftime('%d/%m/%Y %H:%M:%S')}\n")
            texto_historial.insert(tk.END, f"  Placa: {entrada['placa']}\n", 'bold')
            texto_historial.insert(tk.END, f"  Tipo: {entrada['tipo'].title()} ({entrada['color'].title()})\n")
            texto_historial.insert(tk.END, f"  Entrada: {entrada['hora_entrada'].strftime('%H:%M:%S')}\n")
            texto_historial.insert(tk.END, f"  Duración: {entrada['duracion']}\n")
            if entrada.get('tuvo_seguro', False):
                seguro_txt = "Sí (Premium)" if entrada['tipo'] == 'deportivo' else "Sí"
                texto_historial.insert(tk.END, f"  Seguro: {seguro_txt} (+${entrada.get('costo_seguro_aplicado',0):,} COP)\n")
            if entrada.get('descuento_aplicado', 0) > 0:
                 texto_historial.insert(tk.END, f"  Descuento: -${entrada['descuento_aplicado']:,} COP\n")
            texto_historial.insert(tk.END, f"  Total Pagado: ${entrada['costo']:,} COP\n\n", 'bold')
        
        texto_historial.insert(tk.END, "═" * 70 + "\n", 'titulo')
        texto_historial.insert(tk.END, "RESUMEN GENERAL\n\n", 'titulo')
        texto_historial.insert(tk.END, f"Total Vehículos Procesados: {len(self.historial_salidas)}\n\n", 'bold')
        for tipo_v, cantidad in conteo_tipos.items():
            texto_historial.insert(tk.END, f"  {tipo_v.title()}s: {cantidad} (Ingresos: ${ingresos_tipos[tipo_v]:,} COP)\n")
        texto_historial.insert(tk.END, f"\nINGRESOS TOTALES GENERALES: ${total_ingresos_general:,} COP\n", ('titulo', 'bold'))
        texto_historial.insert(tk.END, "═" * 70 + "\n", 'titulo')

        texto_historial.configure(state='disabled') 

        btn_frame = tk.Frame(dialogo, bg=self.colores['secundario'])
        btn_frame.pack(fill=tk.X, pady=(5,0), padx=10) 

        tk.Button(
            btn_frame, text="Exportar a JSON", command=self.exportar_historial_json,
            bg=self.colores['azul'], fg='white', font=('Arial', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(
            btn_frame, text="Cerrar", command=dialogo.destroy,
            bg=self.colores['acento'], fg='white', font=('Arial', 10, 'bold')
        ).pack(side=tk.RIGHT, padx=5, pady=5)
        
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.destroy)


    def exportar_historial_json(self):
        if not self.historial_salidas:
            messagebox.showinfo("Nada que Exportar", "El historial está vacío.", parent=self.root)
            return
        try:
            historial_serializable = []
            for entrada in self.historial_salidas:
                entrada_copia = entrada.copy()
                entrada_copia['hora_entrada'] = entrada['hora_entrada'].isoformat()
                entrada_copia['hora_salida'] = entrada['hora_salida'].isoformat()
                historial_serializable.append(entrada_copia)

            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Guardar Historial Como...",
                initialfile="historial_estacionamiento.json",
                parent=self.root 
            )
            if not filepath: 
                return

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(historial_serializable, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", f"Historial exportado a:\n{filepath}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar el historial:\n{str(e)}", parent=self.root)

    def guardar_estado(self):
        estado = {
            'vehiculos': [
                {
                    'id': v.id, 'tipo': v.tipo, 'color': v.color, 'placa': v.placa,
                    'hora_entrada': v.hora_entrada.isoformat(), 'tiene_seguro': v.tiene_seguro,
                    'id_espacio': v.id_espacio_estacionamiento, 'id_casillero': v.id_casillero,
                    'x': v.x, 'y': v.y, 'angulo': v.angulo 
                } for v in self.vehiculos.values()
            ],
            'espacios': [
                {
                    'id': e.id, 'tipo': e.tipo, 'ocupado': e.esta_ocupado,
                    'id_vehiculo': e.id_vehiculo, 'x': e.x, 'y': e.y
                } for e in self.espacios_estacionamiento
            ],
            'casilleros': self.casilleros,
            'historial': [ 
                 {**h, 'hora_entrada': h['hora_entrada'].isoformat(), 'hora_salida': h['hora_salida'].isoformat()}
                 for h in self.historial_salidas
            ],
            'ultima_actualizacion': datetime.now().isoformat()
        }
        try:
            with open('estado_estacionamiento.json', 'w', encoding='utf-8') as f:
                json.dump(estado, f, indent=4, ensure_ascii=False)
            print("Estado del estacionamiento guardado.")
        except Exception as e:
            print(f"Error guardando estado: {str(e)}")

    def cargar_estado(self):
        try:
            with open('estado_estacionamiento.json', 'r', encoding='utf-8') as f:
                estado = json.load(f)

            self.vehiculos.clear()
            for v_data in estado.get('vehiculos', []):
                vehiculo = Vehiculo(v_data['tipo'], v_data['color'], v_data['placa'], v_data['tiene_seguro'])
                vehiculo.id = v_data['id']
                vehiculo.hora_entrada = datetime.fromisoformat(v_data['hora_entrada'])
                vehiculo.id_espacio_estacionamiento = v_data.get('id_espacio') 
                vehiculo.id_casillero = v_data.get('id_casillero')
                vehiculo.x = v_data.get('x', 50) 
                vehiculo.y = v_data.get('y', 475) # Actualizado a la Y inicial correcta
                vehiculo.angulo = v_data.get('angulo', 0)
                self.vehiculos[vehiculo.id] = vehiculo
            
            loaded_espacios_data = estado.get('espacios', [])
            if not loaded_espacios_data: 
                print("Archivo de estado no contiene datos de espacios o está vacío. Recreando espacios por defecto.")
                self.crear_espacios_estacionamiento()
            else:
                self.espacios_estacionamiento.clear()
                for e_data in loaded_espacios_data:
                    espacio = EspacioEstacionamiento(e_data['id'], e_data['tipo'], e_data['x'], e_data['y'])
                    espacio.esta_ocupado = e_data['ocupado']
                    espacio.id_vehiculo = e_data.get('id_vehiculo')
                    self.espacios_estacionamiento.append(espacio)

            self.casilleros = estado.get('casilleros', [{"id": i, "ocupado": False} for i in range(15)])
            
            self.historial_salidas.clear()
            for h_data in estado.get('historial', []):
                 self.historial_salidas.append({
                     **h_data, 
                     'hora_entrada': datetime.fromisoformat(h_data['hora_entrada']),
                     'hora_salida': datetime.fromisoformat(h_data['hora_salida'])
                 })

            print(f"Estado cargado. Última actualización: {estado.get('ultima_actualizacion', 'N/A')}")
            return True
        except FileNotFoundError:
            print("No se encontró 'estado_estacionamiento.json'. Se iniciará con un estado limpio.")
            self.crear_espacios_estacionamiento() 
            return False
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el estado: {str(e)}\nSe iniciará un estado limpio.", parent=self.root)
            self.vehiculos.clear()
            self.crear_espacios_estacionamiento() 
            self.casilleros = [{"id": i, "ocupado": False} for i in range(15)]
            self.historial_salidas.clear()
            return False

    def reseteo_completo(self):
        if messagebox.askokcancel("Confirmar Reseteo Total", 
                                  "¿Está seguro de que desea resetear TODO el estacionamiento?\n"
                                  "Esto borrará todos los vehículos actuales, el historial y los ingresos acumulados. "
                                  "Los espacios se recrearán vacíos.", parent=self.root):
            self.vehiculos.clear()
            self.crear_espacios_estacionamiento() 
            self.casilleros = [{"id": i, "ocupado": False} for i in range(15)]
            self.historial_salidas.clear()
            
            self.vehiculo_actual = None
            self.modo_conduccion = False
            self.label_estado.config(text="Modo: Vista General")
            
            messagebox.showinfo("Reseteo Completo", "El estacionamiento ha sido reseteado a su estado inicial.", parent=self.root)
            self.actualizar_estadisticas() 
            self.dibujar_estacionamiento()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorEstacionamiento(root)
    
    if not app.cargar_estado(): 
        print("Iniciando con un estacionamiento nuevo o por defecto.")
    
    app.actualizar_estadisticas()
    app.dibujar_estacionamiento()


    def on_closing():
        if messagebox.askyesno("Salir", "¿Desea guardar el estado actual del estacionamiento antes de salir?", parent=root):
            app.guardar_estado()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
