import streamlit as st

def mostrar_registro():

    st.title("🌱 Agroindustria")

    st.subheader("Crear una cuenta")

    st.markdown("---")

    _, centro, _ = st.columns([1,2,1])

    with centro:

        nombre = st.text_input(
            "👤 Nombre completo"
        )

        correo = st.text_input(
            "📧 Correo electrónico"
        )

        password = st.text_input(
            "🔒 Contraseña",
            type="password"
        )

        confirmar = st.text_input(
            "🔒 Confirmar contraseña",
            type="password"
        )

        if st.button(
            "Crear cuenta",
            use_container_width=True
        ):

            if nombre == "":
                st.warning("Ingrese su nombre.")

            elif correo == "":
                st.warning("Ingrese un correo.")

            elif password == "":
                st.warning("Ingrese una contraseña.")

            elif password != confirmar:
                st.error("Las contraseñas no coinciden.")

            else:

                st.success("Cuenta creada correctamente.")

        st.markdown("---")

        st.write("¿Ya tienes cuenta?")

        if st.button(
            "Iniciar sesión",
            use_container_width=True
        ):

        #validar campos vacios
            if not nombre or not correo or not password or not confirmar:
            
                st.warning("Complete todos los campos")

                st.session_state.pagina = "login"

                st.rerun()

        #validar correo
            elif "@" not in correo or "." not in correo:

                st.error("Ingrese un correo electronico valido.")


        #validar longitud

            elif len(password) < 8:

                st.error("La contraseña debe tener al menos 8 caracteres.")

        #confirmar contrasena 
        # 

            elif password != confirmar: 

                st.error("Las contraseñas no coinsiden")

        #base de datos

            else:

                """
                crea_usuario(
                nombre,
                correo,
                password
                )
                """  

                st.success("cuenta creada correctamente")

                st.info("Ahora puedes iniciar sesión.")

                st.session_state.pagina = "login"

                st.rerun()

        st.markdown("---")

        st.write("Ya tienes cuenta?")

        if st.button(
            "Iniciar sesión",
            use_container_width=True
        ):

            st.session_state.pagina = "login"

            st.rerun()                      