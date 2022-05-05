from django.shortcuts import render
from .forms import CityForm
from django.template import RequestContext
from django.contrib import messages

import requests
import math
import weatherDresserApp.helpers

def index(request):
    # OpenWeatherMap URLs. 
    # Calls to weatherURL require GPS coordinates so we call locationURL first.
    apiKey = "09b624c0aba9297fd6cf6349c21a8018" 
    locationURL = "https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={apiId}"
    weatherURL = " https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&excludes=minutely&appid={apiId}"
    
    # Initialize structures for context data.
    # Note: When rendering the template, Django doesn't throw 'undefined variable' errors if context is empty.
    # This can all be initialized and defined in the try block without being repeated up here,
    # but that's probably bad practice.
    searchForm = CityForm()
    weather = {
        "city" :        "",
        "country" :     "",
        "temperature" : "",
        "feel" :        "",
        "description" : "",
        "humidity" :    "",
        "pop" :         "",
        "pressure" :    "",
        "wind_speed" :  "",
        "bfScaleDesc" :     "",
        "icon" :        "",
    }
    time = {
        "dayOfWeek" :   "",
        "month" :       "",
        "day" :         "",
        "year" :        "",
        "time" :        "",
    }
    clothes = {
        "title" :       "",
        "head":         "",
        "accessories":  "",
        "top":          "",
        "bottom":       "",
        "shoes":        "",
    }
    
    # City search.
    if request.method == "POST":
        searchForm = CityForm(request.method)       
        city = request.POST["city"]
        
        try:
            # Call to get GPS coordinates for the queried city.
            locationResponse = requests.get(locationURL.format(city=city, apiId=apiKey)).json()[0]

            # Call to get weather (current, hourly, daily forecasts) at coordinates. Convert to JSON.
            weatherResponse = requests.get(weatherURL.format(lat=locationResponse["lat"], lon=locationResponse["lon"], apiId=apiKey)).json()
            
            # Split up JSON response into appropriate structures. 
            # Catch cases where API responds with an empty list.
            currentWeather = weatherResponse["current"]
            dailyWeather = weatherResponse["daily"]
            hourlyWeather = weatherResponse["hourly"]
            timezone = weatherResponse["timezone_offset"]
            
        # Catch errors raised by API
        except (IndexError, KeyError) as error:      
                # Display an error message if the OWM API doesn't return anything.
                messages.info(request, 'City not found! Please check your spelling and try again.')
            
        else:
            # Gather weather and location data for display.
            weather["city"] =        locationResponse["name"]
            weather["country"] =     locationResponse["country"]
            weather["temperature"] = str(round(int(currentWeather["temp"])))  + "°C "
            weather["feel"] =        "Feels like: " + str(round(int(currentWeather["feels_like"]))) + "°C"
            weather["description"] = currentWeather["weather"][0]["description"]
            weather["humidity"] =    "Humidity: " + str(round(int(currentWeather["humidity"]))) + "%"
            weather["pop"] =         "Chance of Rain: " + str(round(int(hourlyWeather[0]["pop"]*100))) + "%"
            weather["pressure"] =    "Air Pressure: " + str(round(int(currentWeather["pressure"]))) + " hPa"
            weather["wind_speed"] =  "Wind Speed: " + str(weatherDresserApp.helpers.toKmph(hourlyWeather[0]["wind_speed"])) + " km/h"
            weather["bfScaleDesc"] =  weatherDresserApp.helpers.bfScale(weatherDresserApp.helpers.toKmph(hourlyWeather[0]["wind_speed"]))[1]
            weather["icon"] =        "http://openweathermap.org/img/wn/" + currentWeather["weather"][0]["icon"] + "@2x.png"
            weather["high"] =         "High: " + str(round(int(dailyWeather[0]["temp"]["max"]))) + "°C"
            weather["low"] =          "Low: " + str(round(int(dailyWeather[0]["temp"]["min"]))) + "°C"

            # Convert unix dt to a friendlier format. 
            weatherDate = weatherDresserApp.helpers.unixToDate(currentWeather["dt"] + timezone)
            # Split date components into a list for formatting. List = [weekday, month, day#, year, hh:mmAM/PM] 
            weatherDate = weatherDate.split()

            # Gather date and time for display. 
            time["dayOfWeek"] =   weatherDate[0]
            time["month"] =       weatherDate[1]
            time["day"] =         weatherDate[2]
            time["year"] =        weatherDate[3]
            time["time"] =        weatherDate[4].lstrip('0')

            # Get clothing suggestions.
            clothingSuggestion = weatherDresserApp.helpers.getClothing(currentWeather, dailyWeather, hourlyWeather)

            # Gather articles.
            clothes["title"] =       "Clothing"
            clothes["head"] =        clothingSuggestion[0]
            clothes["accessories"] = clothingSuggestion[1]
            clothes["top"] =         clothingSuggestion[2]
            clothes["bottom"] =      clothingSuggestion[3]
            clothes["shoes"] =       clothingSuggestion[4]
    
    # Group data for template use.
    context = { 
        "form" :    searchForm,
        "weather" : weather,
        "time" :    time,
        "clothes":  clothes,
    }

    # Render
    return render(request, 'weatherDresserApp/index.html', context)