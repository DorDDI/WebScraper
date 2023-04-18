import json
import requests
from PyMovieDb import IMDB
from requests_html import HTMLSession
import re

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

        print('Movie Menu\n~~~~~~~~~~~~~~~\n1. search movie/tv by name \n2. upcoming movies from imdb \n3. get the popular movies in spesific genre')
        print('4. returns top 50 popular TV Series \n5. return')
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

            res = get_by_id(a[choose-1][0][1:])

            type = res.split("\"@type\":")[1].split(",")[0].replace('"',"")

            if (type == "Movie"):
                MovieOption(res)
            else:
                TVOption(res)


        elif(options == 2):

            # upcoming movies from imdb
            number = int(input("enter number of upcoming movies: "))
            upcoming(number)
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
            numberofmovies = int(input("enter number of movies: "))
            res = get_popular(1,genre=genreArr[chooseGenre-1], start_id=1, movienumber=numberofmovies)
            genreArr[0] = "All"
            counter = 1
            for element in res["results"]:
                print(f"{counter}. {(element['name'])}")
                counter = counter +1
            option = int(input("Enter 0 to return or movie number for details: "))
            if (option!=0):
                moviedetail = get_by_id(res['results'][option-1]['id'])
                MovieOption(moviedetail)


        elif (options == 4):
            # returns top 50 popular TV Series starting from start id
            print("choose genere by number:\n")
            count = 1
            for i in range(len(genreArr)):
                print(f"{count}. {genreArr[count - 1]}")
                count = count + 1
            chooseGenre = int(input())
            genreArr[0] = "None"
            numberofmovies = int(input("enter number of movies up to 50: "))
            res = get_popular(2,genre=genreArr[chooseGenre-1], start_id=1, movienumber=numberofmovies)
            genreArr[0] = "All"
            counter = 1
            for element in res["results"]:
                print(f"{counter}. {(element['name'])}")
                counter = counter +1
            option = int(input("Enter 0 to return or movie number for details: "))
            if (option!=0):
                tvdetail = get_by_id(res['results'][option-1]['id'])
                TVOption(tvdetail)

        else:
            break

def upcoming(movienumber = 20):
    """
     @description:- Helps to get upcoming movies/tv-series.
     @parameter-1:- <str:region> OPTIONAL, country code (like US, IN etc.) to filter results by region/country.
     @returns:- upcoming movies/TV-Series info as JSON string.
    """
    numberOfMovies = 1
    url = f"https://www.imdb.com/calendar?region=US"
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
                actors = ["TBD"]
            else:
                detail = detail[1]
                detail = detail.split('class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base" role="presentation"><li role="presentation" class="ipc-inline-list__item"><span ')
                genre = detail[0].split('aria-disabled="false">')[1:]
                if len(detail)!=1:
                    actors = detail[1].split('</span></li></ul></div></div><div')
                    if len(actors) > 1:
                        actors = actors[0].split('aria-disabled="false">')[1:]
                    else:
                        actors = ["TBD"]
                else:
                    actors = ["TBD"]
                for i in range (len(genre)):
                    genre[i]=genre[i].split('<')[0]
                for i in range (len(actors)):
                    actors[i] = actors[i].split('<')[0]
            print(f"{name}, {actors}, {genre}")
            numberOfMovies = numberOfMovies+1
            if (numberOfMovies>movienumber):
                break
        print("\n")

        pass

def MovieOption(res):
    movieName, movieyear, movieRate, movieGenre, movieContentRate, movieDescript, movieTime, movieactors = ValueUpdate(res,1)

    print("\n\n")
    print(
        f"Name: {movieName}\nDuration: {movieTime}\nActors: {movieactors}\nYear: {movieyear}\nRate: {movieRate}\nGenre: {movieGenre}\nContent Rate: {movieContentRate}")
    print(f"\nDescription: {movieDescript}")
    print("\n\n")

def TVOption(res):
    TVName, TVyear, TVRate, TVGenre, TVContentRate, TVDescript, TVactors = ValueUpdate(res,0)

    print("\n\n")
    print(
        f"Name: {TVName}\nActors: {TVactors}\nYear: {TVyear}\nRate: {TVRate}\nGenre: {TVGenre}\nContent Rate: {TVContentRate}")
    print(f"\nDescription: {TVDescript}")
    print("\n\n")

def ValueUpdate(res, type):
    """

    :param res:
    :param type: 1 if movie, 0 if TV seria
    :return:
    """
    name = res.split("\"name\":")[1].split(",")[0].replace("\"", "")

    year = res.split("\"datePublished\":")[1].split(",\"director\"")[0].split(",")[0].replace("\"", "").replace(" ", "")
    rate = res.split("\"ratingValue\":")
    if len(rate)==1:
        rate = "TBD"
    elif  len(rate)<=2:
        rate = rate[1].split("}")[0]
    else:
        rate = rate[2].split("}")[0]
    genre = res.split("\"genre\":")[1].split("]")[0].replace("[","").replace("\"","").replace(",",", ")
    ContentRate = res.split("\"contentRating\":")
    if len(ContentRate)==1:
        ContentRate = "TBD"
    else:
        ContentRate = ContentRate[1].split(",")[0].replace("\"","")

    Descript = res.split("\"description\":")[1].split("\",\"genre\":")[0].split(",\"review\":")[0].replace("\"", "").replace("&apos;","'")

    if type == 1:                                     #movie
        duration = res.split("\"duration\":")
        if len(duration) <= 2:
            duration = "TBD"
        else:
            duration = duration[2].split(",")[0].replace("\"", "").replace("PT", "").replace("H", " Hours and ").replace(
                "M", " Minutes").replace("}", "")
        actor = res.split(",\"director\"")[0].split("\"actor\":")[1].split("\"name\"")[1:]
        for i in range(len(actor)):
            actor[i] = actor[i].split("}")[0].replace("\"", "").replace(":", "")
        return name, year, rate, genre, ContentRate, Descript, duration, actor
    else:                                           #TV seria
        actor = res.split("}],\"creator\":[")[0].split("\"actor\":")[1].split("\"name\"")[1:]
        for i in range(len(actor)):
            actor[i] = actor[i].split("}")[0].replace("\"", "").replace(":", "")
        return name, year, rate, genre, ContentRate, Descript, actor

def get(url):
    """
     @description:- helps to get a file's complete info (used by get_by_name() & get_by_id() )
     @parameter:- <str:url>, url of the file/movie/tv-series.
     @returns:- File/movie/TV info as JSON string.
    """
    response = session.get(url)
    result = response.html.xpath("//script[@type='application/ld+json']")[0].text
    result = ''.join(result.splitlines())  # removing newlines
    result = f"""{result}"""
    return result

def get_by_id(file_id):
    """
     @description:- Helps to search a file/movie/tv by its imdb ID.
     @parameter-1:- <str:file_id>, imdb ID of the file/movie/tv.
     @returns:- File/movie/TV info as JSON string.
    """
    assert isinstance(file_id, str)
    url = f"{baseURL}/title/{file_id}"
    return get(url)


def get_popular(type,genre=None, start_id=1,movienumber = 51):
    """
     @description:- Helps to search popular movies/TV-Series by url, (used by popular_movies() & popular_tv() ).
     @parameter-1:- <str:url>, url to search.
     @returns:- Files/Movies/TV-Series info as JSON string.
    """

    numberOfMovies = 1
    if type == 1:
        searh_type = "movie"         #movie
    else:
        searh_type = "tv_series,tv_miniseries"   #tv
    assert isinstance(start_id, int)
    if genre is not None:
        assert isinstance(genre, str)
        url = f"https://www.imdb.com/search/title/?title_type={searh_type}&genres={genre}&start={start_id}"
    else:
        url = f"https://www.imdb.com/search/title/?title_type={searh_type}&start={start_id}"

    assert isinstance(url, str)
    try:
        response = session.get(url)
    except requests.exceptions.ConnectionError as e:
        response = session.get(url, verify=False)

    links = response.html.xpath('//h3/a')
    years = response.html.xpath("//h3")

    if not bool(links) and bool(years):
        return NA

    output = []
    for link, year in zip(links, years):
        href = link.attrs.get('href', "#")
        if 'title' in href:
            # getting year
            year = year.find('span', containing='(')[0] if bool(year.find('span', containing='(')) else "TBD"
            if year != "TBD":
                year = "".join(re.findall(r"\d+", year.text))
            year = year[:4] + "-" + year[4:] if len(year) == 8 else year   # for TV
            year = year if len(year) == 4 else year  # for movies

            # getting poster
            file_id = href.split('/')[2]
            poster = response.html.xpath(f"//img[@data-tconst='{file_id}']")
            poster = poster[0].attrs.get('loadlate', 'image_not_found') if bool(poster) else 'image_not_found'
            # creating file object
            output.append({
                'id': file_id,
                'name': link.text,
                'year': year,
                'url': baseURL + href,
                'poster': poster
            })
            numberOfMovies = numberOfMovies+1
        if (numberOfMovies > movienumber):
            break
    search_results = {'result_count': len(output), 'results': output}
    return search_results


