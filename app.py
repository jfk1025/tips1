import streamlit as st
import random
import requests
from datetime import datetime, timedelta

# -------------------- CONFIGURACION INICIAL --------------------
st.set_page_config(page_title="Tipster IA Deportivo", layout="wide")
st.title("🤖 Tipster Deportivo Inteligente")
st.write("Selecciona un deporte y equipo/jugador para recibir predicciones diarias con análisis real y simulado.")

# -------------------- OPCIONES DE EJEMPLO --------------------
deportes = ["Fútbol", "Tenis", "Baloncesto"]
equipos = {
    "Fútbol": ["Barcelona FC", "Real Madrid", "Manchester City", "Liverpool"],
    "Tenis": ["Carlos Alcaraz", "Novak Djokovic"],
    "Baloncesto": ["Lakers", "Golden State Warriors"]
}

opciones_apuestas = {
    "Fútbol": [
        "+0.5 goles", "+1.5 goles", "Gana el partido", "Empate",
        "+6.5 corners", "+1.5 tarjetas", "Más de 3 tiros al arco"
    ],
    "Tenis": [
        "Gana el partido", "Más de 2 sets", "Gana 2-0", "Más de 10 aces"
    ],
    "Baloncesto": [
        "Más de 100 puntos", "Gana el partido", "Más de 10 triples", "Victoria por más de 5"
    ]
}

# -------------------- SELECCIÓN DEPORTIVA --------------------
deporte = st.selectbox("Selecciona el deporte", deportes)
equipo = st.selectbox("Selecciona el equipo/jugador", equipos[deporte])

# -------------------- SELECCIONAR FECHA DEL ENFRENTAMIENTO --------------------
fecha_encuentro = st.date_input("Selecciona la fecha del encuentro", datetime.today())

# -------------------- FUNCIONES API Y ANALISIS --------------------
def obtener_cuotas_api(deporte, equipo):
    # Ejemplo usando OddsAPI (requiere clave personal de API)
    API_KEY = "tu_clave_api_oddsapi"
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?regions=eu&markets=totals,spreads,h2h&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return round(float(random.uniform(1.8, 2.2)), 2)  # Simulación básica
        return round(random.uniform(1.8, 2.4), 2)
    except:
        return round(random.uniform(1.8, 2.4), 2)

def obtener_noticia_real(equipo):
    # NewsAPI (requiere clave personal de API)
    API_KEY = "tu_clave_api_newsapi"
    url = f"https://newsapi.org/v2/everything?q={equipo}&language=es&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        noticias = response.json()
        if noticias["articles"]:
            return noticias["articles"][0]["title"]
    except:
        pass
    return f"{equipo} ha sido destacado en las últimas noticias deportivas."

# -------------------- GENERAR PREDICCIONES --------------------
if st.button("Generar predicciones"):
    st.subheader(f"🎯 Predicciones para {equipo} ({deporte}) - {fecha_encuentro.strftime('%d/%m/%Y')}")

    # Asegurarse de que haya suficientes opciones para tomar una muestra
    if len(opciones_apuestas[deporte]) >= 3:
        predicciones = random.sample(opciones_apuestas[deporte], k=3)
    else:
        predicciones = opciones_apuestas[deporte]  # Seleccionamos todas las disponibles

    for opcion in predicciones:
        prob = round(random.uniform(0.55, 0.85), 2)
        cuota = obtener_cuotas_api(deporte, equipo)
        valor_esperado = round(prob * cuota, 2)
        justificacion = obtener_noticia_real(equipo)

        with st.container():
            st.markdown(f
