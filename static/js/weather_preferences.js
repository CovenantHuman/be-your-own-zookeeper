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

maxTempBox.addEventListener("change", () => {
    const tempMax = maxTempBox.value;
    minTempBox.setAttribute("max", String(tempMax));
});

minTempBox.addEventListener("change", () => {
    const tempMin = minTempBox.value;
    maxTempBox.setAttribute("min", String(tempMin));
});

const maxCloudBox = document.querySelector("#max_clouds");
const minCloudBox = document.querySelector("#min_clouds");

maxCloudBox.addEventListener("change", () => {
    const cloudMax = maxCloudBox.value;
    minCloudBox.setAttribute("max", String(cloudMax));
});

minCloudBox.addEventListener("change", () => {
    const cloudMin = minCloudBox.value;
    maxCloudBox.setAttribute("min", String(cloudMin));
});