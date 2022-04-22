from django.shortcuts import render
from .forms import CityForm
from django.template import RequestContext

import requests
import math
import weatherDresserApp.helpers



def index(request):
    apiKey = "09b624c0aba9297fd6cf6349c21a8018" 
    locationURL = "https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={apiId}"
    weatherURL = " https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&excludes=minutely&appid={apiId}"

    cityDefault = "Toronto"
    locationResponse = requests.get(locationURL.format(city=cityDefault, apiId=apiKey)).json()[0]
    searchForm = CityForm()
    
    if request.method == "POST":
        searchForm = CityForm(request.method)       
        city = request.POST["city"]
        if city:    
            try:
                locationResponse = requests.get(locationURL.format(city=city, apiId=apiKey)).json()[0]
            except IndexError:

               pass 
        else:
            locationResponse = requests.get(locationURL.format(city=cityDefault, apiId=apiKey)).json()[0]
            searchForm = CityForm() 
    
    weatherResponse = requests.get(weatherURL.format(lat=locationResponse["lat"], lon=locationResponse["lon"], apiId=apiKey)).json()

    currentWeather = weatherResponse["current"]
    dailyWeather = weatherResponse["daily"]
    hourlyWeather = weatherResponse["hourly"]
    timezone = weatherResponse["timezone_offset"]

    # Convert unix dt to a readable format. 
    weatherDate = weatherDresserApp.helpers.unixToDate(currentWeather["dt"] + timezone)
    # Split date components into 
    weatherDate = weatherDate.split()

    # Get clothing suggestions.
    clothingSuggestion = weatherDresserApp.helpers.getClothing(currentWeather, dailyWeather, hourlyWeather)

    weather = {
        "city" :        locationResponse["name"],
        "country" :     locationResponse["country"],
        "temperature" : str(round(int(currentWeather["temp"]))),
        "feel" :        str(round(int(currentWeather["feels_like"]))),
        "description" : currentWeather["weather"][0]["description"],
        "humidity" :    str(round(int(currentWeather["humidity"]))),
        "pop" :         str(round(int(hourlyWeather[0]["pop"]*100))),
        "pressure" :    str(round(int(currentWeather["pressure"]))),
        "wind_speed" :  weatherDresserApp.helpers.toKmph(hourlyWeather[0]["wind_speed"]),
        "icon" :        "http://openweathermap.org/img/wn/" + currentWeather["weather"][0]["icon"] + "@2x.png",

    }

    time = {
        "dayOfWeek" :   weatherDate[0],
        "month" :       weatherDate[1],
        "day" :         weatherDate[2],
        "year" :        weatherDate[3],
        "time" :        weatherDate[4].lstrip('0'),

    }

    clothes = {
        "head": clothingSuggestion[0],
        "accessories": clothingSuggestion[1],
        "top": clothingSuggestion[2],
        "bottom": clothingSuggestion[3],
        "shoes": clothingSuggestion[4],
    }

    context = { 
        "weather" : weather,
        "form" :    searchForm,
        "time" :    time,
        "clothes":  clothes,

    }

    return render(request, 'weatherDresserApp/index.html', context)
