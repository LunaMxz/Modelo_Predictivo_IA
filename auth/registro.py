import streamlit as st

from auth.sesion import registrar_usuario


def mostrar_registro():

    st.title("📝 Crear cuenta")

    st.markdown("---")

    _, centro, _ = st.columns([1, 2, 1])

    with centro:

        nombre = st.text_input(
            "Nombre completo"
        )

        correo = st.text_input(
            "Correo electrónico"
        )

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        confirmar = st.text_input(
            "Confirmar contraseña",
            type="password"
        )

        if st.button(
            "Registrarse",
            use_container_width=True
        ):

            if nombre == "":

                st.warning("Ingrese un nombre.")

            elif correo == "":

                st.warning("Ingrese un correo.")

            elif password == "":

                st.warning("Ingrese una contraseña.")

            elif password != confirmar:

                st.error("Las contraseñas no coinciden.")

            else:

                if registrar_usuario(
                    nombre,
                    correo,
                    password
                ):

                    st.success(
                        "Usuario registrado correctamente."
                    )

                    st.session_state.pagina = "login"

                    st.rerun()

                else:

                    st.error(
                        "Ese correo ya está registrado."
                    )

        st.markdown("---")

        if st.button(
            "Volver al Login",
            use_container_width=True
        ):

            st.session_state.pagina = "login"

            st.rerun()