# Instalación necesaria:
pip install streamlit segno pillow
import streamlit as st
import segno
import io
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Generador QR Pro", page_icon="🚀")

st.title("🛠️ Generador de QR Multifuncional")
st.write("Selecciona el tipo de QR que deseas crear y personalízalo.")

# 1. Barra lateral para opciones de tipo
opcion = st.sidebar.selectbox(
    "¿Qué tipo de QR necesitas?",
    ("Enlace / Texto", "Wi-Fi", "vCard (Contacto)", "Redes Sociales")
)

# 2. Personalización de colores
color_qr = st.sidebar.color_picker("Color del QR", "#2c3e50")
color_fondo = st.sidebar.color_picker("Color de fondo", "#ffffff")

qr_final = None

# --- LÓGICA POR TIPO ---

if opcion == "Enlace / Texto":
    contenido = st.text_input("Introduce el link o texto:")
    if contenido:
        qr_final = segno.make(contenido, error='h')

elif opcion == "Wi-Fi":
    ssid = st.text_input("Nombre de la red (SSID):")
    password = st.text_input("Contraseña:", type="password")
    seguridad = st.selectbox("Seguridad", ["WPA", "WEP", "None"])
    if ssid:
        qr_final = segno.make_wifi(ssid=ssid, password=password, security=seguridad)

elif opcion == "vCard (Contacto)":
    nombre = st.text_input("Nombre completo:")
    email = st.text_input("Email:")
    tel = st.text_input("Teléfono:")
    if nombre:
        qr_final = segno.make_vcard(name=nombre, email=email, displayname=nombre, phone=tel)

elif opcion == "Redes Sociales":
    red = st.selectbox("Red Social", ["Instagram", "WhatsApp", "YouTube"])
    user = st.text_input(f"Usuario o número de {red}:")
    if user:
        links = {
            "Instagram": f"https://instagram.com/{user}",
            "WhatsApp": f"https://wa.me/{user}",
            "YouTube": f"https://youtube.com/@{user}"
        }
        qr_final = segno.make(links[red], error='h')

# --- RENDERIZADO Y DESCARGA ---

if qr_final:
    # Guardar en un buffer de memoria para mostrarlo sin guardar archivos locales
    buf = io.BytesIO()
    qr_final.save(buf, kind='png', scale=10, dark=color_qr, light=color_fondo)
    
    st.image(buf.getvalue(), caption="Tu código QR generado")
    
    st.download_button(
        label="📥 Descargar Imagen QR",
        data=buf.getvalue(),
        file_name="mi_codigo_qr.png",
        mime="image/png"
    )