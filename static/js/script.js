// ======================================================
// WEATHER POSITIONING SYSTEM
// ======================================================

// ======================================================
// CREATE MAP
// ======================================================

var map = L.map("map").setView([20.5937, 78.9629], 5);

// ======================================================
// OPENSTREETMAP
// ======================================================

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap"
    }
).addTo(map);


// ==========================================
// LIVE RAIN RADAR
// ==========================================

var rainLayer = L.tileLayer(

    "https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=0aa6d898e1473fc83a1a25ea622775e6",

    {

        opacity:0.55

    }

);

// ======================================================
// CAR ICON
// ======================================================

var carIcon = L.icon({

    iconUrl: "https://cdn-icons-png.flaticon.com/512/744/744465.png",

    iconSize: [40,40],

    iconAnchor: [20,20]

});

// ======================================================
// DRAW ROUTE
// ======================================================

if (
    typeof routeCoordinates !== "undefined" &&
    routeCoordinates.length > 0
) {

    let points = [];

    routeCoordinates.forEach(function(coord){

        points.push([coord[1], coord[0]]);

    });

    // Source Marker

    // ======================================================
// MOVING CAR
// ======================================================

        var car = L.marker(points[0], {

            icon: carIcon

        }).addTo(map)

        .bindPopup("Travelling...");

    // Destination Marker

    L.marker(points[points.length - 1])
        .addTo(map)
        .bindPopup("Destination");

    // Route Line

    let routeColor = "#28a745";

        if(routeStatus=="danger"){

            routeColor="#dc3545";

        }

        else if(routeStatus=="warning"){

            routeColor="#ffc107";

        }

        else if(routeStatus=="info"){

            routeColor="#17a2b8";

        }

        L.polyline(points,{

            color:routeColor,

        weight:8,
        lineCap:"round",
        lineJoin:"round",

            opacity:0.9

        }).addTo(map);

    map.fitBounds(points);

    setTimeout(function(){

    map.panTo(points[points.length-1]);

},1200);


    // ======================================================
// CAR ANIMATION
// ======================================================

let index = 0;

function moveCar(){

    if(index >= points.length){

        return;   // Stop when destination is reached

    }

    car.setLatLng(points[index]);

    index++;

    setTimeout(moveCar, 50);

}

moveCar();

}
else{

    map.setView([22.5726,88.3639],10);

}

// ======================================================
// CURRENT LOCATION (Optional)
// ======================================================

function locateUser(){

    if(!navigator.geolocation){

        alert("Geolocation not supported.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function(position){

            let lat = position.coords.latitude;

            let lon = position.coords.longitude;

            map.setView([lat,lon],13);

            L.marker([lat,lon])

                .addTo(map)

                .bindPopup("Your Current Location")

                .openPopup();

        },

        function(){

            console.log("Location permission denied.");

        }

    );

}

// ======================================================
// PAGE ANIMATION
// ======================================================

window.onload = function(){

    document.body.style.opacity = "1";

};

// ======================================================
// BUTTON HOVER EFFECT
// ======================================================

let buttons = document.querySelectorAll("button");

buttons.forEach(function(btn){

    btn.addEventListener("mouseenter",function(){

        btn.style.transform="scale(1.02)";

    });

    btn.addEventListener("mouseleave",function(){

        btn.style.transform="scale(1)";

    });

});

// ======================================================
// CARD HOVER
// ======================================================

let cards=document.querySelectorAll(".card");

cards.forEach(function(card){

    card.addEventListener("mouseenter",function(){

        card.style.transition=".3s";

    });

});


// ==========================================
// TOGGLE RAIN RADAR
// ==========================================

function toggleRain(){

    if(map.hasLayer(rainLayer)){

        map.removeLayer(rainLayer);

    }

    else{

        rainLayer.addTo(map);

    }

}

function getLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            fetch(`/current-location?lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(data => {

                    if(data.city){

                        document.querySelector(
                        "input[name='source']").value = data.city;

                    }

                });

        },

        function(){

            alert("Location permission denied.");

        }

    );

}

// ======================================================
// GET USER CURRENT LOCATION
// ======================================================

function getLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported.");

        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            fetch(`/current-location?lat=${lat}&lon=${lon}`)

            .then(response => response.json())

            .then(data => {

               document.querySelector("input[name='source']").value = data.city;

               document.querySelector("form").submit();

            })

            .catch(error => {

                console.log(error);

                alert("Unable to fetch location.");

            });

        },

        function(error) {

            alert("Location permission denied.");

        }

    );

}


// =====================================
// TEMPERATURE CHART
// =====================================

const chartCanvas = document.getElementById("temperatureChart");

if(chartCanvas){

    new Chart(chartCanvas,{

        type:"line",

        data:{

            labels:forecastDays,

            datasets:[{

                label:"Maximum Temperature (°C)",

                data:forecastTemp,

                borderColor:"#ff5722",

                backgroundColor:"rgba(255,87,34,0.2)",

                borderWidth:3,

                tension:0.4,

                fill:true

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    display:true

                }

            }

        }

    });

}