import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN ---
TAMANO_FOTO  = 100  
TAMANO_RELOJ = 25  
HOJA_GOOGLE  = "Respuestas" 

st.set_page_config(page_title="Topicos de Microeconomia", layout="centered")

# CONEXIÓN (INTACTA)
conn = st.connection("gsheets", type=GSheetsConnection)

# VARIABLES DE ESTADO
if 'fase' not in st.session_state:
    st.session_state.fase = 'perfil'
if 'carrito' not in st.session_state:
    st.session_state.carrito = set()
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

# ESTILOS CSS
st.markdown(f"""
    <style>
    .stButton>button {{ border-radius: 10px !important; background-color: #e21b2c !important; color: white !important; font-weight: bold !important; width: 100% !important; height: 2.8em !important; border: none !important; }}
    .btn-agregado button {{ background-color: #1e7e34 !important; }}
    
    /* MODIFICACIÓN: Caja más ajustada verticalmente */
    .reloj-container {{ 
        background-color: #fff2f2; 
        padding: 2px 20px; /* (MODIFICADO: Menos relleno vertical para quitar aire) */
        border-radius: 15px; 
        border: 2px solid #e21b2c; 
        text-align: center; 
        margin: 10px auto; 
        width: fit-content; 
    }}
    
    /* MODIFICACIÓN: Quitamos el margen del número para que no empuje el borde abajo */
    .reloj-xl {{ 
        color: #e21b2c; 
        font-size: {TAMANO_RELOJ}px !important; 
        font-weight: 900; 
        line-height: 1.1; 
        margin: 0 !important; /* ESTO QUITA EL ESPACIO INFERIOR */
        padding-bottom: 2px;
    }}
    
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {{
        justify-content: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- FASE 0: PERFIL ---
if st.session_state.fase == 'perfil':
    st.markdown("## Datos generales")
    with st.form("perfil"):
        sexo = st.radio("Sexo:", ["Masculino", "Femenino", "Otro"])
        edad = st.selectbox("Edad:", ["Menos de 20", "20-40", "40-60", "Más de 60"])
        if st.form_submit_button("Continuar"):
            st.session_state.datos_usuario.update({'sexo': sexo, 'edad': edad})
            st.session_state.fase = 'Introducción' 
            st.rerun()

# --- FASE NUEVA: INSTRUCCIONES ---
elif st.session_state.fase == 'Introducción':
    st.title("Contexto del Experimento")
    st.info("""
    📢 **Imaginá la siguiente situación:**
    
    21hs estás en tu casa, fue un largo dia de trabajo y no tenes ganas de cocinar. 
    Por suerte existen las aplicaciones de delivery que te permiten pedir comida desde la comodidad de tu cama.
    Abrís la app y tras meditarlo un rato -más largo de lo que uno pensaría- te decidis por pedirte esa...
    
    A continuación vas a ver el menú. Actuá con naturalidad como si fuera una compra real.
    """)
    st.write("")
    if st.button("Ir al experimento"):
        st.session_state.fase = 'compra_milanesa'
        st.rerun()

# --- FASE 1: COMPRA MILANESA ---
elif st.session_state.fase == 'compra_milanesa':
    st.markdown("## 🍽️ Bodegón 'El Buen Gusto'")
    
    if os.path.exists("milanesa.avif"):
        st.image("milanesa.avif", use_container_width=True)
    
    st.write("") 
    
    col_texto, col_boton = st.columns([1.5, 1])
    
    with col_texto:
        st.markdown("### Milanesa con fritas - **$18.000**")
    
    with col_boton:
        if st.button("🛒 PAGAR"):
            st.session_state.fase = 'oferta_reloj'
            st.session_state.timer_start = time.time()
            st.rerun()

# --- FASE 2: RELOJ + POSTRES ---
elif st.session_state.fase == 'oferta_reloj':
    st.markdown("## ¡Pedido confirmado! Se está armando tu pedido...")
    st.markdown("<h4 style='text-align: center;'>Podés agregar un postre antes de que salga el repartidor.</h4>", unsafe_allow_html=True)
    
    reloj_placeholder = st.empty()
    elapsed = time.time() - st.session_state.timer_start
    remaining = max(0, int(35 - elapsed))

    with reloj_placeholder.container():
        # Agregamos margin:0 al texto del título "EL REPARTIDOR..." también
        st.markdown(f"<div class='reloj-container'><p style='margin:0; font-weight:bold; font-size:14px; padding-bottom:2px;'>EL REPARTIDOR SALE EN:</p><p class='reloj-xl'>00:{remaining:02d}</p></div>", unsafe_allow_html=True)

    # Lista de postres
    postres = [("chocotorta.png", "Chocotorta $1.900"), ("flan.jpg", "Flan Mixto $1.900"), ("tiramisu.png", "Tiramisú $1.900")]
    
    for archivo, nombre in postres:
        c1, c2, c3 = st.columns([0.03, 0.04, 0.1], gap="small")
        
        with c1: 
            if os.path.exists(archivo): st.image(archivo, width=TAMANO_FOTO)
        
        with c2: 
            st.markdown(f"<div style='padding-top: 15px; font-size: 18px;'><b>{nombre}</b></div>", unsafe_allow_html=True)
        
        with c3:
            st.markdown("<div style='padding-top: 10px;'>", unsafe_allow_html=True) 
            es_parte = nombre in st.session_state.carrito
            if es_parte: st.markdown('<div class="btn-agregado">', unsafe_allow_html=True)
            
            if st.button("Agregado" if es_parte else "Sumar", key=nombre):
                if 't_reaccion' not in st.session_state.datos_usuario:
                    st.session_state.datos_usuario['t_reaccion'] = round(elapsed, 2)
                if es_parte: st.session_state.carrito.remove(nombre)
                else: st.session_state.carrito.add(nombre)
                st.rerun()
            
            if es_parte: st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---") 

    if remaining > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.fase = 'preguntas'
        st.rerun()

# --- FASE 3: PREGUNTAS Y GUARDADO ---
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
                
                try:
                    df_existente = conn.read(worksheet=HOJA_GOOGLE, ttl=0)
                    df_existente = df_existente.dropna(how='all')
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                except Exception:
                    df_final = nueva_fila

                conn.update(worksheet=HOJA_GOOGLE, data=df_final)
                
                st.session_state.fase = 'gracias'
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

elif st.session_state.fase == 'gracias':
    st.balloons()
    st.success("¡Tu pedido está en camino!")
    st.write("Gracias por participar.")

























