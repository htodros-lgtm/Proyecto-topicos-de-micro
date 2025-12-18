import streamlit as st
import time
import os

# CONFIGURACIÓN DEL RELOJ
TAMANO_RELOJ = 40

st.set_page_config(page_title="Rappi Experimento - Grupo B", layout="centered")

# Estilos CSS
st.markdown(f"""
    <style>
    .stButton>button {{ 
        width: 100%; border-radius: 25px; height: 3.5em; 
        background-color: #e21b2c; color: white; font-weight: bold; border: none; 
    }}
    .reloj-xl {{ 
        color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; margin: 0; text-align: center; 
        font-family: 'Courier New', Courier, monospace; line-height: 0.7 !important;
    }}
    .reloj-container {{ 
        background-color: #fff2f2; padding: 15px; border-radius: 30px; 
        border: 4px solid #e21b2c; margin: 20px 0;
    }}
    .img-horizontal img {{
        height: 120px !important; width: 180px !important;
        object-fit: cover !important; border-radius: 15px;
    }}
    .texto-postre {{
        display: flex; align-items: center; height: 120px;
        font-weight: bold; font-size: 20px;
    }}
    .img-milanesa img {{
        width: 100% !important; height: auto !important;
        border-radius: 15px;
    }}
    .mensaje-final {{
        text-align: center; font-size: 45px;
        font-weight: bold; color: #e21b2c; margin-top: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# Función corregida para buscar imágenes en la carpeta del servidor
def mostrar_imagen_horizontal(nombre_base):
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            st.markdown('<div class="img-horizontal">', unsafe_allow_html=True)
            st.image(ruta, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            return True
    return False

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    # Buscamos la milanesa en la carpeta raíz
    milanesa_encontrada = False
    for ext in [".avif", ".png", ".jpg"]:
        if os.path.exists("milanesa" + ext):
            st.markdown('<div class="img-milanesa">', unsafe_allow_html=True)
            st.image("milanesa" + ext, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            milanesa_encontrada = True
            break
    if not milanesa_encontrada:
        st.warning("Imagen 'milanesa' no encontrada.")
        
    st.write("## Milanesa con Papas Fritas - $14.200")
    if st.button("🛒 AGREGAR AL CARRITO", key="main_buy"):
        st.session_state.fase = 'oferta'
        st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #1e7e34;'>✅ Se está preparando tu pedido</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #0a0a0a;'> ¡Podés agregar un postre a tu compra antes de que salga tu repartidor! </h3>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    # Los postres se buscan sin rutas absolutas
    postres = [
        ("chocotorta", "Chocotorta $2.000", "add_choco"),
        ("flan", "Flan Mixto $2.000", "add_flan"),
        ("tiramisu", "Tiramisú $2.000", "add_tira")
    ]

    for archivo, nombre, key in postres:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1: mostrar_imagen_horizontal(archivo)
        with c2: st.markdown(f'<div class="texto-postre">{nombre}</div>', unsafe_allow_html=True)
        with c3:
            st.write("")
            if st.button("Agregar al carrito", key=key):
                st.session_state.postre = nombre
                st.session_state.fase = 'final'
                st.rerun()
        st.divider()

    for t in range(15, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"""
                <div class='reloj-container'>
                    <p style='margin: 0; text-align: center; font-weight: bold;'>EL REPARTIDOR SALE EN:</p>
                    <p class='reloj-xl'>00:{t:02d}</p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
        if t == 0:
            st.session_state.fase = 'final'
            st.rerun()

# --- FASE 3: MENSAJE FINAL ---
elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<div class='mensaje-final'>🛵 ¡Tu pedido está en camino!</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>¡Gracias por elegir El Bodegón!</p>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'

        st.rerun()

