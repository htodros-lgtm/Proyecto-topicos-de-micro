import streamlit as st
import time
import os

st.set_page_config(page_title="App Final", layout="centered")

# --- CSS PARA FORZAR EL DISEÑO PROFESIONAL ---
st.markdown("""
    <style>
    /* 1. Espacio para el título en PC y Celular */
    .main .block-container { padding-top: 5rem !important; }
    
    /* 2. DISEÑO DE FILA HORIZONTAL (Fuerza bruta con Flexbox) */
    .contenedor-fila {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }

    .foto-celeste {
        width: 125px !important;
        height: 125px !important;
        border-radius: 15px;
        object-fit: cover;
        flex-shrink: 0;
    }

    .texto-info {
        flex-grow: 1;
        padding: 0 15px;
        font-weight: bold;
        font-size: 16px;
        color: #333;
        text-align: left;
    }

    /* 3. BOTÓN DE COMPRA MILANESA: Gigante para que no falle */
    .btn-milan-box {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .btn-milan-box button {
        width: 300px !important;
        height: 75px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 20px !important;
    }

    /* 4. BOTÓN SUMAR POSTRES: Circular/Óvalo como tu dibujo */
    .btn-sumar-box button {
        width: 90px !important;
        height: 45px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        font-size: 14px !important;
    }
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
    
    st.markdown('<div class="btn-milan-box">', unsafe_allow_html=True)
    if st.button("🛒 COMPRAR AHORA"):
        st.session_state.fase = 'oferta'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: OFERTA RELÁMPAGO (TODO EN UNA LÍNEA SÍ O SÍ) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center;'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: green;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.write("---")

    postres = [
        ("chocotorta", "Chocotorta $2.000"),
        ("flan", "Flan Mixto $2.000"),
        ("tiramisu", "Tiramisú $2.000")
    ]

    for archivo, nombre in postres:
        # Buscamos la imagen con cualquier extensión
        ext_img = ""
        for e in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + e):
                ext_img = archivo + e
                break
        
        # INYECCIÓN DE HTML PARA LA FILA
        # Creamos la estructura horizontal: Foto | Texto | Botón
        col1, col2, col3 = st.columns([1, 1.5, 0.8])
        
        with col1:
            if ext_img:
                st.markdown(f'<img src="app/static/{ext_img}" class="foto-celeste" onerror="this.src=\'https://via.placeholder.com/125\'">', unsafe_allow_html=True)
                # Backup de imagen estándar por si el HTML falla
                st.image(ext_img, width=125)
        
        with col2:
            st.markdown(f"<div class='texto-info' style='height: 125px; display: flex; align-items: center;'>{nombre}</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown("<div class='btn-sumar-box' style='height: 125px; display: flex; align-items: center;'>", unsafe_allow_html=True)
            if st.button("Agregar", key=nombre):
                st.session_state.fase = 'final'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div style='background-color: #fff2f2; padding: 15px; border-radius: 20px; border: 3px solid #e21b2c; text-align: center;'><h1 style='color: #e21b2c; margin:0;'>00:{t:02d}</h1></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0:
            st.session_state.fase = 'final'
            st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: red; margin-top: 50px;'>🛵 ¡Pedido en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'
        st.rerun()
        


