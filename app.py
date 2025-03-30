import tkinter as tk
from PIL import Image, ImageTk  # Importar Pillow
import pygame
from datetime import datetime
import os
import platform  # Para verificar el sistema operativo

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
sound_file = "announcement.mp3"
if not os.path.exists(sound_file):
    print(f"Advertencia: No se encontró el archivo de sonido '{sound_file}'.")

# Crear la ventana principal
root = tk.Tk()
root.title("Pantalla Principal - Jidoka")
root.geometry("800x600")
root.configure(bg="#2a3d66")  # Fondo azul oscuro

# Variable global para verificar el estado del botón
toggle_state = False
last_report_time = None  # Tiempo del último reporte

# Cargar la imagen para el mensaje de reporte con Pillow y manejar la transparencia
try:
    original_image = Image.open("head.png").convert("RGBA")  # Asegúrate de usar la ruta correcta de la imagen
    report_image = ImageTk.PhotoImage(original_image)  # Convertir la imagen a formato compatible con Tkinter
except FileNotFoundError:
    print("Advertencia: No se pudo cargar la imagen 'head.png'.")
    report_image = None

# Función para actualizar el reloj
def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=f"Hora actual: {current_time}")

    if last_report_time:
        elapsed_time = datetime.now() - last_report_time
        elapsed_label.config(text=f"Tiempo desde el último reporte: {str(elapsed_time).split('.')[0]}")
    else:
        elapsed_label.config(text="Tiempo desde el último reporte: N/A")
    
    root.after(1000, update_clock)  # Actualizar cada segundo

# Función para cambiar el estado del botón y la pantalla
def toggle_button():
    global toggle_state, last_report_time
    
    # Cambiar el estado del botón
    if toggle_state:
        # Cambiar a verde con letras blancas
        btn_toggle.config(bg="green", fg="white", text="OK", font=("Arial", 30, "bold"))
        root.configure(bg="#2a3d66")  # Fondo azul oscuro cuando es "OK"
        label_report.config(text="", font=("Arial", 30, "bold"), fg="white", bg="#2a3d66")  # Fondo azul oscuro
        clock_label.config(bg="#2a3d66", fg="white")  # Fondo azul oscuro para la hora actual
        elapsed_label.config(bg="#2a3d66", fg="white")  # Fondo azul oscuro para el tiempo desde el último reporte
        canvas.configure(bg="#2a3d66")  # Fondo azul oscuro para el canvas
        canvas.delete("all")  # Borrar la imagen del canvas
        
        # Registrar el tiempo del cambio a "OK"
        last_report_time = datetime.now()
    else:
        # Cambiar a rojo con letras blancas y mostrar mensaje
        btn_toggle.config(bg="red", fg="white", text="REPORTE", font=("Arial", 30, "bold"))
        root.configure(bg="yellow")  # Fondo amarillo cuando se activa el reporte
        label_report.config(text="Reporte en la banda", font=("Arial", 30, "bold"), fg="red", bg="yellow")  # Fondo amarillo
        clock_label.config(bg="yellow", fg="black")  # Fondo amarillo para la hora actual
        elapsed_label.config(bg="yellow", fg="black")  # Fondo amarillo para el tiempo desde el último reporte
        canvas.configure(bg="yellow")  # Fondo amarillo para el canvas
        
        # Asegurarnos de que la imagen se ve completamente en el canvas
        if report_image:
            # Ajustamos el tamaño del canvas para que se ajuste a la imagen
            canvas.config(width=500, height=500)  # Tamaño adecuado para la imagen
            canvas.create_image(250, 250, image=report_image)  # Centrar la imagen en el canvas
        
        # Reproducir sonido MP3
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        else:
            print(f"Error: No se encontró el archivo de sonido '{sound_file}'.")
        
    # Cambiar el estado para el próximo clic
    toggle_state = not toggle_state

# Función para simular el estado del botón GPIO (tecla 'b')
def update_label(event=None):
    global toggle_state
    if event and event.keysym == "b":  # Simula que al presionar 'b' se activa el botón GPIO
        toggle_button()  # Llama a la función del botón para cambiar el estado
    else:
        toggle_state = False
        toggle_button()  # Cambia a estado "OK" si el GPIO no está presionado

# Si gpiozero está instalado y estamos en una Raspberry Pi, configurar el botón GPIO
if gpiozero_installed:
    gpio_pin = 17  # Debe coincidir con el pin conectado en la Raspberry Pi
    button_signal = Button(gpio_pin)

    # Función que monitorea el botón GPIO
    def gpio_button_check():
        global toggle_state
        if button_signal.is_pressed:  # Si el botón en el GPIO está presionado
            toggle_button()  # Cambia el estado como si fuera un clic en el botón
        else:
            if toggle_state:
                toggle_button()  # Cambia a estado "OK" si el GPIO no está presionado

    # Iniciar la actualización del estado del botón GPIO
    root.after(100, gpio_button_check)

# Asignar la tecla 'b' para simular el estado del botón GPIO
root.bind("<KeyPress-b>", update_label)

# Crear el botón de encender/apagar
btn_toggle = tk.Button(root, text="OK", bg="green", fg="white", font=("Arial", 30, "bold"), width=20, height=3, command=toggle_button)
btn_toggle.pack(pady=20)

# Crear el label para mostrar la hora y el tiempo desde el último reporte
clock_label = tk.Label(root, text="Hora actual: N/A", font=("Arial", 30, "bold"), bg="#2a3d66", fg="white")
clock_label.pack(pady=10)

elapsed_label = tk.Label(root, text="Tiempo desde el último reporte: N/A", font=("Arial", 30, "bold"), bg="#2a3d66", fg="white")
elapsed_label.pack(pady=10)

# Crear el label para mostrar el mensaje de reporte
label_report = tk.Label(root, text="", font=("Arial", 30, "bold"), bg="#2a3d66", fg="white")
label_report.pack(pady=20)

# Crear un Canvas para mostrar la imagen con transparencia
canvas = tk.Canvas(root, width=500, height=500, bg="#2a3d66", bd=0, highlightthickness=0)
canvas.pack(pady=20)


# Iniciar el reloj
update_clock()

# Ejecutar el loop principal de la aplicación
root.mainloop()
