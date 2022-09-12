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
        if( serverData.sys.sunrise < serverData.dt < serverData.sys.sunset) {
            return "is";
        } else {
            return "is not";
        }
    }

    document.querySelector('.weather').innerHTML = 
        `<p>The current weather is: ${weatherTitle}. </p>
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
  });
});
