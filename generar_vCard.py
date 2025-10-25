import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import os

# Función para generar el QR
def generate_contact_qr():
    first_name = entry_nombre_1.get()
    second_name = entry_nombre_2.get()
    last_name = entry_apellido.get()
    phone = entry_telefono.get()
    email = entry_email.get()
    org = entry_empresa.get()
    title = entry_cargo.get()
    website = entry_web.get()
    address = entry_direccion.get()
    city = entry_localidad.get()
    country = entry_pais.get()
    logo_path = logo_var.get()

    if not first_name or not last_name or not phone:
        messagebox.showerror("Error", "Los campos Nombre, Apellido y Teléfono son obligatorios.")
        return

    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{first_name} {second_name} {last_name}
N;CHARSET=UTF-8:{last_name};{first_name};{second_name};;
ORG:{org}
TITLE:{title}
TEL;TYPE=CELL:{phone}
EMAIL;TYPE=WORK:{email}
URL:{website}
ADR;TYPE=WORK:;;{address};{city};; ;{country}
END:VCARD"""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(),
        embeded_image_path=logo_path if os.path.exists(logo_path) else None
    )

    # Guardar el archivo
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        img.save(save_path)
        messagebox.showinfo("Éxito", f"QR guardado como:\n{save_path}")
        mostrar_qr(save_path)

# Función para mostrar vista previa
def mostrar_qr(ruta):
    try:
        img = Image.open(ruta)
        img = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_imagen_qr.config(image=img_tk)
        label_imagen_qr.image = img_tk
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar el QR.\n{str(e)}")

# Selección de logo
def seleccionar_logo():
    #archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    filetypes = (
        ("Imágenes PNG", "*.png"),
        ("Imágenes JPG", "*.jpg"),
        ("Imágenes JPEG", "*.jpeg"),
        ("Imágenes BMP", "*.bmp")
    )
    #archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png")])
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de imagen",
        filetypes=filetypes
    )
    if archivo:
        logo_var.set(archivo)
        label_logo.config(text=os.path.basename(archivo))

# Interfaz
root = tk.Tk()
root.title("Generador de QR de Contacto By JOSELUWEB SOLUCIONES")
root.configure(bg="#1974b0")

def crear_campo(label_text, row):
    label = tk.Label(root, text=label_text, bg="#1974b0", fg="white", anchor="w")
    label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(root, width=40)
    entry.grid(row=row, column=1, padx=10, pady=5)
    return entry

entry_nombre_1 = crear_campo("Primer Nombre:", 0)
entry_nombre_2 = crear_campo("Segundo Nombre:", 1)
entry_apellido = crear_campo("Apellido:", 2)
entry_telefono = crear_campo("Teléfono:", 3)
entry_email = crear_campo("Email:", 4)
entry_empresa = crear_campo("Empresa:", 5)
entry_cargo = crear_campo("Cargo:", 6)
entry_web = crear_campo("Sitio Web:", 7)
entry_direccion = crear_campo("Dirección:", 8)
entry_localidad = crear_campo("Localidad:", 9)
entry_pais = crear_campo("País:", 10)

# Selector de logo
logo_var = tk.StringVar()
tk.Label(root, text="Logo (opcional):", bg="#1974b0", fg="white").grid(row=11, column=0, padx=10, pady=5, sticky="w")
btn_logo = tk.Button(root, text="Seleccionar Logo", command=seleccionar_logo)
btn_logo.grid(row=11, column=1, padx=10, pady=5, sticky="w")
label_logo = tk.Label(root, text="", bg="#1974b0", fg="white")
label_logo.grid(row=12, column=1, sticky="w", padx=10)

# Botón de generación
btn_generar = tk.Button(root, text="Generar QR", command=generate_contact_qr, bg="white", fg="#1974b0", font=("Arial", 12, "bold"))
btn_generar.grid(row=13, column=0, columnspan=2, pady=20)

# Vista previa
label_imagen_qr = tk.Label(root, bg="#1974b0")
label_imagen_qr.grid(row=14, column=0, columnspan=2, pady=10)

root.mainloop()