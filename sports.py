from bs4 import BeautifulSoup
import requests
import urllib.parse

def SportsDisplay():
    google_url = "https://www.espn.com/nba/standings"
    response = requests.get(google_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())
    temp = soup.find('span' ,class_='stat-cell').text
    print(temp)
