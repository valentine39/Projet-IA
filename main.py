from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WGI_INDICATORS = {
    "political_stability": "PV.EST",
    "government_effectiveness": "GE.EST",
    "regulatory_quality": "RQ.EST",
    "rule_of_law": "RL.EST",
    "control_of_corruption": "CC.EST",
    "voice_accountability": "VA.EST",
}

@app.get("/")
def root():
    return {"message": "Backend OK"}

@app.get("/api/wgi")
def get_wgi(country: str):
    results = {}

    for key, indicator in WGI_INDICATORS.items():
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=100"
        response = requests.get(url)
        data = response.json()

        value = None
        year = None

        if isinstance(data, list) and len(data) > 1:
            for obs in data[1]:
                if obs["value"] is not None:
                    value = obs["value"]
                    year = obs["date"]
                    break

        results[key] = {
            "value": value,
            "year": year
        }

    return {
        "country": country,
        "data": results
    }
