from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import math
import os

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "Pesca API FULL REAL FREE"}


# -------------------------
# 🌙 LUNA
# -------------------------
def get_moon():
    now = datetime.utcnow()
    return (now.day % 29) / 29 * 100


# -------------------------
# 🌬️ METEO (Open-Meteo)
# -------------------------
def get_weather(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=pressure_msl"
        )

        r = requests.get(url, timeout=5)
        data = r.json()

        wind = data.get("current_weather", {}).get("windspeed", 10)
        pressure = data.get("hourly", {}).get("pressure_msl", [1015])[0]

        return wind, pressure

    except:
        return 10, 1015


# -------------------------
# 🌊 ONDE STIMATE
# -------------------------
def estimate_wave(wind):
    return round(wind / 20, 2)


# -------------------------
# 🌊 MAREA SIMULATA
# -------------------------
def generate_tide_series():
    now = datetime.utcnow()
    data = []

    for i in range(24):
        t = now + timedelta(hours=i)

        height = 1.5 + math.sin(i / 12 * 2 * math.pi)

        data.append({
            "time": t.isoformat(),
            "height": round(height, 2)
        })

    return data


# -------------------------
# 📈 ALTA / BASSA MAREA
# -------------------------
def get_high_low(tides):

    highs = []
    lows = []

    for i in range(1, len(tides) - 1):
        prev = tides[i-1]["height"]
        curr = tides[i]["height"]
        next = tides[i+1]["height"]

        if curr > prev and curr > next:
            highs.append(tides[i])

        if curr < prev and curr < next:
            lows.append(tides[i])

    return highs, lows


# -------------------------
# 📊 COEFFICIENTE MAREA
# -------------------------
def calculate_tide_coeff(highs, lows):

    if not highs or not lows:
        return 50

    amp = abs(highs[0]["height"] - lows[0]["height"])

    coeff = (amp / 3) * 120

    return int(max(20, min(120, coeff)))


# -------------------------
# 🌊 CORRENTI
# -------------------------
def calculate_current(tides):

    currents = []

    for i in range(1, len(tides)):
        dh = tides[i]["height"] - tides[i-1]["height"]
        currents.append(round(dh, 2))

    return currents


# -------------------------
# 🎯 SCORE PESCA
# -------------------------
def calculate_score(wave, wind, tide, moon, pressure):

    score = 100

    if wind > 30:
        score -= 30
    elif wind > 15:
        score -= 15

    if wave > 2:
        score -= 25
    elif wave > 1:
        score -= 10

    if tide > 65:
        score += 10
    elif tide < 35:
        score -= 10

    if 40 <= moon <= 70:
        score += 15
    else:
        score -= 10

    if pressure < 1005:
        score -= 10
    elif pressure > 1020:
        score += 5

    return max(0, min(100, score))


# -------------------------
# 🎣 ENDPOINT PESCA
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    wind, pressure = get_weather(lat, lon)

    wave = estimate_wave(wind)

    tide_series = generate_tide_series()
    highs, lows = get_high_low(tide_series)

    tide = highs[0]["height"] if highs else 60

    moon = get_moon()

    score = calculate_score(wave, wind, tide, moon, pressure)

    return {
        "location": {"lat": lat, "lon": lon},
        "environment": {
            "wind": wind,
            "wave": wave,
            "tide": tide,
            "moon": moon,
            "pressure": pressure
        },
        "fishing_score": score,
        "status": "REAL_FREE_MODE"
    }


# -------------------------
# 🌊 ENDPOINT MAREE
# -------------------------
@app.get("/tides")
def tides():

    series = generate_tide_series()
    highs, lows = get_high_low(series)

    coeff = calculate_tide_coeff(highs, lows)
    currents = calculate_current(series)

    return {
        "series": series,
        "high_tides": highs,
        "low_tides": lows,
        "coefficient": coeff,
        "currents": currents,
        "status": "TIDE_MODEL_ACTIVE"
    }


# -------------------------
# RENDER START
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)