import streamlit as st
import requests
from gtts import gTTS
import os
import tempfile

# ===============================
# 🌦 Weather
# ===============================
def get_weather(city):
    try:
        API_KEY = "YOUR_OPENWEATHER_API_KEY"  # optional
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=5).json()
        return data["main"]["temp"], data["main"]["humidity"]
    except:
        return 30, 60  # fallback

# ===============================
# 🌾 Crop → Problems → Solutions
# (you can extend this to 100+)
# ===============================
PROBLEM_SOLUTIONS = {
    "Rice": {
        "yellow": "Aakulu pasupu ga unnayi. Nitrogen deficiency undi. Urea vadandi.",
        "poka": "Keetakala samasya undi. Neem oil 5ml/L spray cheyyandi.",
        "stem": "Stem borer attack undi. Chlorantraniliprole spray cheyyandi.",
        "dry": "Nela podi ga undi. Irrigation penchandi."
    },
    "Cotton": {
        "bollworm": "Bollworm attack undi. Pheromone traps vadandi.",
        "yellow": "Nitrogen deficiency undi. Urea vadandi.",
        "poka": "Keetakala samasya undi. Neem oil spray cheyyandi."
    },
    "Tomato": {
        "blight": "Blight disease undi. Copper fungicide vadandi.",
        "leaf": "Leaf curl virus undochu. Whitefly control cheyyandi.",
        "aphids": "Aphids undi. Imidacloprid spray cheyyandi."
    },
    "Chillies": {
        "curl": "Leaf curl virus undi. Whitefly control cheyyandi.",
        "root": "Root rot undi. Drainage improve cheyyandi."
    },
    "Maize": {
        "slow": "Growth slow undi. Zinc sulphate vadandi.",
        "spot": "Leaf spot disease undi. Carbendazim vadandi."
    },
    "Wheat": {
        "yellow": "Nitrogen deficiency undi. Urea 30kg/acre vadandi.",
        "fungal": "Fungal disease undi. Sulphur spray cheyyandi."
    },
    "Sugarcane": {
        "borer": "Top shoot borer undi. Recommended pesticide vadandi.",
        "dry": "Nela podi ga undi. Irrigation penchandi."
    }
}

# ===============================
# 🤖 Generate Advice
# ===============================
def generate_advice(crop, problem, temp, humidity):
    advice = []

    crop_db = PROBLEM_SOLUTIONS.get(crop, {})
    for key, sol in crop_db.items():
        if key in problem:
            advice.append(sol)

    if temp > 34:
        advice.append("Temperature ekkuva undi. Irrigation frequency penchandi.")
    if humidity > 75:
        advice.append("Humidity ekkuva undi. Fungal disease risk undi.")

    if not advice:
        return "Mee problem clear ga ledu. Agriculture officer ni contact cheyyandi."

    return " ".join(advice)

# ===============================
# 🔊 Text → Voice (optional)
# ===============================
def speak_telugu(text):
    tts = gTTS(text=text, lang="te")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name)

# ===============================
# 🚜 STREAMLIT UI
# ===============================
st.set_page_config(page_title="Farmer AI Assistant", page_icon="🌾")
st.title("🌾 Farmer AI Assistant")

crop = st.selectbox(
    "🌱 Crop select cheyyandi",
    ["Rice", "Cotton", "Tomato", "Chillies", "Maize", "Wheat", "Sugarcane"]
)

problem = st.text_input("📝 Mee problem type cheyyandi (English/Telugu keywords)")

city = st.text_input("📍 Mee city (optional)", value="Hyderabad")

if st.button("🤖 Get Advice"):
    temp, humidity = get_weather(city)
    st.info(f"🌦 Weather: {temp}°C | Humidity: {humidity}%")

    advice = generate_advice(crop, problem.lower(), temp, humidity)

    st.success("🤖 AI Advice:")
    st.write(advice)

    if st.checkbox("🔊 Voice lo cheppali"):
        speak_telugu(advice)

