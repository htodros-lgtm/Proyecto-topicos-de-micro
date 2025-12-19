import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# AJUSTES ORIGINALES
TAMANO_FOTO  = 100  
TAMANO_RELOJ = 35 

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# CONEXIÓN A TU GOOGLE SHEET
conn = st.connection("gsheets", type=GSheetsConnection)

# INICIALIZACIÓN
if 'fase' not in st.session_state:
    st.session_state.fase = 'perfil'
if 'carrito' not in st.session_state:
    st.session_state.carrito = set()
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

st.markdown(f"""
    <style>
    .main .block-container {{ padding-top: 5rem !important; }}
    .stButton>button {{ border-radius: 10px !important; background-color: #e21b2c !important; color: white !important; font-weight: bold !important; width: 100% !important; height: 2.8em !important; border: none !important; }}
    .btn-agregado button {{ background-color: #1e7e34 !important; }}
    .reloj-container {{ background-color: #fff2f2; padding: 10px; border-radius: 15px; border: 2px solid #e21b2c; text-align: center; margin: 15px 0; }}
    .reloj-xl {{ color: #e21b2c; font-size: {TAMANO_RELOJ}px !important; font-weight: 900; line-height: 1; }}
    </style>
    """, unsafe_allow_html=True)

# --- FASE 0: PERFIL ---
if st.session_state.fase == 'perfil':
    st.markdown("## 📋 Datos del Participante")
    with st.form("perfil"):
        sexo = st.radio("Sexo:", ["Masculino", "Femenino", "Otro"])
        edad = st.selectbox("Edad:", ["Menos de 20", "20-30", "30-50", "Más de 50"])
        if st.form_submit_button("Continuar"):
            st.session_state.datos_usuario.update({'sexo': sexo, 'edad': edad})
            st.session_state.fase = 'compra_milanesa'
            st.rerun()

# --- FASE 1: COMPRA MILANESA ---
elif st.session_state.fase == 'compra_milanesa':
    st.image("milanesa.avif", use_container_width=True)
    if st.button("🛒 COMPRAR MILANESA"):
        st.session_state.fase = 'oferta_reloj'
        st.session_state.timer_start = time.time()
        st.rerun()

# --- FASE 2: EL REPARTIDOR SALE EN (OFERTA DIRECTA) ---
elif st.session_state.fase == 'oferta_reloj':
    st.success("¡Pedido confirmado! Se está armando tu pedido...")
    reloj_placeholder = st.empty()
    elapsed = time.time() - st.session_state.timer_start
    remaining = max(0, int(35 - elapsed))

    with reloj_placeholder.container():
        st.markdown(f"<div class='reloj-container'><p style='margin:0; font-weight:bold;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{remaining:02d}</p></div>", unsafe_allow_html=True)

    postres = [("chocotorta.png", "Chocotorta $2.000"), ("flan.jpg", "Flan Mixto $2.000"), ("tiramisu.png", "Tiramisú $2.000")]
    for archivo, nombre in postres:
        c1, c2, c3 = st.columns([1, 1.5, 0.8])
        with c1: 
            if os.path.exists(archivo): st.image(archivo, width=TAMANO_FOTO)
        with c2: st.markdown(f"<br><b>{nombre}</b>", unsafe_allow_html=True)
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            es_parte = nombre in st.session_state.carrito
            if es_parte: st.markdown('<div class="btn-agregado">', unsafe_allow_html=True)
            if st.button("Agregado" if es_parte else "Sumar", key=nombre):
                if 't_reaccion' not in st.session_state.datos_usuario:
                    st.session_state.datos_usuario['t_reaccion'] = round(elapsed, 2)
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

# --- FASE 3: PREGUNTAS Y GUARDADO ---
elif st.session_state.fase == 'preguntas':
    st.title("💡 Unas últimas preguntas")
    with st.form("final"):
        motivo = st.radio("¿Por qué tomaste esa decisión?", ["Tentación", "Precio", "Urgencia", "Otro"])
        hubiera = st.radio("¿Lo hubieras pedido sin la oferta?", ["Sí", "No"])
        if st.form_submit_button("Finalizar"):
            try:
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Sexo": st.session_state.datos_usuario['sexo'],
                    "Edad": st.session_state.datos_usuario['edad'],
                    "Eligio": "SI" if st.session_state.carrito else "NO",
                    "Postres": ", ".join(st.session_state.carrito),
                    "Tiempo_Seg": st.session_state.datos_usuario.get('t_reaccion', "N/A"),
                    "Motivo": motivo,
                    "Sin_Oferta": hubiera
                }])
                conn.create(data=nueva_fila) # AQUÍ SE SINCRONIZA
                st.session_state.fase = 'gracias'
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.fase == 'gracias':
    st.balloons()
    st.success("¡Tu pedido está en camino!")
    st.write("Gracias por participar.")


