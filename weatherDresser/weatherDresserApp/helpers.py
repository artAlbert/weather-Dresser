from datetime import datetime

def unixToDate(dt):
    """ dateTime(dt) -> '' """
    """ Convert UNIX time to date time"""
    return datetime.utcfromtimestamp(dt).strftime("%A %B %d %Y %I:%M%p")

def toKmph(wind_speed):
    """ toKmph(wind_speed) -> integer """
    """ Convert from meters/sec to kilometers/hour"""
    return round(wind_speed*18/5)

def bfScale(wind_speed):
    """ bfScale(wind_speed) -> [] """
    """ Return Beaufort scale force, description for wind speeds given in kmph """
    match wind_speed:
        case 0 if wind_speed < 1:
            return 0, "calm", ""
        case 1 if 1 <= wind_speed < 6:
            return 1, "very light", "bends smoke"
        case 2 if 6 <= wind_speed < 12:
            return 2, "light breeze", "felt on face"
        case 3 if 12 <= wind_speed < 20:
            return 3, "gentle breeze", "shakes leaves"
        case 4 if 20 <= wind_speed < 29:
            return 4, "moderate breeze", "lifts dust and papers"
        case 5 if 29 <= wind_speed < 39:
            return 5, "fresh breeze", "shakes branches"
        case 6 if 39 <= wind_speed < 50:
            return 6, "strong breeze", "shakes big branches"
        case 7 if 50 <= wind_speed < 62:
            return 7, "near gale", "impedes walking"
        case 8 if 62 <= wind_speed < 75:
            return 8, "gale", "shakes big trees"
        case 9 if 75 <= wind_speed < 89:
            return 9, "strong gale", "removes shingles"
        case 10 if 89 <= wind_speed < 103:
            return 10, "storm", "uproots trees"
        case 11 if 103 <= wind_speed < 118:
            return 11, "violent storm", "serious devastation"
        case 12 if wind_speed >= 118:
            return 12, "hurricane", "serious catastrophes"
        case _:
            return -1, "Error: wind_speed must be an int", ""

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




