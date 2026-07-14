// This file contains JavaScript code for interactivity in the Crime Detection System web application.

document.addEventListener('DOMContentLoaded', function() {
    // Dropdown functionality
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function() {
            this.classList.toggle('is-active');
        });
    });

    // Alert display functionality
    const alertBox = document.getElementById('alert-box');
    if (alertBox) {
        setTimeout(() => {
            alertBox.style.display = 'none';
        }, 5000); // Hide alert after 5 seconds
    }

    // Route safety checker
    const routeForm = document.getElementById('route-form');
    if (routeForm) {
        routeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const start = document.getElementById('start-location').value;
            const end = document.getElementById('end-location').value;
            checkRouteSafety(start, end);
        });
    }

    function checkRouteSafety(start, end) {
        // Placeholder for route safety check logic
        alert(`Checking safety for route from ${start} to ${end}`);
        // Implement AJAX call to backend for real data
    }
});

// Geolocation and live zone check
function getLocationAndCheckZone() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function successCallback(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    fetch(`/check_zone?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === "danger") {
                alert(`⚠️ You are in a ${data.severity.toUpperCase()} zone (${data.location}). Be careful!\nRecent crimes: ${data.crimes}`);
            } else {
                alert(`✅ You are in a safe zone (${data.location}).`);
            }
        });
}

function errorCallback(error) {
    alert(`Error: ${error.message}`);
}