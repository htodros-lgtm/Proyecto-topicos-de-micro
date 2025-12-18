import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO
# ============================================================
TAMANO_FOTO  = 100  # Bajé a 100 para que el título tenga más aire y no se corte
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# CSS Profesional para alineación horizontal absoluta
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; }}
    
    /* CONTENEDOR TIPO RAPPI/PEDIDOSYA */
    .fila-container {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        border-bottom: 1px solid #eee;
        padding: 10px 0 !important;
    }}

    /* Cuadrado de la foto (Celeste en tu dibujo) */
    .foto-box {{
        width: {TAMANO_FOTO}px !important;
        height: {TAMANO_FOTO}px !important;
        flex-shrink: 0 !important;
        border-radius: 10px;
        overflow: hidden;
        margin-right: 10px;
    }}
    .foto-box img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    /* Título (Las líneas en tu dibujo) */
    .info-box {{
        flex-grow: 1 !important;
        font-weight: bold;
        font-size: 15px !important;
        color: #333;
        line-height: 1.2;
        padding-right: 5px;
    }}

    /* Botón (El círculo/óvalo en tu dibujo) */
    .div-boton {{
        width: 90px !important;
        flex-shrink: 0 !important;
    }}
    
    /* Estilo del botón de Streamlit dentro del div */
    .stButton>button {{ 
        border-radius: 20px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-size: 12px !important;
        height: 2.5em !important;
        width: 100% !important;
    }}

    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; text-align: center; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 5px; border-radius: 12px; border: 2px solid #e21b2c; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h2 style='text-align: center;'>🍱 El Bodegón</h2>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.write("### Milanesa con Papas Fritas - $14.200")
    if st.button("🛒 AGREGAR AL CARRITO"):
        st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO (INTERFAZ FLEXBOX) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center; margin:0;'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px;'>¡Podés agregar un postre antes de salir!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [
        ("chocotorta", "Chocotorta $2.000"),
        ("flan", "Flan Mixto $2.000"),
        ("tiramisu", "Tiramisú $2.000")
    ]

    for archivo, nombre in postres:
        # Buscamos la extensión correcta para la imagen
        img_url = ""
        for ext in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + ext):
                img_url = archivo + ext
                break

        # CREACIÓN DE LA FILA HORIZONTAL FORZADA
        col_img, col_txt, col_btn = st.columns([1, 2, 1])
        
        with col_img:
            if img_url: st.image(img_url, width=TAMANO_FOTO)
            else: st.write("🖼️")
        
        with col_txt:
            # Usamos un div con CSS para que el texto no se corte y esté centrado
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px; font-weight: bold;'>{nombre}</div>", unsafe_allow_html=True)
            
        with col_btn:
            # El botón ahora tiene su propia columna y no empuja al resto
            st.write(" ") # Espaciador vertical
            st.write(" ")
            if st.button("Sumar", key=nombre):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; text-align:center; font-size:10px;'>REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h2 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Pedido en camino!</h2>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()













