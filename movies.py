import json
import requests
from requests_html import HTMLSession
import re


class Movie:

    def __init__(self):
        self.session = HTMLSession()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/84.0.4147.105 Safari/537.36",
            "Referer": "https://www.imdb.com/"
        }

    def movie_display(self):
        """

        :return:
        """
        genre_arr = ["All", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama",
                     "Family", "Fantasy", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "News",
                     "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"]

        while 1:

            print('Movie Menu\n~~~~~~~~~~~~~~~\n1. Search movie/TV seria by name \n2. Upcoming movies \n3. Popular '
                  'Movies')
            print('4. Popular TV Series \n5. Return')
            options = input('Choose option: ')

            while not options.isnumeric() or int(options) > 5 or int(options) < 1:
                options = input('Wrong input, please choose another option: ')
            options = int(options)
            if options == 1:
                # search movie/TV seria name
                name = input('Enter movie/TV seria name: ')
                res = self.search(name)

                number_of_options = int(res['result_count'])
                if number_of_options == 0:
                    print("No movies or TV series found\n")
                    continue
                count = 1
                for movie in res['results']:
                    print(f"{count}. {movie['name']}")
                    count = count + 1
                choose = input("\nChoose the requested search from the options: ")
                while not choose.isnumeric() or int(choose) > 5 or int(choose) < 1:
                    choose = input('Wrong input, please choose another option: ')
                choose = int(choose)
                res = self.get_by_id(res['results'][choose - 1]['id'])

                search_type = res.split("\"@type\":")[1].split(",")[0].replace('"', "")

                if search_type == "Movie":
                    self.movie_option(res)
                else:
                    self.tv_option(res)

            elif options == 2:

                # upcoming movies
                number = input("Enter number of upcoming movies to show from 1 to 50: ")
                while not number.isnumeric() or int(number) < 1 or int(number) > 50:
                    number = input('Wrong input, please choose another option: ')
                self.upcoming(int(number))

            elif options == 3:
                # popular movies

                count = 1
                start = input("Enter from which index to show (1 for the first): ")
                while not start.isnumeric() or int(start) < 1:
                    start = input('Wrong input, please choose another option: ')

                for i in range(len(genre_arr)):
                    print(f"{count}. {genre_arr[count - 1]}")
                    count = count + 1
                choose_genre = input("Choose genre by number: ")
                while not choose_genre.isnumeric() or int(choose_genre) < 1 or int(choose_genre) > 27:
                    choose_genre = input('Wrong input, please choose another option: ')

                genre_arr[0] = "None"
                number_of_movies = input("Enter number of movies up to 50: ")
                while not number_of_movies.isnumeric() or int(number_of_movies) < 1 or int(number_of_movies) > 50:
                    number_of_movies = input('Wrong input, please choose another option: ')
                res = self.get_popular(1, genre=genre_arr[int(choose_genre) - 1], start_id=int(start), movie_number=int(number_of_movies))
                genre_arr[0] = "All"
                counter = 1
                for element in res["results"]:
                    print(f"{counter}. {(element['name'])}")
                    counter = counter + 1
                option = input("Enter 0 to return or movie number for details: ")
                while not option.isnumeric() or int(option) < 0 or int(option) > int(number_of_movies):
                    option = input('Wrong input, please choose another option: ')
                option = int(option)
                if option != 0:
                    movie_detail = self.get_by_id(res['results'][option - 1]['id'])
                    self.movie_option(movie_detail)

            elif options == 4:
                # popular TV Series
                count = 1
                start = input("Enter from which index to show (1 for the first): ")
                while not start.isnumeric() or int(start) < 1:
                    start = input('Wrong input, please choose another option: ')
                for i in range(len(genre_arr)):
                    print(f"{count}. {genre_arr[count - 1]}")
                    count = count + 1
                choose_genre = input("Choose genre by number: ")
                while not choose_genre.isnumeric() or int(choose_genre) < 1 or int(choose_genre) > 27:
                    choose_genre = input('Wrong input, please choose another option: ')
                genre_arr[0] = "None"
                number_of_tv = input("enter number of TV series up to 50: ")

                while not number_of_tv.isnumeric() or int(number_of_tv) < 1 or int(number_of_tv) > 50:
                    number_of_tv = input('Wrong input, please choose another option: ')

                res = self.get_popular(2, genre=genre_arr[int(choose_genre) - 1], start_id=int(start), movie_number=int(number_of_tv))
                genre_arr[0] = "All"
                counter = 1
                for element in res["results"]:
                    print(f"{counter}. {(element['name'])}")
                    counter = counter + 1
                option = input("Enter 0 to return or movie number for details: ")
                while not option.isnumeric() or int(option) < 0 or int(option) > int(number_of_tv):
                    option = input('Wrong input, please choose another option: ')
                option = int(option)

                if option != 0:
                    tv_detail = self.get_by_id(res['results'][option - 1]['id'])
                    self.tv_option(tv_detail)
            else:
                break

    def upcoming(self, movie_number=20):
        """

        :param movie_number:
        :return:
        """
        number_of_movies = 1
        url = f"https://www.imdb.com/calendar?region=US"
        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError as e:
            response = self.session.get(url, verify=False)

        div = response.html.xpath("//section[@class='ipc-page-section ipc-page-section--base']")[0]

        articles = div.html.split('<article')[1:]
        for article in articles:
            if number_of_movies > movie_number:
                break
            title = article.split('ipc-title__text')[1].split('</h3>')[0][2:]
            print(title)
            movies = article.split('<li class="ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click '
                                   'sc-8c2b7f1f-0 bpqYIE"')[1:]
            for movie in movies:
                name = movie.split('<a class="ipc-metadata-list-summary-item__t" role="button" tabindex="0" '
                                   'aria-disabled="false" href="')[1].split('>')[1].split('<')[0]
                detail = movie.split('<ul class="ipc-inline-list ipc-inline-list--show-dividers '
                                     'ipc-inline-list--no-wrap '
                                     'ipc-inline-list--inline ipc-metadata-list-summary-item__tl base" '
                                     'role="presentation">')
                if len(detail) == 1:
                    genre = "TBD"
                    actors = ["TBD"]
                else:
                    detail = detail[1]
                    detail = detail.split('class="ipc-inline-list ipc-inline-list--show-dividers '
                                          'ipc-inline-list--no-wrap '
                                          'ipc-inline-list--inline ipc-metadata-list-summary-item__stl base" '
                                          'role="presentation"><li role="presentation" '
                                          'class="ipc-inline-list__item"><span ')
                    genre = detail[0].split('aria-disabled="false">')[1:]
                    if len(detail) != 1:
                        actors = detail[1].split('</span></li></ul></div></div><div')
                        if len(actors) > 1:
                            actors = actors[0].split('aria-disabled="false">')[1:]
                        else:
                            actors = ["TBD"]
                    else:
                        actors = ["TBD"]
                    for i in range(len(genre)):
                        genre[i] = genre[i].split('<')[0]
                    for i in range(len(actors)):
                        actors[i] = actors[i].split('<')[0]
                actors = ", ".join(actors)
                genre = ", ".join(genre)
                print(f"Name: {name}, actors: {actors}, genre: {genre}")
                number_of_movies = number_of_movies + 1
                if number_of_movies > movie_number:
                    break
            print("\n")

    def movie_option(self, res):
        """

        :param res:
        :return:
        """
        movie_name, movie_year, movie_rate, movie_genre, movie_content_rate, movie_descript, movie_time, movie_actors = self.value_update(
            res, 1)
        movie_actors = ", ".join(movie_actors)
        print(
            f"\nName: {movie_name}\nDuration: {movie_time}\nActors: {movie_actors}\nYear: {movie_year}\
            \nRate: {movie_rate}\nGenre: {movie_genre}\nContent Rate: {movie_content_rate}")
        print(f"\nDescription: {movie_descript}\n")

    def tv_option(self, res):
        """

        :param res:
        :return:
        """
        tv_name, tv_year, tv_rate, tv_genre, tv_content_rate, tv_descript, tv_actors = self.value_update(res, 0)
        tv_actors = ", ".join(tv_actors)
        print(
            f"\nName: {tv_name}\nActors: {tv_actors}\nYear: {tv_year}\nRate: {tv_rate}\nGenre: {tv_genre}\
            \nContent Rate: {tv_content_rate}")
        print(f"\nDescription: {tv_descript}\n")

    def value_update(self, res, type_req):
        """

        :param res:
        :param type_req:
        :return:
        """

        name = res.split("\"name\":")[1].split(",")[0].replace("\"", "")
        year = res.split("\"datePublished\":")
        if len(year) != 1:
            year = year[1].split(",\"director\"")[0].split(",")[0].replace("\"", "").replace(" ", "")
        else:
            year = "TBD"
        rate = res.split("\"ratingValue\":")
        if len(rate) == 1:
            rate = "TBD"
        elif len(rate) <= 2:
            rate = rate[1].split("}")[0]
        else:
            rate = rate[2].split("}")[0]
        genre = res.split("\"genre\":")[1].split("]")[0].replace("[", "").replace("\"", "").replace(",", ", ")
        content_rate = res.split("\"contentRating\":")
        if len(content_rate) == 1:
            content_rate = "TBD"
        else:
            content_rate = content_rate[1].split(",")[0].replace("\"", "")

        descript = res.split("\"description\":")[1].split("\",\"genre\":")[0].split(",\"review\":")[0]\
            .replace("\"", "").replace("&apos;", "'")

        if type_req == 1:  # movie
            duration = res.split("\"duration\":")
            if len(duration) <= 2:
                duration = "TBD"
            else:
                duration = duration[2].split(",")[0].replace("\"", "").replace("PT", "").replace("H",
                                                                                                 " Hours and ").replace(
                    "M", " Minutes").replace("}", "")
            actor = res.split(",\"director\"")[0].split("\"actor\":")[1].split("\"name\"")[1:]
            for i in range(len(actor)):
                actor[i] = actor[i].split("}")[0].replace("\"", "").replace(":", "")
            return name, year, rate, genre, content_rate, descript, duration, actor
        else:  # TV seria
            actor = res.split("}],\"creator\":[")[0].split("\"actor\":")[1].split("\"name\"")[1:]
            for i in range(len(actor)):
                actor[i] = actor[i].split("}")[0].replace("\"", "").replace(":", "")
            return name, year, rate, genre, content_rate, descript, actor

    def get_by_id(self, file_id):
        """

        :param file_id:
        :return:
        """
        assert isinstance(file_id, str)
        url = f"https://www.imdb.com/title/{file_id}"
        response = self.session.get(url)
        result = response.html.xpath("//script[@type='application/ld+json']")[0].text
        result = ''.join(result.splitlines())  # removing newlines
        result = f"""{result}"""
        return result

    def get_popular(self, type_req, genre=None, start_id=1, movie_number=51):
        """

        :param type_req:
        :param genre:
        :param start_id:
        :param movie_number:
        :return:
        """

        number_of_movies = 1
        if type_req == 1:
            search_type = "movie"  # movie
        else:
            search_type = "tv_series,tv_miniseries"  # tv
        assert isinstance(start_id, int)
        if genre is not None:
            assert isinstance(genre, str)
            url = f"https://www.imdb.com/search/title/?title_type={search_type}&genres={genre}&start={start_id}"
        else:
            url = f"https://www.imdb.com/search/title/?title_type={search_type}&start={start_id}"

        assert isinstance(url, str)
        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError as e:
            response = self.session.get(url, verify=False)

        links = response.html.xpath('//h3/a')
        years = response.html.xpath("//h3")

        output = []
        for link, year in zip(links, years):
            href = link.attrs.get('href', "#")
            if 'title' in href:
                # getting year
                year = year.find('span', containing='(')[0] if bool(year.find('span', containing='(')) else "TBD"
                if year != "TBD":
                    year = "".join(re.findall(r"\d+", year.text))
                year = year[:4] + "-" + year[4:] if len(year) == 8 else year  # for TV
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
                    'url': "https://www.imdb.com" + href,
                    'poster': poster
                })
                number_of_movies = number_of_movies + 1
            if number_of_movies > movie_number:
                break
        search_results = {'result_count': len(output), 'results': output}
        return search_results

    def search(self, name):
        """

        :param name:
        :return:
        """
        assert isinstance(name, str)
        search_results = {'result_count': 0, 'results': []}

        name = name.replace(" ", "+")
        url = f"https://www.imdb.com/find?q={name}"

        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError as e:
            response = self.session.get(url, verify=False)

        results = response.html.xpath("//section[@data-testid='find-results-section-title']/div/ul/li")

        output = []
        for result in results:
            name = result.text.replace('\n', ' ')
            url = result.find('a')[0].attrs['href']
            image = result.xpath("//img")[0].attrs['src']
            file_id = url.split('/')[2]
            output.append({
                'id': file_id,
                "name": name,
                "url": f"https://www.imdb.com{url}",
                "poster": image
            })
            search_results = {'result_count': len(output), 'results': output}
        return search_results
