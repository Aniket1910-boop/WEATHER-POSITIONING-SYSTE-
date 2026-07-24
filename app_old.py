from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)


# ==========================================================
# Traffic Calculator
# ==========================================================
def calculate_traffic(weather, air, rain_chance, elevation):

    score = 0

    # Rain contributes most
    score += rain_chance * 0.5

    # Wind contributes moderately
    score += weather["wind"] * 0.3

    # Air quality contributes slightly
    score += air["pm25"] * 0.2

    # Low elevation increases congestion risk
    if elevation < 20:
        score += 20
    elif elevation < 50:
        score += 10

    score = min(100, int(score))

    if score < 25:
        status = "🟢 Smooth"
    elif score < 50:
        status = "🟡 Moderate"
    elif score < 75:
        status = "🟠 Heavy"
    else:
        status = "🔴 Severe"

    return {
        "status": status,
        "congestion": score
    }


# ==========================================================
# Home Page
# ==========================================================
@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    air = None
    elevation = None
    forecast = []

    recommendation = None

    traffic = {
        "status": "🟢 Smooth",
        "congestion": 0
    }

    route_coordinates = []


    flood_risk = {
        "status": "",
        "message": ""
    }

    alerts = []

    travel_score = 0
    travel_status = ""
    road_risk = 0
    weather_score = 0
    best_time = ""

    sunrise = ""
    sunset = ""
    rain_chance = 0

    city = ""

    latitude = ""
    longitude = ""

    destination = ""

    destination_lat = None
    destination_lon = None

    error = None
    try:

        # ==================================================
        # Search City
        # ==================================================
        if request.method == "POST":

            city = request.form.get("city", "").strip()
            latitude = request.form.get("latitude", "").strip()
            longitude = request.form.get("longitude", "").strip()

            # If city is entered
            if city:

                geo_url = (
                    "https://geocoding-api.open-meteo.com/v1/search"
                    f"?name={city}&count=1"
                )

                geo_data = requests.get(geo_url, timeout=10).json()

                if "results" not in geo_data:
                    return render_template("index.html", error="City not found")

                latitude = geo_data["results"][0]["latitude"]
                longitude = geo_data["results"][0]["longitude"]

            # ==================================================
            # Weather API
            # ==================================================
            weather_url = (
                "https://api.open-meteo.com/v1/forecast?"
                f"latitude={latitude}"
                f"&longitude={longitude}"
                "&current=temperature_2m,apparent_temperature,"
                "relative_humidity_2m,wind_speed_10m,weather_code"
                "&daily=temperature_2m_max,temperature_2m_min,"
                "weather_code,sunrise,sunset,precipitation_probability_max"
                "&forecast_days=7&timezone=auto"
            )

            weather_data = requests.get(weather_url, timeout=15).json()

            weather = {
                "temperature": weather_data["current"]["temperature_2m"],
                "feels_like": weather_data["current"]["apparent_temperature"],
                "humidity": weather_data["current"]["relative_humidity_2m"],
                "wind": weather_data["current"]["wind_speed_10m"],
            }

            # Weather icon
            code = weather_data["current"]["weather_code"]

            if code == 0:
                weather["icon"] = "☀️"
                weather["status"] = "Clear Sky"
            elif code in [1, 2]:
                weather["icon"] = "🌤"
                weather["status"] = "Partly Cloudy"
            elif code == 3:
                weather["icon"] = "☁️"
                weather["status"] = "Cloudy"
            else:
                weather["icon"] = "🌧"
                weather["status"] = "Rain"

            # Recommendation
            temp = weather["temperature"]

            if temp > 35:
                recommendation = {
                    "title": "🔥 Very Hot",
                    "message": "Drink plenty of water and avoid afternoon sun."
                }
            elif temp > 25:
                recommendation = {
                    "title": "😊 Pleasant Weather",
                    "message": "Perfect for outdoor activities."
                }
            else:
                recommendation = {
                    "title": "🥶 Cool Weather",
                    "message": "Carry a light jacket."
                }

            # Forecast
            dates = weather_data["daily"]["time"]
            max_t = weather_data["daily"]["temperature_2m_max"]
            min_t = weather_data["daily"]["temperature_2m_min"]

            for i in range(len(dates)):

                day = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%A")

                forecast.append({
                    "date": day,
                    "max": max_t[i],
                    "min": min_t[i],
                    "icon": "☀️"
                })

            sunrise = weather_data["daily"]["sunrise"][0]
            sunset = weather_data["daily"]["sunset"][0]
            rain_chance = weather_data["daily"]["precipitation_probability_max"][0]

            # ==================================================
            # Air Quality
            # ==================================================
            air_url = (
                "https://air-quality-api.open-meteo.com/v1/air-quality?"
                f"latitude={latitude}&longitude={longitude}"
                "&current=pm10,pm2_5,carbon_monoxide"
            )

            air_data = requests.get(air_url, timeout=15).json()

            air = {
                "pm10": air_data["current"]["pm10"],
                "pm25": air_data["current"]["pm2_5"],
                "co": air_data["current"]["carbon_monoxide"],
            }

            # ==================================================
            # Elevation
            # ==================================================
            elevation_url = (
                "https://api.open-meteo.com/v1/elevation?"
                f"latitude={latitude}&longitude={longitude}"
            )

            elevation_data = requests.get(elevation_url, timeout=15).json()
            elevation = elevation_data["elevation"][0]

            # ==================================================
            # Traffic
            # ==================================================
            traffic = calculate_traffic(weather, air, rain_chance, elevation)

            # ==================================================
            # Route Coordinates (Patna Example)
            # ==================================================
            route_coordinates = [
                [25.5819, 85.0818],
                [25.5850, 85.0950],
                [25.5890, 85.1120],
                [25.5920, 85.1250],
                [25.5941, 85.1376]
            ]

    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        weather=weather,
        air=air,
        elevation=elevation,
        forecast=forecast,
        recommendation=recommendation,
        sunrise=sunrise,
        sunset=sunset,
        rain_chance=rain_chance,
        traffic=traffic,
        latitude=latitude,
        longitude=longitude,
        route_coordinates=route_coordinates,
        destination=destination,
        destination_lat=destination_lat,
        destination_lon=destination_lon,
        route_advice=route_advice,
        city=city,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)