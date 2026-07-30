// ===============================
// Dark Mode Toggle
// ===============================

const themeToggle = document.getElementById("themeToggle");

// Load saved theme
if (localStorage.getItem("theme") === "light") {

    document.body.classList.add("light-mode");

    themeToggle.innerHTML = "☀️ Light Mode";

}

// Toggle Theme
themeToggle.addEventListener("click", function () {

    document.body.classList.toggle("light-mode");

    if (document.body.classList.contains("light-mode")) {

        localStorage.setItem("theme", "light");

        themeToggle.innerHTML = "☀️ Light Mode";

    } else {

        localStorage.setItem("theme", "dark");

        themeToggle.innerHTML = "🌙 Dark Mode";

    }

});