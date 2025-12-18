import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO (125px fijos para que luzcan los postres)
# ============================================================
TAMANO_FOTO  = 125  
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# CSS Profesional para forzar horizontalidad y arreglar botones
st.markdown(f"""
    <style>
    /* 1. Espacio superior para que el título no se tape en PC */
    .main .block-container {{ padding-top: 4rem !important; }}
    
    /* 2. FORZAR FILA HORIZONTAL (Foto - Texto - Botón) */
    .fila-custom {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        padding: 10px 0 !important;
        border-bottom: 1px solid #eee;
        gap: 10px;
    }}

    .foto-cuadrada {{
        width: {TAMANO_FOTO}px !important;
        height: {TAMANO_FOTO}px !important;
        flex-shrink: 0 !important;
        border-radius: 12px;
        overflow: hidden;
    }}
    .foto-cuadrada img {{ width: 100%; height: 100%; object-fit: cover; }}

    .info-nombre {{
        flex-grow: 1 !important;
        font-weight: bold;
        font-size: 15px !important;
        padding-left: 5px;
    }}

    /* 3. BOTÓN ROJO ESTILO CAPTURA IDEAL */
    .div-boton-fijo {{ width: 90px !important; flex-shrink: 0 !important; }}
    
    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-size: 14px !important;
        height: 3em !important;
        width: 100% !important;
        border: none !important;
        line-height: 1 !important; /* Arregla el texto raro en el botón */
    }}

    /* Estilo para el botón de inicio (Milanesa) */
    .btn-inicio button {{
        width: 180px !important;
        height: 3.5em !important;
        font-size: 16px !important;
    }}

    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 8px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA (Botón Centrado y Grande) ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    # Botón de inicio centrado
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.markdown('<div class="btn-inicio">', unsafe_allow_html=True)
        if st.button("🛒 COMPRAR", key="main_buy"):
            st.session_state.fase = 'oferta'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: OFERTA RELÁMPAGO (Alineación Horizontal Forzada) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px;'>¡Podés agregar un postre antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        img_src = ""
        for ext in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + ext):
                img_src = archivo + ext
                break
        
        # HTML PURO PARA FORZAR LA HORIZONTALIDAD
        # Creamos una fila que no se rompe en celular
        c1, c2, c3 = st.columns([1, 1.8, 1])
        
        with c1:
            if img_src: st.image(img_src, width=TAMANO_FOTO)
            else: st.write("🖼️")
        
        with c2:
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px; font-weight: bold; font-size: 14px;'>{nombre}</div>", unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"<div style='height: {TAMANO_FOTO}px; display: flex; align-items: center;'>", unsafe_allow_html=True)
            if st.button("Agregar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

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







