import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import book_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Book
from ..utils import current_time

books = Blueprint("books", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

@books.route("/")
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
    # try:
    #     result = book_client.retrieve_book_by_id(movie_id)
    # except ValueError as e:
    #     return render_template("movie_detail.html", error_msg=str(e))
    
    # book = request.form.get("book")

    # form = MovieReviewForm()
    # if form.validate_on_submit():
    #     review = Review(
    #         commenter=current_user._get_current_object(),
    #         content=form.text.data,
    #         date=current_time(),
    #         imdb_id=movie_id,
    #         movie_title=result.title,
    #     )

    #     review.save()

    #     return redirect(request.path)

    # reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html"
    )

    # , form=form, movie=result, reviews=reviews


@books.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()

    if user is None:
        return render_template("user_detail.html", error = f"user \"{username}\" doesn't exist.")
    else:
        reviews = list(Book.objects(commenter = user))
        return render_template("user_detail.html", error = None, image = get_b64_img(username), username = username, reviews = reviews)
