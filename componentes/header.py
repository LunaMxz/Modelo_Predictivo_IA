import streamlit as st
from datetime import datetime

def mostrar_header():

    usuario = st.session_state.get("usuario")

    if usuario is None:
        return

    nombre = usuario["nombre"]
    correo = usuario["correo"]
    rol = usuario["rol"]

        # Saludo según la hora
    hora = datetime.now().hour

    if hora < 12:
        saludo = "☀ Buenos días"
    elif hora < 19:
        saludo = "🌤 Buenas tardes"
    else:
        saludo = "🌙 Buenas noches"

    fecha = datetime.now().strftime("%d/%m/%Y")

    col1, col2, col3 = st.columns([8, 1, 1])

    # =============================
    # SALUDO
    # =============================

    with col1:

        st.markdown(f"""
        <div style="margin-top:-4px;">            
        
        <div style="
            font-size:18px;
            color:#D9D9D9;
            font-weight:600;
        ">
                    
        {saludo},
        <span style="color:#57C84D;">{nombre}</span>

        </div>

        <div style="
        color:#9E9E9E;
        font-size:14px;
        margin-top:4px;
        ">

        
        <div style="
            color:#8C8C8C;
            font-size:14px;
            margin-top:2px;
        ">
        {fecha}
        </div>
        """, unsafe_allow_html=True)

    # =============================
    # NOTIFICACIONES
    # =============================

    with col2:

        with st.popover("🔔"):

            st.subheader("Notificaciones")

            st.divider()

            st.success("Sistema funcionando correctamente.")

            st.info("No existen alertas críticas.")

            st.caption("Última actualización hace unos segundos.")

    # =============================
    # USUARIO
    # =============================
    
    with col3:

        with st.popover("👤"):

            st.markdown(f"""
            <div style="
            background:#2A2D34;
            border:1px solid #3A3D45;
            border-radius:14px;
            padding:15px;
            text-align:center;
            ">

            <div style="font-size:34px;">
            👨🏻‍💻
            </div>

            <div style="
            font-size:17px;
            font-weight:600;
            color:white;
            margin-top:-4px;
            ">
            {nombre}
            </div>

            <div style="
            font-size:12px;
            color:#A8A8A8;
            ">
            {correo}
            </div>

            <div style="
            margin-top:10px;
            color:#57C84D;
            font-size:13px;
            font-weight:600;
            ">
            🟢 En línea
            </div>

            </div>
            """, unsafe_allow_html=True)

            st.divider()

            if st.button(
                "⚙ Configuración",
                use_container_width=True
            ):

                st.session_state.vista="Configuración"

                st.rerun()

            if st.button(
                "🚪 Cerrar sesión",
                use_container_width=True,
                type="primary",
                key="logout"
            ):

                st.session_state.logueado = False
                st.session_state.pagina = "login"

                if "usuario" in st.session_state:
                    del st.session_state["usuario"]

                st.rerun()

    

    st.divider()