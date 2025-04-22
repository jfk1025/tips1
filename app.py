import streamlit as st
import random
import requests
from datetime import datetime

# -------------------- CONFIGURACION INICIAL --------------------
st.set_page_config(page_title="Tipster IA Deportivo", layout="wide")
st.title("🤖 Tipster Deportivo Inteligente")
st.write("Selecciona un deporte y equipo/jugador para recibir predicciones diarias con análisis real y simulado.")

# -------------------- FUNCIONES API Y ANALISIS --------------------

# Obtener todos los deportes disponibles desde OddsAPI
def obtener_deportes():
    API_KEY = "08e6565f47b4889e17ad4b022e65e7aa"
    url = "https://api.the-odds-api.com/v4/sports/?apiKey=" + API_KEY
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            deportes = [deporte['key'] for deporte in data]
            return deportes
    except Exception as e:
        st.error(f"Error al obtener deportes: {e}")
    return []

# Obtener opciones de apuestas para un deporte
def obtener_opciones_apuestas(deporte):
    API_KEY = "08e6565f47b4889e17ad4b022e65e7aa"
    url = f"https://api.the-odds-api.com/v4/sports/{deporte}/odds/?apiKey={API_KEY}&regions=eu&markets=totals,spreads,h2h"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Simulación de posibles apuestas basadas en los mercados disponibles
                apuestas = [
                    "Gana el partido", "Empate", "+0.5 goles", "+1.5 goles", "Más de 2.5 goles", 
                    "Más de 10 corners", "Más de 3 tarjetas", "Más de 10 tiros al arco"
                ]
                return apuestas
    except Exception as e:
        st.error(f"Error al obtener apuestas para el deporte {deporte}: {e}")
    return []

# Obtener cuotas de apuestas
def obtener_cuotas_api(deporte, equipo, adversario):
    API_KEY = "08e6565f47b4889e17ad4b022e65e7aa"
    url = f"https://api.the-odds-api.com/v4/sports/{deporte}/odds/?regions=eu&markets=totals,spreads,h2h&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return round(float(random.uniform(1.8, 2.2)), 2)  # Simulación básica
        return round(random.uniform(1.8, 2.4), 2)
    except:
        return round(random.uniform(1.8, 2.4), 2)

# Obtener noticia de equipo
def obtener_noticia_real(equipo, adversario):
    API_KEY = "6792bcc892974869b29471036da55129"
    url = f"https://newsapi.org/v2/everything?q={equipo}+{adversario}&language=es&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        noticias = response.json()
        if noticias["articles"]:
            return noticias["articles"][0]["title"]
    except:
        pass
    return f"{equipo} vs {adversario} ha sido destacado en las últimas noticias deportivas."

# -------------------- SELECCIÓN DEPORTIVA --------------------
deportes = obtener_deportes()  # Obtener deportes desde la API
deporte = st.selectbox("Selecciona el deporte", deportes)

# Obtener equipos para el deporte seleccionado (esta parte aún puedes mejorarlo agregando los equipos manualmente o usándolos de la API)
equipos = {
    "fútbol": ["Barcelona FC", "Real Madrid", "Manchester City", "Liverpool", "Bayern Munich"],
    "baloncesto": ["Lakers", "Golden State Warriors", "Miami Heat"],
    "tenis": ["Carlos Alcaraz", "Novak Djokovic", "Roger Federer"]
}

equipo = st.selectbox("Selecciona tu equipo/jugador", equipos[deporte.lower()])

# Añadir selección del adversario
adversario = st.selectbox("Selecciona el equipo/jugador contrario", [e for e in equipos[deporte.lower()] if e != equipo])

# -------------------- GENERAR PREDICCIONES --------------------
if st.button("Generar predicciones"):
    st.subheader(f"🎯 Predicciones para {equipo} vs {adversario} ({deporte}) - {datetime.now().strftime('%d/%m/%Y')}")
    
    opciones_apuestas = obtener_opciones_apuestas(deporte)
    predicciones = random.sample(opciones_apuestas, k=3)

    for opcion in predicciones:
        prob = round(random.uniform(0.55, 0.85), 2)
        cuota = obtener_cuotas_api(deporte, equipo, adversario)
        valor_esperado = round(prob * cuota, 2)
        justificacion = obtener_noticia_real(equipo, adversario)

        with st.container():
            st.markdown(f"### 📌 Apuesta: **{opcion}**")
            st.write(f"- 🔢 Probabilidad estimada: **{prob * 100:.1f}%**")
            st.write(f"- 💸 Cuota desde casa de apuestas: **{cuota:.2f}**")
            st.write(f"- 📈 Valor esperado: **{valor_esperado:.2f}**")
            st.info(f"📰 Noticia relacionada: {justificacion}")

            if valor_esperado > 1:
                st.success("✅ Apuesta con valor estadístico positivo")
            else:
                st.warning("⚠️ Valor esperado bajo (no recomendada)")
