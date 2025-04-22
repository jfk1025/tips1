import streamlit as st
import random
from datetime import datetime

# -------------------- CONFIGURACION INICIAL --------------------
st.set_page_config(page_title="Tipster IA Deportivo", layout="wide")
st.title("🤖 Tipster Deportivo Inteligente")
st.write("Selecciona un deporte y equipo/jugador para recibir predicciones diarias con análisis.")

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

# -------------------- FUNCIONES SIMULADAS --------------------
def obtener_cuota_simulada(prob):
    return round(1 / prob + random.uniform(0.05, 0.3), 2)

def analizar_noticias_simulado(equipo):
    ejemplos = [
        f"El equipo/jugador {equipo} ha mostrado un gran rendimiento en los últimos partidos.",
        f"Bajas confirmadas por lesión afectan el desempeño de {equipo}.",
        f"Condiciones favorables para un resultado positivo de {equipo}.",
        f"{equipo} viene de una racha positiva en esta categoría de apuestas."
    ]
    return random.choice(ejemplos)

# -------------------- GENERAR PREDICCIONES --------------------
if st.button("Generar predicciones"):
    st.subheader(f"🎯 Predicciones para {equipo} ({deporte}) - {datetime.now().strftime('%d/%m/%Y')}")

    predicciones = random.sample(opciones_apuestas[deporte], k=3)

    for opcion in predicciones:
        prob = round(random.uniform(0.55, 0.85), 2)
        cuota = obtener_cuota_simulada(prob)
        valor_esperado = round(prob * cuota, 2)
        justificacion = analizar_noticias_simulado(equipo)

        with st.container():
            st.markdown(f"### 📌 Apuesta: **{opcion}**")
            st.write(f"- 🔢 Probabilidad estimada: **{prob * 100:.1f}%**")
            st.write(f"- 💸 Cuota promedio: **{cuota:.2f}**")
            st.write(f"- 📈 Valor esperado: **{valor_esperado:.2f}**")
            st.info(f"🧠 Justificación automática: {justificacion}")

            if valor_esperado > 1:
                st.success("✅ Apuesta con valor estadístico positivo")
            else:
                st.warning("⚠️ Valor esperado bajo (no recomendada)")
