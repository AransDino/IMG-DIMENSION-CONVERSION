import os
import subprocess
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

# Función para seleccionar la carpeta
def seleccionar_carpeta():
    global carpeta
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con las fotos")
    if carpeta:
        print(f"Carpeta seleccionada: {carpeta}")
        button_listar.config(state="normal")

def listar_archivos():
    if not carpeta:
        print("No se ha seleccionado una carpeta.")
        return
    for item in tree.get_children():
        tree.delete(item)
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            tree.insert("", "end", values=(archivo, "Pendiente"))

def procesar_imagenes():
    if not carpeta:
        print("No se ha seleccionado una carpeta.")
        return
    referencia = entry_referencia.get()
    if not referencia:
        messagebox.showerror("Error", "Debes ingresar una referencia")
        return
    try:
        ancho = int(entry_ancho.get())
        alto = int(entry_alto.get())
    except ValueError:
        messagebox.showerror("Error", "Debes ingresar valores numéricos para el ancho y el alto")
        return
    carpeta_salida = os.path.join(carpeta, "FOTOS REDIMENSIONADAS")
    os.makedirs(carpeta_salida, exist_ok=True)
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            ruta_imagen = os.path.join(carpeta, archivo)
            ruta_salida = os.path.join(carpeta_salida, archivo)
            redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia)
            tree.insert("", "end", values=(archivo, "Procesado"))
            tree_detalles.insert("", "end", values=(f"Procesado: {archivo}"))

def redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia):
    with Image.open(ruta_imagen) as img:
        img = img.resize((ancho, alto), Image.LANCZOS)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40)
        texto = f"REF{referencia} - www.inmobiliariatias.com"
        text_width, text_height = draw.textbbox((0, 0), texto, font=font)[2:]
        position = ((ancho - text_width) // 2, alto - text_height - 10)
        draw.text(position, texto, fill="white", font=font)
        img.save(ruta_salida)

# Crear la interfaz gráfica
root = Tk()
root.title("Redimensionador de Imágenes")
root.geometry("800x800")
root.configure(bg="#F3F4F6")

# Estilo Moderno para la Interfaz
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=10, font=("Helvetica", 10, "bold"), background="#4F46E5", foreground="white")
style.map("TButton", background=[("active", "#3B82F6")])
style.configure("TLabel", font=("Helvetica", 10), background="#F3F4F6", foreground="#1F2937")
style.configure("TEntry", padding=8, font=("Helvetica", 10), relief="solid", borderwidth=1)

# Crear un Frame para Agrupar la Entrada de Datos
frame_inputs = ttk.Frame(root, padding=10)
frame_inputs.pack(pady=10, padx=20, fill="x")

label_referencia = ttk.Label(frame_inputs, text="Referencia:")
label_referencia.pack()
entry_referencia = ttk.Entry(frame_inputs)
entry_referencia.pack()

entry_ancho = ttk.Entry(frame_inputs)
entry_ancho.pack()
entry_ancho.insert(0, "1366")

entry_alto = ttk.Entry(frame_inputs)
entry_alto.pack()
entry_alto.insert(0, "1025")

button_seleccionar_carpeta = ttk.Button(frame_inputs, text="Seleccionar Carpeta", command=seleccionar_carpeta)
button_seleccionar_carpeta.pack()
button_listar = ttk.Button(frame_inputs, text="Listar Archivos", command=listar_archivos, state="disabled")
button_listar.pack()
button_procesar = ttk.Button(frame_inputs, text="Procesar Imágenes", command=procesar_imagenes)
button_procesar.pack()

# Crear Treeview para Mostrar Archivos
frame_tree = ttk.Frame(root, padding=10)
frame_tree.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tree, columns=("Archivo", "Estado"), show="headings")
tree.heading("Archivo", text="Archivo", anchor="w")
tree.heading("Estado", text="Estado", anchor="w")
tree.pack(pady=10, fill="both", expand=True)

# Crear el Treeview para mostrar la información detallada del procesamiento
frame_tree_detalles = ttk.Frame(root)
frame_tree_detalles.pack(pady=10, fill="both", expand=True)

tree_detalles = ttk.Treeview(frame_tree_detalles, columns=("Mensaje",), show="headings")
tree_detalles.heading("Mensaje", text="Mensaje", anchor="w")
tree_detalles.pack(pady=10, fill="both", expand=True)

# Ejecutar la Aplicación
root.mainloop()