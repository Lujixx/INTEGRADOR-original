import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import tkinter.messagebox as msg
import subprocess

archivo_comprobante = "comprobante.json"
archivo_stock = "stock.json"  

def cargar_stock():
    try:
        with open(archivo_stock, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def guardar_stock(stock):
    with open(archivo_stock, "w") as f:
        json.dump(stock, f, indent=4)

def cargar_carrito():
    try:
        with open(archivo_comprobante, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_carrito(carrito):
    try:
        with open(archivo_comprobante, "w") as f:
            json.dump(carrito, f, indent=4)
        print("Carrito guardado exitosamente:", carrito)
    except Exception as e:
        print("Error al guardar el carrito:", e)

def guardar_comprobante(comprobante):
    try:
        # Creamos una lista para almacenar la información de cada ítem del comprobante
        comprobante_info = []
        for item in comprobante:
            producto = item['producto']
            cantidad = item['cantidad']
            for combo_info in botones_combos:
                if combo_info[0] == producto:
                    precio_unitario = combo_info[3]
                    subtotal = precio_unitario * cantidad
                    # Creamos un diccionario con la información del ítem y lo agregamos a la lista
                    item_info = {
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'subtotal': subtotal
                    }
                    comprobante_info.append(item_info)

        # Guardamos la lista de información del comprobante en el archivo JSON
        with open(archivo_comprobante, "w") as f:
            json.dump(comprobante_info, f, indent=4)
        print("Comprobante guardado exitosamente:", comprobante_info)
    except Exception as e:
        print("Error al guardar el comprobante:", e)


def confirmar_reserva():
    carrito = cargar_carrito()
    stock = cargar_stock()

    for item in carrito:
        producto = item['producto']
        cantidad_reservada = item['cantidad']
        if producto in stock:
            stock[producto] -= cantidad_reservada
            if stock[producto] < 0:
                stock[producto] = 0  # No permitir cantidades negativas
        else:
            print(f"Error: El producto '{producto}' no está en el stock.")

    imprimir_ticket()
    limpiar_carrito()  # Limpiar el carrito después de confirmar las reservas
    # Primero guardamos el carrito vacío y luego el stock actualizado
    guardar_carrito([])
    guardar_stock(stock)
    guardar_comprobante(carrito)

def limpiar_carrito():
    guardar_carrito([])  # Guardar un carrito vacío

def imprimir_ticket():
    carrito = cargar_carrito()
    if not carrito:
        msg.showwarning("Aviso", "No hay productos en el carrito.")
        return

    ticket_content = "---- TICKET DE COMPRA ----\n\n"
    for item in carrito:
        if isinstance(item['producto'], str):
            ticket_content += f"{item['producto']} - Cantidad: {item['cantidad']}\n"
        else:
            msg.showerror("Error", "Los datos del carrito no son válidos.")
            return

    msg.showinfo("Ticket de compra", ticket_content)
    msg.showinfo("Ticket Impreso", "Se ha impreso el ticket con éxito")

# El resto del código permanece sin cambios


    ticket_content = "---- TICKET DE COMPRA ----\n\n"
    for item in carrito:
        if isinstance(item['producto'], str):
            ticket_content += f"{item['producto']} - Cantidad: {item['cantidad']}\n"
        else:
            msg.showerror("Error", "Los datos del carrito no son válidos.")
            return

    msg.showinfo("Ticket de compra", ticket_content)
    msg.showinfo("Ticket Impreso", "Se ha impreso el ticket con éxito")

def llamar_reserva():
    global carrito_window
    carrito_window = tk.Toplevel(ventana)
    carrito_window.title("Carrito de Compras")
    carrito_window.attributes("-fullscreen", True)

    screen_width = carrito_window.winfo_screenwidth()
    screen_height = carrito_window.winfo_screenheight()
    window_width = 1666
    window_height = 760
    x = (screen_width - window_width) // 24
    y = (screen_height - window_height) // 3

    carrito_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    global treeview
    treeview = ttk.Treeview(carrito_window, columns=("combo", "cantidad", "precio_unitario", "subtotal"))
    treeview.heading("#0", text="ID")
    treeview.heading("combo", text="Combo")
    treeview.heading("cantidad", text="Cantidad")
    treeview.heading("precio_unitario", text="Precio Unitario")
    treeview.heading("subtotal", text="Subtotal")
    treeview.pack(expand=True, fill="both")

    carrito = cargar_carrito()
    total = 0
    for i, combo in enumerate(carrito):
        for combo_info in botones_combos:
            if combo_info[0] == combo['producto']:
                precio_unitario = combo_info[3]
                subtotal = precio_unitario * combo['cantidad']
                total += subtotal
                treeview.insert("", "end", text=str(i), values=(combo['producto'], combo['cantidad'], f"${precio_unitario}", f"${subtotal}"))

    treeview.insert("", "end", text="Total", values=("", "", "", f"${total}"))

    boton_confirmar = tk.Button(carrito_window, text="Confirmar Reserva", command=confirmar_reserva)
    boton_confirmar.pack()

    boton_eliminar = tk.Button(carrito_window, text="Eliminar Seleccionado", command=eliminar_seleccionado)
    boton_eliminar.pack()

    boton_aumentar = tk.Button(carrito_window, text="+", command=aumentar_cantidad, font=("Helvetica", 12), width=2, height=1)
    boton_aumentar.place(x=330, y=300)

    boton_disminuir = tk.Button(carrito_window, text="-", command=disminuir_cantidad, font=("Helvetica", 12), width=2, height=1)
    boton_disminuir.place(x=360, y=300)

    boton_volver = tk.Button(carrito_window, text="Volver a la carta", command=volver_a_carta)
    boton_volver.pack()

    boton_actualizar = tk.Button(carrito_window, text="Actualizar Pantalla", command=actualizar_lista_carrito)
    boton_actualizar.pack()

def volver_a_carta():
    carrito_window.destroy()
    ventana.deiconify()
    
def salir():
    ventana.destroy()
    subprocess.Popen(["python", "menu.py"])
    
    
def eliminar_seleccionado():
    seleccion = treeview.selection()
    if not seleccion:
        msg.showwarning("Aviso", "No hay ningún producto seleccionado.")
        return

    carrito = cargar_carrito()
    id_seleccionado = seleccion[0]
    item_seleccionado = treeview.item(id_seleccionado)
    indice = int(item_seleccionado['text'])

    del carrito[indice]
    guardar_carrito(carrito)

    treeview.delete(id_seleccionado)
    actualizar_contador()

def aumentar_cantidad():
    seleccion = treeview.selection()
    if not seleccion:
        msg.showwarning("Aviso", "No hay ningún producto seleccionado.")
        return

    id_seleccionado = seleccion[0]
    item_seleccionado = treeview.item(id_seleccionado)
    indice = int(item_seleccionado['text'])
    carrito = cargar_carrito()
    carrito[indice]['cantidad'] += 1
    guardar_carrito(carrito)
    actualizar_lista_carrito()

def disminuir_cantidad():
    seleccion = treeview.selection()
    if not seleccion:
        msg.showwarning("Aviso", "No hay ningún producto seleccionado.")
        return

    id_seleccionado = seleccion[0]
    item_seleccionado = treeview.item(id_seleccionado)
    indice = int(item_seleccionado['text'])
    carrito = cargar_carrito()
    if carrito[indice]['cantidad'] > 1:
        carrito[indice]['cantidad'] -= 1
        guardar_carrito(carrito)
        actualizar_lista_carrito()
    else:
        msg.showwarning("Aviso", "La cantidad mínima es 1.")

def actualizar_lista_carrito():
    carrito_window.destroy()
    llamar_reserva()

def actualizar_contador():
    carrito = cargar_carrito()
    contador = sum(item['cantidad'] for item in carrito)
    contador_var.set(contador)

def agregar_carrito(combo):
    carrito = cargar_carrito()
    encontrado = False
    for item in carrito:
        if item['producto'] == combo:
            item['cantidad'] += 1
            encontrado = True
            break
    
    if not encontrado:
        carrito.append({"producto": combo, "cantidad": 1})
    guardar_carrito(carrito)
    msg.showinfo("Confirmación", message=f"El combo '{combo}' ha sido agregado al carrito")
    actualizar_contador()

def agregar_combo_a_carrito(combo):
    agregar_carrito(combo)

ventana = tk.Tk()
ventana.geometry("1920x1080")
ventana.title("*** CARTA DE TIENDA ***")
ventana.configure(bg="red")
ventana.attributes("-fullscreen", True)

fuente_personalizada = ("Helvetica", 18, "bold")

ruta_imagen1 = "fondo1.jpg"
imagen1 = Image.open(ruta_imagen1)
imagen1 = imagen1.resize((1920, 900))
imagen1 = ImageTk.PhotoImage(imagen1)

ruta_imagen_carrito = "carrito.jpg"
imagen_carrito = Image.open(ruta_imagen_carrito)
imagen_carrito = imagen_carrito.resize((80, 80))
imagen_carrito = ImageTk.PhotoImage(imagen_carrito)

ruta_imagen_volver = "volver.jpg"
imagen_volver = Image.open(ruta_imagen_volver)
imagen_volver = imagen_volver.resize((80, 80))
imagen_volver = ImageTk.PhotoImage(imagen_volver)

etiqueta1 = tk.Label(ventana, font=fuente_personalizada, image=imagen1, compound="top")
etiqueta1.place(x=0, y=0)

contador_var = tk.IntVar()
contador_label = tk.Label(ventana, textvariable=contador_var, font=("Helvetica", 18, "bold"), bg="red", fg="white")
contador_label.place(x=1850, y=50)
actualizar_contador()

boton_carrito = tk.Button(ventana, image=imagen_carrito, command=llamar_reserva, borderwidth=0)
boton_carrito.place(x=1750, y=50)

texto_carrito = tk.Label(ventana, text="Ver Carrito", font=("Helvetica", 12))
texto_carrito.place(x=1750, y=140)

boton_volver = tk.Button(ventana, command= salir ,image=imagen_volver, borderwidth=0)
boton_volver.place(x=1750, y=250)

botones_combos = [
    ("Combo película - Pow patrol", 900, 200, 13000),  
    ("Combo Premium - Patos", 1700, 200, 14500),      
    ("Combo Película - Garfield", 900, 500, 13000),  
    ("Combo Familia", 1700, 500, 16000),              
    ("Combo Duo", 900, 750, 9500),                    
    ("Fanta x 500ml", 1160, 750, 1200),                
    ("Sprite x 500ml", 1400, 750, 1200),              
    ("Coca-cola x 500ml", 1650, 750, 1200),         
    ("Pochoclo", 1950, 750, 2500)                  
]

for combo, x, y, precio in botones_combos:
    tk.Button(ventana, text="+", command=lambda c=combo: agregar_combo_a_carrito(c), font=fuente_personalizada).place(x=x - 100, y=y)

ventana.mainloop()
