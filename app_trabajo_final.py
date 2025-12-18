import streamlit as st
import time
import os

# ============================================================
# SECCIÓN DE AJUSTES (Modificá solo estos números)
# ============================================================
TAMANO_POSTRES = 65  # Achica este número para que entren los 3 juntos
TAMANO_RELOJ   = 30  # Achica este número para que el reloj ocupe menos lugar
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1.5rem !important; }}
    
    /* TAMAÑO DE LOS POSTRES (Cuadraditos celestes de tu dibujo) */
    .img-mini img {{
        height: {TAMANO_POSTRES}px !important;
        width: {TAMANO_POSTRES}px !important;
        object-fit: cover !important;
        border-radius: 8px;
    }}

    /* TAMAÑO DEL RELOJ (El círculo/recuadro de tiempo) */
    .reloj-xl {{ 
        color: #e21b2c; 
        font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; 
        text-align: center; 
        line-height: 1; 
    }}
    
    .reloj-container {{ 
        background-color: #fff2f2; 
        padding: 5px; 
        border-radius: 12px; 
        border: 2px solid #e21b2c; 
        margin: 5px 0; 
    }}

    .texto-info {{
        font-weight: bold; font-size: 13px; display: flex;
        align-items: center; height: {TAMANO_POSTRES}px; line-height: 1.1;
    }}
    
    .stButton>button {{ 
        width: 100%; border-radius: 10px; height: 2.2em; 
        background-color: #e21b2c; color: white; font-weight: bold; 
        border: none; font-size: 11px;
    }}

    /* LA MILANESA (Se mantiene grande, no se ve afectada por TAMANO_POSTRES) */
    .img-milanesa img {{
        width: 100% !important;
        max-height: 250px !important;
        object-fit: contain;
        border-radius: 15px;
    }}
    
    hr {{ margin: 0.2em 0px !important; opacity: 0.3; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

def mostrar_foto_mini(nombre_base):
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            st.markdown('<div class="img-mini">', unsafe_allow_html=True)
            st.image(ruta, width=TAMANO_POSTRES)
            st.markdown('</div>', unsafe_allow_html=True)
            return True
    return False

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h2 style='text-align: center; margin:0;'>🍱 El Bodegón</h2>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.markdown('<div class="img-milanesa">', unsafe_allow_html=True)
        st.image("milanesa.avif", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h4>", unsafe_allow_html=True)
    if st.button("🛒 AGREGAR AL CARRITO", key="main_buy"):
        st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center; margin:0;'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 12px; margin:0;'>¡Podés agregar un postre antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        c1, c2, c3 = st.columns([0.6, 2.2, 1.2]) 
        with c1: mostrar_foto_mini(archivo)
        with c2: st.markdown(f'<div class="texto-info">{nombre}</div>', unsafe_allow_html=True)
        with c3:
            st.write("") 
            if st.button("Agregar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"""
                <div class='reloj-container'>
                    <p style='margin:0; text-align:center; font-size:10px;'>REPARTIDOR SALE EN:</p>
                    <p class='reloj-xl'>00:{t:02d}</p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h2 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h2>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()









