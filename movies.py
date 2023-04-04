from bs4 import BeautifulSoup
import requests
import urllib.parse
from PyMovieDb import IMDB
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
            name = input('enter actor name: ')
            res = imdb.search('Leonardo DiCaprio')

            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
            url = "https://www.imdb.com/name/nm0000138"
            result = requests.get(url, headers=HEADERS)
            content = result.text

            soup = BeautifulSoup(content, 'html.parser')
            name = soup.find('div', class_='wob_loc q8U8x').get_text()


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


            count = 1
            print("choose genere by number:\n")
            for i in range (len(genreArr)):
                print(f"{count}. {genreArr[count-1]}")
                count = count +1
            chooseGenre = int(input())
            genreArr[0] = "None"
            res = imdb.popular_tv(genre=genreArr[chooseGenre-1], start_id=1, sort_by=None)
            genreArr[0] = "All"
            pass

        elif (options == 5):
            # upcoming movies from imdb
            res = imdb.upcoming(region=None)
            pass

        else:
            break



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


MovieDisplay()
