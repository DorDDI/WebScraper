from bs4 import BeautifulSoup
import requests
import urllib.parse
from weather import WeatherDisplay

# menu style

while(1):
    print('1. movie section \n2. weather section \n3. flight section \n4. sport section \n8. exit')
    section = int(input('Choose a section: '))
    if (section == 1):
        pass
    elif (section == 2):
        WeatherDisplay()
    elif (section == 3):
        pass
    elif (section == 4):
        pass
    elif (section == 8):
        break



