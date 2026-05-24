import streamlit as st

import re

from urllib.parse import urlparse



# ---------------- CONFIG ---------------- #



st.set_page_config(

    page_title="ScamShield",

    page_icon="🛡",

    layout="centered"

)



# ---------------- TITULO ---------------- #



st.title("🛡 ScamShield")

st.subheader("Detector Anti Estafas para WhatsApp, SMS y Correos")



st.write(

    "Pega un mensaje sospechoso y ScamShield analizará "

    "si podría tratarse de phishing o fraude."

)



# ---------------- INPUT ---------------- #



mensaje = st.text_area(

    "Mensaje a analizar",

    height=220,

    placeholder="Pega aquí el mensaje sospechoso..."

)



# ---------------- BASE DE DATOS SIMPLE ---------------- #



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

    "código",

    "otp",

    "dinero",

    "bono",

    "regalo",

    "cuenta suspendida",

    "actualiza",

    "confirmar",

    "paypal",

    "bitcoin"

]



dominios_sospechosos = [

    ".xyz",

    ".ru",

    ".tk",

    ".top",

    ".click",

    ".gq"

]



# ---------------- ANALISIS ---------------- #



if st.button("Analizar Mensaje"):



    riesgo = 0

    razones = []



    texto = mensaje.lower()



    # Revisar palabras sospechosas

    for palabra in palabras_peligrosas:

        if palabra in texto:

            riesgo += 1

            razones.append(f"⚠ Palabra sospechosa detectada: '{palabra}'")



    # Buscar links

    urls = re.findall(r'https?://\S+|www\.\S+', mensaje)



    if urls:

        riesgo += 2

        razones.append("El mensaje contiene enlaces")



        for url in urls:



            dominio = urlparse(url).netloc



            for extension in dominios_sospechosos:



                if extension in dominio:

                    riesgo += 2

                    razones.append(

                        f" Dominio sospechoso detectado: {dominio}"

                    )



    # Exceso de mayúsculas

    if mensaje.isupper() and len(mensaje) > 15:

        riesgo += 2

        razones.append("Texto escrito completamente en MAYÚSCULAS")



    # Muchas exclamaciones

    if mensaje.count("!") >= 3:

        riesgo += 1

        razones.append( " Uso excesivo de signos de exclamación")



    # ---------------- RESULTADO ---------------- #



    st.divider()



    if riesgo >= 6:

        st.error(f" POSIBLE ESTAFA\n\nPuntaje de riesgo: {riesgo}")



    elif riesgo >= 3:

        st.warning(f" MENSAJE SOSPECHOSO\n\nPuntaje de riesgo: {riesgo}")



    else:

        st.success(f" MENSAJE SEGURO\n\nPuntaje de riesgo: {riesgo}")



    # ---------------- DETALLES ---------------- #



    st.subheader(" Detalles del análisis")



    if razones:

        for razon in razones:

            st.write(razon)

    else:

        st.write(" No se detectaron amenazas aparentes.")



# ---------------- FOOTER ---------------- #



st.divider()



st.caption("Proyecto de detección anti phishing hecho en Python ")
