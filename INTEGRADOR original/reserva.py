import tkinter as tk
from tkinter import ttk
import json
import tkinter.messagebox as msg

archivo_comprobante = "comprobante.json"

def cargar_carrito():
    try:
        with open(archivo_comprobante, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def actualizar_contador():
    carrito = cargar_carrito()
    contador_var.set(len(carrito))

def imprimir_ticket():
    carrito = cargar_carrito()
    if not carrito:
        msg.showwarning("Aviso", "No hay productos en el carrito.")
        return
    
    ticket_content = "---- TICKET DE COMPRA ----\n\n"
    total = 0
    for item in carrito:
        if isinstance(item, dict) and 'producto' in item and 'cantidad' in item and 'precio' in item:
            subtotal = item['cantidad'] * item['precio']
            ticket_content += f"{item['producto']} - Cantidad: {item['cantidad']} - Precio: {item['precio']} - Subtotal: {subtotal}\n"
            total += subtotal
        else:
            msg.showerror("Error", "Los datos del carrito no son válidos.")
            return
    
    ticket_content += f"\nTotal: {total}"
    
    msg.showinfo("Ticket de compra", ticket_content)
    msg.showinfo("Ticket Impreso", "Se ha impreso el ticket con éxito")

def confirmar_reserva():
    imprimir_ticket()

carrito_window = tk.Tk()
carrito_window.title("*** CARRITO DE COMPRA ***")
carrito_window.geometry("600x400")

# Crear el Treeview
treeview = ttk.Treeview(carrito_window, columns=("combo", "cantidad", "precio"))
treeview.heading("#0", text="ID")
treeview.heading("combo", text="Combo")
treeview.heading("cantidad", text="Cantidad")
treeview.heading("precio", text="Precio")
treeview.pack(expand=True, fill="both")

# Cargar carrito y agregar elementos al Treeview
carrito = cargar_carrito()
for i, item in enumerate(carrito):
    if 'precio' not in item:
        # Si no hay precio, asumimos un precio de 0
        item['precio'] = 0
    treeview.insert("", "end", text=str(i), values=(item.get("producto", ""), item.get("cantidad", ""), item.get("precio", "")))

boton_confirmar = tk.Button(carrito_window, text="Confirmar Reserva", command=confirmar_reserva)
boton_confirmar.pack()

boton_actualizar = tk.Button(carrito_window, text="Actualizar Carrito", command=actualizar_contador)
boton_actualizar.pack()

# Definir contador_var antes de usarla
contador_var = tk.IntVar()
actualizar_contador()  # Actualizar el contador cuando se inicia la aplicación

carrito_window.mainloop()
