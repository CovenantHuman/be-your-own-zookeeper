'use strict';

const celsiusSelector = document.querySelector("#celsius");
const fahrenheitSelector = document.querySelector("#fahrenheit")
const maxTempBox = document.querySelector("#max_temp");
const minTempBox = document.querySelector("#min_temp");

celsiusSelector.addEventListener('change', () => {
    if (celsiusSelector.checked) {
        maxTempBox.setAttribute("max", "32");
        maxTempBox.setAttribute("min", "-17");
        minTempBox.setAttribute("max", "32");
        minTempBox.setAttribute("min", "-17");
    }
});

fahrenheitSelector.addEventListener('change', () => {
    if (fahrenheitSelector.checked) {
        maxTempBox.setAttribute("max", "90");
        maxTempBox.setAttribute("min", "0");
        minTempBox.setAttribute("max", "90");
        minTempBox.setAttribute("min", "0");
    }
});