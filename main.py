from fastapi import FastAPI
import requests
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
# FISHING ENDPOINT
# -------------------------
@app.get("/fishing")
def fishing(lat: float, lon: float):

    # 🌊 MOCK / PLACEHOLDER (mantieni tua logica reale qui)
    wave_score = 70
    wind_score = 60
    tide_score = 80
    moon_score = 65

    # 🎯 SCORE FINALE
    score = (wave_score + wind_score + tide_score + moon_score) / 4

    return {
        "location": {"lat": lat, "lon": lon},
        "scores": {
            "wave": wave_score,
            "wind": wind_score,
            "tide": tide_score,
            "moon": moon_score
        },
        "fishing_score": round(score, 2)
    }

# -------------------------
# RENDER COMPATIBILITY
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)