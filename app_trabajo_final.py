import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO
# ============================================================
TAMANO_FOTO  = 120  # Tamaño ideal para que entre el texto al lado
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    /* 1. Arreglo para que el título se vea en PC y Celular */
    .main .block-container {{ padding-top: 5rem !important; }}
    
    /* 2. DISEÑO HORIZONTAL FORZADO (Flexbox) */
    .contenedor-rappi {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        padding: 10px 0 !important;
        border-bottom: 1px solid #eee;
    }}

    .foto-box {{
        width: {TAMANO_FOTO}px !important;
        height: {TAMANO_FOTO}px !important;
        flex-shrink: 0 !important;
        border-radius: 12px;
        overflow: hidden;
        margin-right: 10px;
    }}
    .foto-box img {{ width: 100%; height: 100%; object-fit: cover; }}

    .info-box {{
        flex-grow: 1 !important;
        font-weight: bold;
        font-size: 15px !important;
        padding-right: 5px;
        line-height: 1.2;
    }}

    /* 3. BOTÓN ROJO COMPACTO */
    .div-btn {{ width: 90px !important; flex-shrink: 0 !important; }}
    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        height: 2.8em !important;
        width: 100% !important;
        border: none !important;
        font-size: 13px !important;
    }}

    /* 4. ARREGLO BOTÓN MILANESA (FASE 1) */
    .boton-milanesa-fix button {{
        width: 250px !important; /* Más ancho para que no se corte el texto */
        height: 4em !important;
        font-size: 18px !important;
    }}

    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; text-align: center; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 8px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA (Arreglada) ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center; margin:0;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    # Usamos un solo contenedor centrado para el botón de compra
    st.markdown('<div style="display: flex; justify-content: center;" class="boton-milanesa-fix">', unsafe_allow_html=True)
    if st.button("🛒 COMPRAR AHORA", key="btn_inicial"):
        st.session_state.fase = 'oferta'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: OFERTA RELÁMPAGO (Diseño Horizontal Forzado) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        img_url = ""
        for ext in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + ext):
                img_url = archivo + ext
                break
        
        # Mezclamos HTML y Streamlit para asegurar la horizontalidad
        c1, c2, c3 = st.columns([1, 1.6, 1])
        with c1:
            if img_url: st.image(img_url, width=TAMANO_FOTO)
        with c2:
            # Forzamos que el texto esté alineado con la foto
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px; font-weight: bold;'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px;'>", unsafe_allow_html=True)
            if st.button("Sumar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; font-size:10px; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Pedido en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()




