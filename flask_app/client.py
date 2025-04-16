import requests


class Book(object):
    def __init__(self, library_json, detailed=False):
        if detailed:
            self.genres = library_json["Genre"]
            self.director = library_json["Director"]
            self.actors = library_json["Actors"]
            self.plot = library_json["Plot"]
            self.awards = library_json["Awards"]

        self.title = library_json["Title"]
        self.year = library_json["Year"]
        self.imdb_id = library_json["imdbID"]
        self.type = "Movie"
        self.poster_url = library_json["Poster"]

    def __repr__(self):
        return self.title


class BookClient(object):
    def __init__(self):
        self.sess = requests.Session()

    def search(self, search_string):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        search_string = "+".join(search_string.split())
        page = 1

        search_url = f"s={search_string}&page={page}"

        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        search_results_json = data["Search"]
        remaining_results = int(data["totalResults"])

        result = []

        ## We may have more results than are first displayed
        while remaining_results != 0:
            for item_json in search_results_json:
                result.append(Movie(item_json))
                remaining_results -= len(search_results_json)
            page += 1
            search_url = f"s={search_string}&page={page}"
            resp = self.sess.get(self.base_url + search_url)
            if resp.status_code != 200 or resp.json()["Response"] == "False":
                break
            search_results_json = resp.json()["Search"]

        return result

    def retrieve_movie_by_id(self, imdb_id):
        """
        Use to obtain a Movie object representing the movie identified by
        the supplied imdb_id
        """
        movie_url = self.base_url + f"i={imdb_id}&plot=full"

        resp = self.sess.get(movie_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        movie = Movie(data, detailed=True)

        return movie


## -- Example usage -- ###
if __name__ == "__main__":
    import os
    
    books = BookClient().search("guardians")

    for book in books:
        print(book)

    print(len(movies))
