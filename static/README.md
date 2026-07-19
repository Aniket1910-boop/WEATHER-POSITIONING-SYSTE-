# 🌍 Weather Positioning System

A professional Flask-based Weather Dashboard that collects real-time environmental information using multiple Open-Meteo APIs.

---

## 📌 Features

- 🌤 Current Weather
- 🌡 Temperature
- 🤗 Feels Like Temperature
- 💧 Humidity
- 🌬 Wind Speed
- 🧭 Wind Direction
- 🌅 Sunrise
- 🌇 Sunset
- 🌧 Rain Probability
- 🌫 Air Quality
- 📍 Elevation
- 📅 7-Day Weather Forecast
- 📊 Temperature Chart
- 🗺 Interactive Leaflet Map
- 📄 PDF Weather Report
- 📱 Responsive Bootstrap Dashboard

---

## 🛠 Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js
- Leaflet.js

---

## 🌐 APIs Used

### 1. Open-Meteo Weather API

Provides:

- Temperature
- Humidity
- Wind
- Weather Code
- Sunrise
- Sunset
- Forecast

---

### 2. Open-Meteo Air Quality API

Provides:

- PM10
- PM2.5
- Carbon Monoxide

---

### 3. Open-Meteo Elevation API

Provides:

- Elevation above sea level

---

### 4. Open-Meteo Geocoding API

Converts city names into latitude and longitude.

---

## 📁 Project Structure

```
Weather_Positioning_System
│
├── app.py
├── pdf_generator.py
├── requirements.txt
│
├── templates
│      └── index.html
│
├── static
│      ├── css
│      │      └── style.css
│      │
│      └── js
│             └── script.js
│
└── weather_report.pdf
```

---

## ▶ How to Run

Install dependencies

```
pip install flask requests reportlab
```

Run

```
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## 📸 Dashboard Features

- Current Weather
- Weather Highlights
- Air Quality
- Elevation
- Forecast
- Interactive Map
- Temperature Graph
- Download PDF

---

## 👨‍💻 Developer

Aniket Panda

B.Tech Computer Science Engineering

Weather Positioning System using Flask and Open-Meteo APIs.