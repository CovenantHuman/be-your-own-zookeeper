'use strict';

function convertKelvinToCelsius(kelvin) {
    return Math.round(kelvin - 273.15);
}

function convertKelvinToFahrenheit(kelvin) {
    return Math.round(((kelvin - 273.15)*(9/5)) + 32);
}

function convertMetersPerSecondToMilesAnHour(metersPerSecond) {
    return Math.round(metersPerSecond*2.237);
}

function isWalkingWeather(temp, wind, rain, snow, daylight) {
     if ((60 < temp) && ( temp < 80) && (wind < 18) && (rain !== "is") && 
     (snow !== "is") && (daylight === "is")) {
        return "It is walking weather!";
    } else {
        return "It is not walking weather."
    }
}

const weatherForm = document.querySelector('.get-weather');

weatherForm.addEventListener('submit', (evt) => {
  evt.preventDefault();

  const zipcode = document.querySelector('#zipcode-field').value;
  const queryString = new URLSearchParams(
    {zipcode : zipcode}).toString();

  fetch(`/zip-form?${queryString}`)
  .then(response => response.json())
  .then(serverData => {
    const weatherTitle = serverData.weather[0].main;
    const currentTemp = serverData.main.temp;
    const currentTempC = convertKelvinToCelsius(currentTemp);
    const currentTempF = convertKelvinToFahrenheit(currentTemp);
    const feelsLike = serverData.main.feels_like;
    const feelsLikeC = convertKelvinToCelsius(feelsLike);
    const feelsLikeF = convertKelvinToFahrenheit(feelsLike);
    const humidity = serverData.main.humidity;
    const wind = serverData.wind.speed;
    const imperialWind = convertMetersPerSecondToMilesAnHour(wind);
    const clouds = serverData.clouds.all;
    const isRaining = () => {
        if (serverData.rain){
            return "is";
        } else {
            return "is not";
        }
    }
    const isSnowing = () => {
        if (serverData.snow){
            return "is";
        } else {
            return "is not";
        }
    }
    const isDaylight = () => {
        if((serverData.sys.sunrise < serverData.dt) && ( serverData.dt < serverData.sys.sunset)) {
            return "is";
        } else {
            return "is not";
        }
    }

    const walking = isWalkingWeather(feelsLikeF, wind, isRaining(), isSnowing(), isDaylight());

    document.querySelector('.weather').innerHTML = 
        `<h3>${walking}</h3>
        <p>The current weather is: ${weatherTitle}. </p>
        <p>The current temperature is ${currentTempC}
        degrees celsius or ${currentTempF} degrees fahrenheit. </p>
        <p>It feels like ${feelsLikeC} degrees celsius or ${feelsLikeF}
        degrees fahrenheit.</p> 
        <p>The humidity is currently ${humidity}%.</p>
        <p>The wind speed is ${wind} meters/second or ${imperialWind}
        miles/hour.</p>
        <p>It is ${clouds}% cloudy.</p>
        <p>It ${isRaining()} raining.</p>
        <p>It ${isSnowing()} snowing.</p>
        <p>It ${isDaylight()} between sunrise and sunset.</p>
        `;

    if (walking === "It is not walking weather.") {
        document.querySelector(".alternate").innerHTML = `
        <h4>Here are some alternate activities to try:</h4>
        <ul>
            <li>Yoga</li>
            <li>Jumping Jacks</li>
            <li>Sit Ups</li>
            <li>Private Dance Party</li>
            <li>Push Ups</li>
        </ul>
        `;
    } else {
        document.querySelector(".alternate").innerHTML = "";
    }
  });
});
