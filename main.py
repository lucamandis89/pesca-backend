from fastapi import FastAPI
import os

app = FastAPI()

# -------------------------
# HOME
# -------------------------
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Pesca API online"
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
# FUNZIONE SCORE PESCA
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

    # 🌊 maree
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
# FISHING ENDPOINT STABILE
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    try:
        # 🌊 DATI BASE STABILI (NO CRASH)
        wave = 1.2
        wind = 12
        tide = 60
        moon = 55

        score = calculate_score(wave, wind, tide, moon)

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
            "fishing_score": score,
            "status": "stable_ok"
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