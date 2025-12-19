import streamlit as st
import time
import os

# ============================================================
# AJUSTES DE TAMAÑO
# ============================================================
TAMANO_FOTO  = 100  
TAMANO_RELOJ = 35 
# ============================================================

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# --- INICIALIZACIÓN DE VARIABLES ---
if 'fase' not in st.session_state:
    st.session_state.fase = 'cuestionario'
if 'carrito' not in st.session_state:
    st.session_state.carrito = set()
if 'eligio_postre' not in st.session_state:
    st.session_state.eligio_postre = False

st.markdown(f"""
    <style>
    .main .block-container {{ padding-top: 5rem !important; }}
    
    div.stButton > button {{
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 2.8em !important;
        border: none !important;
        font-size: 13px !important;
    }}

    .btn-agregado button {{
        background-color: #1e7e34 !important;
    }}

    .contenedor-milanesa {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 20px;
    }}
    .btn-milanesa button {{
        width: 280px !important; 
        height: 4.5em !important;
        font-size: 18px !important;
        display: block !important;
        margin: 0 auto !important;
    }}

    .reloj-container {{ 
        background-color: #fff2f2; 
        padding: 10px; 
        border-radius: 15px; 
        border: 2px solid #e21b2c; 
        text-align: center; 
        margin: 15px 0; 
    }}
    .reloj-xl {{ 
        color: #e21b2c; 
        font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FASE 0: CUESTIONARIO ---
if st.session_state.fase == 'cuestionario':
    st.title("📋 Perfil del Participante")
    with st.form("perfil"):
        sexo = st.radio("Sexo:", ["Masculino", "Femenino", "Otro"])
        edad = st.selectbox("Edad:", ["Menos de 20", "Entre 20 y 30 años", "Entre 30 y 50 años", "Más de 50"])
        if st.form_submit_button("Continuar"):
            st.session_state.fase = 'instrucciones'
            st.rerun()

# --- FASE 1: INSTRUCCIONES ---
elif st.session_state.fase == 'instrucciones':
    st.title("Dinámica de la Simulación")
    st.markdown("""
    Estás por ingresar a un simulador de compra de una aplicación de delivery. 
    Es sábado, termina la semana y no tenés ganas de cocinar... Nada te tienta más que esa milanesa con fritas.
    
    Mientras esperás que confirmen tu pedido, se te ofrece agregar al carrito un postre.
    """)
    if st.button("COMENZAR EXPERIMENTO"):
        st.session_state.fase = 'compra'
        st.rerun()

# --- FASE 2: LA MILANESA ---
elif st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 El Bodegón</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.markdown("<h3 style='text-align: center;'>Milanesa con Papas Fritas - $14.200</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="contenedor-milanesa btn-milanesa">', unsafe_allow_html=True)
    if st.button("🛒 COMPRAR AHORA", key="buy_milan"):
        st.session_state.fase = 'oferta'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 3: OFERTA RELÁMPAGO (SIN PARPADEO) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    # RELOJ ESTÁTICO QUE SE ACTUALIZA SOLO POR JS (EVITA EL PARPADEO)
    st.markdown(f"""
        <div class="reloj-container">
            <p style="margin:0; font-size:12px; font-weight:bold;">EL REPARTIDOR SALE EN:</p>
            <p id="countdown" class="reloj-xl">00:35</p>
        </div>
        <script>
            var seconds = 35;
            var countdown = document.getElementById('countdown');
            var timer = setInterval(function() {{
                seconds--;
                countdown.innerHTML = "00:" + (seconds < 10 ? "0" : "") + seconds;
                if (seconds <= 0) {{
                    clearInterval(timer);
                    window.location.reload(); // Recarga al final para pasar a la encuesta
                }}
            }}, 1000);
        </script>
    """, unsafe_allow_html=True)

    # Detectar el final del tiempo para cambiar de fase
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = time.time()
    
    if time.time() - st.session_state.timer_start > 36:
        st.session_state.eligio_postre = len(st.session_state.carrito) > 0
        st.session_state.fase = 'final'
        st.rerun()

    postres = [("chocotorta", "Chocotorta $2.000"), ("flan", "Flan Mixto $2.000"), ("tiramisu", "Tiramisú $2.000")]

    for archivo, nombre in postres:
        img_url = ""
        for ext in [".png", ".jpg", ".jpeg", ".avif"]:
            if os.path.exists(archivo + ext):
                img_url = archivo + ext
                break
        
        c1, c2, c3 = st.columns([1, 1.5, 0.8])
        with c1:
            if img_url: st.image(img_url, width=TAMANO_FOTO)
        with c2:
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px; font-weight: bold;'>{nombre}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='display: flex; align-items: center; height: {TAMANO_FOTO}px;'>", unsafe_allow_html=True)
            agregado = nombre in st.session_state.carrito
            label = "Agregado" if agregado else "Sumar"
            
            if agregado: st.markdown('<div class="btn-agregado">', unsafe_allow_html=True)
            if st.button(label, key=nombre):
                if agregado: st.session_state.carrito.remove(nombre)
                else: st.session_state.carrito.add(nombre)
                st.rerun() # Solo parpadea cuando el usuario hace clic, no cada segundo
            if agregado: st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")

# --- FASE 4: PREGUNTAS ---
elif st.session_state.fase == 'final':
    st.title("💡 Unas últimas preguntas")
    with st.form("preguntas_finales"):
        if st.session_state.eligio_postre:
            st.success(f"Agregaste: {', '.join(st.session_state.carrito)}")
            q1 = st.radio("¿Por qué agregaste el postre?", ["Porque me tentó", "Por el precio", "Por el tiempo", "Otro motivo..."])
            if q1 == "Otro motivo...": st.text_input("Contanos por qué:")
            st.radio("Si no hubiese sido ofrecido, ¿lo hubieras pedido igual?", ["Sí", "No"])
        else:
            st.warning("No agregaste postre.")
            q1 = st.radio("¿Por qué no elegiste el postre?", ["No quería dulce", "Muy caro", "Presión del tiempo", "Otras razones..."])
            if q1 == "Otras razones...": st.text_input("Contanos por qué:")

        if st.form_submit_button("Finalizar"):
            st.session_state.fase = 'agradecimiento'
            st.rerun()

elif st.session_state.fase == 'agradecimiento':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c;'>🛵 ¡Pedido en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.carrito = set()
        st.session_state.fase = 'cuestionario'
        if "timer_start" in st.session_state: del st.session_state.timer_start
        st.rerun()







