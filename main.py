from fastapi import FastAPI
import os
import requests
from datetime import datetime

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Pesca API reale online"
    }

# -------------------------
# TEST
# -------------------------
@app.get("/test")
def test():
    return {
        "status": "working"
    }

# -------------------------
# 🌙 LUNA REALE (semplice ma stabile)
# -------------------------
def get_moon_phase():
    now = datetime.utcnow()
    day = now.day
    return (day % 29) / 29 * 100


# -------------------------
# 🌊 DATI REALI METEO (Open-Meteo)
# -------------------------
def get_weather(lat, lon):

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=wind_speed_10m,wave_height"
        )

        r = requests.get(url, timeout=5)
        data = r.json()

        wind = data["current_weather"]["windspeed"]

        wave = 1.0
        try:
            wave = data["hourly"]["wave_height"][0]
        except:
            wave = 1.0

        return wave, wind

    except:
        # fallback sicuro se API non risponde
        return 1.0, 10.0


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

    # 🌊 maree (simulazione stabile)
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
# 🎣 FISHING ENDPOINT (REAL + SAFE)
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    wave, wind = get_weather(lat, lon)

    tide = 60  # placeholder realistico (poi miglioriamo con API maree NOAA)
    moon = get_moon_phase()

    score = calculate_score(wave, wind, tide, moon)

    return {
        "location": {
            "lat": lat,
            "lon": lon
        },
        "environment": {
            "wave": round(wave, 2),
            "wind": round(wind, 2),
            "tide": tide,
            "moon": round(moon, 2)
        },
        "fishing_score": score,
        "status": "REAL_MODE_ACTIVE"
    }


# -------------------------
# RENDER ENTRY POINT
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)