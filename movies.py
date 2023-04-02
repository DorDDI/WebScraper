from bs4 import BeautifulSoup
import requests
import urllib.parse
from PyMovieDb import IMDB
def MovieDisplay():
    imdb = IMDB()

    while (1):

        print('Movie Menu\n~~~~~~~~~~~~~~~\n1. search movie/tv by name \n2. search actor \n3. get the popular movies in spesific genre')
        print('4. returns top 50 popular TV Series \n5. upcoming movies from imdb \n6. return')
        options = int(input('what do you want to do:'))

        if (options == 1):
            # search movie / seria name from imdb
            name = input('enter movie / tv name ')
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
            movieName = res.split("\"name\":")[1].split(",\n")[0].replace("\"", "")[1:]
            movieTime = res.split("\"duration\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "")
            movieactors = res.split("\"actor\":")[1].split("],\n")[0].split("\"name\"")[1:]
            movieyear = res.split("\"datePublished\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "")
            movieRate = res.split("\"rating\":")[1].split("\"ratingValue\":")[1].split("\n")[0].replace(" ", "")
            movieGenre = res.split("\"genre\":")[1].split("],\n")[0].split("\n")
            movieGenre = movieGenre[1:len(movieGenre)-1]
            movieContentRate = res.split("\"contentRating\":")[1].split(",\n")[0].replace("\"", "").replace(" ", "")

            for i in range (len(movieactors)):
                movieactors[i]=movieactors[i].split("\n")[0].replace("\"", "").replace(": ", "")
            for i in range (len(movieGenre)):
                movieGenre[i]=movieGenre[i].replace("\"", "").replace(" ", "")
            print("\n\n")
            print(f"Name: {movieName}, Duration: {movieTime}, Actors: {movieactors}, Year: {movieyear}, Rate: {movieRate}, Genre: {movieGenre}, Content Rate: {movieContentRate}")
            print("\n\n")

        elif(options == 2):
            # search person from imdb
            res = imdb.person_by_name('Rajkummar Rao')

        elif(options == 3):
            # returns top 50 popular movies starting from start id
            res = imdb.popular_movies(genre=None, start_id=1, sort_by=None)

        elif (options == 4):
            # returns top 50 popular TV Series starting from start id
            res = imdb.popular_tv(genre=None, start_id=1, sort_by=None)

        elif (options == 5):
            # upcoming movies from imdb
            res = imdb.upcoming(region=None)

        else:
            break




MovieDisplay()