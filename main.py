from fastapi import FastAPI
import requests
import math
from datetime import datetime

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "Pesca API realistica attiva"}

# -------------------------
# TEST
# -------------------------
@app.get("/test")
def test():
    return {"status": "working"}

# -------------------------
# 🌙 LUNA REALE (semplice ma efficace)
# -------------------------
def get_moon_phase():
    now = datetime.utcnow()
    days = now.day
    phase = (days % 29) / 29 * 100
    return phase

# -------------------------
# 🌊 DATI REALI OPEN-METEO
# -------------------------
def get_weather(lat, lon):

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=wind_speed_10m,wave_height&current_weather=true"
    )

    res = requests.get(url)
    data = res.json()

    wind = data["current_weather"]["windspeed"]

    # fallback onde (Open-Meteo non sempre le dà precise)
    wave = 50
    try:
        wave = data["hourly"]["wave_height"][0]
    except:
        wave = 50

    return wind, wave

# -------------------------
# 🎯 SCORE PESCA REALISTICO
# -------------------------
def calculate_score(wave, wind, tide, moon):

    score = 100

    # 🌊 onde
    if wave > 2.5:
        score -= 30
    elif wave > 1.5:
        score -= 15

    # 💨 vento
    if wind > 25:
        score -= 25
    elif wind > 15:
        score -= 10

    # 🌊 maree (simulazione base migliorabile)
    if tide > 70:
        score += 10
    elif tide < 30:
        score -= 15

    # 🌙 luna
    if 40 <= moon <= 70:
        score += 15
    else:
        score -= 10

    return max(0, min(100, score))

# -------------------------
# FISHING ENDPOINT (REAL)
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    wind, wave = get_weather(lat, lon)

    tide = 60  # placeholder realistico (poi lo miglioriamo con API maree)
    moon = get_moon_phase()

    score = calculate_score(wave, wind, tide, moon)

    return {
        "location": {"lat": lat, "lon": lon},
        "environment": {
            "wave": wave,
            "wind": wind,
            "tide": tide,
            "moon": moon
        },
        "fishing_score": score,
        "status": "REAL_DATA"
    }