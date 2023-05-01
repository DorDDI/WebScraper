from bs4 import BeautifulSoup
import requests
import urllib.parse
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playercareerstats
from PIL import Image
from io import BytesIO

def east_con():
    url = "https://www.espn.com/nba/standings"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table1 = soup.find('table', class_='Table Table--align-right')

    rows = table1.find_all('tr')

    # Extract data from the first cell of each row
    win = []
    lose = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            win.append(cells[0].text.strip())
        if cells:
            lose.append(cells[1].text.strip())
    print(win)
    print(lose)

    table1 = soup.find('table', class_='Table Table--align-right Table--fixed Table--fixed-left')
    rows = table1.find_all('tr')
    # Extract data from the first cell of each row
    names = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            names.append(cells[0].text.strip())

    new_string_list = []
    for string in names:
        index = string.find("--")
        if index != -1:
            modified_string = string[index + 2:]
            new_string_list.append(modified_string)
        else:
            new_string_list.append(string)

    new_strings = []

    for string in new_string_list:
        index = 0
        for char in string:
            if char.islower():
                break
            index += 1
        new_string = string[index - 1:]
        new_strings.append(new_string)
    print(new_strings)

def west_con():
    url = "https://www.espn.com/nba/standings"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    div = soup.find('div', class_ = "tabs__content")

    div = div.find_all('table')
    div1 = div[3]

    rows = div1.find_all('tr')

    # Extract data from the first cell of each row
    win = []
    lose = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            win.append(cells[0].text.strip())
        if cells:
            lose.append(cells[1].text.strip())
    print(win)
    print(lose)

    table = div[2]
    rows = table.find_all('tr')
    # Extract data from the first cell of each row
    names = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            names.append(cells[0].text.strip())

    new_string_list = []
    for string in names:
        index = string.find("--")
        if index != -1:
            modified_string = string[index + 2:]
            new_string_list.append(modified_string)
        else:
            new_string_list.append(string)

    new_strings = []

    for string in new_string_list:
        index = 0
        for char in string:
            if char.islower():
                break
            index += 1
        new_string = string[index - 1:]
        new_strings.append(new_string)
    print(new_strings)

def get_id_by_name(player_name):
    player = players.find_players_by_full_name(player_name)
    player_id = ""
    if player:
        player_id = player[0]["id"]
        return player_id
    else:
        return None


def image_show(url):
    # Send a GET request to download the image
    response = requests.get(url)

    # Open the image using PIL
    img = Image.open(BytesIO(response.content))

    # Display the image
    img.show()


def player_stats(player_name):
    player_id = get_id_by_name(player_name)
    while player_id == None :
        player_name = input("Player wasn't found, try again:")
        player_id = get_id_by_name(player_name)
    url = f"https://www.nba.com/stats/player/{player_id}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    points = soup.find('div', class_="PlayerSummary_summary__CGowU")
    points = points.find_all('div')



    avg_points = points[15].text
    avg_points = "".join([c for c in avg_points if not c.isalpha()])  #keep just numbers in the string
    avg_rebouns = points[17].text
    avg_rebouns = "".join([c for c in avg_rebouns if not c.isalpha()])  #keep just numbers in the string
    avg_assists = points[19].text
    avg_assists = "".join([c for c in avg_assists if not c.isalpha()])  #keep just numbers in the string
    stat_list = [f"Points per game {avg_points}", f"Rebouns per game {avg_rebouns}",f"Assists per game {avg_assists}"]
    for x in stat_list:
        print(x)

    #image show
    # Find the element with the desired class that contains the image source URL
    element_with_image_url = soup.find('img',
                                       class_='PlayerImage_image__wH_YX PlayerSummary_playerImage__sysif')
    # Extract the source URL of the image
    if element_with_image_url:
        img_src = element_with_image_url['src']

        image_show(img_src)
    else:
        print('Image not found with the specified class.')




def SportsDisplay():

    while(1):
        print('1. nba east conference \n2. nba east conference \n3. player statistics \n4. exit')
        section = int(input('Choose a section: '))
        if (section == 1):
            east_con()
        elif (section == 2):
            west_con()
        elif (section == 3):
            player_name = input("enter player name: ")
            player_stats(player_name)
        elif (section == 4):
            break


