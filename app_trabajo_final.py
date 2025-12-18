import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO
# ============================================================
TAMANO_FOTO  = 100  # Bajé un poco para asegurar espacio al texto
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    .main .block-container {{ padding-top: 5rem !important; }}
    
    /* BLOQUE DE POSTRE: FUERZA LA LÍNEA HORIZONTAL */
    .fila-postre {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        margin-bottom: 15px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }}

    .foto-contenedor {{
        width: {TAMANO_FOTO}px !important;
        height: {TAMANO_FOTO}px !important;
        flex-shrink: 0 !important;
        border-radius: 10px;
        overflow: hidden;
    }}
    .foto-contenedor img {{ width: 100%; height: 100%; object-fit: cover; }}

    .texto-contenedor {{
        flex-grow: 1 !important;
        padding: 0 10px !important;
        font-weight: bold;
        font-size: 14px !important;
        line-height: 1.2;
    }}

    /* BOTÓN SUMAR COMPACTO */
    .btn-sumar-col {{ width: 80px !important; flex-shrink: 0 !important; }}
    
    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 2.8em !important;
        border: none !important;
        font-size: 13px !important;
    }}

    /* BOTÓN MILANESA: ARREGLO FINAL */
    .contenedor-milanesa {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 20px;
    }}
    .btn-milanesa button {{
        width: 280px !important; 
        height: 4.5em !important;
        font-size: 18px !important;
        display: block !important;
        margin: 0 auto !important;
    }}

    .reloj-container {{ background-color: #fff2f2; padding: 10px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 15px 0; }}
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    # Botón de milanesa con clase única para que no falle
    st.markdown('<div class="contenedor-milanesa btn-milanesa">', unsafe_allow_html=True)
    if st.button("🛒 COMPRAR AHORA", key="buy_milan"):
        st.session_state.fase = 'oferta'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: OFERTA RELÁMPAGO (HTML PURO) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.write("")

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        img_url = ""
        for ext in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + ext):
                img_url = archivo + ext
                break
        
        # AQUÍ ESTÁ EL TRUCO: USAMOS COLUMNAS PERO SIN MARGENES PARA QUE NO SE BAJEN
        c1, c2, c3 = st.columns([1, 1.5, 0.8])
        with c1:
            if img_url: st.image(img_url, width=TAMANO_FOTO)
        with c2:
            # Alineamos el texto verticalmente con la imagen
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px; font-weight: bold;'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            # Forzamos que el botón aparezca al lado
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px;'>", unsafe_allow_html=True)
            if st.button("Sumar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; font-size:12px; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()


