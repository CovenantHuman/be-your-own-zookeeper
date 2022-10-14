'use strict';

function getWeather(zipcode) {
    const queryString = new URLSearchParams(
        {zipcode : zipcode}).toString();

    fetch(`/zip-form?${queryString}`)
    .then(response => response.json())
    .then(serverData => {
        const walking = serverData.walking;
        const description = serverData.description;
        const currentTemp = serverData.real_temp;
        const feelsLike = serverData.feels_like;
        const isFahrenheit = serverData.is_fahrenheit;
        const humidity = serverData.humidity;
        const displayWind = serverData.display_wind;
        const isImperial = serverData.is_imperial;
        const clouds = serverData.clouds;
        const rain = serverData.rain;
        const snow = serverData.snow;
        const daylight = serverData.daylight;
        const activities = serverData.activities;

        displayWeather(walking, 
                    description, 
                    currentTemp, 
                    feelsLike, 
                    isFahrenheit, 
                    humidity, 
                    displayWind, 
                    isImperial,
                    clouds,
                    rain,
                    snow,
                    daylight,
                    activities)
    }).catch(() => {
        document.querySelector('.weather').innerHTML = "Problem getting weather information.";
    });
}

function displayWeather(walking, 
                        weatherDescription, 
                        displayTemp,
                        displayFeels, 
                        isFahrenheit,
                        humidity, 
                        displayWind, 
                        isImperial,
                        clouds, 
                        rain, 
                        snow, 
                        daylight,
                        activities){

    let tempUnit;
    if (isFahrenheit) {
        tempUnit = "degrees Fahrenheit";
    } else {
        tempUnit = "degrees Celsius";
    }

    let windUnit;
    if (isImperial) {
        windUnit = "miles per hour";
    } else {
        windUnit = "meters per second";
    }

    let rainState;
    if (rain) {
        rainState = "is";
    } else {
        rainState = "is not";
    }
    let snowState;
    if (snow) {
        snowState = "is";
    } else {
        snowState = "is not";
    }
    let dayState;
    if (daylight) {
        dayState = "is";
    } else {
        dayState = "is not";
    }
    let walkingWeather;
    if (walking) {
        walkingWeather = "It is walking weather!";
    } else {
        walkingWeather = "It is not walking weather.";
    }

    document.querySelector('.weather').innerHTML = 
            `<h3>${walkingWeather}</h3>
            <p>The current weather is ${weatherDescription}. 
            The current temperature is ${displayTemp} ${tempUnit}.
            It feels like ${displayFeels} ${tempUnit}.
            The humidity is currently ${humidity}%.
            The wind speed is ${displayWind} ${windUnit}.
            It is ${clouds}% cloudy.
            It ${rainState} raining.
            It ${snowState} snowing.
            It ${dayState} between sunrise and sunset.</p>
            `;

        if (!walking) {
            document.querySelector(".alternate").innerHTML = `
            <h4>Here are some alternate activities to try:</h4>
            <ul class="activities">
            </ul>
            `;
            for (const activity of activities) {
                document.querySelector(".activities").insertAdjacentHTML("beforeend", `<li>${activity}</li>`) 
            }
        } else {
            document.querySelector(".alternate").innerHTML = "";
        }
}

export default getWeather; 