
import streamlit as st
import requests
import random
from datetime import datetime

# -------------------- CONFIGURACION INICIAL --------------------
st.set_page_config(page_title="Tipster IA Deportivo", layout="wide")
st.title("🤖 Tipster Deportivo Inteligente")
st.write("Selecciona un deporte y equipo/jugador para recibir predicciones diarias con análisis.")

# -------------------- OPCIONES DE EJEMPLO --------------------
deportes = ["Fútbol", "Tenis", "Baloncesto"]
equipos_futbol = ["Barcelona FC", "Real Madrid", "Manchester City", "Liverpool"]
jugadores_tenis = ["Carlos Alcaraz", "Novak Djokovic"]
equipos_basket = ["Lakers", "Golden State Warriors"]

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

if deporte == "Fútbol":
    equipo = st.selectbox("Selecciona el equipo", equipos_futbol)
elif deporte == "Tenis":
    equipo = st.selectbox("Selecciona el jugador", jugadores_tenis)
elif deporte == "Baloncesto":
    equipo = st.selectbox("Selecciona el equipo", equipos_basket)

# -------------------- API FAKE DE CUOTAS --------------------
def obtener_cuota_simulada(prob):
    return round(1 / prob + random.uniform(
