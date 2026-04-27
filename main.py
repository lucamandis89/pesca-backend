from fastapi import FastAPI
import os

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "Pesca API attiva"}

# -------------------------
# TEST
# -------------------------
@app.get("/test")
def test():
    return {"status": "working"}

# -------------------------
# ALGORITMO PESCA PRO
# -------------------------
def calculate_score(wave: float, wind: float, tide: float, moon: float):

    score = 100

    # 🌊 Onde
    if wave > 80:
        score -= 25
    elif wave > 60:
        score -= 10
    elif wave < 30:
        score += 5

    # 💨 Vento
    if wind > 70:
        score -= 20
    elif wind > 50:
        score -= 10
    elif wind < 20:
        score += 5

    # 🌊 Maree
    if tide > 70:
        score += 10
    elif tide < 30:
        score -= 15

    # 🌙 Luna
    if 40 <= moon <= 70:
        score += 10
    else:
        score -= 5

    return max(0, min(100, score))


# -------------------------
# FISHING ENDPOINT
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    # 🌊 DATI MOCK (poi li colleghiamo API reali)
    wave = 55
    wind = 40
    tide = 65
    moon = 50

    # 🎯 SCORE FINALE
    fishing_score = calculate_score(wave, wind, tide, moon)

    return {
        "location": {
            "lat": lat,
            "lon": lon
        },
        "environment": {
            "wave": wave,
            "wind": wind,
            "tide": tide,
            "moon": moon
        },
        "fishing_score": fishing_score,
        "status": "calculated"
    }


# -------------------------
# RENDER ENTRY POINT
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)