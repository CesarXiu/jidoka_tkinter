import tkinter as tk
from PIL import Image, ImageTk  # Importar Pillow
import pygame
from datetime import datetime
import os
import platform  # Para verificar el sistema operativo

# Configuración de colores
COLOR_BG_DARK_BLUE = "#2a3d66"
COLOR_BG_YELLOW = "yellow"
COLOR_BTN_OK = "green"
COLOR_BTN_REPORT = "red"
COLOR_TEXT_WHITE = "white"
COLOR_TEXT_BLACK = "black"
COLOR_TEXT_RED = "red"
COLOR_BELT_SECTION_LIGHT_GREEN = "#90EE90"
COLOR_BELT_SECTION_DARKER_GREEN = "#76c776"

# Intentar importar gpiozero solo si estamos en una Raspberry Pi
gpiozero_installed = False
if platform.system() == 'Linux' and 'raspberrypi' in platform.uname().machine:
    try:
        from gpiozero import Button
        gpiozero_installed = True
    except ImportError:
        print("gpiozero no está instalado. No se utilizarán los pines GPIO.")

# Inicializar pygame para reproducir sonidos
pygame.mixer.init()

# Ruta al archivo MP3
SOUND_FILE = "announcement.mp3"
if not os.path.exists(SOUND_FILE):
    print(f"Advertencia: No se encontró el archivo de sonido '{SOUND_FILE}'.")

# Crear la ventana principal
root = tk.Tk()
root.title("Pantalla Principal - Jidoka")
root.geometry("800x600")
root.configure(bg=COLOR_BG_DARK_BLUE)

# Variables globales
toggle_state = False
last_report_time = None  # Tiempo del último reporte

# Cargar la imagen para el mensaje de reporte con Pillow y manejar la transparencia
try:
    original_image = Image.open("head.png").convert("RGBA")
    report_image = ImageTk.PhotoImage(original_image)
except FileNotFoundError:
    print("Advertencia: No se pudo cargar la imagen 'head.png'.")
    report_image = None

def toggle_button():
    global toggle_state, last_report_time
    
    if toggle_state:
        # Configuración para estado OK
        set_background_color(COLOR_BG_DARK_BLUE)
        label_report.config(
            text="", 
            font=("Arial", 30, "bold"), 
            fg=COLOR_TEXT_WHITE, 
            bg=COLOR_BG_DARK_BLUE
        )
        canvas.delete("all")
        last_report_time = datetime.now()
    else:
        # Configuración para estado REPORTE
        set_background_color(COLOR_BG_YELLOW)
        label_report.config(
            text="Reporte en la banda", 
            font=("Arial", 30, "bold"), 
            fg=COLOR_TEXT_RED, 
            bg=COLOR_BG_YELLOW
        )
        
        if report_image:
            canvas.config(width=500, height=500)
            canvas.create_image(250, 250, image=report_image)
        
        play_sound()
    
    toggle_state = not toggle_state
    update_belt_color()

def set_background_color(color):
    """Establece el color de fondo para todos los elementos principales"""
    root.configure(bg=color)
    clock_label.config(bg=color, fg=COLOR_TEXT_WHITE if color == COLOR_BG_DARK_BLUE else COLOR_TEXT_BLACK)
    elapsed_label.config(bg=color, fg=COLOR_TEXT_WHITE if color == COLOR_BG_DARK_BLUE else COLOR_TEXT_BLACK)
    clock_value.config(bg="white", fg="black")  # Mantener el fondo blanco para los valores
    elapsed_value.config(bg="white", fg="black")  # Mantener el fondo blanco para los valores
    time_frame.config(bg=color)  # Cambiar el fondo del frame de hora y tiempo
    canvas.configure(bg=color)
    frame.config(bg=color)
    for widget in frame.winfo_children():
        widget.config(bg=color, fg=COLOR_TEXT_WHITE if color == COLOR_BG_DARK_BLUE else COLOR_TEXT_BLACK)

def play_sound():
    """Reproduce el sonido de anuncio si existe"""
    if os.path.exists(SOUND_FILE):
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.play()
    else:
        print(f"Error: No se encontró el archivo de sonido '{SOUND_FILE}'.")

def update_clock():
    """Actualiza el reloj y el tiempo transcurrido"""
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_value.config(text=current_time)

    if last_report_time:
        elapsed_time = datetime.now() - last_report_time
        elapsed_value.config(text=str(elapsed_time).split('.')[0])
    else:
        elapsed_value.config(text="N/A")
    
    root.after(1000, update_clock)

def update_label(event=None):
    """Maneja eventos de teclado para simular el botón GPIO"""
    global toggle_state
    if event and event.keysym == "b":
        toggle_button()
    else:
        toggle_state = False
        toggle_button()

def update_belt_color():
    """Actualiza el color de la banda según el estado actual"""
    background_color = root.cget("bg")
    if background_color == COLOR_BG_YELLOW:
        draw_belt(COLOR_BG_YELLOW, COLOR_BELT_SECTION_DARKER_GREEN)
    else:
        draw_belt(COLOR_BG_DARK_BLUE, COLOR_BELT_SECTION_LIGHT_GREEN)

def draw_belt(background_color=COLOR_BG_DARK_BLUE, section_color1="#90EE90", section_color2="#76c776"):
    """Dibuja la banda con secciones mejoradas"""
    belt_canvas.delete("all")
    belt_canvas.configure(bg=background_color)

    num_sections = 21  # Número de secciones
    section_width = 50  # Ancho de cada sección
    section_height = 100  # Altura de cada sección
    padding = 10  # Espaciado entre secciones
    start_x = 10  # Margen inicial en X
    start_y = 40  # Margen inicial en Y

    for i in range(num_sections):
        # Alternar colores entre las secciones
        fill_color = section_color1 if i % 2 == 0 else section_color2

        # Coordenadas del rectángulo
        x1 = start_x + i * (section_width + padding)
        y1 = start_y
        x2 = x1 + section_width
        y2 = y1 + section_height

        # Dibujar el rectángulo
        belt_canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=fill_color,
            outline="black",  # Borde negro
            width=2           # Grosor del borde
        )

        # Dibujar el texto centrado
        belt_canvas.create_text(
            x1 + section_width / 2,
            y1 + section_height / 2,
            text=str(i + 1),
            font=("Arial", 18, "bold"),
            fill="black"
        )

# Configuración de la interfaz gráfica
belt_canvas = tk.Canvas(
    root, 
    width=1400,  # Aumentar el ancho del Canvas
    height=200, 
    bg=COLOR_BG_DARK_BLUE, 
    bd=0, 
    highlightthickness=0
)
belt_canvas.pack(pady=10)
draw_belt()

# Frame para la hora actual y el tiempo transcurrido en una fila
time_frame = tk.Frame(root, bg=COLOR_BG_DARK_BLUE)
time_frame.pack(pady=10)

# Hora actual
clock_label = tk.Label(
    time_frame, 
    text="HORA ACTUAL", 
    font=("Arial", 20, "bold"), 
    bg=COLOR_BG_DARK_BLUE, 
    fg=COLOR_TEXT_WHITE
)
clock_label.pack(side="left", padx=20)

clock_value = tk.Label(
    time_frame, 
    text="00:00:00", 
    font=("Arial", 24, "bold"), 
    bg="white", 
    fg="black",
    relief="solid",  # Borde sólido
    bd=2,           # Grosor del borde
    padx=20,        # Padding horizontal
    pady=10         # Padding vertical
)
clock_value.pack(side="left", padx=20)

# Tiempo transcurrido
elapsed_label = tk.Label(
    time_frame, 
    text="TIEMPO DESDE EL ÚLTIMO REPORTE", 
    font=("Arial", 20, "bold"), 
    bg=COLOR_BG_DARK_BLUE, 
    fg=COLOR_TEXT_WHITE
)
elapsed_label.pack(side="left", padx=20)

elapsed_value = tk.Label(
    time_frame, 
    text="N/A", 
    font=("Arial", 24, "bold"), 
    bg="white", 
    fg="black",
    relief="solid",  # Borde sólido
    bd=2,           # Grosor del borde
    padx=20,        # Padding horizontal
    pady=10         # Padding vertical
)
elapsed_value.pack(side="left", padx=20)

label_report = tk.Label(
    root, 
    text="", 
    font=("Arial", 30, "bold"), 
    bg=COLOR_BG_DARK_BLUE, 
    fg=COLOR_TEXT_WHITE
)
label_report.pack(pady=20)

frame = tk.Frame(root, bg=COLOR_BG_DARK_BLUE)
frame.pack(pady=10)

canvas = tk.Canvas(
    root, 
    width=500, 
    height=500, 
    bg=COLOR_BG_DARK_BLUE, 
    bd=0, 
    highlightthickness=0
)
canvas.pack(pady=20)

# Configuración de eventos
root.bind("<KeyPress-b>", update_label)

# Configuración GPIO si está disponible
if gpiozero_installed:
    gpio_pin = 17
    button_signal = Button(gpio_pin)

    def gpio_button_check():
        global toggle_state
        if button_signal.is_pressed:
            toggle_button()
        else:
            if toggle_state:
                toggle_button()

    root.after(100, gpio_button_check)

# Iniciar el reloj
update_clock()

# Ejecutar la aplicación
root.mainloop()