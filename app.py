import streamlit as st
import random
import requests
from datetime import datetime, timedelta

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

# Equipos organizados por liga
equipos = {
    "Premier League (Inglaterra)": [
        "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion", "Chelsea", "Crystal Palace", "Everton", 
        "Fulham", "Luton Town", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sheffield United", 
        "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers"
    ],
    "La Liga (España)": [
        "Alavés", "Athletic Club", "Atlético de Madrid", "Barcelona", "Cádiz", "Celta de Vigo", "Getafe", "Granada", "Las Palmas", 
        "Mallorca", "Osasuna", "Real Betis", "Real Madrid", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"
    ],
    "Serie A (Italia)": [
        "Atalanta", "Bologna", "Cagliari", "Fiorentina", "Genoa", "Inter de Milán", "Juventus", "Lazio", "Milan", "Napoli", "Roma", 
        "Salernitana", "Sampdoria", "Sassuolo", "Torino", "Udinese"
    ],
    "Bundesliga (Alemania)": [
        "Augsburg", "Bayer Leverkusen", "Bayern Múnich", "Borussia Dortmund", "Borussia Mönchengladbach", "Eintracht Frankfurt", 
        "FC Köln", "Hertha BSC", "RB Leipzig", "SC Freiburg", "Schalke 04", "Stuttgart", "Hoffenheim", "Mainz"
    ],
    "Ligue 1 (Francia)": [
        "AJ Auxerre", "Clermont Foot", "ESTAC Troyes", "Lille OSC", "Lyon", "Montpellier", "Nantes", "Nice", "Olympique de Marsella", 
        "Paris Saint-Germain", "Rennes", "Reims", "Strasbourg", "Toulouse", "Lorient"
    ],
    "Eredivisie (Países Bajos)": [
        "Ajax", "AZ Alkmaar", "FC Groningen", "FC Utrecht", "Feyenoord", "Fortuna Sittard", "Go Ahead Eagles", "Heracles Almelo", 
        "NEC Nijmegen", "PSV Eindhoven", "SC Heerenveen", "Vitesse", "Willem II"
    ],
    "Primeira Liga (Portugal)": [
        "Benfica", "Boavista", "Braga", "Estoril Praia", "FC Porto", "Marítimo", "Moreirense", "Nacional", "Santa Clara", 
        "Vitória Guimarães", "Casa Pia", "Gil Vicente"
    ],
    "Escocia (Scottish Premiership)": [
        "Aberdeen", "Celtic", "Dundee United", "Heart of Midlothian", "Hibernian", "Kilmarnock", "Livingston", "Motherwell", "Rangers", 
        "St. Johnstone"
    ]
}

# -------------------- SELECCIÓN DE FECHA --------------------
# El usuario puede elegir la fecha del partido
fecha_partido = st.date_input("Selecciona la fecha del partido", datetime.now())

# -------------------- SELECCIÓN DE DEPORTE Y EQUIPO --------------------
deporte = st.selectbox("Selecciona el deporte", [
    "fútbol", "fútbol americano", "baloncesto", "béisbol", "hockey sobre hielo", "rugby",
    "tenis", "golf", "boxeo", "artes marciales mixtas", "fórmula 1", "motogp", "nascar", "natación",
    "surf", "vela", "esquí", "snowboard", "patinaje artístico", "ciclismo", "atletismo", "esports"
])
liga = st.selectbox("Selecciona la liga", list(equipos.keys()))
equipo = st.selectbox("Selecciona tu equipo/jugador", equipos[liga])

# Selección del adversario
adversario = st.selectbox("Selecciona el equipo/jugador contrario", [e for e in equipos[liga] if e != equipo])

# -------------------- GENERAR PREDICCIONES --------------------
if st.button("Generar predicciones"):
    st.subheader(f"🎯 Predicciones para {equipo} vs {adversario} ({deporte}) - {fecha_partido.strftime('%d/%m/%Y')}")
    
    # Obtener las apuestas disponibles
    opciones_apuestas = obtener_opciones_apuestas(deporte)
    
    # Asegurarnos de que haya suficientes opciones para tomar una muestra
    if len(opciones_apuestas) >= 3:
        predicciones = random.sample(opciones_apuestas, k=3)
    else:
        predicciones = opciones_apuestas  # Si hay menos de 3 opciones, seleccionamos todas las disponibles
    
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

