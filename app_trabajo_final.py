import streamlit as st
import time
import os

# CONFIGURACIÓN DEL RELOJ REDUCIDA PARA CELULAR
TAMANO_RELOJ = 30 

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# Estilos CSS para maximizar el espacio vertical
st.markdown(f"""
    <style>
    /* Eliminar espacios en blanco superiores de Streamlit */
    .block-container {{ padding-top: 0.5rem; padding-bottom: 0rem; }}
    
    /* Botones más bajos */
    .stButton>button {{ 
        width: 100%; border-radius: 15px; height: 2em; 
        background-color: #e21b2c; color: white; font-weight: bold; border: none;
        font-size: 12px;
    }}
    
    /* Reloj compacto */
    .reloj-xl {{ 
        color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; margin: 0; text-align: center; 
        line-height: 1 !important;
    }}
    
    .reloj-container {{ 
        background-color: #fff2f2; padding: 5px; border-radius: 15px; 
        border: 2px solid #e21b2c; margin: 5px 0;
    }}

    /* Fotos miniatura para que entren todas */
    .img-horizontal img {{
        height: 60px !important;
        width: 80px !important;
        object-fit: cover !important;
        border-radius: 10px;
    }}

    .texto-postre {{
        display: flex; align-items: center;
        height: 60px; font-weight: bold; font-size: 13px;
    }}

    /* Reducir títulos para ahorrar espacio */
    h1 {{ font-size: 20px !important; margin: 0 !important; padding: 0 !important; }}
    h3 {{ font-size: 16px !important; margin: 0 !important; padding: 5px 0 !important; }}
    
    .img-milanesa img {{
        width: 100% !important; max-height: 180px !important;
        object-fit: contain; border-radius: 15px;
    }}
    
    hr {{ margin: 0.3em 0px !important; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

def mostrar_imagen_horizontal(nombre_base):
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            st.markdown('<div class="img-horizontal">', unsafe_allow_html=True)
            st.image(ruta, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            return True
    return False

# --- FASE 1: COMPRA ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas - $14.200</h3>", unsafe_allow_html=True)
    if st.button("🛒 AGREGAR AL CARRITO"):
        st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO ---
elif st.session_state.fase == 'oferta':
    # Títulos ultra-breves para que suba la oferta
    st.markdown("<h1 style='text-align: center;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1e7e34; margin:0; font-weight:bold;'>✅ Preparando...</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [
        ("chocotorta", "Chocotorta $2k", "add_choco"),
        ("flan", "Flan Mixto $2k", "add_flan"),
        ("tiramisu", "Tiramisú $2k", "add_tira")
    ]

    for archivo, nombre, key in postres:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1: mostrar_imagen_horizontal(archivo)
        with c2: st.markdown(f'<div class="texto-postre">{nombre}</div>', unsafe_allow_html=True)
        with c3:
            st.write("")
            if st.button("Sumar", key=key):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡En camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()


