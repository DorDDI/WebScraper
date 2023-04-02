from bs4 import BeautifulSoup
import requests
import urllib.parse
from PyMovieDb import IMDB
def MovieDisplay():

    imdb = IMDB()
    res = imdb.get_by_name('Titanic')
    res = imdb.popular_movies(genre='Action', start_id=1, sort_by=None)
    print(res)



MovieDisplay()