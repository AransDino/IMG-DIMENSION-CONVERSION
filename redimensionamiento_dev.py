import os
import subprocess  # Add this import
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

# Función para redimensionar las imágenes y agregar marca de agua y texto
def redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia):
    mensaje = f"Redimensionando imagen: {ruta_imagen} a {ancho}x{alto}"
    print(mensaje)
    actualizar_grid_detalles(mensaje)
    with Image.open(ruta_imagen) as img:
        img = img.resize((ancho, alto), Image.LANCZOS)
        
        # Agregar marca de agua con una imagen centrada
        try:
            ruta_logo = "logo.png"  # Asegurar que el logo está en el mismo directorio
            with Image.open(ruta_logo).convert("RGBA") as logo:
                # Redimensionar el logo para que tenga el mismo tamaño que la imagen de fondo
                logo = logo.resize((ancho, alto), Image.LANCZOS)
                
                # Aplicar transparencia
                logo = logo.copy()
                logo.putalpha(int(255 * 0.15))  # 10% de opacidad
                
                # Combinar la imagen con el logo centrado
                img.paste(logo, (0, 0), logo)
                mensaje = "Marca de agua agregada correctamente en el centro."
                print(mensaje)
                actualizar_grid_detalles(mensaje)
        except Exception as e:
            mensaje = f"Error al agregar la marca de agua: {e}"
            print(mensaje)
            actualizar_grid_detalles(mensaje)
        
        # Agregar texto en la parte inferior con un tamaño de fuente más grande
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40)  # Aumentando el tamaño de la fuente
        texto = f"REF{referencia} - www.inmobiliariatias.com"
        text_width, text_height = draw.textbbox((0, 0), texto, font=font)[2:]
        position = ((ancho - text_width) // 2, alto - text_height - 10)
        draw.text(position, texto, fill="white", font=font)
        
        img.save(ruta_salida)
    mensaje = f"Imagen guardada en: {ruta_salida}"
    print(mensaje)
    actualizar_grid_detalles(mensaje)

# Función para seleccionar la carpeta
def seleccionar_carpeta():
    global carpeta
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con las fotos")
    if carpeta:
        print(f"Carpeta seleccionada: {carpeta}")
        verificar_entrada()
        actualizar_estadisticas()
        actualizar_grid_inicial()

# Función para verificar la entrada
def verificar_entrada():
    if entry_referencia.get() and carpeta:
        button_procesar.config(state="normal")
        button_listar.config(state="normal")
    else:
        button_procesar.config(state="disabled")
        button_listar.config(state="disabled")

# Función para actualizar la información estadística
def actualizar_estadisticas():
    total_original = len([archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
    total_procesadas = len(os.listdir(carpeta_salida)) if os.path.exists(carpeta_salida) else 0
    label_total_original.config(text=f"Imágenes a procesar: {total_original}")
    label_total_procesadas.config(text=f"Total imágenes procesadas: {total_procesadas}")
    root.update()  # Actualizar la ventana

# Función para actualizar el grid con la información de las imágenes procesadas
def actualizar_grid(archivo, estado):
    tree.insert("", "end", values=(archivo, estado))
    tree.yview_moveto(1)  # Hace que el Treeview haga scroll automático
    root.update()  # Asegura que la UI se refresque completamente

# Función para actualizar el grid con la información inicial de las imágenes en la carpeta
def actualizar_grid_inicial():
    # Limpiar el grid
    for item in tree.get_children():
        tree.delete(item)
    # Añadir encabezado para los archivos a procesar
    tree.insert("", "end", values=("Archivos a procesar", ""), tags=("header",))
    # Añadir información de las imágenes en la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            actualizar_grid(archivo, "Pendiente")
    # Actualizar estadísticas después de listar los archivos
    actualizar_estadisticas()

# Función para listar los archivos en el grid
def listar_archivos():
    actualizar_grid_inicial()

# Función para actualizar el grid de detalles del procesamiento
def actualizar_grid_detalles(mensaje):
    tree_detalles.insert("", "end", values=(mensaje,))
    tree_detalles.yview_moveto(1)  # Scroll automático
    root.update()  # Actualizar la ventana

# Función para procesar las imágenes en la carpeta
def procesar_imagenes():
    global carpeta_salida
    if not carpeta:
        print("No se seleccionó ninguna carpeta.")
        return

    referencia = entry_referencia.get()
    if not referencia:
        messagebox.showerror("Error", "Debes ingresar una referencia")
        print("Error: No se ingresó referencia.")
        return

    # Obtener los valores de ancho y alto ingresados por el usuario
    try:
        ancho = int(entry_ancho.get())
        alto = int(entry_alto.get())
    except ValueError:
        messagebox.showerror("Error", "Debes ingresar valores numéricos para el ancho y el alto")
        print("Error: Valores de ancho y alto no válidos.")
        return

    # Crear la carpeta de salida dentro de la carpeta seleccionada
    carpeta_salida = os.path.join(carpeta, "FOTOS REDIMENSIONADAS")
    os.makedirs(carpeta_salida, exist_ok=True)
    print(f"Carpeta de salida creada: {carpeta_salida}")

    # Añadir encabezado para los archivos procesados
    tree.insert("", "end", values=("Archivos procesados", ""), tags=("header",))

    numerador = 1
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            ruta_imagen = os.path.join(carpeta, archivo)
            nombre_nuevo = f"{referencia}_{numerador}.jpg"
            ruta_salida = os.path.join(carpeta_salida, nombre_nuevo)
            mensaje = f"Procesando archivo: {archivo} -> {nombre_nuevo}"
            print(mensaje)
            actualizar_grid_detalles(mensaje)
            try:
                redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia)
                actualizar_grid(archivo, "Procesado")
            except Exception as e:
                actualizar_grid(archivo, f"Error: {e}")
                mensaje = f"Error al procesar la imagen: {e}"
                print(mensaje)
                actualizar_grid_detalles(mensaje)
            numerador += 1
            actualizar_estadisticas()

    mensaje = "Proceso completado. Todas las imágenes han sido procesadas."
    print(mensaje)
    actualizar_grid_detalles(mensaje)
    messagebox.showinfo("Completado", mensaje)
    # Abrir el explorador de archivos en la carpeta de salida
    subprocess.Popen(f'explorer /select,"{carpeta_salida}"')
    mensaje = f"Explorador de archivos abierto en: {carpeta_salida}"
    print(mensaje)
    actualizar_grid_detalles(mensaje)

# Función para salir de la aplicación
def salir():
    root.quit()

# Crear la interfaz gráfica
root = Tk()
root.title("Redimensionador de Imágenes")
root.geometry("800x800")  # Change dimensions to 800x800

# Estilo (simulando Tailwind con ttkthemes)
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4F46E5", foreground="black")  # Change 'foreground' to 'black'
style.configure("TLabel", padding=6, background="#F3F4F6", foreground="#1F2937")
style.configure("TEntry", padding=6, relief="flat", background="#E5E7EB", foreground="#1F2937")

# Widgets
label_instrucciones = ttk.Label(root, text="Introduce una referencia y selecciona la carpeta:")
label_instrucciones.pack(pady=10)

frame_inputs = ttk.Frame(root)
frame_inputs.pack(pady=5, fill="x")

frame_ancho_alto = ttk.Frame(frame_inputs, width=240, relief="solid", borderwidth=1)  # 30% of 800px with border
frame_ancho_alto.grid(row=0, column=0, padx=5, sticky="w")

label_ancho = ttk.Label(frame_ancho_alto, text="Ancho:")
label_ancho.grid(row=0, column=0, padx=5)

entry_ancho = ttk.Entry(frame_ancho_alto)
entry_ancho.grid(row=0, column=1, padx=5)
entry_ancho.insert(0, "1366")  # Valor por defecto

label_alto = ttk.Label(frame_ancho_alto, text="Alto:")
label_alto.grid(row=1, column=0, padx=5)

entry_alto = ttk.Entry(frame_ancho_alto)
entry_alto.grid(row=1, column=1, padx=5)
entry_alto.insert(0, "1025")  # Valor por defecto

frame_referencia_botones = ttk.Frame(frame_inputs, width=560, relief="solid", borderwidth=1)  # 70% of 800px with border
frame_referencia_botones.grid(row=0, column=1, padx=5, sticky="w")

frame_referencia_botones.columnconfigure(0, weight=1)

label_referencia = ttk.Label(frame_referencia_botones, text="Referencia:")
label_referencia.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

entry_referencia = ttk.Entry(frame_referencia_botones)
entry_referencia.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_referencia.bind("<KeyRelease>", lambda event: verificar_entrada())

button_seleccionar_carpeta = ttk.Button(frame_referencia_botones, text="Seleccionar Carpeta", command=seleccionar_carpeta)
button_seleccionar_carpeta.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

button_listar = ttk.Button(frame_referencia_botones, text="Listar Archivos", command=listar_archivos, state="disabled")
button_listar.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

button_procesar = ttk.Button(frame_referencia_botones, text="Procesar Imágenes", command=procesar_imagenes, state="disabled")
button_procesar.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

button_salir = ttk.Button(root, text="Salir", command=salir)
button_salir.pack(pady=10)

label_total_original = ttk.Label(root, text="Imágenes a procesar: 0")
label_total_original.pack(pady=5)

label_total_procesadas = ttk.Label(root, text="Total imágenes procesadas: 0")
label_total_procesadas.pack(pady=5)

# Crear el Treeview para mostrar la información de las imágenes procesadas
frame_tree = ttk.Frame(root)
frame_tree.pack(pady=10, fill="both", expand=True)

tree_scroll = ttk.Scrollbar(frame_tree)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(frame_tree, columns=("Archivo", "Estado"), show="headings", yscrollcommand=tree_scroll.set)
tree.heading("Archivo", text="Archivo", anchor="w")
tree.heading("Estado", text="Estado", anchor="w")
tree.column("Archivo", width=200, stretch=True)
tree.column("Estado", width=100, stretch=True)
tree.tag_configure("header", background="#D3D3D3", font=("Helvetica", 10, "bold"))
tree.pack(pady=10, fill="both", expand=True)

tree_scroll.config(command=tree.yview)

# Crear el Treeview para mostrar la información detallada del procesamiento
frame_tree_detalles = ttk.Frame(root)
frame_tree_detalles.pack(pady=10, fill="both", expand=True)

tree_detalles_scroll = ttk.Scrollbar(frame_tree_detalles)
tree_detalles_scroll.pack(side="right", fill="y")

tree_detalles = ttk.Treeview(frame_tree_detalles, columns=("Mensaje",), show="headings", yscrollcommand=tree_detalles_scroll.set)
tree_detalles.heading("Mensaje", text="Mensaje", anchor="w")
tree_detalles.column("Mensaje", width=400, stretch=True)
tree_detalles.pack(pady=10, fill="both", expand=True)

tree_detalles_scroll.config(command=tree_detalles.yview)

# Ejecutar la aplicación
print("Iniciando aplicación...")
root.mainloop()
