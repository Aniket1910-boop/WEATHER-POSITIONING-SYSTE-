def calculate_traffic(weather, air, rain_chance, elevation):

    traffic = {}

    score = 0

    # Rain
    score += rain_chance * 0.5

    # Wind
    score += weather["wind"] * 0.3

    # Air Quality
    score += air["pm25"] * 0.2

    # Elevation

    if elevation < 20:
        score += 20

    elif elevation < 50:
        score += 10

    if score > 100:
        score = 100

    traffic["congestion"] = int(score)

    if score < 25:

        traffic["status"] = "🟢 Smooth"

    elif score < 50:

        traffic["status"] = "🟡 Moderate"

    elif score < 75:

        traffic["status"] = "🟠 Heavy"

    else:

        traffic["status"] = "🔴 Severe"

    return traffic