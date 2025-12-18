import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO (125px como pediste)
# ============================================================
TAMANO_FOTO  = 125  
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    /* 1. Eliminamos márgenes laterales del contenedor principal */
    .block-container {{ padding: 1rem 0.5rem !important; }}
    
    /* 2. Reducción drástica de espacio entre columnas de Streamlit */
    [data-testid="column"] {{
        width: min-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0px 2px !important; /* Espacio mínimo entre foto-texto-botón */
    }}

    /* 3. Ajuste de imagen (125px fijos) */
    .img-mini img {{
        height: {TAMANO_FOTO}px !important;
        width: {TAMANO_FOTO}px !important;
        object-fit: cover !important;
        border-radius: 10px;
    }}

    /* 4. Texto ceñido a la imagen */
    .texto-info {{
        font-weight: bold;
        font-size: 14px !important;
        color: #333;
        display: flex;
        align-items: center;
        height: {TAMANO_FOTO}px;
        line-height: 1.1;
        width: 130px !important; /* Ancho fijo para el texto */
    }}

    /* 5. Botón compacto */
    .stButton>button {{ 
        border-radius: 20px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-size: 11px !important;
        height: 2.5em !important;
        width: 70px !important; /* Botón angosto para que no empuje */
        padding: 0px !important;
    }}

    /* Títulos y Reloj */
    .header-text {{ text-align: center; margin: 0px !important; padding: 5px 0 !important; }}
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 8px; border-radius: 12px; border: 2px solid #e21b2c; text-align: center; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h2 class='header-text'>🍱 El Bodegón</h2>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h4 class='header-text'>Milanesa con Papas Fritas - $14.200</h4>", unsafe_allow_html=True)
    if st.button("🛒 AGREGAR AL CARRITO"):
        st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO (ESPACIADO REDUCIDO) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 class='header-text'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 class='header-text' style='color: #1e7e34;'>✅ Preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p class='header-text' style='font-size: 13px;'>¡Podés agregar un postre antes de salir!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        # Usamos columnas con anchos fijos mínimos para evitar el salto de línea
        c1, c2, c3 = st.columns([1.3, 1.4, 0.8])
        
        with c1:
            for ext in [".png", ".jpg", ".jpeg", ".avif"]:
                if os.path.exists(archivo + ext):
                    st.image(archivo + ext, width=TAMANO_FOTO)
                    break
        
        with c2:
            st.markdown(f"<div class='texto-info'>{nombre}</div>", unsafe_allow_html=True)
            
        with c3:
            st.write(" ") # Alineación vertical
            st.write(" ")
            if st.button("Sumar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; font-size:10px;'>REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h2 class='header-text' style='color: #e21b2c; margin-top: 50px;'>🛵 ¡Pedido en camino!</h2>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()









