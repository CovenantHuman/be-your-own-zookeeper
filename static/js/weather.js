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

function isWalkingWeatherImproved(user, tempInKelvin, humidity, windInMetric, clouds, rain, snow, daylight) {
    let temp;

    if (user.is_fahrenheit) {
        temp = convertKelvinToFahrenheit(tempInKelvin);
    } else {
        temp = convertKelvinToCelsius(tempInKelvin);
    }

    let wind;

    if (user.is_imperial) {
        wind = convertMetersPerSecondToMilesAnHour(windInMetric);
    } else {
        wind = windInMetric;
    }

    if ((user.max_temp >= temp) && 
        (user.min_temp <= temp) &&
        (user.max_hum >= humidity) &&
        (user.max_wind_speed >= wind) &&
        (user.max_clouds >= clouds) &&
        (user.min_clouds <= clouds) &&
        (user.rain === rain) &&
        (user.snow === snow)) {
            return ((user.daylight === daylight) || (user.night !== daylight));
        } else {
            return false;
        }
}

function improvedGetWeather(zipcode) {
    const queryString = new URLSearchParams(
        {zipcode : zipcode}).toString();

    fetch(`/zip-form?${queryString}`)
    .then(response => response.json())
    .then(serverData => {
        const weatherDescription = serverData.weather[0].description;
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
                return true;
            } else {
                return false;
            }
        }
        const isSnowing = () => {
            if (serverData.snow){
                return true;
            } else {
                return false;
            }
        }
        const isDaylight = () => {
            return ((serverData.sys.sunrise < serverData.dt) && ( serverData.dt < serverData.sys.sunset)) 
        }
        
        fetch(`/api/user`)
        .then(response => response.json())
        .then(userData => {

            const walking = isWalkingWeatherImproved(userData, feelsLike, humidity, wind, clouds, isRaining(), isSnowing(), isDaylight());
            displayWeather(walking, weatherDescription, currentTempC, currentTempF, feelsLikeC, feelsLikeF, humidity, wind, imperialWind, clouds, isRaining(), isSnowing(), isDaylight());
        });
    });
}

function displayWeather(walking, weatherDescription, currentTempC, currentTempF, feelsLikeC, feelsLikeF, humidity, wind, imperialWind, clouds, rain, snow, daylight){
    let rainState;
    if (rain) {
        rainState = "is"
    } else {
        rainState = "is not"
    }
    let snowState;
    if (snow) {
        snowState = "is"
    } else {
        snowState = "is not"
    }
    let dayState;
    if (daylight) {
        dayState = "is"
    } else {
        dayState = "is not"
    }
    let walkingWeather
    if (walking) {
        walkingWeather = "It is walking weather!"
    } else {
        walkingWeather = "It is not walking weather."
    }

    document.querySelector('.weather').innerHTML = 
            `<h3>${walkingWeather}</h3>
            <p>The current weather is ${weatherDescription}. </p>
            <p>The current temperature is ${currentTempC}
            degrees celsius or ${currentTempF} degrees fahrenheit. </p>
            <p>It feels like ${feelsLikeC} degrees celsius or ${feelsLikeF}
            degrees fahrenheit.</p> 
            <p>The humidity is currently ${humidity}%.</p>
            <p>The wind speed is ${wind} meters/second or ${imperialWind}
            miles/hour.</p>
            <p>It is ${clouds}% cloudy.</p>
            <p>It ${rainState} raining.</p>
            <p>It ${snowState} snowing.</p>
            <p>It ${dayState} between sunrise and sunset.</p>
            `;

        if (!walking) {
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
}

export default improvedGetWeather; 