import customtkinter as ctk
from tkinter import messagebox
import re
from urllib.parse import urlparse

# ---------------- CONFIG ---------------- #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- PALABRAS SOSPECHOSAS ---------------- #

palabras_peligrosas = [
    "ganaste",
    "premio",
    "urgente",
    "haz clic",
    "verifica",
    "contraseña",
    "banco",
    "transferencia",
    "bloqueada",
    "whatsapp support",
    "codigo",
    "otp",
    "dinero",
    "regalo",
    "cuenta suspendida"
]

dominios_sospechosos = [
    ".xyz",
    ".top",
    ".ru",
    ".tk"
]

# ---------------- FUNCIONES ---------------- #

def analizar_mensaje():

    mensaje = texto_input.get("1.0", "end").lower()

    riesgo = 0
    razones = []

    # Revisar palabras peligrosas
    for palabra in palabras_peligrosas:
        if palabra in mensaje:
            riesgo += 1
            razones.append(f"⚠ Contiene palabra sospechosa: {palabra}")

    # Detectar links
    urls = re.findall(r'https?://\S+|www\.\S+', mensaje)

    if urls:
        riesgo += 2
        razones.append("🔗 Contiene enlaces")

        for url in urls:
            dominio = urlparse(url).netloc

            for ext in dominios_sospechosos:
                if ext in dominio:
                    riesgo += 2
                    razones.append(f"🚨 Dominio sospechoso: {dominio}")

    # Detectar exceso de urgencia
    if mensaje.count("!") >= 3:
        riesgo += 1
        razones.append("❗ Uso excesivo de signos de exclamación")

    # Detectar mayúsculas exageradas
    if mensaje.upper() == mensaje and len(mensaje) > 15:
        riesgo += 2
        razones.append("📢 Texto completamente en MAYÚSCULAS")

    # Resultado final
    if riesgo >= 6:
        resultado = "🔴 POSIBLE ESTAFA"
        color = "#ff3b30"

    elif riesgo >= 3:
        resultado = "🟡 MENSAJE SOSPECHOSO"
        color = "#ffcc00"

    else:
        resultado = "🟢 MENSAJE SEGURO"
        color = "#34c759"

    resultado_label.configure(
        text=f"{resultado}\n\nPuntaje de riesgo: {riesgo}",
        text_color=color
    )

    detalles_text.configure(state="normal")
    detalles_text.delete("1.0", "end")

    if razones:
        for razon in razones:
            detalles_text.insert("end", razon + "\n")
    else:
        detalles_text.insert("end", "No se detectaron amenazas.")

    detalles_text.configure(state="disabled")


def limpiar():

    texto_input.delete("1.0", "end")

    resultado_label.configure(
        text="Esperando análisis...",
        text_color="white"
    )

    detalles_text.configure(state="normal")
    detalles_text.delete("1.0", "end")
    detalles_text.configure(state="disabled")


# ---------------- VENTANA ---------------- #

app = ctk.CTk()
app.title("ScamShield - Detector Anti Estafas")
app.geometry("750x600")

# ---------------- TITULO ---------------- #

titulo = ctk.CTkLabel(
    app,
    text="🛡 ScamShield",
    font=("Arial", 32, "bold")
)
titulo.pack(pady=15)

subtitulo = ctk.CTkLabel(
    app,
    text="Detector de mensajes sospechosos por SMS, Correo y WhatsApp",
    font=("Arial", 15)
)
subtitulo.pack(pady=5)

# ---------------- INPUT ---------------- #

texto_input = ctk.CTkTextbox(
    app,
    width=650,
    height=180,
    font=("Consolas", 14)
)
texto_input.pack(pady=20)

# ---------------- BOTONES ---------------- #

frame_botones = ctk.CTkFrame(app, fg_color="transparent")
frame_botones.pack(pady=10)

boton_analizar = ctk.CTkButton(
    frame_botones,
    text="🔍 Analizar",
    command=analizar_mensaje,
    width=160,
    height=40
)
boton_analizar.grid(row=0, column=0, padx=10)

boton_limpiar = ctk.CTkButton(
    frame_botones,
    text="🧹 Limpiar",
    command=limpiar,
    width=160,
    height=40,
    fg_color="#444"
)
boton_limpiar.grid(row=0, column=1, padx=10)

# ---------------- RESULTADO ---------------- #

resultado_label = ctk.CTkLabel(
    app,
    text="Esperando análisis...",
    font=("Arial", 24, "bold")
)
resultado_label.pack(pady=20)

# ---------------- DETALLES ---------------- #

detalles_text = ctk.CTkTextbox(
    app,
    width=650,
    height=140,
    font=("Consolas", 13)
)

detalles_text.pack(pady=10)
detalles_text.configure(state="disabled")

# ---------------- FOOTER ---------------- #

footer = ctk.CTkLabel(
    app,
    text="Proyecto Anti-Phishing en Python 🐍",
    font=("Arial", 12)
)
footer.pack(pady=10)

# ---------------- START ---------------- #

app.mainloop()