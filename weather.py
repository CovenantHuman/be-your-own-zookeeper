import requests
import os

OPEN_WEATHER_KEY = os.environ["OPEN_WEATHER_KEY"]

def convert_kelvin_to_celsius(kelvin):
    return round(kelvin-273.15)

def convert_kelvin_to_fahrenheit(kelvin):
    return round(((kelvin-273.15)*(9/5))+32)

def convert_meters_per_second_to_miles_an_hour(meters_per_second):
    return round(meters_per_second*2.237)

def get_walking_weather(zipcode, user):
    """Takes in a user and returns whether the current weather is fit for walking for them."""
    zip_with_country_code = zipcode + ",us"
    url = "https://api.openweathermap.org/data/2.5/weather"
    payload = {"zip": zip_with_country_code, "appid": OPEN_WEATHER_KEY}
    response = requests.get(url, params=payload)
    data = response.json()

    temp_in_kelvin = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_in_metric = data['wind']['speed']
    clouds = data['clouds']['all']
    rain = data.get('rain', False)
    snow = data.get('snow', False)
    now = data['dt']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    description = data['weather'][0]['description']
    real_temp_in_kelvin = data['main']['temp']
    
    is_imperial = user.is_imperial
    is_fahrenheit = user.is_fahrenheit
    max_temp = user.max_temp
    min_temp = user.min_temp
    max_hum = user.max_hum
    max_wind_speed = user.max_wind_speed
    max_clouds = user.max_clouds
    min_clouds = user.min_clouds
    user_rain = user.rain
    user_snow = user.snow
    user_daylight = user.daylight
    user_night = user.night
    activities = user.activities
    activity_names = []
    for activity in activities:
        activity_names.append(activity.name)

    if is_fahrenheit:
        feels_like = convert_kelvin_to_fahrenheit(temp_in_kelvin)
        real_temp = convert_kelvin_to_fahrenheit(real_temp_in_kelvin)
    else:
        feels_like = convert_kelvin_to_celsius(temp_in_kelvin)
        real_temp = convert_kelvin_to_fahrenheit(real_temp_in_kelvin)

    wind_in_imperial = convert_meters_per_second_to_miles_an_hour(wind_in_metric)

    wind_speed_lookup = {0: 0, 1: 3, 2: 7, 3: 12, 4: 18, 5: 24, 6: 31, 7: 38}

    wind = wind_speed_lookup[max_wind_speed]

    if user_rain == True:
        rain_filter = True
    else:
        if rain == False:
            rain_filter = True
        else:
            rain_filter = False

    if user_snow == True:
        snow_filter = True
    else:
        if snow == False:
            snow_filter = True
        else:
            snow_filter = False
            
    if (now >= sunrise) and (now <= sunset):
        daylight = True
    else:
        daylight = False
    
    if ((max_temp >= feels_like) and (min_temp <= feels_like) and (max_hum >= humidity) and 
    (wind >= wind_in_imperial) and (max_clouds >= clouds) and (min_clouds <= clouds) and 
    (rain_filter) and (snow_filter)):
        walking = ((user_daylight == daylight) or (user_night != daylight))
    else:
        walking = False

    if is_imperial:
        display_wind = wind_in_imperial
    else:
        display_wind = wind_in_metric

    return {"walking": walking,
            "description": description, 
            "real_temp": real_temp, 
            "feels_like": feels_like, 
            "is_fahrenheit": is_fahrenheit, 
            "humidity": humidity, 
            "display_wind": display_wind, 
            "is_imperial": is_imperial, 
            "clouds": clouds, 
            "rain": rain, 
            "snow": snow, 
            "daylight": daylight,
            "activities": activity_names}
