import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Crear la ventana principal
root = tk.Tk()
root.title("Pantalla Principal - Jidoka")
root.geometry("800x600")
root.configure(bg="#f4f4f4")

# Contenedor principal
frame_container = tk.Frame(root, bg="white", padx=20, pady=20)
frame_container.pack(pady=20, fill=tk.BOTH, expand=True)

# Título
label_title = tk.Label(frame_container, text="Pantalla Principal - Banda Transportadora", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Banda transportadora
frame_band = tk.Frame(frame_container, bg="#f4f4f4")
frame_band.pack(pady=10)

slots = []
statuses = ["default", "ok", "report", "stopped"]
colors = {"default": "#d1ffd1", "ok": "#19f324", "report": "#eeff04", "stopped": "#ff0404"}

for i in range(1, 22):
    frame_slot = tk.Frame(frame_band, width=50, height=80, bg=colors["default"], bd=2, relief="solid")
    frame_slot.pack(side=tk.LEFT, padx=5)
    
    label_num = tk.Label(frame_slot, text=str(i), font=("Arial", 10, "bold"), bg=colors["default"])
    label_num.pack()
    
    label_id = tk.Label(frame_slot, text="#", font=("Arial", 10), bg=colors["default"])
    label_id.pack()
    
    slots.append((frame_slot, label_num, label_id))

# Botones de inicio y detención
frame_buttons = tk.Frame(frame_container)
frame_buttons.pack(pady=10)

btn_start = tk.Button(frame_buttons, text="Iniciar", bg="#4CAF50", fg="white", font=("Arial", 12), width=10)
btn_start.pack(side=tk.LEFT, padx=10)

btn_stop = tk.Button(frame_buttons, text="Detener", bg="#f44336", fg="white", font=("Arial", 12), width=10)
btn_stop.pack(side=tk.LEFT, padx=10)

# Datos
frame_data = tk.Frame(frame_container)
frame_data.pack(pady=10)

def create_data_slot(parent, title):
    frame = tk.Frame(parent, width=90, height=80, bg="#d1ffd1", bd=2, relief="solid")
    frame.pack(side=tk.LEFT, padx=10)
    
    label = tk.Label(frame, text=title, font=("Arial", 10, "bold"))
    label.pack()
    
    entry = tk.Entry(frame, font=("Arial", 10), justify="center", width=5, state="readonly")
    entry.pack()
    
    return entry

entry_OA = create_data_slot(frame_data, "OA")
entry_RR = create_data_slot(frame_data, "RR")
entry_OT = create_data_slot(frame_data, "OVERTIME")
entry_TM = create_data_slot(frame_data, "TIME")

# Función para actualizar la hora
def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    entry_TM.config(state="normal")
    entry_TM.delete(0, tk.END)
    entry_TM.insert(0, current_time)
    entry_TM.config(state="readonly")
    root.after(1000, update_time)

update_time()

root.mainloop()
