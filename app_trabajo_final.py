import streamlit as st
import time
import os

# CONFIGURACIÓN DEL RELOJ
TAMANO_RELOJ = 32 

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# CSS para forzar que todo entre en una sola pantalla de celular
st.markdown(f"""
    <style>
    /* 1. Eliminar espacios muertos superiores e internos */
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem; }}
    [data-testid="stVerticalBlock"] > div {{ padding: 0px !important; margin: 0px !important; }}
    
    /* 2. Estilo de los Botones (Círculos/Óvalos en tu dibujo) */
    .stButton>button {{ 
        width: 100%; border-radius: 10px; height: 2.2em; 
        background-color: #e21b2c; color: white; font-weight: bold; border: none;
        font-size: 11px; padding: 0px;
    }}
    
    /* 3. Reloj Compacto */
    .reloj-xl {{ 
        color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; margin: 0; text-align: center; line-height: 1 !important;
    }}
    .reloj-container {{ 
        background-color: #fff2f2; padding: 5px; border-radius: 12px; 
        border: 2px solid #e21b2c; margin: 5px 0;
    }}

    /* 4. FOTOS MINIATURA (Los cuadrados celestes de tu dibujo) */
    .img-mini img {{
        height: 50px !important;
        width: 50px !important;
        object-fit: cover !important;
        border-radius: 5px;
    }}

    /* 5. TEXTO ALINEADO (Las líneas de tu dibujo) */
    .texto-info {{
        font-weight: bold;
        font-size: 13px;
        display: flex;
        align-items: center;
        height: 50px;
        line-height: 1.1;
    }}

    /* Estilo para los textos de encabezado */
    .header-text {{ text-align: center; margin: 0px !important; padding: 0px !important; }}
    
    hr {{ margin: 0.2em 0px !important; opacity: 0.5; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'oferta'

def mostrar_foto_mini(nombre_base):
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            st.markdown('<div class="img-mini">', unsafe_allow_html=True)
            st.image(ruta, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            return True
    return False

# --- FASE 2: OFERTA RELÁMPAGO ---
if st.session_state.fase == 'oferta':
    # Todo el texto original compactado
    st.markdown("<h2 class='header-text'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 class='header-text' style='color: #1e7e34;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p class='header-text' style='font-size: 13px;'>¡Podés agregar un postre a tu compra antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [
        ("chocotorta", "Chocotorta $2.000", "add_choco"),
        ("flan", "Flan Mixto $2.000", "add_flan"),
        ("tiramisu", "Tiramisú $2.000", "add_tira")
    ]

    # Renderizado de las 3 filas
    for archivo, nombre, key in postres:
        c1, c2, c3 = st.columns([0.7, 2, 1.3]) 
        with c1: mostrar_foto_mini(archivo)
        with c2: st.markdown(f'<div class="texto-info">{nombre}</div>', unsafe_allow_html=True)
        with c3:
            st.write("") # Espaciador
            if st.button("Agregar al carrito", key=key):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    # Motor del Reloj
    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"""
                <div class='reloj-container'>
                    <p style='margin: 0; text-align: center; font-weight: bold; font-size: 10px;'>EL REPARTIDOR SALE EN:</p>
                    <p class='reloj-xl'>00:{t:02d}</p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<div style='text-align: center; font-size: 30px; font-weight: bold; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</div>", unsafe_allow_html=True)
    st.markdown("<p class='header-text'>¡Gracias por elegir El Bodegón!</p>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'oferta'; st.rerun()




