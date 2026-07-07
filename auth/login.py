import streamlit as st

def mostrar_login():

    st.title("🌱 Agroindustria")

    st.subheader("Sistema Inteligente de Monitoreo para Invernaderos")

    st.markdown("---")

    _, centro, _ = st.columns([1,2,1])

    with centro:

        correo = st.text_input("📧 Correo electrónico")

        password = st.text_input(
            "🔒 Contraseña",
            type="password"
        )

        if st.button(
            "Iniciar sesión",
            use_container_width=True
        ):

            if correo == "admin@gmail.com" and password == "1234":

                st.session_state.logueado = True
                st.rerun()

            else:

                st.error("Correo o contraseña incorrectos.")

        st.write("")

        st.markdown("---")

        if st.button(
            "Crear cuenta",
            use_container_width=True
        ):

            st.session_state.pagina = "registro"
            st.rerun()