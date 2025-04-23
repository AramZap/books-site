import requests
import json


class Book(object):
    def __init__(self, library_json):
        self.title = library_json["title"]
        self.book_key = library_json["cover_edition_key"]
        self.book_cover = f"https://covers.openlibrary.org/b/olid/{library_json['cover_edition_key']}-M.jpg"
        self.author = library_json["author_name"][0]
        self.author_img_key = library_json["author_key"][0]
        self.author_img = f"https://covers.openlibrary.org/a/olid/{library_json['author_key'][0]}-M.jpg"
        self.publish_year = library_json["first_publish_year"]

    def to_dict(self):
        return {
            "title": self.title,
            "book_key": self.book_key,
            "book_cover": self.book_cover,
            "author": self.author,
            "author_img_key": self.author_img_key,
            "author_img": self.author_img,
            "publish_year": self.publish_year
        }

    def __str__(self):
        return json.dumps(self.to_dict())


class BookClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = "https://openlibrary.org/search.json?"

    def search(self, search_string):
        search_string = "+".join(search_string.split())

        search_url = f"q={search_string}"

        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed!"
            )

        search_results_json = resp.json()["docs"]
        result = []

        for item_json in search_results_json:
            if all(key in item_json for key in {"title", "cover_edition_key", "author_name", "author_key", "first_publish_year"}):
                result.append(Book(item_json))

        return result

## -- Example usage -- ###
if __name__ == "__main__":
    
    books = BookClient().search("curtain poirot's last case")

    for book in books:
        print(book)
        print(book.author_img)

    print(len(books))
