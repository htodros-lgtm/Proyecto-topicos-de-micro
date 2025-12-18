import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO (Según tu captura ideal)
# ============================================================
TAMANO_FOTO  = 125  
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    /* 1. ESPACIO SUPERIOR PARA EL TITULO (Funciona en PC y Celular) */
    .main .block-container {{ 
        padding-top: 5rem !important; 
    }}
    
    /* 2. ALINEACIÓN HORIZONTAL SIN ESPACIOS (Estilo Rappi) */
    [data-testid="column"] {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        width: min-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0px 8px !important; 
    }}

    /* 3. IMÁGENES CUADRADAS */
    .img-mini img {{
        height: {TAMANO_FOTO}px !important;
        width: {TAMANO_FOTO}px !important;
        object-fit: cover !important;
        border-radius: 12px;
    }}

    /* 4. TEXTO DE LOS POSTRES */
    .texto-info {{
        font-weight: bold;
        font-size: 15px !important;
        color: #333;
        width: 140px !important; 
        line-height: 1.2;
    }}

    /* 5. BOTÓN ROJO DE TU CAPTURA */
    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        height: 3em !important;
        width: 90px !important; 
        border: none !important;
    }}

    /* Estilos de encabezado y Reloj */
    .header-text {{ text-align: center; margin-bottom: 5px !important; }}
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
    .reloj-container {{ 
        background-color: #fff2f2; 
        padding: 10px; 
        border-radius: 15px; 
        border: 2px solid #e21b2c; 
        text-align: center; 
        margin-bottom: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 class='header-text'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 class='header-text'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    # Botón de compra centrado
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🛒 COMPRAR", key="main_buy"):
            st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO (Igual a tu imagen) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 class='header-text'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='header-text' style='color: #1e7e34;'>✅ Se está preparando tu pedido</h3>", unsafe_allow_html=True)
    st.markdown("<p class='header-text' style='font-size: 14px;'>¡Podés agregar un postre antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.write("---")

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        # Distribución de columnas para forzar horizontalidad
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c1:
            for ext in [".png", ".jpg", ".jpeg", ".avif"]:
                if os.path.exists(archivo + ext):
                    st.image(archivo + ext, width=TAMANO_FOTO)
                    break
        with c2:
            st.markdown(f"<div class='texto-info'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            if st.button("Agregar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
        st.write("---")

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; font-size:12px; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 class='header-text' style='color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()










