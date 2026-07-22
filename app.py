import traceback
from flask import Flask, render_template, request, send_file
import requests
from datetime import datetime
from pdf_generator import create_pdf
from traffic import calculate_traffic

app = Flask(__name__)

# ==========================================================
# Store latest searched data for PDF Generation
# ==========================================================

latest_weather = None
latest_air = None
latest_elevation = None
latest_recommendation = None
latest_sunrise = None
latest_sunset = None


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    global latest_weather
    global latest_air
    global latest_elevation
    global latest_recommendation
    global latest_sunrise
    global latest_sunset

    weather = None
    air = None
    elevation = None
    forecast = []
    recommendation = None

    route_advice = {}

    road_risk = 0
    travel_score = 0
    travel_status = ""
    best_time = ""
    weather_score = 0

    alerts = []

    flood_risk = {
        "status": "",
        "message": ""
    }

    sunrise = ""
    sunset = ""
    rain_chance = ""

    city = ""
    latitude = ""
    longitude = ""

    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()

    try:

        if not city and not latitude and not longitude:
            return render_template("index.html")

        # ==================================================
        # CITY SEARCH
        # ==================================================

        if city:

            geo_url = (
                "https://geocoding-api.open-meteo.com/v1/search"
                f"?name={city}&count=1"
            )

            geo_response = requests.get(geo_url, timeout=10)
            geo_data = geo_response.json()

            if "results" not in geo_data:

                return render_template(
                    "index.html",
                    error="City not found."
                )

            latitude = geo_data["results"][0]["latitude"]
            longitude = geo_data["results"][0]["longitude"]

        # ==================================================
        # WEATHER API
        # ==================================================

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
            "&current="
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "weather_code"
            "&daily="
            "temperature_2m_max,"
            "temperature_2m_min,"
            "weather_code,"
            "sunrise,"
            "sunset,"
            "precipitation_probability_max"
            "&forecast_days=7"
            "&timezone=auto"
        )

        weather_response = requests.get(weather_url, timeout=15)
        weather_data = weather_response.json()

        weather = {

            "temperature":
            weather_data["current"]["temperature_2m"],

            "feels_like":
            weather_data["current"]["apparent_temperature"],

            "humidity":
            weather_data["current"]["relative_humidity_2m"],

            "wind":
            weather_data["current"]["wind_speed_10m"],

            "wind_direction":
            weather_data["current"]["wind_direction_10m"]

        }

        temperature = weather["temperature"]
        weather_code = weather_data["current"]["weather_code"]

        # ==================================================
        # WEATHER ICON
        # ==================================================

        if weather_code == 0:
            weather["icon"] = "☀️"
            weather["status"] = "Clear Sky"

        elif weather_code in [1, 2]:
            weather["icon"] = "🌤"
            weather["status"] = "Partly Cloudy"

        elif weather_code == 3:
            weather["icon"] = "☁️"
            weather["status"] = "Cloudy"

        elif weather_code in [45, 48]:
            weather["icon"] = "🌫"
            weather["status"] = "Fog"

        elif weather_code in [51, 53, 55]:
            weather["icon"] = "🌦"
            weather["status"] = "Drizzle"

        elif weather_code in [61, 63, 65]:
            weather["icon"] = "🌧"
            weather["status"] = "Rain"

        elif weather_code in [71, 73, 75]:
            weather["icon"] = "❄️"
            weather["status"] = "Snow"

        elif weather_code == 95:
            weather["icon"] = "⛈"
            weather["status"] = "Thunderstorm"

        else:
            weather["icon"] = "🌍"
            weather["status"] = "Unknown"

        # ==================================================
        # RECOMMENDATION
        # ==================================================

        if temperature > 35:

            recommendation = {
                "title": "🔥 Very Hot",
                "message": "Drink plenty of water, wear light clothes and avoid direct sunlight during afternoon."
            }

        elif temperature > 25:

            recommendation = {
                "title": "😊 Pleasant Weather",
                "message": "Perfect weather for outdoor activities. Stay hydrated and enjoy your day."
            }

        elif temperature > 15:

            recommendation = {
                "title": "☁️ Cool Weather",
                "message": "A pleasant day. Carry a light jacket if you are going out in the evening."
            }

        else:

            recommendation = {
                "title": "🥶 Cold Weather",
                "message": "Wear warm clothes and avoid staying outside for long periods."
            }

        # ==================================================
        # FORECAST
        # ==================================================

        dates = weather_data["daily"]["time"]
        max_temp = weather_data["daily"]["temperature_2m_max"]
        min_temp = weather_data["daily"]["temperature_2m_min"]
        forecast_codes = weather_data["daily"]["weather_code"]

        forecast = []

        for i in range(len(dates)):

            code = forecast_codes[i]

            if code == 0:
                icon = "☀️"
            elif code in [1,2]:
                icon = "🌤"
            elif code == 3:
                icon = "☁️"
            elif code in [45,48]:
                icon = "🌫"
            elif code in [51,53,55]:
                icon = "🌦"
            elif code in [61,63,65]:
                icon = "🌧"
            elif code in [71,73,75]:
                icon = "❄️"
            elif code == 95:
                icon = "⛈"
            else:
                icon = "🌍"

            day_name = datetime.strptime(
                dates[i],
                "%Y-%m-%d"
            ).strftime("%A")

            forecast.append({
                "date": day_name,
                "max": max_temp[i],
                "min": min_temp[i],
                "icon": icon
})

        sunrise = datetime.strptime(
            weather_data["daily"]["sunrise"][0],
            "%Y-%m-%dT%H:%M"
        ).strftime("%I:%M %p")

        sunset = datetime.strptime(
            weather_data["daily"]["sunset"][0],
            "%Y-%m-%dT%H:%M"
        ).strftime("%I:%M %p")

        rain_chance = weather_data["daily"]["precipitation_probability_max"][0]
        
        
        # ==================================================
        # AIR QUALITY API
        # ==================================================

        air_url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
            "&current=pm10,pm2_5,carbon_monoxide"
        )

        air_response = requests.get(
            air_url,
            timeout=15
        )

        air_data = air_response.json()

        air = {

            "pm10":
            air_data["current"]["pm10"],

            "pm25":
            air_data["current"]["pm2_5"],

            "co":
            air_data["current"]["carbon_monoxide"]

        }
        
        
                # ==================================================
        # ELEVATION API
        # ==================================================

        elevation_url = (
            "https://api.open-meteo.com/v1/elevation?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
        )

        elevation_response = requests.get(
            elevation_url,
            timeout=15
        )

        elevation_data = elevation_response.json()

        elevation = elevation_data["elevation"][0]

        # ==================================================
        # AQI STATUS
        # ==================================================

        pm25 = air["pm25"]

        if pm25 <= 12:

            air["status"] = "🟢 Good"
            air["color"] = "success"

        elif pm25 <= 35:

            air["status"] = "🟡 Moderate"
            air["color"] = "warning"

        elif pm25 <= 55:

            air["status"] = "🟠 Poor"
            air["color"] = "danger"

        else:

            air["status"] = "🔴 Very Poor"
            air["color"] = "danger"
                # ==================================================
        # SMART ROUTE ADVISOR
        # ==================================================

        route_advice = {}

        if rain_chance < 20:

            route_advice["status"] = "🟢 Safe to Travel"
            route_advice["message"] = (
                "No significant rainfall expected. Roads should remain clear."
            )

        elif rain_chance < 50:

            route_advice["status"] = "🟡 Carry Umbrella"
            route_advice["message"] = (
                "Light rain expected. Drive carefully."
            )

        elif rain_chance < 80:

            route_advice["status"] = "🟠 Possible Waterlogging"
            route_advice["message"] = (
                "Heavy rain may cause waterlogging on low-lying roads. Prefer major roads."
            )

        else:

            route_advice["status"] = "🔴 Avoid Non-Essential Travel"
            route_advice["message"] = (
                "Very heavy rainfall expected. Travel only if necessary."
            )
            
         # ==================================================
        # ROAD RISK INDEX
        # ==================================================

        road_risk = int((rain_chance * 0.7) + (weather["wind"] * 0.8))

        if road_risk > 100:
            road_risk = 100
            
        # ==================================================
        # TRAVEL SAFETY SCORE
        # ==================================================

        travel_score = 10

        # Rain Penalty
        if rain_chance > 80:
            travel_score -= 4
        elif rain_chance > 50:
            travel_score -= 3
        elif rain_chance > 20:
            travel_score -= 2

        # Wind Penalty
        if weather["wind"] > 40:
            travel_score -= 2
        elif weather["wind"] > 20:
            travel_score -= 1

        # Air Quality Penalty
        if air["pm25"] > 55:
            travel_score -= 2
        elif air["pm25"] > 35:
            travel_score -= 1

        # Keep score between 1 and 10
        travel_score = max(1, min(10, travel_score))
        
        # ==================================================
        # BEST TIME TO TRAVEL
        # ==================================================

        if rain_chance > 80:

            best_time = "After the rain stops (Evening recommended)"

        elif temperature > 35:

            best_time = "Early Morning (6 AM - 9 AM)"

        elif weather["wind"] > 35:

            best_time = "Travel after wind speed decreases"

        else:

            best_time = "Anytime Today"
            
            
        # ==================================================
# FLOOD RISK PREDICTION
# ==================================================

        flood_risk = {}

        risk_score = 0

        # Rain contributes most
        risk_score += rain_chance * 0.6

        # Low elevation increases risk
        if elevation < 20:
            risk_score += 25
        elif elevation < 50:
            risk_score += 15
        else:
            risk_score += 5

        # High humidity slightly increases risk
        risk_score += weather["humidity"] * 0.2

        if risk_score < 40:

            flood_risk["status"] = "🟢 Low"

            flood_risk["message"] = (
                "Very low possibility of waterlogging."
            )

        elif risk_score < 70:

            flood_risk["status"] = "🟡 Moderate"

            flood_risk["message"] = (
                "Some roads may collect water after rain."
            )

        else:

            flood_risk["status"] = "🔴 High"

            flood_risk["message"] = (
                "Avoid low-lying roads. Waterlogging is possible."
            )
            
            
            
                    # ==================================================
        # WEATHER ALERTS
        # ==================================================

        alerts = []

        if temperature > 35:
            alerts.append("🔥 Heat Alert")

        if rain_chance > 70:
            alerts.append("🌧 Heavy Rain Alert")

        if weather["wind"] > 30:
            alerts.append("💨 Strong Wind Alert")

        if air["pm25"] > 55:
            alerts.append("😷 Poor Air Quality")

        if flood_risk["status"] == "🔴 High":
            alerts.append("🌊 Waterlogging Possible")

        if len(alerts) == 0:
            alerts.append("✅ No Weather Alerts")
            
            
                    # ==================================================
        # WEATHER SCORE
        # ==================================================

        weather_score = 100

        weather_score -= rain_chance * 0.3

        if air["pm25"] > 35:
            weather_score -= 20

        if temperature > 35:
            weather_score -= 10

        if flood_risk["status"] == "🔴 High":
            weather_score -= 20

        weather_score = max(0, int(weather_score))    
    
    
            # ==================================================
        # TRAVEL SAFETY METER
        # ==================================================

        travel_score = weather_score

        if flood_risk["status"] == "🔴 High":
            travel_score -= 20

        travel_score = max(0, min(100, travel_score))

        if travel_score >= 80:

            travel_status = "🟢 Safe"

        elif travel_score >= 60:

            travel_status = "🟡 Moderate"

        else:

            travel_status = "🔴 Unsafe"            
        

        # ==================================================
        # SAVE DATA FOR PDF
        # ==================================================

        traffic = calculate_traffic(
        weather,
        air,
        rain_chance,
        elevation
    )

        latest_weather = weather
        latest_air = air
        latest_elevation = elevation
        latest_recommendation = recommendation
        latest_sunrise = sunrise
        latest_sunset = sunset

    except Exception as e:

        traceback.print_exc()
        error = str(e)

    # ======================================================
    # RETURN HTML
    # ======================================================

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
        
        route_advice=route_advice,
        
        road_risk=road_risk,
        
        travel_score=travel_score,
        
        travel_status=travel_status,
        
        best_time=best_time,
        
        flood_risk=flood_risk,
        
        alerts=alerts,
        
        weather_score=weather_score,

        latitude=latitude,
        
        longitude=longitude,
        
        traffic=traffic,
        
        city=city,

        error=error
   
     )
    
    # ==========================================================
# PDF DOWNLOAD
# ==========================================================

@app.route("/download")
def download():

    global latest_weather
    global latest_air
    global latest_elevation
    global latest_recommendation
    global latest_sunrise
    global latest_sunset
    
    if latest_weather is None:

        return "Please search weather first."

    create_pdf(

        latest_weather,
        latest_air,
        latest_elevation,
        latest_recommendation,
        latest_sunrise,
        latest_sunset


    )

    return send_file(

        "weather_report.pdf",
        as_attachment=True

    )


# ==========================================================
# RUN FLASK APP
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )