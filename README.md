# 🌦️ Weather Positioning System

> **An Intelligent Weather, Traffic & Route Analysis Platform built using Flask and Multiple APIs**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/HTML-5-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS-3-blue?logo=css3)

---

# 📌 Project Overview

The **Weather Positioning System** is a smart travel assistant that helps users make better travel decisions using **real-time weather**, **traffic analysis**, **air quality**, **waterlogging prediction**, and **AI-powered travel recommendations**.

Instead of showing only weather information, the system analyzes multiple environmental factors and recommends whether travelling is safe.

---

# ✨ Key Features

## 🌤️ Weather Information
- Current Temperature
- Feels Like Temperature
- Humidity
- Wind Speed
- Wind Direction
- Weather Description
- Sunrise & Sunset
- 7-Day Weather Forecast

---

## 🌫️ Air Quality Monitoring
- PM2.5
- PM10
- Carbon Monoxide
- Air Quality Classification

---

## 🚗 Smart Traffic Analysis
- Estimated Travel Time
- Distance Calculation
- Traffic Status
- Route Analysis
- Congestion Detection

---

## 🌧️ Waterlogging Prediction

Predicts waterlogging risk using:

- Rain Probability
- Humidity
- Elevation

Risk Levels:

- 🟢 Low
- 🟡 Moderate
- 🔴 High

---

## ⭐ Weather Score

Calculates a weather score (0–100) based on:

- Temperature
- Rain Probability
- Wind Speed

Higher score indicates better weather conditions.

---

## ⭐ Travel Score

Calculates travel suitability by combining:

- Weather Score
- Traffic Conditions
- Waterlogging Risk

Travel Score ranges from **1 to 10**.

---

## 🤖 AI Travel Recommendation

The system intelligently suggests whether to:

- ✅ Travel
- ⚠️ Travel Carefully
- 🚫 Avoid Travelling

---

## 🛣️ Safe Route Recommendation

Provides:

- Best Route
- Alternative Route
- Safer Route
- Route Warnings

---

## 📍 Current Location

Automatically detects user's location using reverse geocoding.

---

## 🗺️ Interactive Map

Displays:

- Source Location
- Destination Location
- Travel Route
- Weather Location

---

## 📄 Download PDF Report

Generates a professional report containing:

- Weather Summary
- Forecast
- Air Quality
- Traffic Analysis
- Weather Score
- Travel Score
- AI Recommendation

---

# 🛠️ Technologies Used

## Backend

- Python
- Flask

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Maps

- Leaflet.js

---

# 🌐 APIs Used

| API | Purpose |
|------|----------|
| Open-Meteo Weather API | Current Weather & Forecast |
| Open-Meteo Air Quality API | AQI |
| Open-Meteo Elevation API | Elevation |
| Geoapify Geocoding API | City → Coordinates |
| Geoapify Routing API | Route & Traffic |
| Nominatim Reverse Geocoding | Current Location |

---

# 📂 Project Structure

```text
WEATHER-POSITIONING-SYSTEM
│
├── app.py
├── traffic.py
├── pdf_generator.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   └── theme.js
│   └── images/
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Aniket1910-boop/WEATHER-POSITIONING-SYSTEM.git
```

Move into the project directory

```bash
cd WEATHER-POSITIONING-SYSTEM
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 📊 Workflow

```
User Input
      │
      ▼
Geocoding API
      │
      ▼
Weather APIs
      │
      ▼
Traffic Analysis
      │
      ▼
Waterlogging Prediction
      │
      ▼
Weather Score
      │
      ▼
Travel Score
      │
      ▼
AI Recommendation
      │
      ▼
Dashboard + PDF Report
```

---

# 🚀 Future Enhancements

- Machine Learning Weather Prediction
- Live Traffic API Integration
- User Login System
- Historical Weather Analytics
- Weather Alerts
- Mobile Application
- Multi-language Support
- Database Integration
- Push Notifications

---

# 📚 Learning Outcomes

This project helped in learning:

- REST APIs
- Flask Framework
- Python Programming
- JSON Processing
- Frontend–Backend Integration
- Route Analysis
- Weather Forecasting APIs
- PDF Generation using ReportLab
- Responsive UI Design

---

# 👨‍💻 Developer

**Aniket Panda**

B.Tech Computer Science Engineering

GitHub: **https://github.com/Aniket1910-boop**

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📄 License

This project is developed for educational and internship purposes.