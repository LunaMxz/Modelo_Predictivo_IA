import streamlit as st

def mostrar_configuracion():

    st.title("⚙ Configuración")

    st.subheader("Preferencias del usuario")

    st.toggle("Recibir notificaciones por correo")

    st.toggle("Modo oscuro")

    st.selectbox(

        "Frecuencia de actualización",

        [
            "30 segundos",
            "1 minuto",
            "5 minutos"
        ]

    )

    st.button("Guardar cambios")