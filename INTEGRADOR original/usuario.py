import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import re


def on_enter(e):
    e.widget["background"] = "red"
    
def on_leave(e):
    e.widget["background"] = "white"

# Función para iniciar sesión
def iniciar_sesion():
    nombre_usuario = nombre_usuario_entry.get()
    contraseña = contraseña_entry.get()
    tipo_usuario = tipo_usuario_var.get()

    if not nombre_usuario or not contraseña:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    if tipo_usuario == "Administrador":
        # Verificar las credenciales del usuario Administrador predefinido
        if nombre_usuario == "Admin" and contraseña == "Admin2024":
            messagebox.showinfo("Éxito", "¡Bienvenido Administrador!")
        else:
            messagebox.showerror("Error", "Credenciales de Administrador incorrectas")
    else:
        # Verificar las credenciales de usuario normal
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as archivo:
                datos = json.load(archivo)
            usuarios = datos.get("usuarios", {})
        else:
            usuarios = {}

        if nombre_usuario in usuarios and usuarios[nombre_usuario]["contraseña"] == contraseña and usuarios[nombre_usuario]["tipo"] == tipo_usuario:
            messagebox.showinfo("Éxito", f"¡Bienvenido/a {nombre_usuario} al Cinema Cuenca!")
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

# Función para abrir la ventana de registro
def abrir_ventana_registro():
    global ventana_registro, imagen_fondo_detalle  # Mantener una referencia a la imagen de fondo
    ventana.withdraw()  # Ocultar la ventana de inicio de sesión
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registro")
    ventana_registro.geometry("1366x768")
    
    rutaojito = "ojito.png"
    imagen_ojito = Image.open(rutaojito)
    imagen_ojito = imagen_ojito.resize((20, 20))
    imagen_ojito = ImageTk.PhotoImage(imagen_ojito)

    # Cargar la imagen de fondo para la ventana de registro
    imagen_fondo_detalle = Image.open("fondo_registro.png")  # Cambia "fondo_registro.png" por la imagen que desees usar
    imagen_fondo_detalle = imagen_fondo_detalle.resize((1366, 768))  # Ajustar al tamaño de la ventana
    imagen_fondo_detalle = ImageTk.PhotoImage(imagen_fondo_detalle)
    fondo_detalle_label = tk.Label(ventana_registro, image=imagen_fondo_detalle)
    fondo_detalle_label.place(x=0, y=0, relwidth=1, relheight=1)

    nombre_usuario_entry_reg = tk.Entry(ventana_registro,bg="honeydew3")
    nombre_usuario_entry_reg.place(x=700, y=350)
    
    contraseña_entry_reg = tk.Entry(ventana_registro,bg="honeydew3", show="*")
    contraseña_entry_reg.place(x=715, y=450)

    def alternar_visibilidad_reg():
        if contraseña_entry_reg["show"] == "*":
            contraseña_entry_reg.config(show="")
            boton_alternar_reg.config(text="Ocultar")
        else:
            contraseña_entry_reg.config(show="*")
            boton_alternar_reg.config(image=imagen_ojito)

    boton_alternar_reg = tk.Button(ventana_registro, image=imagen_ojito, command=alternar_visibilidad_reg)
    boton_alternar_reg.place(x=895, y=455)

    tk.Button(ventana_registro, text="Registrarse", command=lambda: registrar(nombre_usuario_entry_reg.get(), contraseña_entry_reg.get(), "Cliente", ventana_registro)).place(x=680, y=550)

# Función para validar nombre de usuario
def validar_nombre_usuario(nombre_usuario):
    if len(nombre_usuario) < 3 or " " in nombre_usuario:
        return False
    return True

# Función para validar contraseña
def validar_contraseña(contraseña):
    if len(contraseña) < 8:
        return False
    if not re.search("[a-z]", contraseña):
        return False
    if not re.search("[A-Z]", contraseña):
        return False
    if not re.search("[0-9]", contraseña):
        return False
    return True

# Función para registrar un nuevo usuario
def registrar(nombre_usuario, contraseña, tipo_usuario, ventana_registro):
    if not nombre_usuario or not contraseña:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    if not validar_nombre_usuario(nombre_usuario):
        messagebox.showerror("Error", "El nombre de usuario debe tener al menos 3 caracteres y no contener espacios")
        return

    if not validar_contraseña(contraseña):
        messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número")
        return

    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)
        usuarios = datos.get("usuarios", {})
    else:
        datos = {"usuarios": {}}
        usuarios = datos["usuarios"]

    if nombre_usuario in usuarios:
        messagebox.showerror("Error", "El usuario ya existe")
    else:
        usuarios[nombre_usuario] = {"contraseña": contraseña, "tipo": tipo_usuario}
        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
        messagebox.showinfo("Éxito", "Registro exitoso")
        ventana_registro.destroy()
        ventana.deiconify()  # Mostrar nuevamente la ventana de inicio de sesión

# Función para alternar la visibilidad de la contraseña en la ventana de inicio de sesión
def alternar_visibilidad():
    if contraseña_entry["show"] == "*":
        contraseña_entry.config(show="")
        boton_alternar.config(text="Ocultar")
    else:
        contraseña_entry.config(show="*")
        boton_alternar.config(image=imagen_ojito)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Inicio de Sesión y Registro")
ventana.geometry("1366x768")

canvas = tk.Canvas(ventana, width=1366, height=768)
canvas.pack()

# Cargar la imagen de fondo para la ventana de inicio de sesión
imagen_fondo = Image.open("fondoo.jpg")  
imagen_fondo = imagen_fondo.resize((1366, 768))  
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)

rutaojito = "ojito.png"
imagen_ojito = Image.open(rutaojito)
imagen_ojito = imagen_ojito.resize((20, 20))
imagen_ojito = ImageTk.PhotoImage(imagen_ojito)

# Componentes de la ventana de inicio de sesión

nombre_usuario_entry = tk.Entry(ventana,bg="honeydew3")
nombre_usuario_entry.place(x=700, y=360)

contraseña_entry = tk.Entry(ventana, bg="honeydew3",show="*")
contraseña_entry.place(x=715, y=460)

tk.Label(ventana, text="Tipo de Usuario:").place(x=460, y=520)
tipo_usuario_var = tk.StringVar(value="Cliente")
tk.Radiobutton(ventana, text="Cliente", variable=tipo_usuario_var, value="Cliente").place(x=600, y=520)
tk.Radiobutton(ventana, text="Administrador", variable=tipo_usuario_var, value="Administrador").place(x=680, y=520)

boton_alternar = tk.Button(ventana, image=imagen_ojito, command=alternar_visibilidad)
boton_alternar.place(x=895, y=460)

boton_iniciar = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar.place(x=820, y=520)
boton_iniciar.bind("<Enter>", on_enter)
boton_iniciar.bind("<Leave>", on_leave)


tk.Label(ventana, text="No posees una cuenta?", bg="black", fg="white").place(x=640, y=610)
boton_registro = tk.Button(ventana, text="Registrarse", command=abrir_ventana_registro)
boton_registro.place(x=670, y=640)
boton_registro.bind("<Enter>", on_enter)
boton_registro.bind("<Leave>", on_leave)




ventana.mainloop()
