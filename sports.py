from bs4 import BeautifulSoup
import requests
import urllib.parse


def SportsDisplay():
    url = "https://www.espn.com/nba/standings"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table1 = soup.find('table',class_ = 'Table Table--align-right')

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
        new_string = string[index-1:]
        new_strings.append(new_string)
    print(new_strings)
