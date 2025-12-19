import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ============================================================
# AJUSTES DE TAMAÑO (Tus medidas exactas)
# ============================================================
TAMANO_FOTO  = 100  
TAMANO_RELOJ = 35 

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- INICIALIZACIÓN DE VARIABLES ---
if 'fase' not in st.session_state:
    st.session_state.fase = 'perfil'
if 'carrito' not in st.session_state:
    st.session_state.carrito = set()
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

# TU CSS ORIGINAL (Protegido para que no se rompa nada)
st.markdown(f"""
    <style>
    .main .block-container {{ padding-top: 5rem !important; }}
    .stButton>button {{ 
        border-radius: 10px !important; 
        background-color: #e21b2c !important; 
        color: white !important; 
        font-weight: bold !important; 
        width: 100% !important; 
        height: 2.8em !important; 
        border: none !important; 
    }}
    .btn-agregado button {{ background-color: #1e7e34 !important; }}
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
        line-height: 1; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FASE 0: PERFIL ---
if st.session_state.fase == 'perfil':
    st.markdown("## 📋 Datos del Participante")
    with st.form("perfil_inicial"):
        sexo = st.radio("Sexo:", ["Masculino", "Femenino", "Otro"])
        edad = st.selectbox("Edad:", ["Menos de 20", "Entre 20 y 30 años", "Entre 30 y 50 años", "Más de 50"])
        if st.form_submit_button("Continuar"):
            st.session_state.datos_usuario['sexo'] = sexo
            st.session_state.datos_usuario['edad'] = edad
            st.session_state.fase = 'instrucciones'
            st.rerun()

# --- FASE 1: INSTRUCCIONES ---
elif st.session_state.fase == 'instrucciones':
    st.title("Dinámica")
    st.write("Imaginá que acabás de comprar una milanesa por Rappi. Tu pedido ya está en camino, pero de repente aparece una oferta relámpago de postres que solo dura unos segundos...")
    if st.button("COMENZAR"):
        st.session_state.fase = 'compra'
        st.rerun()

# --- FASE 2: COMPRA MILANESA (ESTADO PREVIO) ---
elif st.session_state.fase == 'compra':
    st.markdown("<h1 style='text-align: center;'>🍱 ¡Pedido Confirmado!</h1>", unsafe_allow_html=True)
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    st.info("Tu Milanesa con Papas Fritas ya se está preparando.")
    if st.button("VER OFERTA DE POSTRES"):
        st.session_state.fase = 'oferta'
        st.session_state.timer_start = time.time()
        st.rerun()

# --- FASE 3: OFERTA RELÁMPAGO (SISTEMA 1) ---
elif st.session_state.fase == 'oferta':
    reloj_placeholder = st.empty()
    elapsed = time.time() - st.session_state.timer_start
    remaining = max(0, int(35 - elapsed))

    with reloj_placeholder.container():
        st.markdown(f"<div class='reloj-container'><p class='reloj-xl'>00:{remaining:02d}</p></div>", unsafe_allow_html=True)

    # REINCORPORACIÓN DE FOTOS Y TEXTOS ORIGINALES
    postres = [
        ("chocotorta.png", "Chocotorta $2.000"),
        ("flan.jpg", "Flan Mixto $2.000"),
        ("tiramisu.png", "Tiramisú $2.000")
    ]
    
    for archivo, nombre in postres:
        c1, c2, c3 = st.columns([1, 1.5, 0.8])
        with c1:
            if os.path.exists(archivo):
                st.image(archivo, width=TAMANO_FOTO)
        with c2:
            st.markdown(f"<br><b>{nombre}</b>", unsafe_allow_html=True)
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            es_parte = nombre in st.session_state.carrito
            if es_parte: st.markdown('<div class="btn-agregado">', unsafe_allow_html=True)
            if st.button("Agregado" if es_parte else "Sumar", key=nombre):
                if 'tiempo_reaccion' not in st.session_state.datos_usuario:
                    st.session_state.datos_usuario['tiempo_reaccion'] = round(elapsed, 2)
                if es_parte: st.session_state.carrito.remove(nombre)
                else: st.session_state.carrito.add(nombre)
                st.rerun()
            if es_parte: st.markdown('</div>', unsafe_allow_html=True)

    if remaining > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.fase = 'preguntas'
        st.rerun()

# --- FASE 4: PREGUNTAS (SISTEMA 2) ---
elif st.session_state.fase == 'preguntas':
    st.title("💡 Unas últimas preguntas")
    with st.form("final"):
        eligio = len(st.session_state.carrito) > 0
        st.write(f"**Resultado:** {'Agregaste postre' if eligio else 'No agregaste postre'}")
        
        motivo = st.radio("¿Por qué tomaste esa decisión?", ["Tentación", "Precio", "Urgencia", "Otro"])
        hubiera = st.radio("¿Lo hubieras pedido sin la oferta?", ["Si", "No"])

        if st.form_submit_button("Finalizar y Enviar"):
            try:
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Sexo": st.session_state.datos_usuario['sexo'],
                    "Edad": st.session_state.datos_usuario['edad'],
                    "Eligio": "SI" if eligio else "NO",
                    "Postres": ", ".join(st.session_state.carrito),
                    "Tiempo_Seg": st.session_state.datos_usuario.get('tiempo_reaccion', "N/A"),
                    "Motivo": motivo,
                    "Sin_Oferta": hubiera
                }])
                conn.create(data=nueva_fila)
                st.session_state.fase = 'final'
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

# --- FASE 5: FINALIZACIÓN ---
elif st.session_state.fase == 'final':
    st.balloons()
    st.success("¡Tu pedido está en camino!")
    st.write("Gracias por participar en este experimento de microeconomía.")
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()






