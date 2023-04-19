
from weather import Weather
from sports import SportsDisplay
from movies import Movie
from flight import FlightDisplay

# menu style

while 1:
    print('1. movie section \n2. weather section \n3. flight section \n4. sport section \n8. exit')
    section = input('Choose a section: ')
    while not section.isnumeric():
        section = input('Wrong input, please try again: ')
    section = int(section)
    if section == 1:
        print("")
        movie = Movie()
        movie.movie_display()
    elif section == 2:
        weather = Weather()
        weather.weather_display()
    elif section == 3:
        FlightDisplay()
    elif section == 4:
        SportsDisplay()
    elif section == 8:
        break
    print("\n")
