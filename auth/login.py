import streamlit as st

from auth.sesion import validar_usuario


def mostrar_login():

    st.title("🌱 Agroindustria")

    st.subheader(
        "Sistema Inteligente de Monitoreo para Invernaderos"
    )

    st.markdown("---")

    _, centro, _ = st.columns([1,2,1])

    with centro:

        correo = st.text_input(
            "📧 Correo electrónico"
        )

        password = st.text_input(

            "🔒 Contraseña",

            type="password"

        )

        if st.button(

            "Iniciar sesión",

            use_container_width=True

        ):

            usuario = validar_usuario(

                correo,

                password

            )

            if usuario:

                st.session_state.logueado = True

                st.session_state.usuario = usuario

                st.success("Bienvenido")

                st.rerun()

            else:

                st.error(
                    "Correo o contraseña incorrectos."
                )

        st.markdown("---")

        if st.button(

            "Crear cuenta",

            use_container_width=True

        ):

            st.session_state.pagina = "registro"

            st.rerun()