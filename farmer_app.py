import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import requests
import os
import time

# ===============================
# 🎙 Record voice
# ===============================
def record_voice(filename="temp.wav", duration=4, fs=44100):
    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        sf.write(filename, audio_data, fs)
        return filename
    except Exception as e:
        st.write("❌ Mic problem:", e)
        return None

# ===============================
# 🗣 Speech to Text (Telugu)
# ===============================
def speech_to_text(filename):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.record(source)
        text = r.recognize_google(audio, language="te-IN")
        return text.lower()
    except:
        return None

# ===============================
# 🌦 Weather API
# ===============================
def get_weather(city):
    try:
        API_KEY = "265470f445c17e91c1c1addba961bf5a1"  # Replace with your OpenWeatherMap key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return temp, humidity
    except:
        return 30, 60

# ===============================
# 🌾 Crop → Problem → Solution Database (50 problems included)
# ===============================
PROBLEM_SOLUTIONS = {
    "Rice": {
        "yellow leaves": "Nitrogen deficiency undi. Urea 45 kg/acre vadandi.",
        "pale leaves": "Nitrogen thakkuva undi. Urea spray cheyyandi.",
        "brown spot": "Brown spot disease undi. Mancozeb spray cheyyandi.",
        "blast disease": "Rice blast undi. Tricyclazole spray cheyyandi.",
        "leaf folder": "Leaf folder undi. Chlorantraniliprole vadandi.",
        "stem borer": "Stem borer undi. Pheromone traps vadandi.",
        "hispa": "Rice hispa undi. Quinalphos spray cheyyandi.",
        "sheath blight": "Sheath blight undi. Validamycin spray cheyyandi.",
        "water logging": "Neellu jam ayyayi. Drainage improve cheyyandi.",
        "dry soil": "Neellu thakkuva. Irrigation penchandi.",
        "poor tillering": "Nitrogen deficiency undi. Top dressing cheyyandi.",
        "lodging": "Excess nitrogen undi. Fertilizer thagginchandi.",
        "slow growth": "Zinc deficiency undi. Zinc sulphate vadandi.",
        "grain discoloration": "Fungal infection undi. Fungicide vadandi."
    },
    "Cotton": {
        "bollworm": "Bollworm undi. Emamectin benzoate spray cheyyandi.",
        "pink bollworm": "Pink bollworm undi. Pheromone traps vadandi.",
        "whitefly": "Whitefly undi. Yellow sticky traps vadandi.",
        "aphids": "Aphids undi. Imidacloprid spray cheyyandi.",
        "thrips": "Thrips undi. Spinosad spray cheyyandi.",
        "jassids": "Jassids undi. Acephate spray cheyyandi.",
        "leaf reddening": "Magnesium deficiency undi. MgSO4 spray cheyyandi.",
        "yellow leaves": "Nitrogen deficiency undi. Urea vadandi.",
        "poor flowering": "Phosphorus thakkuva undi. DAP vadandi.",
        "square shedding": "Water stress undi. Regular irrigation cheyyandi.",
        "root rot": "Root rot undi. Drainage improve cheyyandi.",
        "slow growth": "Micronutrient deficiency undi. Multi-mix spray cheyyandi."
    },
    "Maize": {
        "yellow leaves": "Nitrogen deficiency undi. Urea vadandi.",
        "slow growth": "Zinc deficiency undi. Zinc sulphate vadandi.",
        "leaf blight": "Leaf blight undi. Mancozeb spray cheyyandi.",
        "stem borer": "Stem borer undi. Chlorantraniliprole vadandi.",
        "fall armyworm": "Armyworm undi. Emamectin spray cheyyandi.",
        "poor cob formation": "Nutrient imbalance undi. Balanced fertilizer vadandi.",
        "dry soil": "Irrigation thakkuva undi. Neellu ivvandi.",
        "lodging": "High wind damage undi. Earthing-up cheyyandi."
    },
    "Wheat": {
        "yellow leaves": "Nitrogen deficiency undi. Urea 30 kg/acre vadandi.",
        "rust disease": "Rust disease undi. Propiconazole spray cheyyandi.",
        "powdery mildew": "Powdery mildew undi. Sulphur spray cheyyandi.",
        "aphids": "Aphids undi. Imidacloprid spray cheyyandi.",
        "poor tillering": "Nitrogen thakkuva undi. Top dressing cheyyandi.",
        "lodging": "Excess nitrogen undi. Fertilizer control cheyyandi.",
        "dry soil": "Irrigation penchandi."
    },
    "Sugarcane": {
        "early shoot borer": "Early shoot borer undi. Carbofuran vadandi.",
        "top shoot borer": "Top shoot borer undi. Chlorantraniliprole spray cheyyandi.",
        "internode borer": "Internode borer undi. Insecticide vadandi.",
        "red rot": "Red rot disease undi. Infected canes remove cheyyandi.",
        "wilt": "Wilt disease undi. Resistant varieties vadandi.",
        "yellow leaves": "Nitrogen deficiency undi. Urea vadandi.",
        "dry soil": "Neellu thakkuva undi. Irrigation penchandi."
    },
    "Tomato": {
        "leaf curl": "Leaf curl virus undi. Whitefly control cheyyandi.",
        "blight": "Blight disease undi. Copper fungicide vadandi.",
        "early blight": "Early blight undi. Mancozeb spray cheyyandi.",
        "late blight": "Late blight undi. Metalaxyl spray cheyyandi.",
        "fruit borer": "Fruit borer undi. Pheromone traps vadandi.",
        "blossom end rot": "Calcium deficiency undi. Calcium nitrate spray cheyyandi.",
        "yellow leaves": "Nitrogen deficiency undi. Urea spray cheyyandi.",
        "flower drop": "Water stress undi. Regular irrigation cheyyandi.",
        "thrips": "Thrips undi. Spinosad spray cheyyandi.",
        "aphids": "Aphids undi. Imidacloprid spray cheyyandi.",
        "powdery mildew": "Powdery mildew undi. Sulphur spray cheyyandi.",
        "root rot": "Root rot undi. Drainage improve cheyyandi.",
        "fruit rot": "Fruit rot undi. Carbendazim spray cheyyandi."
    },
    "Chillies": {
        "leaf curling": "Leaf curl virus undi. Whitefly control cheyyandi.",
        "thrips": "Thrips undi. Spinosad spray cheyyandi.",
        "aphids": "Aphids undi. Imidacloprid spray cheyyandi.",
        "powdery mildew": "Powdery mildew undi. Sulphur spray cheyyandi.",
        "root rot": "Root rot undi. Drainage improve cheyyandi.",
        "fruit rot": "Fruit rot undi. Carbendazim spray cheyyandi.",
        "flower drop": "Water stress undi. Neellu sarigga ivvandi.",
        "yellow leaves": "Nitrogen deficiency undi. Urea vadandi."
    }
}

# ===============================
# 🤖 Generate Advice
# ===============================
def generate_advice(crop, problem, temp, humidity):
    advice_list = []

    crop_db = PROBLEM_SOLUTIONS.get(crop, {})
    for key, solution in crop_db.items():
        if key in problem:
            advice_list.append(solution)

    if temp > 34:
        advice_list.append("Temperature ekkuva undi. Irrigation frequency penchandi.")
    if humidity > 75:
        advice_list.append("Humidity ekkuva undi. Fungal disease risk undi.")

    if not advice_list:
        return "Mee problem clear ga ledu. Agriculture officer ni contact cheyyandi."

    return ". ".join(advice_list)

# ===============================
# 🔊 Speak in Telugu
# ===============================
def speak(text):
    try:
        tts = gTTS(text=text, lang="te")
        tts.save("reply.mp3")
        return "reply.mp3"
    except:
        return None

# ===============================
# 🚜 Streamlit App
# ===============================
st.title("🌾 FARMER AI ASSISTANT 🌾")

# Crop selection
crop_name = st.selectbox("🌱 Select Crop:",
                         ["Rice","Cotton","Maize","Wheat","Sugarcane","Tomato","Chillies"])
st.write(f"✅ Crop selected: {crop_name}")

# Text input
problem_text = st.text_input("Type your problem here:")

# Voice input
if st.button("🎙 Record Voice Problem"):
    st.write("Recording... Speak now")
    voice_file = record_voice()
    if voice_file:
        text_from_voice = speech_to_text(voice_file)
        if text_from_voice:
            problem_text = text_from_voice
            st.write(f"🗣 Voice detected: {problem_text}")
        else:
            st.write("❌ Speech not clear")

# Weather
city = st.text_input("Enter your city:", "Hyderabad")
temp, humidity = get_weather(city)
st.write(f"🌦 Weather in {city}: Temperature {temp}°C, Humidity {humidity}%")

# Generate advice
if problem_text:
    advice = generate_advice(crop_name, problem_text, temp, humidity)
    st.subheader("🤖 AI Advice:")
    for step in advice.split(". "):
        st.write(f"🌱 {step.strip()}")
        audio_file = speak(step.strip())
        if audio_file:
            st.audio(audio_file)
        time.sleep(1)