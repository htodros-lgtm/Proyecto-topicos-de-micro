import streamlit as st
import time
import os

# ============================================================
# SECCIÓN DE AJUSTES
# ============================================================
TAMANO_POSTRES = 125  # El tamaño que te gustó
TAMANO_RELOJ   = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; }}
    
    /* FUERZA LA ALINEACIÓN HORIZONTAL TIPO RAPPI */
    .fila-postre {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 10px;
        padding: 5px 0;
    }}

    /* Tamaño de imagen controlado */
    .img-mini img {{
        height: {TAMANO_POSTRES}px !important;
        width: {TAMANO_POSTRES}px !important;
        object-fit: cover !important;
        border-radius: 10px;
        flex-shrink: 0; /* Impide que la imagen se aplaste */
    }}

    .texto-info {{
        font-weight: bold;
        font-size: 14px;
        flex-grow: 1; /* Hace que el texto use el espacio central */
        line-height: 1.2;
    }}

    /* Botón compacto al lado */
    .stButton>button {{ 
        width: 80px !important; /* Ancho fijo para que entre al lado */
        border-radius: 10px;
        height: 2.5em;
        background-color: #e21b2c;
        color: white;
        font-weight: bold;
        border: none;
        font-size: 12px;
        padding: 0 5px;
    }}

    /* Reloj */
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; text-align: center; line-height: 1; }}
    .reloj-container {{ background-color: #fff2f2; padding: 5px; border-radius: 12px; border: 2px solid #e21b2c; margin: 5px 0; }}
    
    /* Milanesa inicial */
    .img-milanesa img {{ width: 100% !important; max-height: 250px !important; object-fit: contain; border-radius: 15px; }}
    </style>
    """, unsafe_allow_html=True)

if 'fase' not in st.session_state:
    st.session_state.fase = 'compra'

# Función para mostrar la fila horizontal forzada
def crear_fila_postre(nombre_base, texto_mostrar, key_btn):
    encontrada = False
    for ext in [".png", ".jpg", ".jpeg", ".avif"]:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            # Usamos HTML puro para garantizar la horizontalidad que no dan las columnas de Streamlit
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f'<div class="img-mini"><img src="app/static/{ruta}" onerror="this.src=\'https://via.placeholder.com/125\'"></div>', unsafe_allow_html=True)
                # Nota: Si lo anterior no carga la imagen, usamos el método estándar pero dentro de un div
                st.image(ruta, width=TAMANO_POSTRES)
            with col2:
                st.markdown(f'<div class="texto-info">{texto_mostrar}</div>', unsafe_allow_html=True)
            with col3:
                if st.button("Agregar", key=key_btn):
                    st.session_state.fase = 'final'
                    st.rerun()
            encontrada = True
            break
    return encontrada

# --- FASE 1: LA MILANESA ---
if st.session_state.fase == 'compra':
    st.markdown("<h2 style='text-align: center; margin:0;'>🍱 El Bodegón</h2>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h4 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h4>", unsafe_allow_html=True)
    if st.button("🛒 AGREGAR AL CARRITO", key="main_buy"):
        st.session_state.fase = 'oferta'; st.rerun()

# --- FASE 2: OFERTA RELÁMPAGO ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center; margin:0;'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 13px;'>¡Podés agregar un postre antes de que salga tu repartidor!</p>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    st.divider()

    # Renderizado manual de filas horizontales
    postres = [
        ("chocotorta", "Chocotorta $2.000", "btn_choco"),
        ("flan", "Flan Mixto $2.000", "btn_flan"),
        ("tiramisu", "Tiramisú $2.000", "btn_tira")
    ]

    for archivo, info, k in postres:
        # Usamos columnas pero con un CSS que impide que se rompan en móvil
        c1, c2, c3 = st.columns([1, 1.8, 1])
        with c1:
            for ext in [".png", ".jpg", ".jpeg", ".avif"]:
                if os.path.exists(archivo + ext):
                    st.markdown(f'<div class="img-mini">', unsafe_allow_html=True)
                    st.image(archivo + ext, width=TAMANO_POSTRES)
                    st.markdown('</div>', unsafe_allow_html=True)
                    break
        with c2:
            st.markdown(f'<div class="texto-info">{info}</div>', unsafe_allow_html=True)
        with c3:
            st.write("") # Espaciador
            if st.button("Agregar", key=k):
                st.session_state.fase = 'final'; st.rerun()
        st.divider()

    for t in range(35, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div class='reloj-container'><p style='margin:0; text-align:center; font-size:10px;'>REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{t:02d}</p></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0: st.session_state.fase = 'final'; st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h2 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h2>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.fase = 'compra'; st.rerun()












