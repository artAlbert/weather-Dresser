from datetime import datetime

def unixToDate(dt):
    """ dateTime(dt) -> String """
    """ Convert UNIX time to readable format """
    return datetime.utcfromtimestamp(dt).strftime("%A %B %d %Y %I:%M%p")

def toKmph(wind_speed):
    """ toKmph(wind_speed) -> int """
    """ Convert from meters/sec to kilometers/hour """
    return round(wind_speed*18/5)

def bfScale(wind_speed):
    """ bfScale(wind_speed) -> [] """
    """ Return Beaufort scale force, description for wind speeds given in kmph """
    if wind_speed < 1:
        return [0, "calm"]
    elif wind_speed >= 1 and wind_speed < 6:
        return [1, "very light - bends smoke"]
    elif wind_speed >= 6 and wind_speed < 12:
        return [2, "light breeze - felt on face"]
    elif wind_speed >= 12 and wind_speed < 20:
        return [3, "gentle breeze - shakes leaves"]
    elif wind_speed >= 20 and wind_speed < 29:
        return [4, "moderate breeze - lifts dust and papers"]
    elif wind_speed >= 29 and wind_speed < 39:
        return [5, "fresh breeze - shakes branches"]
    elif wind_speed >= 39 and wind_speed < 50:
        return [6, "strong breeze - shakes big branches"]
    elif wind_speed >= 50 and wind_speed < 62:
        return [7, "near gale - impedes walking"]
    elif wind_speed >= 62 and wind_speed < 75:
        return [8, "gale - shakes big trees"]
    elif wind_speed >= 75 and wind_speed < 89:
        return [9, "strong gale - removes shingles"]
    elif wind_speed >= 89 and wind_speed < 103:
        return [10, "storm - uproots trees"]
    elif wind_speed >= 103 and wind_speed < 118:
        return [11, "violent storm - serious devastation"]
    elif wind_speed >= 118:
        return [12, "hurricane - serious catastrophes"]
    else:
        return [-1, "Error: Couldn't match. wind_speed must be an int"]

def getClothing(currentWeather, dailyWeather, hourlyWeather):
    """ """
    """ """
    clothingSuggestion = []
    
    clothingRange = {

        # Keys represent bottom temperature bounds in Celsius. Values represent clothing suggestions.
        # temperature: [head, accessories, top, bottom, shoes]

        -30: ["warm hat", "earmuffs, scarf, gloves, base layers, thick socks", "winter jacket, warm sweater", "warm pants", "winter boots"],
        -20: ["warm hat", "earmuffs, gloves, thick socks", "winter jacket, warm sweater", "warm pants", "winter boots"],
        -10: ["warm hat", "earmuffs, gloves, thick socks", "winter jacket, warm sweater", "warm pants", "boots"],
        0: ["warm hat", "earmuffs, gloves", "winter jacket, warm sweater", "warm pants", "boots"],
        10: ["light hat", "","light jacket, sweater", "pants", "sneakers, light boots"],
        20: ["hat", "", "t-shirt, light sweater", "shorts, dress", "light shoes"],
        30: ["hat", "", "t-shirt", "shorts, sundress", "light shoes"],
    }

    temp = int(currentWeather["feels_like"])

    # Round temperature to nearest lower bound. Get clothing suggestions from clothingRange dict. 
    # Account for out-of-bounds ranges

    clothingRangeKey = temp // 10 * 10
    if clothingRangeKey <= -30:
        clothingSuggestion = clothingRange[-30] 
    elif clothingRangeKey >= 30:
        clothingSuggestion = clothingRange[30]
    else:
        clothingSuggestion = clothingRange[clothingRangeKey]


    return clothingSuggestion




