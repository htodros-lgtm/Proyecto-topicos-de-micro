import streamlit as st
import time
import os

# ============================================================
# CONFIGURACIÓN Y ESTILOS
# ============================================================
st.set_page_config(page_title="Experimento Economía Conductual", layout="centered")

st.markdown("""
    <style>
    .main .block-container { padding-top: 3rem !important; }
    /* Botón Comprar Grande */
    .stButton>button[kind="primary"] {
        width: 100% !important; height: 60px !important;
        background-color: #e21b2c !important; color: white !important;
        font-size: 20px !important; font-weight: bold !important; border-radius: 15px !important;
    }
    /* Estilo para filas de postres horizontales */
    .fila-postre { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar estados
if 'fase' not in st.session_state:
    st.session_state.fase = 'perfil'
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

# ============================================================
# FASE 0: PANTALLA DE PERFIL (ENCUESTA)
# ============================================================
if st.session_state.fase == 'perfil':
    st.title("📋 Breve Encuesta Inicial")
    st.write("Por favor, completá estos datos para comenzar la simulación.")
    
    with st.form("encuesta_inicial"):
        sexo = st.radio("Sexo:", ["Masculino", "Femenino", "Otro"])
        edad = st.selectbox("Edad:", ["Menos de 20", "Entre 20 y 30 años", "Entre 30 y 50 años", "Más de 50"])
        hambre = st.slider("¿Cuánta hambre tenés ahora? (1: Nada - 5: Mucha)", 1, 5, 3)
        uso_apps = st.radio("¿Frecuencia de uso de apps de delivery?", ["Nunca/Raro", "1 vez por semana", "3 o más veces por semana"])
        
        submitted = st.form_submit_button("EMPEZAR SIMULACIÓN")
        if submitted:
            st.session_state.datos_usuario = {
                "sexo": sexo, "edad": edad, "hambre": hambre, "uso_apps": uso_apps
            }
            st.session_state.fase = 'compra'
            st.rerun()

# ============================================================
# FASE 1: LA MILANESA (ANCLAJE DE PRECIO)
# ============================================================
elif st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    if st.button("🛒 AGREGAR AL CARRITO", type="primary"):
        st.session_state.fase = 'oferta'
        st.rerun()

# ============================================================
# FASE 2: OFERTA RELÁMPAGO (NUDGING Y ESCASEZ)
# ============================================================
elif st.session_state.fase == 'oferta':
    st.markdown("<h2 style='text-align: center;'>¡Pedido recibido!</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    # RELOJ DE CUENTA ATRÁS
    reloj_placeholder = st.empty()
    st.write("---")

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        c1, c2, c3 = st.columns([1, 1.5, 0.8])
        with c1:
            for ext in [".png", ".jpg", ".jpeg", ".avif"]:
                if os.path.exists(archivo + ext):
                    st.image(archivo + ext, width=120)
                    break
        with c2:
            st.markdown(f"<div style='height: 120px; display: flex; align-items: center; font-weight: bold;'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div style='height: 120px; display: flex; align-items: center;'>", unsafe_allow_html=True)
            if st.button("Sumar", key=nombre):
                st.session_state.fase = 'final'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

    # Logica del Timer
    for t in range(30, -1, -1):
        with reloj_placeholder.container():
            st.markdown(f"<div style='background-color: #fff2f2; padding: 10px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center;'><p style='margin:0; font-size:12px; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><h1 style='color: #e21b2c; margin:0;'>00:{t:02d}</h1></div>", unsafe_allow_html=True)
        time.sleep(1)
        if t == 0:
            st.session_state.fase = 'final'
            st.rerun()

elif st.session_state.fase == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c; margin-top: 50px;'>🛵 ¡Tu pedido está en camino!</h1>", unsafe_allow_html=True)
    st.write("Gracias por participar en el experimento.")
    if st.button("Reiniciar"):
        st.session_state.fase = 'perfil'
        st.rerun()
        





