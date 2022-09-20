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

function isWalkingWeather(user, 
                                  tempInKelvin, 
                                  humidity, 
                                  windInMetric, 
                                  clouds, 
                                  rain, 
                                  snow, 
                                  daylight) {
    let temp;

    if (user.is_fahrenheit) {
        temp = convertKelvinToFahrenheit(tempInKelvin);
    } else {
        temp = convertKelvinToCelsius(tempInKelvin);
    }

    let wind;
    wind = convertMetersPerSecondToMilesAnHour(windInMetric);

    const windSpeedLookup = {0: 0, 1: 3, 2: 7, 3: 12, 4: 18, 5: 24, 6: 31, 7: 38};
    let maxWindSpeed;

    maxWindSpeed = windSpeedLookup[user.max_wind_speed];

    let rainFilter; 

    if (user.rain === true) {
        rainFilter = true;
    } else {
        if (rain === false) {
            rainFilter = true;
        } else {
            rainFilter = false;
        }
    }

    let snowFilter; 

    if (user.snow === true) {
        snowFilter = true;
    } else {
        if (snow === false) {
            snowFilter = true;
        } else {
            snowFilter = false;
        }
    }

    if ((user.max_temp >= temp) && 
        (user.min_temp <= temp) &&
        (user.max_hum >= humidity) &&
        (maxWindSpeed >= wind) &&
        (user.max_clouds >= clouds) &&
        (user.min_clouds <= clouds) &&
        (rainFilter) &&
        (snowFilter)) {
            return ((user.daylight === daylight) || (user.night !== daylight));
        } else {
            return false;
        }
}

function getWeather(zipcode) {
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
            return ((serverData.sys.sunrise < serverData.dt) && ( serverData.dt < serverData.sys.sunset));
        }
        
        fetch(`/api/user`)
        .then(response => response.json())
        .then(userData => {

            const walking = isWalkingWeather(userData, 
                                                    feelsLike, 
                                                    humidity, 
                                                    wind, 
                                                    clouds, 
                                                    isRaining(), 
                                                    isSnowing(), 
                                                    isDaylight());
                                                    
            let displayTemp;
            let displayFeels;
            let displayWind;
            if (userData.is_fahrenheit === true) {
                displayTemp = currentTempF;
                displayFeels = feelsLikeF;
            } else {
                displayTemp = currentTempC;
                displayFeels = feelsLikeC;
            }
            if(userData.is_imperial === true) {
                displayWind = imperialWind;
            } else {
                displayWind = wind;
            }
            displayWeather(walking, 
                           weatherDescription, 
                           displayTemp,
                           displayFeels,
                           userData.is_fahrenheit, 
                           humidity, 
                           displayWind, 
                           userData.is_imperial,
                           clouds, 
                           isRaining(), 
                           isSnowing(), 
                           isDaylight());
        }).catch(() => {
            document.querySelector('.weather').innerHTML = "Problem getting user information.";
        });
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
                        daylight){

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
            <p>The current weather is ${weatherDescription}. </p>
            <p>The current temperature is ${displayTemp} ${tempUnit}.</p>
            <p>It feels like ${displayFeels} ${tempUnit}.</p> 
            <p>The humidity is currently ${humidity}%.</p>
            <p>The wind speed is ${displayWind} ${windUnit}.</p>
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

export default getWeather; 