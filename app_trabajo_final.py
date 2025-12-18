import streamlit as st
import time
import os

# CONFIGURACIÓN DEL RELOJ
TAMANO_RELOJ = 35 

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# Estilos CSS para mantener el texto y achicar fotos
st.markdown(f"""
    <style>
    /* 1. Ajuste superior para que no se tape el título */
    .block-container {{ padding-top: 2rem !important; }}
    
    /* 2. Botón "Agregar al carrito" original */
    .stButton>button {{ 
        width: 100%; border-radius: 20px; height: 2.5em; 
        background-color: #e21b2c; color: white; font-weight: bold; border: none;
        font-size: 11px; /* Letra pequeña para que no se corte el botón */
    }}
    
    /* 3. Reloj Compacto */
    .reloj-xl {{ 
        color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; margin: 0; text-align: center; line-height: 1 !important;
    }}
    .reloj-container {{ 
        background-color: #fff2f2; padding: 10px; border-radius: 15px; 
        border: 3px solid #e21b2c; margin: 10px 0;
    }}

    /* 4. IMÁGENES MUY PEQUEÑAS (Estilo miniatura de lista) */
    .img-mini img {{
        height: 50px !important;
        width: 50px !important;
        object-fit: cover !important;
        border-radius: 8px;
    }}

    /* 5. Estilo para el texto original */
    .texto-original {{
        font-weight: bold;
        font-size: 14px;
        line-height: 1.2;
        display: flex;
        align-items: center;
        height: 50px;
    }}

    /* Reducción de espacios entre bloques */
    [data-testid="stVerticalBlock"] > div {{
        padding-top: 0.1rem !important;
        padding-bottom: 0.1rem !important;
    }}
    hr {{ margin: 0.3em 0px !important; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'oferta'

def mostrar_miniatura(nombre_base):
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            st.markdown('<div class="img-mini">', unsafe_allow_html=True)
            st.image(ruta, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            return True
    return False

# --- FASE 2: OFERTA RELÁMPAGO (CON TODO EL TEXTO) ---
if st.session_state.fase == 'oferta':
    # Texto Original Completo
    st.markdown("<h1 style='text-align: center; font-size: 24px;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #1e7e34; font-size: 18px;'>✅ Se está preparando tu pedido</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #0a0a0a; font-weight: 500;'>¡Podés agregar un postre a tu compra antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    postres = [
        ("chocotorta", "Chocotorta $2.000", "add_choco"),
        ("flan", "Flan Mixto $2.000", "add_flan"),
        ("tiramisu", "Tiramisú $2.000", "add_tira")
    ]

    for archivo, nombre, key in postres:
        # Distribución de columnas para aprovechar el ancho
        c1, c2, c3 = st.columns([0.6, 2.4, 1.2]) 
        with c1: mostrar_miniatura(archivo)
        with c2: st.markdown(f'<div class="texto-original">{nombre}</div>', unsafe_allow_html=True)
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
                    <p style='margin: 0; text-align: center; font-weight: bold; font-size: 12px;'>EL REPARTIDOR SALE EN:</p>
                    <p class='reloj-xl'>00:{t:02d}</p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<div style='text-align: center; font-size: 35px; font-weight: bold; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>¡Gracias por elegir El Bodegón!</p>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'oferta'; st.rerun()



