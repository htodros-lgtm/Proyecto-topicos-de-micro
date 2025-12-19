import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN ---
TAMANO_FOTO  = 100  
TAMANO_RELOJ = 35 
HOJA_GOOGLE  = "Respuestas" # ¡Asegurate que tu hoja en Excel se llame así!

st.set_page_config(page_title="Rappi Experimento", layout="centered")

# CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)

# VARIABLES DE ESTADO
if 'fase' not in st.session_state:
    st.session_state.fase = 'perfil'
if 'carrito' not in st.session_state:
    st.session_state.carrito = set()
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

st.markdown(f"""
    <style>
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
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    if st.button("🛒 COMPRAR MILANESA"):
        st.session_state.fase = 'oferta_reloj'
        st.session_state.timer_start = time.time()
        st.rerun()

# --- FASE 2: RELOJ + POSTRES ---
elif st.session_state.fase == 'oferta_reloj':
    st.success("¡Pedido confirmado! Se está armando tu pedido...")
    st.write("Podés agregar un postre antes de que salga el repartidor.")
    
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

# --- FASE 3: PREGUNTAS Y GUARDADO ACUMULATIVO ---
elif st.session_state.fase == 'preguntas':
    st.title("💡 Unas últimas preguntas")
    compro_postre = len(st.session_state.carrito) > 0
    
    with st.form("final"):
        if compro_postre:
            st.info("Vimos que **AGREGASTE** postre.")
            motivo = st.radio("¿Qué influyó más en tu decisión?", ["La oferta/precio", "La urgencia del reloj", "Tenía antojo", "Otro"])
            hubiera = st.radio("¿Lo hubieras comprado a precio normal ($4000)?", ["Sí", "No"])
        else:
            st.info("Vimos que **NO** agregaste postre.")
            motivo = st.radio("¿Por qué decidiste no comprar?", ["Muy caro", "No quería postre", "Me puso nervioso el tiempo", "Otro"])
            hubiera = st.radio("¿Si tuvieras más tiempo para pensar, lo comprabas?", ["Sí", "No"])

        if st.form_submit_button("Finalizar"):
            try:
                # 1. Creamos la fila nueva con los datos actuales
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Sexo": st.session_state.datos_usuario['sexo'],
                    "Edad": st.session_state.datos_usuario['edad'],
                    "Eligio": "SI" if compro_postre else "NO",
                    "Postres": ", ".join(st.session_state.carrito),
                    "Tiempo_Seg": st.session_state.datos_usuario.get('t_reaccion', "N/A"),
                    "Motivo": motivo,
                    "Sin_Oferta": hubiera
                }])
                
                # 2. Leemos lo que ya existe en la hoja "Respuestas"
                # ttl=0 es CLAVE para que no use memoria vieja
                try:
                    df_existente = conn.read(worksheet=HOJA_GOOGLE, ttl=0)
                    df_existente = df_existente.dropna(how='all') # Limpiamos filas vacías
                    # 3. Pegamos lo nuevo abajo de lo viejo
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                except Exception:
                    # Si falla al leer (ej. es la primera vez), usamos solo la nueva fila
                    df_final = nueva_fila

                # 4. Actualizamos la hoja completa
                conn.update(worksheet=HOJA_GOOGLE, data=df_final)
                
                st.session_state.fase = 'gracias'
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

elif st.session_state.fase == 'gracias':
    st.balloons()
    st.success("¡Tu pedido está en camino!")
    st.write("Gracias por participar.")



