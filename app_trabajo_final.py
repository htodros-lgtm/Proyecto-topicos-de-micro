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
if 'eligio_postre' not in st.session_state:
    st.session_state.eligio_postre = False
if 'postre_seleccionado' not in st.session_state:
    st.session_state.postre_seleccionado = None

st.markdown(f"""
    <style>
    .main .block-container {{ padding-top: 5rem !important; }}
    
    .fila-postre {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        margin-bottom: 15px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }}

    .stButton>button {{ 
        border-radius: 10px !important;
        background-color: #e21b2c !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 2.8em !important;
        border: none !important;
        font-size: 13px !important;
    }}

    /* Estilo especial para cuando el postre está seleccionado */
    .btn-seleccionado button {{
        background-color: #1e7e34 !important;
        content: "AGREGADO" !important;
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

    .reloj-container {{ background-color: #fff2f2; padding: 10px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 15px 0; }}
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
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
    Es sábado, termina la semana y no tenés ganas de cocinar por lo que abrís tu app favorita de pedidos. 
    Nada te tienta más que esa milanesa con fritas así que la comprás. Mientras esperás que confirmen tu pedido, se te ofrece agregar al carrito un postre.
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
        st.session_state.fase = 'oferta'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 3: OFERTA RELÁMPAGO (INTERACTIVA) ---
elif st.session_state.fase == 'oferta':
    st.markdown("<h1 style='text-align: center; margin:0;'>¡Pedido recibido!</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #1e7e34; margin:0;'>✅ Se está preparando tu pedido</h4>", unsafe_allow_html=True)
    
    # Mostrar qué postre está en el carrito actualmente
    if st.session_state.postre_seleccionado:
        st.info(f"Seleccionado: {st.session_state.postre_seleccionado}")
    else:
        st.write("¿Querés agregar un postre?")

    reloj_placeholder = st.empty()
    st.write("")

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
            # El botón ahora no cambia de fase, solo cambia el estado
            label_boton = "Sumado" if st.session_state.postre_seleccionado == nombre else "Sumar"
            if st.button(label_boton, key=nombre):
                st.session_state.eligio_postre = True
                st.session_state.postre_seleccionado = nombre
                st.rerun() # Recarga para mostrar el cambio pero sigue en esta fase
            st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")

    # Cronómetro que corre en segundo plano
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(35 - elapsed))

    with reloj_placeholder.container():
        st.markdown(f"<div class='reloj-container'><p style='margin:0; font-size:12px; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{remaining:02d}</p></div>", unsafe_allow_html=True)
    
    if remaining > 0:
        time.sleep(1)
        st.rerun()
    else:
        # Solo cuando llega a cero pasa a la siguiente fase
        st.session_state.fase = 'final'
        st.rerun()

# --- FASE 4: PREGUNTAS FINALES ---
elif st.session_state.fase == 'final':
    st.title("💡 Unas últimas preguntas")
    with st.form("preguntas_finales"):
        if st.session_state.eligio_postre:
            st.success(f"Agregaste: {st.session_state.postre_seleccionado}")
            q1 = st.radio("¿Por qué agregaste el postre?", ["Porque me tentó", "Por el precio", "Por el tiempo", "Otro motivo..."])
            if q1 == "Otro motivo...":
                st.text_input("Contanos por qué:")
            st.radio("Si no hubiese sido ofrecido, ¿lo hubieras pedido igual?", ["Sí", "No"])
        else:
            st.warning("No agregaste postre.")
            q1 = st.radio("¿Por qué no elegiste el postre?", ["No quería dulce", "Muy caro", "Presión del tiempo", "Otras razones..."])
            if q1 == "Otras razones...":
                st.text_input("Contanos por qué:")

        if st.form_submit_button("Finalizar"):
            st.session_state.fase = 'agradecimiento'
            st.rerun()

elif st.session_state.fase == 'agradecimiento':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #e21b2c;'>🛵 ¡Pedido en camino!</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.eligio_postre = False
        st.session_state.postre_seleccionado = None
        st.session_state.fase = 'cuestionario'
        del st.session_state.start_time
        st.rerun()






