from flask import Flask, render_template, request, send_file
import requests
from datetime import datetime
from pdf_generator import create_pdf

app = Flask(__name__)

# ==========================================================
# Store latest searched data for PDF Generation
# ==========================================================

latest_weather = None
latest_air = None
latest_elevation = None
latest_recommendation = None


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    global latest_weather
    global latest_air
    global latest_elevation
    global latest_recommendation

    # ======================================================
    # Default Variables
    # ======================================================

    weather = None
    air = None
    elevation = None
    forecast = []
    recommendation = None

    sunrise = ""
    sunset = ""
    rain_chance = ""

    city = ""
    latitude = ""
    longitude = ""

    error = None

    # ======================================================
    # POST REQUEST
    # ======================================================

    if request.method == "POST":

        city = request.form.get("city", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()

        try:

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

            weather_response = requests.get(
                weather_url,
                timeout=15
            )

            weather_data = weather_response.json()
            
            print(weather_data["daily"]["sunrise"][0])
            print(weather_data["daily"]["sunset"][0])

            # ==================================================
            # CURRENT WEATHER
            # ==================================================

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
            # WEATHER ICON & STATUS
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
            # SMART WEATHER RECOMMENDATION
            # ==================================================

            if temperature > 35:

                recommendation = {
                    "title": "🔥 Very Hot",
                    "message": (
                        "Drink plenty of water, wear light clothes "
                        "and avoid direct sunlight during afternoon."
                    )
                }

            elif temperature > 25:

                recommendation = {
                    "title": "😊 Pleasant Weather",
                    "message": (
                        "Perfect weather for outdoor activities. "
                        "Stay hydrated and enjoy your day."
                    )
                }

            elif temperature > 15:

                recommendation = {
                    "title": "☁️ Cool Weather",
                    "message": (
                        "A pleasant day. Carry a light jacket "
                        "if you are going out in the evening."
                    )
                }

            else:

                recommendation = {
                    "title": "🥶 Cold Weather",
                    "message": (
                        "Wear warm clothes and avoid staying "
                        "outside for long periods."
                    )
                }

            # ==================================================
            # 7-DAY FORECAST
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

                elif code in [1, 2]:
                    icon = "🌤"

                elif code == 3:
                    icon = "☁️"

                elif code in [45, 48]:
                    icon = "🌫"

                elif code in [51, 53, 55]:
                    icon = "🌦"

                elif code in [61, 63, 65]:
                    icon = "🌧"

                elif code in [71, 73, 75]:
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

            # ==================================================
            # SUNRISE & SUNSET
            # ==================================================

            sunrise = datetime.strptime(
                weather_data["daily"]["sunrise"][0],
                "%Y-%m-%dT%H:%M"
            ).strftime("%I:%M %p")

            sunset = datetime.strptime(
                weather_data["daily"]["sunset"][0],
                "%Y-%m-%dT%H:%M"
            ).strftime("%I:%M %p")

            # ==================================================
            # RAIN CHANCE
            # ==================================================

            rain_chance = weather_data["daily"][
                "precipitation_probability_max"
            ][0]
            
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
            # SAVE DATA FOR PDF
            # ==================================================

            latest_weather = weather
            latest_air = air
            latest_elevation = elevation
            latest_recommendation = recommendation

        except Exception as e:

            error = f"Error: {str(e)}"

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

        latitude=latitude,

        longitude=longitude,

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

    if latest_weather is None:

        return "Please search weather first."

    create_pdf(

        latest_weather,
        latest_air,
        latest_elevation,
        latest_recommendation

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