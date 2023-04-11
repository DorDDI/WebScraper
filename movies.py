from bs4 import BeautifulSoup
import json
import requests
import urllib.parse
from PyMovieDb import IMDB
from requests_html import HTMLSession

"""
def __init__(self):
    self.session = HTMLSession()
    self.headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Referer": "https://www.imdb.com/"
    }
    self.baseURL = "https://www.imdb.com"
    self.search_results = {'result_count': 0, 'results': []}
    self.NA = json.dumps({"status": 404, "message": "No Result Found!", 'result_count': 0, 'results': []})

"""

session = HTMLSession()
headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Referer": "https://www.imdb.com/"
    }
baseURL = "https://www.imdb.com"
search_results = {'result_count': 0, 'results': []}
NA = json.dumps({"status": 404, "message": "No Result Found!", 'result_count': 0, 'results': []})


def MovieDisplay():
    imdb = IMDB()
    genreArr = ["All", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama",
                "Family", "Fantasy", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "News",
                "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"]

    while (1):

        print('Movie Menu\n~~~~~~~~~~~~~~~\n1. search movie/tv by name \n2. search actor \n3. get the popular movies in spesific genre')
        print('4. returns top 50 popular TV Series \n5. upcoming movies from imdb \n6. return')
        options = int(input('what do you want to do:'))

        if (options == 1):
            # search movie / seria name from imdb
            name = input('enter movie / tv name: ')
            res = imdb.search(name)

            a = res.split('{\n  "result_count":')[1].split('\n  "results":')
            numberofoptions = int(a[0][1])
            if numberofoptions == 0:
                print("no movies or serias found")
                continue
            a = a[1].split('{')[1:numberofoptions+1]

            for i in range(numberofoptions):
                a[i] = a[i].split('\n')[1:5]
                for j in range(4):
                    b = ""
                    for leter in a[i][j]:
                        if (leter !=",") and (leter!= "\""):
                            b = b+leter
                    a[i][j] = b.replace("     ","").replace("name: ","").replace("id: ","").replace("url: ","").replace("poster: ","")
            print("choose option")
            count = 1
            for optionsMovie in a:
                print(f"{count}. {optionsMovie[1]}")
                count = count + 1
            choose = int(input())

            res = imdb.get_by_id(a[choose-1][0][1:])

            type = res.split("\"type\":")[1].split("\n")[0].replace("\"", "").replace(" ", "").replace(",", "")

            if (type == "Movie"):
                MovieOption(res)
            else:
                TVOption(res)


        elif(options == 2):
            # search person from imdb
            name = 'Leonardo dicaprio'
            res= imdb.search( name, year=None, tv=False, person=True)


            pass

        elif(options == 3):
            # returns top 50 popular movies starting from start id

            count = 1
            print("choose genere by number:\n")
            for i in range(len(genreArr)):
                print(f"{count}. {genreArr[count - 1]}")
                count = count + 1
            chooseGenre = int(input())

            genreArr[0] = "None"
            res = imdb.popular_movies(genre=genreArr[chooseGenre-1], start_id=1, sort_by=None)
            genreArr[0] = "All"
            pass

        elif (options == 4):
            # returns top 50 popular TV Series starting from start id
            print("choose genere by number:\n")
            count = 1
            for i in range(len(genreArr)):
                print(f"{count}. {genreArr[count - 1]}")
                count = count + 1
            chooseGenre = int(input())
            genreArr[0] = "None"
            res = imdb.popular_tv(genre=genreArr[chooseGenre-1], start_id=1, sort_by=None)
            genreArr[0] = "All"
            pass


        elif (options == 5):
            # upcoming movies from imdb
            number = int(input("enter number of upcoming movies: "))
            upcoming('US',number)
            pass

        else:
            break

def upcoming(region=None,movienumber = 20):
    """
     @description:- Helps to get upcoming movies/tv-series.
     @parameter-1:- <str:region> OPTIONAL, country code (like US, IN etc.) to filter results by region/country.
     @returns:- upcoming movies/TV-Series info as JSON string.
    """
    numberOfMovies = 1
    if region is not None:
        assert isinstance(region, str)
        url = f"https://www.imdb.com/calendar?region={region}"
    else:
        url = "https://www.imdb.com/calendar"

    try:
        response = session.get(url)
    except requests.exceptions.ConnectionError as e:
        response = session.get(url, verify=False)

    div = response.html.xpath("//section[@class='ipc-page-section ipc-page-section--base']")[0]

    articles = div.html.split('<article')[1:]
    for article in articles:
        if (numberOfMovies > movienumber):
            break
        title = article.split('ipc-title__text')[1].split('</h3>')[0][2:]
        print (title)
        movies = article.split('<li class="ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 bpqYIE"')[1:]
        for movie in movies:
            name = movie.split('<a class="ipc-metadata-list-summary-item__t" role="button" tabindex="0" aria-disabled="false" href="')[1].split('>')[1].split('<')[0]
            detail = movie.split('<ul class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base" role="presentation">')
            if (len(detail) == 1):
                genre = "TBD"
                actors = "TBD"
            else:
                detail = detail[1]
                detail = detail.split('class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base" role="presentation"><li role="presentation" class="ipc-inline-list__item"><span ')
                genre = detail[0].split('aria-disabled="false">')[1:]
                actors = detail[1].split('</span></li></ul></div></div><div')[0].split('aria-disabled="false">')[1:]
                for i in range (len(genre)):
                    genre[i]=genre[i].split('<')[0]
                for i in range (len(actors)):
                    actors[i] = actors[i].split('<')[0]
            print(f"{name}, {actors}, {genre}")
            numberOfMovies = numberOfMovies+1
            if (numberOfMovies>movienumber):
                break

        pass

    h4 = div.find('h4')
    ul = div.find('ul')
    data = zip(h4, ul)
    output = []
    for zip_el in data:
        rel_date = zip_el[0].text
        ulist = zip_el[1].find('a')
        for movie in ulist:
            output.append({
                'id': movie.attrs['href'].split('/')[2],
                'name': movie.text,
                'url': baseURL + movie.attrs['href'],
                'release_data': rel_date
            })
    results = {'result_count': len(output), 'results': output}
    if results['result_count'] > 0:
        return json.dumps(results, indent=2)
    else:
        return NA

def MovieOption(res):
    movieName = res.split("\"name\":")[1].split(",\n")[0].replace("\"", "")[1:].replace("null", "TBD")
    movieTime = res.split("\"duration\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "").replace("null", "TBD").replace("PT", "").replace("H", " Hours and ").replace("M", " Minutes")
    movieactors = res.split("\"actor\":")[1].split("],\n")[0].split("\"name\"")[1:]
    movieyear = res.split("\"datePublished\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "").replace("null",
                                                                                                              "TBD")
    movieRate = res.split("\"rating\":")[1].split("\"ratingValue\":")[1].split("\n")[0].replace(" ", "").replace("null",
                                                                                                                 "TBD")
    movieGenre = res.split("\"genre\":")[1].split("],\n")[0].split("\n")
    movieGenre = movieGenre[1:len(movieGenre) - 1]
    movieContentRate = res.split("\"contentRating\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "").replace(
        "null", "TBD")
    movieDescript = res.split("\"description\":")[1].split("],\n")[0].split("\n")[0][1:-1].replace("&apos;", "'").replace("\"", "")

    for i in range(len(movieactors)):
        movieactors[i] = movieactors[i].split("\n")[0].replace("\"", "").replace(": ", "").replace("null", "TBD")
    for i in range(len(movieGenre)):
        movieGenre[i] = movieGenre[i].replace("\"", "").replace(" ", "").replace("null", "TBD")
    print("\n\n")
    print(
        f"Name: {movieName}, Duration: {movieTime}, Actors: {movieactors}, Year: {movieyear}, Rate: {movieRate}, Genre: {movieGenre}, Content Rate: {movieContentRate}")
    print(f"\nDescription: {movieDescript}")
    print("\n\n")

def TVOption(res):
    TVName = res.split("\"name\":")[1].split(",\n")[0].replace("\"", "")[1:].replace("null", "TBD")

    TVactors = res.split("\"actor\":")[1].split("],\n")[0].split("\"name\"")[1:]
    TVyear = res.split("\"datePublished\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "").replace("null",
                                                                                                              "TBD")
    TVRate = res.split("\"rating\":")[1].split("\"ratingValue\":")[1].split("\n")[0].replace(" ", "").replace("null",
                                                                                                                 "TBD")
    TVGenre = res.split("\"genre\":")[1].split("],\n")[0].split("\n")
    TVGenre = TVGenre[1:len(TVGenre) - 1]
    TVContentRate = res.split("\"contentRating\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "").replace(
        "null", "TBD")
    TVDescript = res.split("\"description\":")[1].split("],\n")[0].split("\n")

    for i in range(len(TVactors)):
        TVactors[i] = TVactors[i].split("\n")[0].replace("\"", "").replace(": ", "").replace("null", "TBD")
    for i in range(len(TVGenre)):
        TVGenre[i] = TVGenre[i].res.split("\"description\":")[1].split("],\n")[0].split("\n")[0][1:-1].replace("&apos;", "'").replace("\"", "")

    print("\n\n")
    print(
        f"Name: {TVName}, Actors: {TVactors}, Year: {TVyear}, Rate: {TVRate}, Genre: {TVGenre}, Content Rate: {TVContentRate}")
    print(f"\nDescription: {TVDescript}")
    print("\n\n")

    pass

imdb = IMDB()
#res = imdb.popular_tv(genre="Comedy", start_id=1, sort_by=None)

#res = imdb.upcoming(region="Spain")


MovieDisplay()



