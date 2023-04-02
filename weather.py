from bs4 import BeautifulSoup
import requests
import urllib.parse

def WeatherDisplay():
    # Take input from the user
    input_string = input("Enter a string: ")

    # Encode the input string for URL
    encoded_input = urllib.parse.quote_plus(input_string)

    # Construct the Google search URL
    google_url = f"https://www.google.com/search?q={encoded_input}+weather"

    result = requests.get(google_url)
    content = result.text

    soup = BeautifulSoup(content, 'html.parser')
    #print(soup.prettify())
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    #a = soup.find('article', class_='main-article')
    #print (soup.prettify())
    #title = soup.find('div', class_='wob_loc q8U8x').get_text()
    #ss = soup.find('span',class_='wob_t q8U8x').get_text(strip= True, separator=' ')
    #number = round(((int(ss[0:2])-32)/1.8))



    print("Temperature is", temp)
    print("Time: ", time)
    print("Sky Description: ", sky)

    #print(f'{number}{ss[-1]} in celsius')

WeatherDisplay()