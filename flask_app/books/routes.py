import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from werkzeug.utils import secure_filename

from .. import book_client
from ..forms import AddBookForm, SearchForm
from ..models import User, Book
from ..utils import current_time
import json
import requests
from io import BytesIO

books = Blueprint("books", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

@books.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@books.route("/add_book", methods=["GET", "POST"])
def add_book():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("books.query_results", query=form.search_query.data))

    return render_template("add_book.html", form=form)

@books.route("/query-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = book_client.search(query)
    except ValueError as e:
        return render_template("query_results.html", error_msg=str(e))

    return render_template("query_results.html", results=results)


@books.route("/book_query_info", methods=["POST"])
def book_query_info():
    book = json.loads(request.form.get("book"))
    form = AddBookForm()
    return render_template("book_query_info.html", form=form, book=book)

@books.route("/add_book_to_collection", methods=["POST"])
def add_book_to_collection():

    form = AddBookForm()
    if form.validate_on_submit():
        book = json.loads(request.form.get("book"))

        book_img_response = requests.get(book["book_cover"])
        book_img_data = BytesIO(book_img_response.content)
        book_img_data.name = secure_filename(book["book_cover"].split("/")[-1])
        book_img_data.content_type = book_img_response.headers.get("Content-Type", "image/jpeg")

        author_img_response = requests.get(book["author_img"])
        author_img_data = BytesIO(author_img_response.content)
        author_img_data.name = secure_filename(book["author_img"].split("/")[-1])
        author_img_data.content_type = author_img_response.headers.get("Content-Type", "image/jpeg")

        book_to_add = Book(
            user=current_user._get_current_object(),
            notes=form.notes.data,
            rating=int(form.rating.data),
            date=current_time(),
            book_key=book["book_key"],
            title=book["title"],
            book_cover=book_img_data,
            author=book["author"],
            author_img=author_img_data,
            publish_year=str(book["publish_year"])
        )
        
        book_to_add.save()
        return redirect(url_for('books.index'))

    return redirect(request.referrer)


@books.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()

    if user is None:
        return render_template("user_detail.html", error = f"user \"{username}\" doesn't exist.")
    else:
        reviews = list(Book.objects(commenter = user))
        return render_template("user_detail.html", error = None, image = get_b64_img(username), username = username, reviews = reviews)
