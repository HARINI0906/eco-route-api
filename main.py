from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS Middleware (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Distance data (KM)
distance_data = {
    ("Chennai", "Bangalore"): 350,
    ("Chennai", "Hyderabad"): 630,
    ("Bangalore", "Hyderabad"): 570
}

# Emission factors (grams per km)
emission_factors = {
    "car": 120,
    "bike": 60,
    "bus": 40
}

class RouteRequest(BaseModel):
    source: str
    destination: str


@app.post("/route")
def calculate_route(data: RouteRequest):

    key = (data.source, data.destination)

    if key not in distance_data:
        return {"error": "Route not available"}

    distance = distance_data[key]

    results = {}

    for vehicle, factor in emission_factors.items():
        emission = (distance * factor) / 1000
        results[vehicle] = round(emission, 2)

    recommended = min(results, key=results.get)

    return {
        "distance_km": distance,
        "emission_kg": results,
        "recommended_option": recommended
    }
