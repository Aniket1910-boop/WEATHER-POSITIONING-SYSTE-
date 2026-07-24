import requests
from config import GEOAPIFY_API_KEY


def calculate_traffic(start_lat, start_lon,
                      end_lat, end_lon):

    url = (
        "https://api.geoapify.com/v1/routing"
        f"?waypoints={start_lat},{start_lon}|{end_lat},{end_lon}"
        "&mode=drive"
        "&apiKey=" + GEOAPIFY_API_KEY
    )

    response = requests.get(url)

    data = response.json()

    feature = data["features"][0]

    distance = feature["properties"]["distance"]

    duration = feature["properties"]["time"]

    coordinates = feature["geometry"]["coordinates"][0]

    # Convert seconds into km/h

    speed = (distance / 1000) / (duration / 3600)

    if speed > 40:

        status = "🟢 Smooth"

        congestion = 20

    elif speed > 25:

        status = "🟡 Moderate"

        congestion = 45

    elif speed > 15:

        status = "🟠 Heavy"

        congestion = 70

    else:

        status = "🔴 Severe"

        congestion = 90

    return {

        "distance": round(distance / 1000, 2),

        "duration": round(duration / 60, 1),

        "speed": round(speed, 1),

        "status": status,

        "congestion": congestion,

        "coordinates": coordinates

    }