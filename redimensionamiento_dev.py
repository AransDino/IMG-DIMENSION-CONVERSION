import os  # Import the os module to interact with the operating system
import subprocess  # Import the subprocess module to run system commands
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox  # Import tkinter modules for GUI
from tkinter import ttk  # Import ttk for themed widgets
from PIL import Image, ImageDraw, ImageFont  # Import PIL modules for image processing
import pkg_resources  # Import pkg_resources to access package resources

# Obtener la ruta absoluta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to resize images and add watermark and text
def redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia):
    mensaje = f"Redimensionando imagen: {ruta_imagen} a {ancho}x{alto}"  # Create a message string
    print(mensaje)  # Print the message to the console
    actualizar_grid_detalles(mensaje)  # Update the details grid with the message
    with Image.open(ruta_imagen) as img:  # Open the image file
        img = img.resize((ancho, alto), Image.LANCZOS)  # Resize the image
        
        # Add watermark with a centered image
        try:
            ruta_logo = pkg_resources.resource_filename(__name__, "assets/logo.png")  # Access the logo from the package
            with Image.open(ruta_logo).convert("RGBA") as logo:  # Open the logo file and convert to RGBA
                logo = logo.resize((ancho, alto), Image.LANCZOS)  # Resize the logo to match the image size
                logo = logo.copy()  # Create a copy of the logo
                logo.putalpha(int(255 * 0.15))  # Apply 15% opacity to the logo
                img.paste(logo, (0, 0), logo)  # Paste the logo onto the image
                mensaje = "Marca de agua agregada correctamente en el centro."  # Create a success message
                print(mensaje)  # Print the message to the console
                actualizar_grid_detalles(mensaje)  # Update the details grid with the message
        except Exception as e:  # Handle any exceptions
            mensaje = f"Error al agregar la marca de agua: {e}"  # Create an error message
            print(mensaje)  # Print the message to the console
            actualizar_grid_detalles(mensaje)  # Update the details grid with the message
        
        # Add text at the bottom with a larger font size
        draw = ImageDraw.Draw(img)  # Create a drawing context
        font = ImageFont.truetype("arial.ttf", 40)  # Load a TrueType font with size 40
        texto = f"REF{referencia} - www.inmobiliariatias.com"  # Create the text string
        text_width, text_height = draw.textbbox((0, 0), texto, font=font)[2:]  # Get the text size
        position = ((ancho - text_width) // 2, alto - text_height - 10)  # Calculate the text position
        draw.text(position, texto, fill="white", font=font)  # Draw the text on the image
        
        img.save(ruta_salida)  # Save the modified image
    mensaje = f"Imagen guardada en: {ruta_salida}"  # Create a success message
    print(mensaje)  # Print the message to the console
    actualizar_grid_detalles(mensaje)  # Update the details grid with the message
    
    # Add a separator line
    actualizar_grid_detalles("-------------------------------------")

# Function to select the folder
def seleccionar_carpeta():
    global carpeta  # Declare the global variable
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con las fotos")  # Open a folder selection dialog
    if carpeta:  # If a folder is selected
        print(f"Carpeta seleccionada: {carpeta}")  # Print the selected folder path
        verificar_entrada()  # Verify the input
        actualizar_estadisticas()  # Update the statistics
        actualizar_grid_inicial()  # Update the initial grid

# Function to verify the input
def verificar_entrada():
    if entry_referencia.get() and carpeta:  # If the reference entry and folder are not empty
        button_procesar.config(state="normal")  # Enable the process button
        button_listar.config(state="normal")  # Enable the list button
    else:
        button_procesar.config(state="disabled")  # Disable the process button
        button_listar.config(state="disabled")  # Disable the list button

# Function to update the statistical information
def actualizar_estadisticas():
    total_original = len([archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])  # Count the original images
    total_procesadas = len(os.listdir(carpeta_salida)) if os.path.exists(carpeta_salida) else 0  # Count the processed images
    label_total_original.config(text=f"Imágenes a procesar: {total_original}")  # Update the label with the total original images
    label_total_procesadas.config(text=f"Total imágenes procesadas: {total_procesadas}")  # Update the label with the total processed images
    root.update()  # Refresh the window

# Function to update the grid with the processed images information
def actualizar_grid(archivo, estado):
    tree.insert("", "end", values=(archivo, estado))  # Insert a new row in the treeview
    tree.yview_moveto(1)  # Scroll the treeview to the bottom
    root.update()  # Refresh the window

# Function to update the grid with the initial information of the images in the folder
def actualizar_grid_inicial():
    for item in tree.get_children():  # Clear the grid
        tree.delete(item)
    tree.insert("", "end", values=("Archivos a procesar", ""), tags=("header",))  # Add a header row
    for archivo in os.listdir(carpeta):  # Add information of the images in the folder
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            actualizar_grid(archivo, "Pendiente")  # Update the grid with the pending images
    actualizar_estadisticas()  # Update the statistics after listing the files

# Function to list the files in the grid
def listar_archivos():
    actualizar_grid_inicial()  # Update the initial grid

# Function to update the details grid with the processing information
def actualizar_grid_detalles(mensaje):
    tree_detalles.insert("", "end", values=(mensaje,))  # Insert a new row in the details treeview
    tree_detalles.yview_moveto(1)  # Scroll the treeview to the bottom
    root.update()  # Refresh the window

# Function to process the images in the folder
def procesar_imagenes():
    global carpeta_salida  # Declare the global variable
    if not carpeta:  # If no folder is selected
        print("No se seleccionó ninguna carpeta.")  # Print an error message
        return

    referencia = entry_referencia.get()  # Get the reference from the entry
    if not referencia:  # If no reference is entered
        messagebox.showerror("Error", "Debes ingresar una referencia")  # Show an error message
        print("Error: No se ingresó referencia.")  # Print an error message
        return

    try:
        ancho = int(entry_ancho.get())  # Get the width from the entry
        alto = int(entry_alto.get())  # Get the height from the entry
    except ValueError:  # If the width or height is not a valid number
        messagebox.showerror("Error", "Debes ingresar valores numéricos para el ancho y el alto")  # Show an error message
        print("Error: Valores de ancho y alto no válidos.")  # Print an error message
        return

    carpeta_salida = os.path.join(carpeta, "FOTOS REDIMENSIONADAS")  # Create the output folder path
    os.makedirs(carpeta_salida, exist_ok=True)  # Create the output folder if it doesn't exist
    print(f"Carpeta de salida creada: {carpeta_salida}")  # Print a success message

    tree.insert("", "end", values=("Archivos procesados", ""), tags=("header",))  # Add a header row for the processed files

    numerador = 1  # Initialize the counter
    for archivo in os.listdir(carpeta):  # Loop through the files in the folder
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # If the file is an image
            ruta_imagen = os.path.join(carpeta, archivo)  # Create the image path
            nombre_nuevo = f"{referencia}_{numerador}.jpg"  # Create the new image name
            ruta_salida = os.path.join(carpeta_salida, nombre_nuevo)  # Create the output image path
            mensaje = f"Procesando archivo: {archivo} -> {nombre_nuevo}"  # Create a processing message
            print(mensaje)  # Print the message to the console
            actualizar_grid_detalles(mensaje)  # Update the details grid with the message
            try:
                redimensionar_imagen(ruta_imagen, ancho, alto, ruta_salida, referencia)  # Resize the image
                actualizar_grid(archivo, "Procesado")  # Update the grid with the processed image
            except Exception as e:  # Handle any exceptions
                actualizar_grid(archivo, f"Error: {e}")  # Update the grid with the error message
                mensaje = f"Error al procesar la imagen: {e}"  # Create an error message
                print(mensaje)  # Print the message to the console
                actualizar_grid_detalles(mensaje)  # Update the details grid with the message
            numerador += 1  # Increment the counter
            actualizar_estadisticas()  # Update the statistics

    mensaje = "Proceso completado. Todas las imágenes han sido procesadas."  # Create a completion message
    print(mensaje)  # Print the message to the console
    actualizar_grid_detalles(mensaje)  # Update the details grid with the message
    messagebox.showinfo("Completado", mensaje)  # Show a completion message
    subprocess.Popen(f'explorer /select,"{carpeta_salida}"')  # Open the file explorer in the output folder
    mensaje = f"Explorador de archivos abierto en: {carpeta_salida}"  # Create a success message
    print(mensaje)  # Print the message to the console
    actualizar_grid_detalles(mensaje)  # Update the details grid with the message

# Function to exit the application
def salir():
    root.quit()  # Quit the application

# Create the graphical user interface
root = Tk()  # Create the main window
root.title("Redimensionador de Imágenes")  # Set the window title
root.geometry("1000x900")  # Set the window size

# Style (simulating Tailwind with ttkthemes)
style = ttk.Style()  # Create a style object
style.theme_use("clam")  # Apply the "clam" theme
style.configure("TButton", padding=6, relief="flat", background="orange", foreground="black")  # Set button style
style.map("TButton", background=[("active", "green")])  # Change button color to green when mouse is over
style.configure("Exit.TButton", padding=6, relief="flat", background="orange", foreground="black")  # Specific style for exit button
style.map("Exit.TButton", background=[("active", "red")])  # Change exit button color to red when mouse is over
style.configure("TLabel", padding=6, background="#F3F4F6", foreground="#1F2937")  # Set label style
style.configure("TEntry", padding=6, relief="flat", background="#E5E7EB", foreground="#1F2937")  # Set entry style
style.configure("TFrame", background="#F3F4F6", borderwidth=1, relief="solid")  # Set frame style
style.configure("Treeview", background="#FFFFFF", foreground="#1F2937", fieldbackground="#E5E7EB")  # Set treeview style
style.configure("Treeview.Heading", background="orange", foreground="black")  # Set treeview heading style

# Widgets
label_instrucciones = ttk.Label(root, text="Introduce una referencia y selecciona la carpeta:")  # Create an instructions label
label_instrucciones.pack(pady=10)  # Pack the label with padding

frame_inputs = ttk.Frame(root)  # Create a frame for the inputs
frame_inputs.pack(pady=5, fill="x")  # Pack the frame with padding and fill horizontally

frame_ancho_alto = ttk.Frame(frame_inputs, width=240)  # Create a frame for the width and height inputs
frame_ancho_alto.grid(row=0, column=0, padx=5, sticky="w")  # Grid the frame with padding

label_ancho = ttk.Label(frame_ancho_alto, text="Ancho:")  # Create a label for the width input
label_ancho.grid(row=0, column=0, padx=5)  # Grid the label with padding

entry_ancho = ttk.Entry(frame_ancho_alto)  # Create an entry for the width input
entry_ancho.grid(row=0, column=1, padx=5)  # Grid the entry with padding
entry_ancho.insert(0, "1366")  # Set a default value for the width

label_alto = ttk.Label(frame_ancho_alto, text="Alto:")  # Create a label for the height input
label_alto.grid(row=1, column=0, padx=5)  # Grid the label with padding

entry_alto = ttk.Entry(frame_ancho_alto)  # Create an entry for the height input
entry_alto.grid(row=1, column=1, padx=5)  # Grid the entry with padding
entry_alto.insert(0, "1025")  # Set a default value for the height

frame_referencia_botones = ttk.Frame(frame_inputs, width=560)  # Create a frame for the reference and buttons
frame_referencia_botones.grid(row=0, column=1, padx=5, sticky="w")  # Grid the frame with padding

frame_referencia_botones.columnconfigure(0, weight=1)  # Configure the column weight

label_referencia = ttk.Label(frame_referencia_botones, text="Referencia:")  # Create a label for the reference input
label_referencia.grid(row=0, column=0, padx=5, pady=5, sticky="ew")  # Grid the label with padding

entry_referencia = ttk.Entry(frame_referencia_botones)  # Create an entry for the reference input
entry_referencia.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Grid the entry with padding
entry_referencia.bind("<KeyRelease>", lambda event: verificar_entrada())  # Bind the entry to the verify input function

button_seleccionar_carpeta = ttk.Button(frame_referencia_botones, text="Seleccionar Carpeta", command=seleccionar_carpeta)  # Create a button to select the folder
button_seleccionar_carpeta.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="ew")  # Grid the button with padding

button_listar = ttk.Button(frame_referencia_botones, text="Listar Archivos", command=listar_archivos, state="disabled")  # Create a button to list the files
button_listar.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="ew")  # Grid the button with padding

button_procesar = ttk.Button(frame_referencia_botones, text="Procesar Imágenes", command=procesar_imagenes, state="disabled")  # Create a button to process the images
button_procesar.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="ew")  # Grid the button with padding

button_salir = ttk.Button(root, text="Salir", command=salir, style="Exit.TButton")  # Create a button to exit the application
button_salir.pack(pady=10)  # Pack the button with padding

label_total_original = ttk.Label(root, text="Imágenes a procesar: 0")  # Create a label for the total original images
label_total_original.pack(pady=5)  # Pack the label with padding

label_total_procesadas = ttk.Label(root, text="Total imágenes procesadas: 0")  # Create a label for the total processed images
label_total_procesadas.pack(pady=5)  # Pack the label with padding

# Create the Treeview to display the processed images information
frame_tree = ttk.Frame(root)  # Create a frame for the treeview
frame_tree.pack(pady=10, fill="both", expand=True)  # Pack the frame with padding and fill both directions

tree_scroll = ttk.Scrollbar(frame_tree)  # Create a scrollbar for the treeview
tree_scroll.pack(side="right", fill="y")  # Pack the scrollbar on the right side and fill vertically

tree = ttk.Treeview(frame_tree, columns=("Archivo", "Estado"), show="headings", yscrollcommand=tree_scroll.set)  # Create a treeview with columns
tree.heading("Archivo", text="Archivo", anchor="w")  # Set the heading for the "Archivo" column
tree.heading("Estado", text="Estado", anchor="w")  # Set the heading for the "Estado" column
tree.column("Archivo", width=200, stretch=True)  # Set the width and stretch property for the "Archivo" column
tree.column("Estado", width=100, stretch=True)  # Set the width and stretch property for the "Estado" column
tree.tag_configure("header", background="#D3D3D3", font=("Helvetica", 10, "bold"))  # Configure the header style
tree.pack(pady=10, fill="both", expand=True)  # Pack the treeview with padding and fill both directions

tree_scroll.config(command=tree.yview)  # Configure the scrollbar to control the treeview

# Create the Treeview to display the detailed processing information
frame_tree_detalles = ttk.Frame(root)  # Create a frame for the details treeview
frame_tree_detalles.pack(pady=10, fill="both", expand=True)  # Pack the frame with padding and fill both directions

tree_detalles_scroll = ttk.Scrollbar(frame_tree_detalles)  # Create a scrollbar for the details treeview
tree_detalles_scroll.pack(side="right", fill="y")  # Pack the scrollbar on the right side and fill vertically

tree_detalles = ttk.Treeview(frame_tree_detalles, columns=("Mensaje",), show="headings", yscrollcommand=tree_detalles_scroll.set)  # Create a details treeview with columns
tree_detalles.heading("Mensaje", text="Mensaje", anchor="w")  # Set the heading for the "Mensaje" column
tree_detalles.column("Mensaje", width=400, stretch=True)  # Set the width and stretch property for the "Mensaje" column
tree_detalles.pack(pady=10, fill="both", expand=True)  # Pack the details treeview with padding and fill both directions

tree_detalles_scroll.config(command=tree_detalles.yview)  # Configure the scrollbar to control the details treeview

# Run the application
print("Iniciando aplicación...")  # Print a message to the console
root.mainloop()  # Start the main event loop
