from flask import Flask, render_template, request, jsonify, send_file
import requests
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

from traffic import calculate_traffic
from pdf_generator import create_pdf

app = Flask(__name__)

# ==========================================================
# CONFIGURATION
# ==========================================================

HEADERS = {
    "User-Agent": "Weather Positioning System v2.0"
}

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

ELEVATION_URL = "https://api.open-meteo.com/v1/elevation"

# Replace with your Geoapify API Key
GEOAPIFY_KEY = "36cc2184ba5846598fd7a41cf8b207f4"

# ==========================================================
# GLOBAL VARIABLES
# ==========================================================

latest_weather = {}
latest_air = {}
latest_forecast = []
latest_route = {}
latest_waterlogging = {}
latest_travel = {}
latest_recommendation = {}
latest_city = ""
latest_destination = ""
latest_elevation = 0
latest_sunrise = ""
latest_sunset = ""
latest_local_time = ""

# ==========================================================
# GEOCODING
# ==========================================================

def geocode_location(place):

    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": place,
        "apiKey": GEOAPIFY_KEY,
        "limit": 1
    }

    try:

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        if len(data["features"]) == 0:
            return None

        feature = data["features"][0]

        return {

            "name": feature["properties"]["formatted"],

            "lat": feature["properties"]["lat"],

            "lon": feature["properties"]["lon"]

        }

    except Exception:

        return None

# ==========================================================
# WEATHER SCORE
# ==========================================================

def calculate_weather_score(weather, rain):

    score = 100

    if weather["temperature"] > 35:
        score -= 15

    if weather["wind"] > 25:
        score -= 10

    score -= int(rain * 0.4)

    return max(score, 0)

# ==========================================================
# WATERLOGGING
# ==========================================================

def predict_waterlogging(rain, humidity, elevation):

    risk = 0

    risk += rain * 0.5

    risk += humidity * 0.2

    if elevation < 10:
        risk += 30

    elif elevation < 30:
        risk += 15

    if risk < 40:

        return {
            "status": "Low",
            "color": "green",
            "message": "No major waterlogging expected."
        }

    elif risk < 70:

        return {
            "status": "Moderate",
            "color": "orange",
            "message": "Possible waterlogging in low-lying roads."
        }

    else:

        return {
            "status": "High",
            "color": "red",
            "message": "Avoid low-lying areas."
        }

# ==========================================================
# TRAVEL INTELLIGENCE
# ==========================================================

def travel_advice(weather_score, traffic_status, waterlogging):

    advice = []

    if weather_score > 80:
        advice.append("Weather is suitable for travelling.")

    else:
        advice.append("Weather conditions are not ideal.")

    if traffic_status == "Heavy":
        advice.append("Heavy traffic detected.")

    elif traffic_status == "Moderate":
        advice.append("Moderate traffic expected.")

    else:
        advice.append("Traffic conditions are good.")

    if waterlogging["status"] == "High":
        advice.append("Avoid flood-prone roads.")

    elif waterlogging["status"] == "Moderate":
        advice.append("Drive carefully in low-lying areas.")

    else:
        advice.append("Road conditions appear normal.")

    return advice


# ==========================================================
# WEATHER
# ==========================================================

def get_weather(lat, lon):

    url = (
        f"{OPEN_METEO_URL}"
        f"?latitude={lat}"
        f"&longitude={lon}"
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

    return requests.get(url, timeout=20).json()


# ==========================================================
# AIR QUALITY
# ==========================================================

def get_air_quality(lat, lon):

    url = (
        f"{AIR_URL}"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current="
        "pm10,"
        "pm2_5,"
        "carbon_monoxide"
    )

    return requests.get(url, timeout=20).json()


# ==========================================================
# ELEVATION
# ==========================================================

def get_elevation(lat, lon):

    url = (
        f"{ELEVATION_URL}"
        f"?latitude={lat}"
        f"&longitude={lon}"
    )

    return requests.get(url, timeout=20).json()


# ==========================================================
# WEATHER ICON
# ==========================================================

def weather_icon(code):

    weather_codes = {

        0: ("☀️", "Clear Sky"),

        1: ("🌤️", "Mainly Clear"),
        2: ("⛅", "Partly Cloudy"),
        3: ("☁️", "Overcast"),

        45: ("🌫️", "Fog"),
        48: ("🌫️", "Depositing Fog"),

        51: ("🌦️", "Light Drizzle"),
        53: ("🌦️", "Moderate Drizzle"),
        55: ("🌧️", "Heavy Drizzle"),

        56: ("🌧️", "Freezing Drizzle"),
        57: ("🌧️", "Heavy Freezing Drizzle"),

        61: ("🌧️", "Slight Rain"),
        63: ("🌧️", "Moderate Rain"),
        65: ("🌧️", "Heavy Rain"),

        66: ("🌧️", "Freezing Rain"),
        67: ("🌧️", "Heavy Freezing Rain"),

        71: ("❄️", "Slight Snow"),
        73: ("❄️", "Moderate Snow"),
        75: ("❄️", "Heavy Snow"),

        77: ("🌨️", "Snow Grains"),

        80: ("🌦️", "Rain Showers"),
        81: ("🌦️", "Moderate Rain Showers"),
        82: ("⛈️", "Violent Rain Showers"),

        85: ("🌨️", "Snow Showers"),
        86: ("🌨️", "Heavy Snow Showers"),

        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Thunderstorm with Hail"),
        99: ("⛈️", "Severe Thunderstorm")

    }

    return weather_codes.get(
        code,
        ("🌍", f"Weather Code {code}")
    )


# ==========================================================
# AQI STATUS
# ==========================================================

def aqi_status(pm25):

    if pm25 <= 12:

        return {
            "status": "Good",
            "color": "green"
        }

    elif pm25 <= 35:

        return {
            "status": "Moderate",
            "color": "yellow"
        }

    elif pm25 <= 55:

        return {
            "status": "Poor",
            "color": "orange"
        }

    return {
        "status": "Very Poor",
        "color": "red"
    }


# ==========================================================
# FORECAST
# ==========================================================

def build_forecast(weather_json):

    forecast = []

    dates = weather_json["daily"]["time"]

    max_temp = weather_json["daily"]["temperature_2m_max"]

    min_temp = weather_json["daily"]["temperature_2m_min"]

    codes = weather_json["daily"]["weather_code"]

    for i in range(len(dates)):

        icon, status = weather_icon(codes[i])

        forecast.append({

            "day": datetime.strptime(
                dates[i],
                "%Y-%m-%d"
            ).strftime("%A"),

            "max": max_temp[i],

            "min": min_temp[i],

            "icon": icon,

            "status": status

        })

    return forecast

# ==========================================================
# ROUTE ENGINE
# ==========================================================

def get_alternative_routes(

    source_lat,

    source_lon,

    dest_lat,

    dest_lon

):

    url = (

        "https://api.geoapify.com/v1/routing"

        f"?waypoints={source_lat},{source_lon}|{dest_lat},{dest_lon}"

        "&mode=drive"

        "&details=route_details"

        "&alternatives=3"

        f"&apiKey={GEOAPIFY_KEY}"

    )

    try:

        response = requests.get(url, timeout=20)

        data = response.json()

        if "features" not in data:

            return []

        routes=[]

        for feature in data["features"]:

            props=feature["properties"]

            routes.append({

                "distance":round(props["distance"]/1000,2),

                "duration":round(props["time"]/60,1),

                "coordinates":feature["geometry"]["coordinates"][0]

            })

        return routes

    except:

        return []


# ==========================================================
# TRAFFIC STATUS
# ==========================================================

def traffic_status(duration):

    if duration < 20:

        return {

            "status": "Low",

            "color": "green"

        }

    elif duration < 45:

        return {

            "status": "Moderate",

            "color": "yellow"

        }

    return {

        "status": "Heavy",

        "color": "red"

    }


# ==========================================================
# BEST ROUTE ADVICE
# ==========================================================

def best_route_advice(weather_score,
                      traffic,
                      waterlogging):

    advice = []

    if traffic["status"] == "Heavy":

        advice.append(
            "Heavy traffic detected. Consider delaying travel."
        )

    elif traffic["status"] == "Moderate":

        advice.append(
            "Moderate traffic expected."
        )

    else:

        advice.append(
            "Road traffic is smooth."
        )

    if waterlogging["status"] == "High":

        advice.append(
            "Avoid low-lying roads due to waterlogging."
        )

    elif waterlogging["status"] == "Moderate":

        advice.append(
            "Drive carefully in low-lying areas."
        )

    if weather_score > 80:

        advice.append(
            "Weather is favourable for travel."
        )

    else:

        advice.append(
            "Weather conditions may affect travel."
        )

    return advice


# ==========================================================
# AI TRAVEL SUMMARY
# ==========================================================

def ai_summary(city,
               destination,
               weather,
               traffic,
               waterlogging):

    summary = (
        f"Travel from {city} to {destination}. "
        f"Current temperature is "
        f"{weather['temperature']}°C. "
        f"Traffic is {traffic['status']}. "
        f"Waterlogging risk is "
        f"{waterlogging['status']}."
    )

    return summary

# ==========================================================
# AI BEST ROUTE RECOMMENDATION
# ==========================================================

def generate_route_recommendation(
    weather_score,
    traffic,
    waterlogging,
    travel_time
):

    recommendation = {}

    score = weather_score

    # Traffic Impact
    if traffic["status"] == "Low":
        score += 10

    elif traffic["status"] == "Moderate":
        score += 5

    elif traffic["status"] == "Heavy":
        score -= 10

    elif traffic["status"] == "Severe":
        score -= 20

    # Waterlogging Impact
    if waterlogging["status"] == "Low":
        score += 10

    elif waterlogging["status"] == "Moderate":
        score -= 5

    elif waterlogging["status"] == "High":
        score -= 20

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    recommendation["score"] = score

    # AI Decision
    if score >= 90:

        recommendation["title"] = "Excellent Route"

        recommendation["message"] = (
            "Recommended for travelling. "
            "Weather is favourable, roads are safe, "
            "and traffic conditions are good."
        )

    elif score >= 75:

        recommendation["title"] = "Good Route"

        recommendation["message"] = (
            "Safe for travelling. "
            "Minor delays may occur due to moderate traffic."
        )

    elif score >= 60:

        recommendation["title"] = "Travel Carefully"

        recommendation["message"] = (
            "Travel is possible, "
            "but drive carefully because weather or "
            "road conditions may affect your journey."
        )

    else:

        recommendation["title"] = "Avoid Travelling"

        recommendation["message"] = (
            "Heavy traffic or high waterlogging risk detected. "
            "Delay your trip if possible."
        )

    recommendation["estimated_time"] = travel_time

    return recommendation

# ==========================================================
# SAFE ROUTE FINDER
# ==========================================================

def safest_route(weather_score, traffic, waterlogging):

    if waterlogging["status"] == "High":

        return {
            "route": "Alternative Route Recommended",
            "color": "danger",
            "icon": "🔴",
            "reason": "High waterlogging detected on the current route."
        }

    elif traffic["status"] == "Heavy":

        return {
            "route": "Alternative Route Recommended",
            "color": "warning",
            "icon": "🟠",
            "reason": "Heavy traffic may cause long delays."
        }

    elif weather_score >= 80:

        return {
            "route": "Current Route is Safe",
            "color": "success",
            "icon": "🟢",
            "reason": "Weather, traffic and road conditions are favourable."
        }

    else:

        return {
            "route": "Proceed Carefully",
            "color": "info",
            "icon": "🔵",
            "reason": "Drive carefully due to moderate conditions."
        }

# ==========================================================
# BEST ROUTE DECISION
# ==========================================================

def choose_best_route(traffic, waterlogging):

    if waterlogging["status"] == "High":

        return {

            "route_status": "Avoid This Route",

            "route_color": "danger",

            "route_icon": "🚫",

            "reason":
            "High waterlogging risk detected. Choose another road if possible."

        }

    elif traffic["status"] == "Severe":

        return {

            "route_status": "Alternative Route Recommended",

            "route_color": "warning",

            "route_icon": "⚠️",

            "reason":
            "Traffic congestion is very high."

        }

    elif traffic["status"] == "Heavy":

        return {

            "route_status": "Travel Carefully",

            "route_color": "warning",

            "route_icon": "🚗",

            "reason":
            "Heavy traffic expected."

        }

    else:

        return {

            "route_status": "Best Route",

            "route_color": "success",

            "route_icon": "✅",

            "reason":
            "Weather, traffic and road conditions are suitable."

        }
        
# ==========================================================
# GET CURRENT LOCATION NAME
# ==========================================================

@app.route("/current-location")
def current_location():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    url = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?format=json&lat={lat}&lon={lon}"
    )

    headers = {
        "User-Agent": "Weather Positioning System"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    address = data.get("address", {})

    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("county")
        or ""
    )

    return jsonify({
        "city": city
    })

# ==========================================================
# HOME
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    global latest_weather
    global latest_air
    global latest_forecast
    global latest_route
    global latest_waterlogging
    global latest_travel
    global latest_city
    global latest_destination
    global latest_elevation
    global latest_sunrise
    global latest_sunset
    global latest_local_time
    global latest_recommendation

    weather = None
    air = None
    forecast = []
    elevation = None

    route = None
    traffic = None
    waterlogging = None

    travel = []
    summary = ""

    city = ""
    destination = ""

    error = None
    
    # Initial page load
    if request.method == "GET":

     return render_template(
        "index.html",

        weather=None,
        air=None,
        forecast=[],
        elevation=None,

        recommendation=None,

        sunrise="",
        sunset="",

        traffic=None,
        waterlogging=None,

        weather_score=0,
        travel_score=0,

        route_advice=[],

        summary="",

        city="",
        destination="",

        error=None
    )

    if request.method == "POST":

        city = request.form.get("source", "").strip()
        destination = request.form.get("destination", "").strip()

        if city == "":
            error = "Please enter source."

            return render_template(
                "index.html",
                error=error
            )

        source = geocode_location(city)

        if source is None:

            error = "Source not found."

            return render_template(
                "index.html",
                error=error
            )

        source_lat = source["lat"]
        source_lon = source["lon"]

        destination_data = None

        if destination != "":

            destination_data = geocode_location(destination)

            if destination_data is None:

                error = "Destination not found."

                return render_template(
                    "index.html",
                    error=error
                )
                
                

                print("Destination Location:")
                print(destination_data)

        weather_json = get_weather(
            source_lat,
            source_lon
        )
        
# =====================================================
# LOCAL TIME OF SEARCHED CITY
# =====================================================

        timezone_name = weather_json.get("timezone", "UTC")

        local_time = datetime.now(
            ZoneInfo(timezone_name)
        ).strftime("%I:%M %p")

        latest_local_time = local_time

        air_json = get_air_quality(
                    source_lat,
                    source_lon
                )

        elevation_json = get_elevation(
            source_lat,
            source_lon
        )
        
         # ==========================================
        # CURRENT WEATHER
        # ==========================================

        icon, status = weather_icon(
            weather_json["current"]["weather_code"]
        )

        weather = {

            "temperature":
                weather_json["current"]["temperature_2m"],

            "feels_like":
                weather_json["current"]["apparent_temperature"],

            "humidity":
                weather_json["current"]["relative_humidity_2m"],

            "wind":
                weather_json["current"]["wind_speed_10m"],

            "wind_direction":
                weather_json["current"]["wind_direction_10m"],

            "icon": icon,

            "status": status

        }

        # ==========================================
        # AIR QUALITY
        # ==========================================

        air = {

            "pm10":
                air_json["current"]["pm10"],

            "pm25":
                air_json["current"]["pm2_5"],

            "co":
                air_json["current"]["carbon_monoxide"]

        }

        air.update(
            aqi_status(air["pm25"])
        )

        # ==========================================
        # ELEVATION
        # ==========================================

        elevation = elevation_json["elevation"][0]

        # ==========================================
        # SUNRISE / SUNSET
        # ==========================================

        sunrise = datetime.strptime(

            weather_json["daily"]["sunrise"][0],

            "%Y-%m-%dT%H:%M"

        ).strftime("%I:%M %p")

        sunset = datetime.strptime(

            weather_json["daily"]["sunset"][0],

            "%Y-%m-%dT%H:%M"

        ).strftime("%I:%M %p")

        # ==========================================
        # RAIN CHANCE
        # ==========================================

        rain = weather_json["daily"][
            "precipitation_probability_max"
        ][0]

        # ==========================================
        # FORECAST
        # ==========================================

        forecast = build_forecast(
            weather_json
        )

        # ==========================================
        # SMART WEATHER RECOMMENDATION
        # ==========================================

        if weather["temperature"] >= 35:

            recommendation = {

                "title": "🔥 Very Hot",

                "message":
                "Avoid travelling in the afternoon. Carry water."

            }

        elif rain >= 70:

            recommendation = {

                "title": "🌧 Heavy Rain",

                "message":
                "Carry an umbrella and expect delays."

            }

        elif weather["temperature"] <= 15:

            recommendation = {

                "title": "🥶 Cold Weather",

                "message":
                "Wear warm clothes before travelling."

            }

        else:

            recommendation = {

                "title": "😊 Pleasant Weather",

                "message":
                "Perfect weather for travelling."

            }
            
            
            
            # ==========================================
        # WEATHER SCORE
        # ==========================================

        weather_score = calculate_weather_score(
            weather,
            rain
        )

        # ==========================================
        # WATERLOGGING PREDICTION
        # ==========================================

        waterlogging = predict_waterlogging(
            rain,
            weather["humidity"],
            elevation
        )

        # ==========================================
        # ROUTE CALCULATION
        # ==========================================

        if destination_data is not None:

            route = calculate_traffic(
                source_lat,
                source_lon,
                destination_data["lat"],
                destination_data["lon"]
            )
            
            print(route)

            traffic = {

                "status": route["status"],

                "distance": route["distance"],

                "duration": route["duration"],

                "speed": route["speed"],

                "congestion": route["congestion"],

                "coordinates": route["coordinates"]

            }

        else:

            traffic = {

                "status": "Not Selected",

                "distance": 0,

                "duration": 0,

                "speed": 0,

                "congestion": 0,

                "coordinates": []

            }

        # ==========================================
        # AI ROUTE ADVICE
        # ==========================================

        route_advice = best_route_advice(

            weather_score,

            traffic,

            waterlogging

        )
        
        best_route = choose_best_route(

                traffic,

                waterlogging

        )

        # ==========================================
        # AI TRAVEL SUMMARY
        # ==========================================

        if destination != "":

            summary = ai_summary(

                city,

                destination,

                weather,

                traffic,

                waterlogging

            )

        else:

            summary = "Destination not selected."

        # ==========================================
        # TRAVEL SCORE
        # ==========================================

        travel_score = 10

        if weather_score < 80:
            travel_score -= 2

        if traffic["congestion"] > 60:
            travel_score -= 2

        if waterlogging["status"] == "Moderate":
            travel_score -= 2

        if waterlogging["status"] == "High":
            travel_score -= 4

        travel_score = max(1, travel_score)
        
        # ==========================================
# AI ROUTE RECOMMENDATION
# ==========================================

        route_recommendation = generate_route_recommendation(

            weather_score,

            traffic,

            waterlogging,

            traffic["duration"]

        )
        
        safe_route = safest_route(

            weather_score,

            traffic,

            waterlogging

        )
        
        # ==========================================
        # AI BEST ROUTE RECOMMENDATION
        # ==========================================

        ai_recommendation = generate_route_recommendation(

            weather_score,

            traffic,

            waterlogging,

            traffic["duration"]

        )

        # ==========================================
        # SAVE GLOBAL VARIABLES
        # ==========================================

        latest_weather = weather

        latest_air = air

        latest_forecast = forecast

        latest_route = traffic

        latest_waterlogging = waterlogging

        latest_city = city

        latest_destination = destination

        latest_elevation = elevation

        latest_sunrise = sunrise

        latest_sunset = sunset
        
        latest_recommendation = ai_recommendation

        latest_travel = {

            "travel_score": travel_score,

            "weather_score": weather_score,

            "route_advice": route_advice,

            "summary": summary

        }
        
    
        return render_template(

        "index.html",

        weather=weather,

        air=air,

        forecast=forecast,

        elevation=elevation,

        recommendation=recommendation,
        
        route_recommendation=route_recommendation,

        sunrise=sunrise,

        sunset=sunset,

        traffic=traffic,

        waterlogging=waterlogging,

        weather_score=weather_score,

        travel_score=travel_score,

        route_advice=route_advice,
        
        best_route=best_route,

        summary=summary,

        city=city,

        destination=destination,
        
        local_time=latest_local_time,
        
        ai_recommendation=ai_recommendation,
        
        safe_route=safe_route,

        error=error

    )


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

@app.route("/download")
def download():

    if latest_weather == {}:

        return "Please search a location first."

    create_pdf(

        latest_weather,

        latest_air,

        latest_elevation,

        {
            "title": "AI Travel Recommendation",
            "message": latest_travel["summary"]
        },

        latest_sunrise,

        latest_sunset,

        latest_route,

        latest_waterlogging,

        latest_travel["travel_score"],

        latest_travel["weather_score"],

        latest_travel["route_advice"],

        latest_city,

        latest_destination

    )

    return send_file(

        "weather_report.pdf",

        as_attachment=True

    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)                   