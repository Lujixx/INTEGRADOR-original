import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as smg
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import os
import subprocess
import json

video_window = None  
ventana_butacas = None  
def abrir_menu():
    ventana.withdraw()
    subprocess.Popen(["python", "menu.py"])

def play_video(video_path):
    global video_window  
    clip = VideoFileClip(video_path)
    clip_resized = clip.resize(newsize=(1900, 1000))  
    video_window = clip_resized.preview()  
    clip.reader.close()

def stop_video_audio():
    pass  

def cerrar_video_window():
    global video_window, ventana_butacas  
    if video_window is not None:
        video_window.close()  
        video_window = None  
    cerrar_ventana_butacas()  

def cerrar_ventana_butacas():
    global ventana_butacas
    if ventana_butacas is not None:
        ventana_butacas.destroy()
        ventana_butacas = None

def volver_al_menu(ventana_actual):
    ventana_actual.destroy()
    ventana.deiconify()

def mostrar_pelicula(pelicula):
    global imagen_fondo_detalle, ventana_butacas  
    cerrar_ventana_butacas()  

    ventana_detalle = tk.Toplevel(ventana)
    ventana_detalle.title("Detalles de la Película")
    ventana_detalle.geometry("1000x1000")  
    ventana_detalle.configure(bg="black")
    ventana_detalle.attributes("-fullscreen", True)
    
    ancho_pantalla = ventana_detalle.winfo_screenwidth()
    alto_pantalla = ventana_detalle.winfo_screenheight()

    x = (ancho_pantalla - ventana_detalle.winfo_reqwidth()) // 4
    y = (alto_pantalla - ventana_detalle.winfo_reqheight()) // 35

    ventana_detalle.geometry("+%d+%d" % (x, y))

    imagen_fondo_detalle = Image.open("fondo.png")  
    imagen_fondo_detalle = imagen_fondo_detalle.resize((1920, 1080))  
    imagen_fondo_detalle = ImageTk.PhotoImage(imagen_fondo_detalle)
    fondo_detalle_label = tk.Label(ventana_detalle, image=imagen_fondo_detalle)
    fondo_detalle_label.place(x=0, y=0, relwidth=1, relheight=1)

    estilo = ttk.Style()
    estilo.configure("TLabel", background="black", foreground="white", font=("Helvetica", 16, "bold"))  
    ventana_detalle.option_add("*TLabel*highlightBackground", "gold")

    ventana_detalle.grab_set()
    ventana_detalle.transient(ventana)

    info_pelicula = {
        "Película 1": {
            "sinopsis": "garfiel\nHorario: 14:00 - 16:00\nSala: 1\n$1100",
            "video_path": "archivo/garfiel.mp4"
        },
        "Película 2": {
            "sinopsis": "harry potter 3\nHorario: 16:30 - 18:30\nSala: 2\n$1100",
            "video_path": "archivo/harry potter.mp4"
        },
        "Película 3": {
            "sinopsis": "patos\nHorario: 19:00 - 21:00\nSala: 3\n$1100",
            "video_path": "archivo/patos.mp4"
        },
        "Película 4": {
            "sinopsis": "paw patrol\nHorario: 22:00 - 00:00\nSala: 4\n$1100",
            "video_path": "archivo/paw.mp4"
        }
    }

    detalles = info_pelicula.get(pelicula, {
        "sinopsis": "Información no disponible"
    })

    titulo_label = ttk.Label(ventana_detalle, text=pelicula, style="TLabel")
    titulo_label.pack(pady=10)
    titulo_label.place(relx=0.5, rely=0.1, anchor="center")  

    detalles_label = ttk.Label(ventana_detalle, text=detalles["sinopsis"], style="TLabel")
    detalles_label.pack(pady=10)
    detalles_label.place(relx=0.5, rely=0.4, anchor="center")  

    video_path = detalles["video_path"]

    if os.path.exists(video_path):
        play_video(video_path)
    else:
        print("El video no se encontró en la ruta especificada.")
        smg.showerror("Error de Video", "El video no se encontró en la ruta especificada.")

    seleccionar_boton = tk.Button(ventana_detalle, text="Reservar Película", command=lambda peli=pelicula: preparar_butacas(pelicula))
    seleccionar_boton.pack(pady=10)
    seleccionar_boton.place(relx=0.5, rely=0.6, anchor="center")  

    boton_volver = tk.Button(ventana_detalle, text="Volver al Menú", command=lambda: volver_al_menu(ventana_detalle))
    boton_volver.pack(pady=10)
    boton_volver.place(relx=0.5, rely=0.7, anchor="center")  
    
    
imagen_fondo = None  # Variable global para almacenar la imagen de fondo


def preparar_butacas(pelicula):
    global ventana_butacas, imagen_fondo, estado_asientos, boton_asientos  # Asegurarse de que las variables importantes sean globales

    # Cerrar ventana de butacas si ya existe
    cerrar_ventana_butacas()

    # Crear la ventana de butacas
    ventana_butacas = tk.Toplevel(ventana)
    ventana_butacas.title("Selección de Butacas")
    ventana_butacas.attributes("-fullscreen", True)  # Adaptar ventana al tamaño de la pantalla
    ventana_butacas.configure(bg="black")

    # Cargar la imagen de fondo
    try:
        imagen_fondo = Image.open("fondo3.png")
        imagen_fondo = imagen_fondo.resize((ventana_butacas.winfo_screenwidth(), ventana_butacas.winfo_screenheight()))
        imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    except:
        print("Error al cargar la imagen de fondo.")
        return

    # Mostrar la imagen de fondo en un Label
    fondo_label = tk.Label(ventana_butacas, image=imagen_fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Determinar el número de filas y columnas de asientos
    num_filas = 5
    num_columnas = 10

    def toggle_estado_asiento(fila, columna):
        # Función para alternar el estado del asiento y cambiar el color del botón
        if estado_asientos[fila][columna] == "Disponible":
            estado_asientos[fila][columna] = "Seleccionado"
            boton_asientos[fila][columna].configure(bg="red")
        elif estado_asientos[fila][columna] == "Seleccionado":
            estado_asientos[fila][columna] = "Disponible"
            boton_asientos[fila][columna].configure(bg="green")

    def confirmar_reserva(pelicula):

        asientos_seleccionados = []
        for fila in range(num_filas):
            for columna in range(num_columnas):
                if estado_asientos[fila][columna] == "Seleccionado":
                    nombre_asiento = f"Fila {fila+1}, Asiento {columna+1}"  # Nombre del asiento
                    asientos_seleccionados.append(nombre_asiento)

        # Cargar datos previos de reservas si existen
        reservas_previas = []
        try:
            with open("comprobantevideo.json", "r") as file:
                reservas_previas = json.load(file)
        except FileNotFoundError:
            pass

        # Convertir a diccionario si es una lista vacía
        if isinstance(reservas_previas, list):
            reservas_previas = {}

        # Actualizar las reservas previas para la película actual
        reservas_previas[pelicula] = {"asientos": asientos_seleccionados}

        # Guardar las reservas actualizadas en el archivo
        with open("comprobantevideo.json", "w") as file:
            json.dump(reservas_previas, file, indent=2)

        # Actualizar el estado de los asientos seleccionados a "Reservado" y cambiar su color
        for fila in range(num_filas):
            for columna in range(num_columnas):
                if estado_asientos[fila][columna] == "Seleccionado":
                    estado_asientos[fila][columna] = "Reservado"
                    boton_asientos[fila][columna].configure(bg="gray", state=tk.DISABLED)

        # Mostrar mensaje de confirmación
        smg.showinfo("Reserva Confirmada", "Los asientos han sido reservados correctamente.")



    estado_asientos = [["Disponible" for _ in range(num_columnas)] for _ in range(num_filas)]
    boton_asientos = []

    for fila in range(num_filas):
        fila_botones = []
        for columna in range(num_columnas):
            estado_asiento = estado_asientos[fila][columna]
            color = "green"  # Por defecto, los asientos disponibles están en verde
            if estado_asiento == "Seleccionado":
                color = "blue"  # Si están seleccionados, en azul
            elif estado_asiento == "Reservado":
                color = "gray"  # Si están reservados, en gris
            boton_asiento = tk.Button(ventana_butacas, text=f"Fila {fila+1}, Asiento {columna+1}", bg=color,
                                      command=lambda f=fila, c=columna: toggle_estado_asiento(f, c))
            boton_asiento.grid(row=fila+1, column=columna, padx=5, pady=5)
            fila_botones.append(boton_asiento)
        boton_asientos.append(fila_botones)

    # Calcular posición para centrar los botones
    centro_fila = (num_filas + 1) // 2
    centro_columna = (num_columnas - 2) // 2  # Dejamos espacio para los botones de confirmar y cancelar

    boton_confirmar = tk.Button(ventana_butacas, text="Confirmar Reserva", command=lambda: confirmar_reserva(pelicula))
    boton_confirmar.grid(row=num_filas+2, column=centro_columna, pady=10, sticky="nsew")

    boton_volver = tk.Button(ventana_butacas, text="Cancelar", command=lambda: cerrar_ventana_butacas())
    boton_volver.grid(row=num_filas+3, column=centro_columna, pady=10, sticky="nsew")

    # Expandir filas y columnas para centrar los botones
    ventana_butacas.grid_rowconfigure(0, weight=1)
    ventana_butacas.grid_columnconfigure(0, weight=1)
    for i in range(num_filas + 1):
        ventana_butacas.grid_rowconfigure(i, weight=1)
    for j in range(num_columnas):
        ventana_butacas.grid_columnconfigure(j, weight=1)

    ventana_butacas.grab_set()






def cerrar_ventana_butacas():
    global ventana_butacas
    if ventana_butacas:
        ventana_butacas.destroy()




ventana = tk.Tk()
ventana.geometry("2000x4000") 
ventana.title("Cartelera de Cine")
ventana.attributes("-fullscreen", True)

imagen_fondo2 = Image.open("fondo2.png")
imagen_fondo2 = imagen_fondo2.resize((2000, 1100))
imagen_fondo2 = ImageTk.PhotoImage(imagen_fondo2)
fondo_label = tk.Label(ventana, image=imagen_fondo2)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

fuente_personalizada = ("Helvetica", 18, "bold")

imagen1 = Image.open("garfiel.png")
imagen1 = imagen1.resize((230, 280))  
imagen1 = ImageTk.PhotoImage(imagen1)

imagen2 = Image.open("harry potter.png")
imagen2 = imagen2.resize((230, 280))  
imagen2 = ImageTk.PhotoImage(imagen2)

imagen3 = Image.open("patos.png")
imagen3 = imagen3.resize((230, 280))  
imagen3 = ImageTk.PhotoImage(imagen3)

imagen4 = Image.open("paw.png")
imagen4 = imagen4.resize((230, 280))  
imagen4 = ImageTk.PhotoImage(imagen4)

foto1 = tk.Label(ventana, font=("Helvetica", 12, "bold"), image=imagen1, compound="top")
foto1.place(x=20, y=325)  

foto2 = tk.Label(ventana, font=("Helvetica", 12, "bold"), image=imagen2, compound="top")
foto2.place(x=1025, y=325)  

foto3 = tk.Label(ventana, font=("Helvetica", 12, "bold"), image=imagen3, compound="top")
foto3.place(x=20, y=700)  

foto4 = tk.Label(ventana, font=("Helvetica", 12, "bold"), image=imagen4, compound="top")
foto4.place(x=1025, y=700)

texto1 = tk.Label(ventana, text="Película 1: Garfiel", font=("Helvetica", 14, "bold"), fg="black", bg="white")
texto1.place(x=450, y=510)  

texto2 = tk.Label(ventana, text="Película 2:Harry Potter 3", font=("Helvetica", 14, "bold"), fg="black", bg="white")
texto2.place(x=1430, y=465)  

texto3 = tk.Label(ventana, text="Película 3:Patos", font=("Helvetica", 14, "bold"), fg="black", bg="white")
texto3.place(x=470, y=900)  

texto4 = tk.Label(ventana, text="Película 4:Paw Patrol", font=("Helvetica", 14, "bold"), fg="black", bg="white")
texto4.place(x=1450, y=850)  

boton1 = tk.Button(ventana, text="Trailer", command=lambda: mostrar_pelicula("Película 1"), font=("Helvetica", 12, "bold"))
boton1.place(x=490, y=550) 

boton2 = tk.Button(ventana, text="Trailer", command=lambda: mostrar_pelicula("Película 2"), font=("Helvetica", 12, "bold"))
boton2.place(x=1500, y=510)  

boton3 = tk.Button(ventana, text="Trailer", command=lambda: mostrar_pelicula("Película 3"), font=("Helvetica", 12, "bold"))
boton3.place(x=500, y=940)  

boton4 = tk.Button(ventana, text="Trailer", command=lambda: mostrar_pelicula("Película 4"), font=("Helvetica", 12, "bold"))
boton4.place(x=1500, y=890)  

boton = tk.Button(ventana, text="Salir",command=abrir_menu)
boton.place(x=10, y=1050) 

sinopsis1 = tk.Text(
    ventana,
    wrap=tk.WORD,
    width=40,
    height=7,
    font=("verdana", 14),
    fg="black",
    bg="white"
)
sinopsis1.insert("1.0", "SINOPSIS: El mundialmente famoso Garfield, el gato casero que odia los lunes y que adora la lasaña, está a punto de vivir una aventura ¡en el salvaje mundo exterior! Tras una inesperada reunión con su largamente perdido padre – el desaliñado gato callejero Vic – Garfield y su amigo canino Odie se ven forzados a abandonar sus perfectas y consentidas vidas al unirse a Vic en un hilarante y muy arriesgado atraco.\nFecha de estreno:  2 de mayo de 2024 (Argentina)\nDirector: Mark Dindal \nAño: 2024\nBasada en: The Equalizer\nGuion: Richard Wenk")
sinopsis1.config(state=tk.DISABLED)
sinopsis1.place(x=300, y=330)  

sinopsis2 = tk.Text(
    ventana,
    wrap=tk.WORD,
    width=40,
    height=5,
    font=("verdana", 14),
    fg="black",
    bg="white"
)
sinopsis2.insert("1.0", "SINOPSIS:El tercer año de estudios de Harry en Hogwarts se ve amenazado por la fuga de Sirius Black de la prisión para magos de Azkaban. Se trata de un peligroso mago que fue cómplice de Lord Voldemort y que intentará vengarse de Harry Potter.\nFecha de estreno: 6 de diciembre de 2023  (Argentina)\nDirector:  Benjamin Renner, Guylo Homsy\nAño: 2024")
sinopsis2.config(state=tk.DISABLED)
sinopsis2.place(x=1300, y=330)  

sinopsis3 = tk.Text(
    ventana,
    wrap=tk.WORD,
    width=45,
    height=7,
    font=("verdana", 14),
    fg="black",
    bg="white"
)
sinopsis3.insert("1.0", "SINOPSIS:La familia Mallard está estancada. Papá Mack mantiene a su familia a salvo nadando en un estanque para siempre, mientras que mamá Pam quiere cambiar las cosas y mostrar a sus hijos todo el mundo.\nFecha de estreno: 3 de junio de 2004 (Argentina)\nDirector:  Alfonso Cuarón\nAño: 2004")
sinopsis3.config(state=tk.DISABLED)
sinopsis3.place(x=300, y=740)  

sinopsis4 = tk.Text(
    ventana,
    wrap=tk.WORD,
    width=45,
    height=4,
    font=("verdana", 14),
    fg="black",
    bg="white"
)
sinopsis4.insert("1.0", "SINOPSIS: Cuando un meteorito mágico se estrella en Ciudad Aventura, los cachorros de la Patrulla Canina consiguen unos superpoderes que los transforman en Los poderosos cachorros. Ahora, se enfrentan a su mayor desafío cuando su archienemigo Humdinger escapa de la cárcel y se alía con Victoria Vance, una científica loca, para robárselos.\nFecha de estreno:21 de septiembre de 2023\nDirector: Callan Brunker")
sinopsis4.config(state=tk.DISABLED)
sinopsis4.place(x=1300, y=740)  

ventana.mainloop()
