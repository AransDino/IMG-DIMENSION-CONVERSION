import os
import subprocess  # Add this import
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

# Función para redimensionar las imágenes y agregar marca de agua y texto
def redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia):
    print(f"Redimensionando imagen: {ruta_imagen} a {ancho}x{alto}")
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
                print("Marca de agua agregada correctamente en el centro.")
        except Exception as e:
            print(f"Error al agregar la marca de agua: {e}")
        
        # Agregar texto en la parte inferior con un tamaño de fuente más grande
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40)  # Aumentando el tamaño de la fuente
        texto = f"REF{referencia} - www.inmobiliariatias.com"
        text_width, text_height = draw.textbbox((0, 0), texto, font=font)[2:]
        position = ((ancho - text_width) // 2, alto - text_height - 10)
        draw.text(position, texto, fill="white", font=font)
        
        img.save(ruta_salida)
    print(f"Imagen guardada en: {ruta_salida}")

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
    root.update_idletasks()  # Actualizar la ventana

# Función para actualizar el grid con la información de las imágenes procesadas
def actualizar_grid(archivo, estado):
    tree.insert("", "end", values=(archivo, estado))

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

    # Crear la carpeta de salida dentro de la carpeta seleccionada
    carpeta_salida = os.path.join(carpeta, "FOTOS REDIMENSIONADAS")
    os.makedirs(carpeta_salida, exist_ok=True)
    print(f"Carpeta de salida creada: {carpeta_salida}")

    ancho = 1366  # Nueva resolución
    alto = 1025   # Nueva resolución

    # Añadir encabezado para los archivos procesados
    tree.insert("", "end", values=("Archivos procesados", ""), tags=("header",))

    numerador = 1
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            ruta_imagen = os.path.join(carpeta, archivo)
            nombre_nuevo = f"{referencia}_{numerador}.jpg"
            ruta_salida = os.path.join(carpeta_salida, nombre_nuevo)
            print(f"Procesando archivo: {archivo} -> {nombre_nuevo}")
            try:
                redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia)
                actualizar_grid(archivo, "Procesado")
            except Exception as e:
                actualizar_grid(archivo, f"Error: {e}")
            numerador += 1
            actualizar_estadisticas()

    print("Proceso completado. Todas las imágenes han sido procesadas.")
    messagebox.showinfo("Completado", "Todas las imágenes han sido procesadas y guardadas en 'FOTOS REDIMENSIONADAS'.")
    # Abrir el explorador de archivos en la carpeta de salida
    subprocess.Popen(f'explorer /select,"{carpeta_salida}"')
    print(f"Explorador de archivos abierto en: {carpeta_salida}")

    # Presentar el estado de las conversiones en formato de tabla
    presentar_estado_conversiones()

# Función para presentar el estado de las conversiones en formato de tabla
def presentar_estado_conversiones():
    # Limpiar el grid
    for item in tree.get_children():
        tree.delete(item)
    # Añadir encabezado para el estado de las conversiones
    tree.insert("", "end", values=("Archivo", "Estado"), tags=("header",))
    # Añadir información del estado de las conversiones
    for archivo in os.listdir(carpeta_salida):
        estado = "Procesado"
        actualizar_grid(archivo, estado)

# Función para salir de la aplicación
def salir():
    root.quit()

# Crear la interfaz gráfica
root = Tk()
root.title("Redimensionador de Imágenes")
root.geometry("600x800")

# Estilo (simulando Tailwind con ttkthemes)
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#4F46E5", foreground="black")  # Change 'foreground' to 'black'
style.configure("TLabel", padding=6, background="#F3F4F6", foreground="#1F2937")
style.configure("TEntry", padding=6, relief="flat", background="#E5E7EB", foreground="#1F2937")

# Widgets
label_instrucciones = ttk.Label(root, text="Introduce una referencia y selecciona la carpeta:")
label_instrucciones.pack(pady=10)

label_referencia = ttk.Label(root, text="Referencia:")
label_referencia.pack()

entry_referencia = ttk.Entry(root)
entry_referencia.pack(pady=5)
entry_referencia.bind("<KeyRelease>", lambda event: verificar_entrada())

button_seleccionar_carpeta = ttk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta)
button_seleccionar_carpeta.pack(pady=10)

button_listar = ttk.Button(root, text="Listar Archivos", command=listar_archivos, state="disabled")
button_listar.pack(pady=10)

button_procesar = ttk.Button(root, text="Procesar Imágenes", command=procesar_imagenes, state="disabled")
button_procesar.pack(pady=10)

label_total_original = ttk.Label(root, text="Imágenes a procesar: 0")
label_total_original.pack(pady=5)

label_total_procesadas = ttk.Label(root, text="Total imágenes procesadas: 0")
label_total_procesadas.pack(pady=5)

# Crear el Treeview para mostrar la información de las imágenes procesadas
tree = ttk.Treeview(root, columns=("Archivo", "Estado"), show="headings")
tree.heading("Archivo", text="Archivo")
tree.heading("Estado", text="Estado")
tree.tag_configure("header", background="#D3D3D3", font=("Helvetica", 10, "bold"))
tree.pack(pady=10, fill="both", expand=True)

button_salir = ttk.Button(root, text="Salir", command=salir)
button_salir.pack(pady=10)

# Ejecutar la aplicación
print("Iniciando aplicación...")
root.mainloop()
