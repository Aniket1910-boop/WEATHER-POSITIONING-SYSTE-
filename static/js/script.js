// =====================
// LEAFLET MAP
// =====================

const mapElement = document.getElementById("map");

if (mapElement) {

    const map = L.map("map").setView(
        [latitude, longitude],
        10
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    L.marker([latitude, longitude])
        .addTo(map)
        .bindPopup(
            `Latitude: ${latitude}<br>Longitude: ${longitude}`
        )
        .openPopup();
}

// ============================
// 7-DAY FORECAST CHART
// ============================

const chartCanvas = document.getElementById("weatherChart");

if (chartCanvas) {

    new Chart(chartCanvas, {

        type: "line",

        data: {

            labels: forecastDates,

            datasets: [

                {
                    label: "Maximum Temperature (°C)",
                    data: forecastMax,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                },

                {
                    label: "Minimum Temperature (°C)",
                    data: forecastMin,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                }

            ]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: true

                }

            }

        }

    });

}

// ============================
// PAGE ANIMATION
// ============================

window.onload = function () {

    document.body.style.opacity = "1";

};

// ============================
// LIVE DATE & TIME
// ============================

function updateDateTime() {

    const now = new Date();

    const options = {

        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"

    };

    const dateElement = document.getElementById("currentDate");
    const timeElement = document.getElementById("currentTime");

    if (dateElement) {
        dateElement.innerHTML = now.toLocaleDateString("en-IN", options);
    }

    if (timeElement) {
        timeElement.innerHTML = now.toLocaleTimeString("en-IN");
    }

}

updateDateTime();

setInterval(updateDateTime, 1000);

// ============================
// GET USER LOCATION
// ============================

function getLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            function(position) {

                document.getElementById("latitude").value =
                    position.coords.latitude;

                document.getElementById("longitude").value =
                    position.coords.longitude;

                document.querySelector("form").submit();

            },

            function() {

                alert("Unable to get your location.");

            }

        );

    } else {

        alert("Geolocation is not supported by this browser.");

    }

}

// ==========================
// LOADING SCREEN
// ==========================

window.addEventListener("load", function () {

    document.getElementById("loader").style.display = "none";

});

// ==========================
// SHOW LOADER ON FORM SUBMIT
// ==========================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", function () {

        document.getElementById("loader").style.display = "flex";

    });

}

// ==========================
// DYNAMIC WEATHER BACKGROUND
// ==========================

if (typeof temperature !== "undefined") {

    const status = "{{ weather.status if weather else '' }}";

}

// ==========================
// DYNAMIC WEATHER BACKGROUND
// ==========================

if (typeof weatherStatus !== "undefined") {

    if (weatherStatus === "Clear Sky") {

        document.body.classList.add("sunny");

    }

    else if (weatherStatus === "Cloudy") {

        document.body.classList.add("cloudy");

    }

    else if (weatherStatus === "Rain") {

        document.body.classList.add("rainy");

    }

    else if (weatherStatus === "Snow") {

        document.body.classList.add("snow");

    }

    else if (weatherStatus === "Thunderstorm") {

        document.body.classList.add("thunder");

    }

}

// ============================
// DYNAMIC WEATHER BACKGROUND
// ============================

if (weatherStatus !== "") {

    if (weatherStatus === "Clear Sky") {

        document.body.style.background =
        "linear-gradient(135deg,#87CEEB,#E0F7FA)";

    }

    else if (weatherStatus === "Partly Cloudy") {

        document.body.style.background =
        "linear-gradient(135deg,#74b9ff,#dfe6e9)";

    }

    else if (weatherStatus === "Cloudy") {

        document.body.style.background =
        "linear-gradient(135deg,#bdc3c7,#95a5a6)";

    }

    else if (weatherStatus === "Rain") {

        document.body.style.background =
        "linear-gradient(135deg,#2c3e50,#4ca1af)";

    }

    else if (weatherStatus === "Snow") {

        document.body.style.background =
        "linear-gradient(135deg,#ffffff,#dfe9f3)";

    }

    else if (weatherStatus === "Thunderstorm") {

        document.body.style.background =
        "linear-gradient(135deg,#232526,#414345)";

    }

}

// ================= LIVE DATE & TIME =================

function updateClock() {

    const now = new Date();

    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    document.getElementById("currentDate").innerHTML =
        now.toLocaleDateString("en-US", options);

    document.getElementById("currentTime").innerHTML =
        now.toLocaleTimeString();

}

updateClock();

setInterval(updateClock, 1000);

// ================= HUMIDITY GAUGE =================

if(document.getElementById("humidityGauge")){

    var opts = {

        angle:0,

        lineWidth:0.25,

        radiusScale:1,

        pointer:{
            length:0.6,
            strokeWidth:0.04,
            color:"#000000"
        },

        limitMax:false,
        limitMin:false,

        colorStart:"#00BCD4",
        colorStop:"#2196F3",

        strokeColor:"#EEEEEE",

        generateGradient:true

    };

    var target=document.getElementById("humidityGauge");

    var gauge=new Gauge(target).setOptions(opts);

    gauge.maxValue=100;

    gauge.setMinValue(0);

    gauge.animationSpeed=40;

    gauge.set(humidity);
}

// ==========================================================
// DARK MODE
// ==========================================================

function toggleDarkMode(){

    document.body.classList.toggle("dark-mode");

    const button = document.querySelector(".navbar .btn-light");

    if(document.body.classList.contains("dark-mode")){

        localStorage.setItem("theme","dark");

        button.innerHTML="☀️ Light Mode";

    }

    else{

        localStorage.setItem("theme","light");

        button.innerHTML="🌙 Dark Mode";

    }

}

// ==========================================================
// LOAD SAVED THEME
// ==========================================================

window.addEventListener("load",function(){

    const theme=localStorage.getItem("theme");

    const button=document.querySelector(".navbar .btn-light");

    if(theme==="dark"){

        document.body.classList.add("dark-mode");

        if(button){

            button.innerHTML="☀️ Light Mode";

        }

    }

});

// ==========================================================
// ANIMATED COUNTERS
// ==========================================================

function animateCounter(id, endValue, decimals = 0) {

    const element = document.getElementById(id);

    if (!element) return;

    let start = 0;

    const duration = 1500;
    const stepTime = 20;
    const increment = endValue / (duration / stepTime);

    const timer = setInterval(function () {

        start += increment;

        if (start >= endValue) {

            element.innerHTML = Number(endValue).toFixed(decimals);
            clearInterval(timer);

        } else {

            element.innerHTML = Number(start).toFixed(decimals);

        }

    }, stepTime);

}


// ==========================================================
// START ALL COUNTERS
// ==========================================================

window.addEventListener("load", function () {

    animateCounter("tempCounter", temperature, 1);

    animateCounter("humidityCounter", humidity);

    animateCounter("windCounter", wind, 1);

    animateCounter("pm10Counter", pm10, 1);

    animateCounter("pm25Counter", pm25, 1);

    animateCounter("coCounter", co, 1);

    animateCounter("elevationCounter", elevationValue);

});