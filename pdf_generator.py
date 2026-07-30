from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from datetime import datetime

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def create_pdf(
    weather,
    air,
    elevation,
    recommendation,
    sunrise,
    sunset,
    traffic,
    waterlogging,
    travel_score,
    weather_score,
    route_advice,
    city,
    destination
):
    pdf = SimpleDocTemplate("weather_report.pdf")

    story = []

    # ==========================================
    # TITLE
    # ==========================================

    story.append(
        Paragraph(
            "<b>Weather Positioning System Report</b>",
            title_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # WEATHER TABLE
    # ==========================================

    story.append(
        Paragraph(
            "Current Weather",
            heading_style
        )
    )

    data = [

        ["Parameter", "Value"],

        ["Temperature", f"{weather['temperature']} °C"],

        ["Feels Like", f"{weather['feels_like']} °C"],

        ["Humidity", f"{weather['humidity']} %"],

        ["Wind Speed", f"{weather['wind']} km/h"],

        ["Wind Direction", str(weather["wind_direction"])]

    ]

    table = Table(
        data,
        colWidths=[3 * inch, 2.5 * inch]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")

        ])

    )

    story.append(table)

    story.append(Spacer(1, 20))

    # ==========================================
    # AIR QUALITY
    # ==========================================

    story.append(
        Paragraph(
            "Air Quality",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"PM10 : {air['pm10']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"PM2.5 : {air['pm25']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Carbon Monoxide : {air['co']}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # ELEVATION
    # ==========================================

    story.append(
        Paragraph(
            "Elevation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"{elevation} metres",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # SUNRISE / SUNSET
    # ==========================================

    story.append(
        Paragraph(
            "Sun Information",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"Sunrise : {sunrise}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Sunset : {sunset}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))
    
    
    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "Travel Information",
            heading_style
        )
    )

    travel_table = [

        ["Source", city],

        ["Destination", destination],

        ["Distance",
        f"{traffic['distance']} km"],

        ["Duration",
        f"{traffic['duration']} mins"],

        ["Traffic",
        traffic["status"]],

        ["Average Speed",
        f"{traffic['speed']} km/h"]

    ]

    table = Table(travel_table, colWidths=[3*inch,3*inch])

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    story.append(table)

    story.append(Spacer(1,20)) 
    
    
    story.append(
    Paragraph(
        "Waterlogging Prediction",
        heading_style
    )
)

    story.append(
        Paragraph(
            f"Risk : {waterlogging['status']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            waterlogging["message"],
            normal_style
        )
    )

    story.append(Spacer(1,20))  
    
    
    story.append(
    Paragraph(
        "Travel Scores",
        heading_style
    )
)

    story.append(
        Paragraph(
            f"Weather Score : {weather_score}/100",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"Travel Score : {travel_score}/10",
            normal_style
        )
    )

    story.append(Spacer(1,20))

 # ==========================================
# AI TRAVEL RECOMMENDATION
# ==========================================

    story.append(
        Paragraph(
            "AI Travel Recommendation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>{recommendation['title']}</b>",
            normal_style
        )
    )

    story.append(
        Paragraph(
            recommendation["message"],
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Route Advice</b>",
            normal_style
        )
    )

    for item in route_advice:

        story.append(
            Paragraph(
                "• " + item,
                normal_style
            )
        )

    story.append(Spacer(1, 20))   

  # ==========================================
# FOOTER
# ==========================================

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Weather Positioning System v2.0</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "Developed as a Smart Travel & Weather Intelligence Platform.",
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Technologies Used</b>",
            normal_style
        )
    )

    technologies = [
        "Python",
        "Flask Framework",
        "Open-Meteo Weather API",
        "Open-Meteo Air Quality API",
        "OpenStreetMap Nominatim",
        "Geoapify Routing API",
        "ReportLab PDF Library"
    ]

    for tech in technologies:

        story.append(
            Paragraph(
                "• " + tech,
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Report Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Thank you for using Weather Positioning System v2.0</b>",
            normal_style
        )
    )  
    
    pdf.build(story) 