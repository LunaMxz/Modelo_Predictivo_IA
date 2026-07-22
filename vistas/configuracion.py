import streamlit as st

from auth.sesion import obtener_usuarios, actualizar_rol, ROLES_DISPONIBLES
from utils.notificaciones import cargar_preferencias, guardar_preferencias, enviar_correo


def mostrar_configuracion():

    usuario = st.session_state.get("usuario")

    st.title("⚙ Configuración")

    # Ocultar el botón en el header no es suficiente: verificamos el
    # permiso aquí también, por si alguien llega a esta vista de otra forma.
    if usuario is None or usuario.get("rol") != "Dueño":

        st.error(
            "No tienes permisos para ver esta sección. "
            "Solo el Dueño puede acceder a la configuración."
        )

        return

    st.subheader("Preferencias del usuario")

    preferencias = cargar_preferencias()

    activo = st.toggle(
        "Recibir notificaciones por correo",
        value=preferencias["activo"],
    )

    correo_destino = st.text_input(
        "Correo para recibir alertas",
        value=preferencias["correo_destino"] or usuario["correo"],
        disabled=not activo,
    )

    st.toggle("Modo oscuro")

    st.selectbox(

        "Frecuencia de actualización",

        [
            "30 segundos",
            "1 minuto",
            "5 minutos"
        ]

    )

    if st.button("Guardar cambios"):

        preferencias["activo"] = activo
        preferencias["correo_destino"] = correo_destino

        guardar_preferencias(preferencias)

        st.success("Preferencias guardadas.")

    if st.button("📧 Enviar correo de prueba", disabled=not correo_destino):

        exito, detalle = enviar_correo(
            correo_destino,
            "🌱 Correo de prueba -- Agroindustria",
            "Si estás leyendo esto, las notificaciones por correo están "
            "configuradas correctamente.\n\n— Sistema de monitoreo Agroindustria",
        )

        if exito:
            st.success("Correo de prueba enviado. Revisa tu bandeja de entrada (y spam).")
        else:
            st.error(f"No se pudo enviar: {detalle}")

    st.divider()

    # =====================================
    # GESTIÓN DE ROLES (solo visible para el Dueño)
    # =====================================

    st.subheader("👥 Gestión de usuarios")

    st.caption(
        "Como Dueño, puedes cambiar el rol de cada persona con acceso al sistema."
    )

    usuarios = obtener_usuarios()

    for u in usuarios:

        col1, col2, col3 = st.columns([3, 3, 2])

        with col1:

            st.write(f"**{u['nombre']}**")

            st.caption(u["correo"])

        with col2:

            indice_actual = (
                ROLES_DISPONIBLES.index(u["rol"])
                if u["rol"] in ROLES_DISPONIBLES
                else 0
            )

            if u["rol"] not in ROLES_DISPONIBLES:

                st.caption(f"⚠ Rol guardado antiguo: '{u['rol']}'. Elige uno nuevo y guarda.")

            nuevo_rol = st.selectbox(

                "Rol",

                ROLES_DISPONIBLES,

                index=indice_actual,

                key=f"rol_{u['id']}",

                label_visibility="collapsed",

            )

        with col3:

            if st.button(
                "Guardar",
                key=f"guardar_{u['id']}",
                use_container_width=True
            ):

                if actualizar_rol(u["id"], nuevo_rol):

                    st.success(f"Rol actualizado para {u['nombre']}.")

                    st.rerun()

                else:

                    st.error("No se pudo actualizar el rol.")

        st.divider()