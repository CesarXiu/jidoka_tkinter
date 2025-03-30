import tkinter as tk
from PIL import Image, ImageTk  # Importar Pillow
import pygame
from datetime import datetime
import os

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
root.configure(bg="#add8e6")  # Configurar el fondo azul claro desde el inicio

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

# Función para actualizar la hora actual y el tiempo desde el último reporte
def update_clock():
    # Actualizar la hora actual
    current_time = datetime.now().strftime('%H:%M:%S')
    label_current_time.config(text=f"Hora actual: {current_time}")
    
    # Actualizar el tiempo desde el último reporte
    if last_report_time:
        elapsed_time = datetime.now() - last_report_time
        clock_label.config(text=f"Tiempo desde el último reporte: {str(elapsed_time).split('.')[0]}")
    else:
        clock_label.config(text="Tiempo desde el último reporte: N/A")
    
    # Llamar a esta función nuevamente después de 1 segundo
    root.after(1000, update_clock)

# Función para cambiar el estado del botón y la pantalla
def toggle_button():
    global toggle_state, last_report_time
    
    # Cambiar el estado del botón
    if toggle_state:
        # Cambiar a verde con letras blancas
        btn_toggle.config(bg="green", fg="white", text="OK")
        root.configure(bg="#add8e6")  # Fondo azul claro cuando es "OK"
        canvas.configure(bg="#add8e6")  # Canvas también tiene fondo azul claro
        canvas.delete("all")  # Borrar la imagen del canvas
        
        # Ocultar el mensaje de reporte
        label_report.config(text="")
        
        # Registrar el tiempo del cambio a "OK"
        last_report_time = datetime.now()
    else:
        # Cambiar a rojo con letras blancas y mostrar mensaje
        btn_toggle.config(bg="red", fg="white", text="REPORTE")
        root.configure(bg="yellow")  # Fondo amarillo cuando se activa el reporte
        label_report.config(text="Reporte en la banda")  # Mostrar el mensaje de reporte
        canvas.configure(bg="yellow")  # Canvas con fondo amarillo también
        
        # Asegurarnos de que la imagen se ve completamente en el canvas
        if report_image:
            canvas.config(width=500, height=500)  # Tamaño adecuado para la imagen
            canvas.create_image(250, 250, image=report_image)  # Centrar la imagen en el canvas
        
        # No registrar el tiempo aquí, ya que el contador comienza en "OK"
        
        # Reproducir sonido MP3
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        else:
            print(f"Error: No se encontró el archivo de sonido '{sound_file}'.")
        
    # Cambiar el estado para el próximo clic
    toggle_state = not toggle_state

# Crear el botón de encender/apagar
btn_toggle = tk.Button(root, text="OK", bg="green", fg="white", font=("Arial", 24), width=20, height=3, command=toggle_button)
btn_toggle.pack(pady=20)

# Crear el label para mostrar la hora actual
label_current_time = tk.Label(root, text="Hora actual: N/A", font=("Arial", 32, "bold"), bg="#add8e6", fg="black")
label_current_time.pack(pady=20)

# Crear el label para mostrar el tiempo desde el último reporte
clock_label = tk.Label(root, text="Tiempo desde el último reporte: N/A", font=("Arial", 28), bg="#add8e6", fg="black")
clock_label.pack(pady=20)

# Crear el label para mostrar el mensaje de reporte
label_report = tk.Label(root, text="", font=("Arial", 32, "bold"), bg="#add8e6", fg="red")
label_report.pack(pady=20)

# Crear un Canvas para mostrar la imagen con transparencia
canvas = tk.Canvas(root, width=500, height=500, bg="#add8e6", bd=0, highlightthickness=0)
canvas.pack(pady=20)

# Iniciar el reloj
update_clock()

# Ejecutar el loop principal de la aplicación
root.mainloop()
