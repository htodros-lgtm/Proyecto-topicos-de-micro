import streamlit as st
import time
import os

# Configuración compacta
st.set_page_config(page_title="Simulador de Pedido", layout="centered")

# Estilos CSS Profesionales para Interfaz Móvil
st.markdown("""
    <style>
    /* 1. Eliminar espacios muertos de Streamlit */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem; }
    
    /* 2. Estilo de Botón "Agregar" tipo Rappi */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 2.4em; 
        background-color: #e21b2c; color: white; font-weight: bold; border: none;
        font-size: 14px; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 3. Reloj de urgencia estilizado */
    .reloj-container { 
        background-color: #fff2f2; padding: 10px; border-radius: 12px; 
        border: 2px solid #e21b2c; margin-bottom: 15px; text-align: center;
    }
    .reloj-numero { 
        color: #e21b2c; font-size: 32px !important; font-weight: 900; 
        font-family: 'Courier New', monospace; line-height: 1;
    }

    /* 4. Diseño de FILA DE PRODUCTO (Card Horizontal) */
    .product-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 8px 0; border-bottom: 1px solid #f0f0f0;
    }
    .img-product img {
        height: 65px !important; width: 65px !important;
        object-fit: cover !important; border-radius: 8px;
    }
    .text-product {
        font-weight: 600; font-size: 15px; color: #333;
    }
    
    /* Ajuste de títulos */
    h2 { font-size: 22px !important; margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'oferta'

# --- INTERFAZ DE OFERTA ---
if st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center;'>✅ ¡Pedido recibido!</h2>", unsafe_allow_html=True)
    
    # Marcador de posición para el reloj (Urgencia visual)
    reloj_placeholder = st.empty()

    # Base de datos de productos (Simulada)
    # Asegúrate de tener estas imágenes en tu carpeta de GitHub
    productos = [
        ("chocotorta", "Chocotorta", "$2.000", "btn_1"),
        ("flan", "Flan Mixto", "$2.000", "btn_2"),
        ("tiramisu", "Tiramisú", "$2.000", "btn_3")
    ]

    # Renderizado de productos en columnas para simular "Cards" horizontales
    for img_name, nombre, precio, key in productos:
        col_img, col_txt, col_btn = st.columns([1, 2, 1])
        
        with col_img:
            # Busca la imagen con cualquier extensión
            encontrada = False
            for ext in [".png", ".jpg", ".avif"]:
                if os.path.exists(f"{img_name}{ext}"):
                    st.markdown(f'<div class="img-product">', unsafe_allow_html=True)
                    st.image(f"{img_name}{ext}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    encontrada = True
                    break
            if not encontrada: st.caption("🖼️")

        with col_txt:
            st.markdown(f'<div style="padding-top:15px;"><span class="text-product">{nombre}</span><br><small>{precio}</small></div>', unsafe_allow_html=True)
        
        with col_btn:
            st.write("") # Espaciador
            if st.button("Sumar", key=key):
                st.session_state.fase = 'final'; st.rerun()
        
        st.markdown("<hr style='margin:0.2em 0; opacity:0.1;'>", unsafe_allow_html=True)

    # Motor del reloj (Sistema 1 de decisión rápida)
    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"""
                <div class='reloj-container'>
                    <p style='margin: 0; font-size: 11px; font-weight: bold; color: #555;'>EL REPARTIDOR SALE EN:</p>
                    <p class='reloj-numero'>00:{t:02d}</p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡En camino!</h1>", unsafe_allow_html=True)
    if st.button("Hacer otro pedido"):
        st.session_state.fase = 'oferta'; st.rerun()



