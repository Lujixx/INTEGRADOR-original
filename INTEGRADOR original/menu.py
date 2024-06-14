import os
import tkinter as tk
from PIL import ImageTk, Image
import subprocess
import ttkbootstrap as btp

def on_enter(e):
    e.widget["background"] = "red"
    
def on_leave(e):
    e.widget["background"] = "black"

def salir():
    ventana.withdraw()
    subprocess.Popen(["python","login.py"])

def abrir_Combos():
    ventana.withdraw()
    subprocess.Popen(["python", "combos.py"])

def abrir_estrenos():
    ventana.withdraw()
    subprocess.Popen(["python", "estrenos.py"])

def abrir_Cartelera():
    ventana.withdraw()
    subprocess.Popen(["python", "video.py"])

def cambiar_imagen(direccion):
    global current_image_index
    current_image_index += direccion
    current_image_index %= len(imagenes_tk)
    imagen_label.config(image=imagenes_tk[current_image_index])

ventana = tk.Tk()
ventana.title("Menu Cine Cuenca")
ventana.geometry("2000x4000")
ventana.attributes("-fullscreen", True)

imagen_fondo = Image.open("fondo2.png")  
imagen_fondo = imagen_fondo.resize((1920, 1080), Image.Resampling.LANCZOS)  
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

canvas = tk.Canvas(ventana, width=1920, height=1080)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo_tk)

fuente = ("Bryant Light", 14)
boton_cartelera = tk.Button(canvas, text="CARTELERA", font=fuente, background="black", foreground="white", command=abrir_Cartelera)
boton_combos = tk.Button(canvas, text="COMBOS", font=fuente, background="black", foreground="white", command=abrir_Combos)
boton_salir = tk.Button(canvas, text="SALIR", font=fuente, background="black", foreground="white", command=salir)

boton_cartelera.place(x=750, y=215)
boton_combos.place(x=900, y=215)
boton_salir.place(x=1050, y=215)

boton_cartelera.bind("<Enter>", on_enter)
boton_cartelera.bind("<Leave>", on_leave)

boton_combos.bind("<Enter>", on_enter)
boton_combos.bind("<Leave>", on_leave)

boton_salir.bind("<Enter>", on_enter)
boton_salir.bind("<Leave>", on_leave)

# Lista de imágenes
imagenes = ["tarot.png", "planeta.png", "inmaculada.png","intensamente.png"]  
imagenes_tk = [ImageTk.PhotoImage(Image.open(img).resize((1100, 500), Image.Resampling.LANCZOS)) for img in imagenes]

current_image_index = 0
imagen_label = tk.Label(canvas, image=imagenes_tk[current_image_index])
imagen_label.place(x=960, y=640, anchor="center")  # Centramos la imagen en la ventana

# Botones para cambiar de imagen
boton_anterior = tk.Button(canvas, text="<--", font=fuente, bg="black", fg="white", command=lambda: cambiar_imagen(-1))
boton_siguiente = tk.Button(canvas, text="-->", font=fuente, bg="black", fg="white", command=lambda: cambiar_imagen(1))

boton_anterior.place(x=445, y=580)  # Ajusta la posición del botón según sea necesario
boton_siguiente.place(x=1445, y=580)  # Ajusta la posición del botón según sea necesario

ventana.mainloop()
