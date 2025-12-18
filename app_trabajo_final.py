import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO (125px para postres como pediste)
# ============================================================
TAMANO_FOTO  = 125  
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    /* 1. Espacio para el título en PC y Celular */
    .main .block-container {{ padding-top: 4rem !important; }}
    
    /* 2. FORZAR LA FILA (Evita que se pongan uno abajo del otro) */
    [data-testid="column"] {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        width: min-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0px 5px !important; 
    }}

    /* 3. Fotos Cuadradas de 125px */
    .img-mini img {{
        height: {TAMANO_FOTO}px !important;
        width: {TAMANO_FOTO}px !important;
        object-fit: cover !important;
        border-radius: 12px;
    }}

    /* 4. Texto que no se corta y se queda al lado */
    .texto-info {{
        font-weight: bold;
        font-size: 15px !important;
        color: #333;
        width: 145px !important; /* Espacio justo para el nombre */
        line-height: 1.2;
    }}

    /* 5. Botón "Agregar" Compacto */
    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        height: 2.8em !important;
        width: 85px !important; 
        border: none !important;
    }}

    /* Arreglo para el botón de la milanesa (Fase 1) */
    .btn-grande button {{
        width: 200px !important;
        height: 3.5em !important;
        font-size: 16px !important;
    }}

    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; text-align: center; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 8px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA (ARREGLADA) ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    col_c = st.columns([1, 2, 1])
    with col_c[1]:
        st.markdown('<div class="btn-grande">', unsafe_allow_html=True)
        if st.button("🛒 COMPRAR", key="compra_inicial"):
            st.session_state.fase = 'oferta'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: OFERTA RELÁMPAGO (AL COSTADO SÍ O SÍ) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px;'>¡Podés agregar un postre antes de salir!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        # Usamos columnas fijas y forzamos la horizontalidad
        c1, c2, c3 = st.columns([1.1, 1.4, 0.9])
        
        with c1:
            for ext in [".png", ".jpg", ".jpeg", ".avif"]:
                if os.path.exists(archivo + ext):
                    st.image(archivo + ext, width=TAMANO_FOTO)
                    break
        with c2:
            st.markdown(f"<div class='texto-info' style='display: flex; align-items: center; height: {TAMANO_FOTO}px;'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px;'>", unsafe_allow_html=True)
            if st.button("Agregar", key=nombre):
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
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()




