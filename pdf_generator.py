from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def create_pdf(weather, air, elevation, recommendation, sunrise, sunset):

    pdf = SimpleDocTemplate("weather_report.pdf")

    story = []

    # ================= TITLE =================

    story.append(
        Paragraph(
            "<b>🌍 Weather Positioning System</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "<font size='12'>Professional Weather Intelligence Report</font>",
            normal_style
        )
    )
    
    current_time = datetime.now().strftime("%d-%m-%Y   %I:%M %p")

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {current_time}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ================= CURRENT WEATHER =================

    story.append(Paragraph("Current Weather", heading_style))

    weather_table = [

        ["Parameter", "Value"],

        ["🌡 Temperature", f"{weather['temperature']} °C"],

        ["💧 Humidity", f"{weather['humidity']} %"],

        ["🌬 Wind Speed", f"{weather['wind']} km/h"]

    ]

    table = Table(weather_table, colWidths=[3 * inch, 2 * inch])

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("GRID", (0,0), (-1,-1), 1, colors.grey),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10)

    ]))

    story.append(table)

    story.append(Spacer(1,20))
    # ================= AIR QUALITY =================

    story.append(Paragraph("Air Quality", heading_style))

    story.append(
        Paragraph(
            f"<b>PM10 :</b> {air['pm10']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>PM2.5 :</b> {air['pm25']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Carbon Monoxide :</b> {air['co']}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ================= ELEVATION =================

    story.append(Paragraph("Elevation", heading_style))

    story.append(
        Paragraph(
            f"<b>Elevation :</b> {elevation} metres",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ================= WEATHER RECOMMENDATION =================

    story.append(Paragraph("Weather Recommendation", heading_style))

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

    story.append(Spacer(1, 30))

    # ================= FOOTER =================

    story.append(
        Paragraph(
            "Generated using Flask + Open-Meteo API",
            normal_style
        )
    )

    pdf.build(story)