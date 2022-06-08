# [Weather Dresser](https://weather-dresser.herokuapp.com/)

A simple web app that tells you how to dress for the weather. Created with Django and hosted on Heroku. 

  This is a project I made for my girlfriend. She has a hard time figuring out what to wear based on temperature alone
so she asked me to create a more descriptive weather app for her that can make personal clothing suggestions.

  There aren't any fancy machine learning algorithms or AI processes making conclusions behind the scenes. 
She usually just asks me what the weather will be like and I tell her if she needs a jacket or not. I translated this into some code.


## Getting Started:

  Before I started coding this thing, we discussed what the application should look like in terms of functionality. I asked some HCI-style questions to identify what kinds of data she considers, how she makes her decisions, and which datapoints she struggles with when making inferences. This lead to establishing some requirements for the application.

  The requirements were:
1. display what the weather is like currently and what it will be like later. Include: low/high temperatures for morning, day, evening, night; sunrise, sunset times; humidity; UV index; wind speeds; chance of rain.

2. supplement weather conditions with qualitative information. Include: physical effects descriptions of the weather conditions.

3. recommend appropriate styles of dress.

  It also had to be mobile responsive since that would be the primary method of viewing. We went through some mockups online and picked out a layout. I had creative control over the look of the desktop UI since that wasn't a priority.


## How It Works:
	
The user enters the city they're searching for into an input form and the application makes two api calls: one call to get the latitiude and longitude coordinates for the searched city, and one call to get weather data for those coordinates. I used OpenWeatherMap's API to translate the city name into coordinates and to source the weather data. If the input is blank, or the API returns nothing for the city input, an error message tells the user to check their input and try again. 

Information like current conditions, sunrise/sunset times, temperatures throughout the day, humidity, uv, chance of rain, and wind speed is extracted from the response and displayed back to the user. 

To help the user better understand some of these conditions I wrote helper functions that qualified the data: UVI numbers were translated into radiation levels and sunblock protection suggestions, temperatures were translated into humidex range levels, the dew point was translated into moisture comfort levels, and the wind speed was translated into effects on the Beaufort wind scale. 

The clothing suggestions are based on preset temperature ranges. Current temperatures and weather conditions determine the recommended articles.
 

## Thoughts:

  Determining how to translate getting dressed into code was an interesting challenge. I brain-stormed starting with a 'base case' of clothing articles and building it up or down. I considered decision trees where the root would be something neutral like a hoodie with pants and running shoes, and then the outfit would be dressed up or down to appropriately reflect the temperature and weather conditions. You would add an umbrella if its raining, a wind breaker if its windy, a warm hat and a proper winter jacket if its snowing, or remove the hoodie and replace the pants if its too hot, and so on. But all of this became too complicated too quickly. There were a lot of variables and a lot of clothes. How do you determine a 'neutral' base-case temperature anyways? So I thought it would be better if I made generalizations. I limited the clothing combinations to the basics and the temperature ranges to general seasonal ranges. Heavy winter clothing for average winter temperatures, lighter clothing for the fall, and the lightest clothing for the summers.

  The design of the mobile UI was hard-set and I ended up following a mockup made by Damian Martelli. Since I had free reign over the layout of the desktop version I chose to implement another layout, which was based on a mockup by Hassanur Rakib on dribbble, for more HTML experience.

  I chose Heroku for hosting because it was free, easy to set up, and you could choose your own subdomain. It also updates the live project as the github repo changes, so that was nice. I had some issues with getting the right dependencies for Heroku going - the django buildpack module was deprecated so I had to use forks. I also ran into some trouble getting the format of the procfile right, along with some Django network settings. This was mostly resolved through trial and error working through error messages.  


## Improvements and Scaling:
	
  After some feedback it seems like the code for clothing recommendations is too general. A better solution would be to let users alter the temperature ranges themselves and provide their own clothing combinations for those ranges. Since theres only one user, all we need to do is add a form that saves the range and outfit input. To scale it for other users, the app would need authentication and a database to store users and user preferences. This would make it more personal as everyone experiences temperature differently, and their recommendations would be based on clothing that they own. 
