from fastapi import FastAPI
import requests
from datetime import datetime
import os

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Pesca API attiva"
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
# 🌙 LUNA (semplice e stabile)
# -------------------------
def get_moon():
    now = datetime.utcnow()
    return (now.day % 29) / 29 * 100


# -------------------------
# 🌬️ METEO SICURO (Open-Meteo)
# -------------------------
def get_wind(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url, timeout=5)
        data = r.json()
        return data.get("current_weather", {}).get("windspeed", 10)
    except:
        return 10


# -------------------------
# 🎯 SCORE PESCA
# -------------------------
def calculate_score(wave, wind, tide, moon):

    score = 100

    # vento
    if wind > 25:
        score -= 25
    elif wind > 15:
        score -= 10

    # onde
    if wave > 2:
        score -= 20

    # maree
    if tide > 70:
        score += 10
    elif tide < 30:
        score -= 10

    # luna
    if 40 <= moon <= 70:
        score += 10
    else:
        score -= 5

    return max(0, min(100, score))


# -------------------------
# 🎣 FISHING ENDPOINT STABILE
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    try:
        wind = get_wind(lat, lon)

        wave = 1.0   # fallback stabile (onde reali richiedono API premium)
        tide = 60    # placeholder realistico
        moon = get_moon()

        score = calculate_score(wave, wind, tide, moon)

        return {
            "location": {
                "lat": lat,
                "lon": lon
            },
            "environment": {
                "wind": wind,
                "wave": wave,
                "tide": tide,
                "moon": moon
            },
            "fishing_score": score,
            "status": "STABLE_OK"
        }

    except Exception as e:
        return {
            "status": "error_handled",
            "message": str(e)
        }


# -------------------------
# RENDER START
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)