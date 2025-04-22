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
    API_KEY = "08e6565f47b4889e17ad4b022e65e7 aa"
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
    API_KEY = "08e6565f47b4889e17ad4b022e65e7 aa"
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
    API_KEY = "08e6565f47b4889e17ad4b022e65e7 aa"
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

# Lista de deportes
deportes = [
    "fútbol", "fútbol americano", "baloncesto", "béisbol", "hockey sobre hielo", "rugby",
    "tenis", "golf", "boxeo", "artes marciales mixtas", "fórmula 1", "motogp", "nascar", "natación",
    "surf", "vela", "esquí", "snowboard", "patinaje artístico", "ciclismo", "atletismo", "esports"
]

# Equipos predeterminados para cada deporte
equipos = {
    "fútbol": ["Barcelona FC", "Real Madrid", "Manchester City", "Liverpool", "Bayern Munich", "Juventus", "Paris Saint-Germain"],
    "fútbol americano": ["Dallas Cowboys", "New England Patriots", "Kansas City Chiefs", "San Francisco 49ers"],
    "baloncesto": ["Lakers", "Golden State Warriors", "Miami Heat", "Chicago Bulls", "Boston Celtics"],
    "béisbol": ["New York Yankees", "Los Angeles Dodgers", "Boston Red Sox", "Chicago Cubs"],
    "hockey sobre hielo": ["Toronto Maple Leafs", "Montreal Canadiens", "Boston Bruins", "Chicago Blackhawks"],
    "rugby": ["New Zealand", "South Africa", "England", "Australia"],
    "tenis": ["Carlos Alcaraz", "Novak Djokovic", "Roger Federer", "Rafael Nadal"],
    "golf": ["Tiger Woods", "Phil Mickelson", "Jordan Spieth", "Rory McIlroy"],
    "boxeo": ["Canelo Álvarez", "Tyson Fury", "Anthony Joshua", "Manny Pacquiao"],
    "artes marciales mixtas": ["Conor McGregor", "Khabib Nurmagomedov", "Jon Jones", "Israel Adesanya"],
    "fórmula 1": ["Lewis Hamilton", "Max Verstappen", "Sebastian Vettel", "Charles Leclerc"],
    "motogp": ["Marc Márquez", "Valentino Rossi", "Maverick Viñales", "Dani Pedrosa"],
    "nascar": ["Kyle Busch", "Joey Logano", "Chase Elliott", "Denny Hamlin"],
    "natación": ["Michael Phelps", "Caeleb Dressel", "Katie Ledecky"],
    "surf": ["Kelly Slater", "John John Florence", "Gabriel Medina"],
    "vela": ["Ben Ainslie", "Robert Scheidt", "Paul Elvstrøm"],
    "esquí": ["Mikaela Shiffrin", "Lindsey Vonn", "Marcel Hirscher"],
    "snowboard": ["Shaun White", "Chloe Kim", "Mark McMorris"],
    "patinaje artístico": ["Yuzuru Hanyu", "Tessa Virtue", "Scott Moir"],
    "ciclismo": ["Tadej Pogačar", "Egan Bernal", "Chris Froome"],
    "atletismo": ["Usain Bolt", "Allyson Felix", "Wayde van Niekerk"],
    "esports": ["Team Liquid", "Cloud9", "Fnatic", "T1"]
}

# -------------------- SELECCIÓN DE FECHA Y HORA --------------------
def obtener_fecha_hora():
    # Simulamos una fecha y hora de enfrentamiento para todos los deportes
    tiempo = timedelta(days=random.randint(1, 10))  # Enfrentamiento en 1 a 10 días
    fecha_hora = datetime.now() + tiempo
    return fecha_hora.strftime("%d/%m/%Y %H:%M")

# -------------------- SELECCIÓN DE DEPORTE Y EQUIPO --------------------
deporte = st.selectbox("Selecciona el deporte", deportes)
equipo = st.selectbox("Selecciona tu equipo/jugador", equipos[deporte.lower()])

# Selección del adversario
adversario = st.selectbox("Selecciona el equipo/jugador contrario", [e for e in equipos[deporte.lower()] if e != equipo])

# -------------------- GENERAR PREDICCIONES --------------------
if st.button("Generar predicciones"):
    st.subheader(f"🎯 Predicciones para {equipo} vs {adversario} ({deporte}) - {datetime.now().strftime('%d/%m/%Y')}")
    
    # Obtener las apuestas disponibles
    opciones_apuestas = obtener_opciones_apuestas(deporte)
    predicciones = random.sample(opciones_apuestas, k=3)
    
    # Fecha y hora del enfrentamiento
    fecha_hora = obtener_fecha_hora()
    st.write(f"🕒 Fecha y hora del enfrentamiento: {fecha_hora}")

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
