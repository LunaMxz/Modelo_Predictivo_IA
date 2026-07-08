import streamlit as st

def cargar_estilos():

    st.markdown("""
    <style>

    /* Tarjetas */

    .card{

        background:#F5FFF6;

        border-radius:18px;

        padding:20px;

        box-shadow:0px 4px 15px rgba(0,0,0,.08);

        border:1px solid #DCEFD9;

    }

    .titulo-card{

        color:#2E7D32;

        font-size:18px;

        font-weight:bold;

    }

    .valor-card{

        font-size:35px;

        font-weight:bold;

        margin-top:10px;

    }
                
    /* Reduce el espacio superior */

    .block-container{

        padding-top: 0.8rem;

    }            

    .sub-card{

        color:gray;

        font-size:15px;

    }
                
    /* ===========================
    BOTONES MENÚ
    =========================== */

    div.stButton > button{

        width:100%;

        background:#292C33;

        color:#ECECEC;

        border:1px solid #353840;

        border-radius:12px;

        padding:12px 15px;

        text-align:left;

        font-size:15px;

        font-weight:500;

        transition:all .25s ease;

        margin-bottom:8px;

    }

    div.stButton > button:hover{

        background:#32363E;

        border-color:#57C84D;

        box-shadow:0 0 12px rgba(87,200,77,.12);

        transform:translateX(3px);

    }

    </style>
    """, unsafe_allow_html=True)