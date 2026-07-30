import requests
from config import GEOAPIFY_API_KEY


def calculate_traffic(start_lat, start_lon, end_lat, end_lon):

    url = (
        "https://api.geoapify.com/v1/routing"
        f"?waypoints={start_lat},{start_lon}|{end_lat},{end_lon}"
        "&mode=drive"
        "&details=route_details"
        f"&apiKey={GEOAPIFY_API_KEY}"
    )

    try:

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        data = response.json()

        if "features" not in data or len(data["features"]) == 0:
            raise Exception("Route not found")

        feature = data["features"][0]

        props = feature["properties"]

        geometry = feature["geometry"]

        distance = props["distance"]          # metres
        duration = props["time"]             # seconds

        coordinates = geometry["coordinates"][0]

        speed = (distance / 1000) / (duration / 3600)

        if speed >= 45:

            status = "Low"

            color = "green"

            congestion = 15

            message = "Traffic is smooth."

        elif speed >= 30:

            status = "Moderate"

            color = "yellow"

            congestion = 40

            message = "Moderate traffic."

        elif speed >= 15:

            status = "Heavy"

            color = "orange"

            congestion = 70

            message = "Heavy traffic. Drive carefully."

        else:

            status = "Severe"

            color = "red"

            congestion = 95

            message = "Severe congestion. Avoid this route."

        return {

            "distance": round(distance / 1000, 2),

            "duration": round(duration / 60, 1),

            "speed": round(speed, 1),

            "status": status,

            "color": color,

            "message": message,

            "congestion": congestion,

            "coordinates": coordinates

        }

    except Exception as e:

        return {

            "distance": 0,

            "duration": 0,

            "speed": 0,

            "status": "Unavailable",

            "color": "gray",

            "message": str(e),

            "congestion": 0,

            "coordinates": []

        }