import streamlit as st


def mostrar_hero():

    col1, col2 = st.columns([1.3, 1])

    with col1:

        html_hero = """<div style="padding-top:40px;">
<span style="color:#57C84D; font-size:18px; font-weight:600;">🌱 AGROINDUSTRIA</span>
<h1 style="font-size:52px; margin-top:10px; margin-bottom:10px;">Monitoreo inteligente para invernaderos</h1>
<p style="font-size:20px; color:#A7A7A7; line-height:1.8;">Supervisa en tiempo real la temperatura, humedad del ambiente, humedad del suelo y lluvia mediante sensores IoT e Inteligencia Artificial.</p>
</div>"""

        st.markdown(html_hero, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        # with c1:

        #     st.button(
        #         "🌱 Ver estado",
        #         use_container_width=True
        #     )

        # with c2:

        #     st.button(
        #         "📊 Análisis",
        #         use_container_width=True
        #     )

    with col2:

        st.image(
            "imagenes/manoia.jpeg",
            use_container_width=True
        )

    st.divider()