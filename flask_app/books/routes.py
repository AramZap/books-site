import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from .. import book_client
from ..forms import AddBookForm, SearchForm, ModifyBookForm
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
@login_required
def add_book():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("books.query_results", query=form.search_query.data))

    return render_template("add_book.html", form=form)

@books.route("/query-results/<query>", methods=["GET"])
@login_required
def query_results(query):
    try:
        results = book_client.search(query)
    except ValueError as e:
        return render_template("query_results.html", error_msg=str(e))

    return render_template("query_results.html", results=results)


@books.route("/book_query_info", methods=["POST"])
@login_required
def book_query_info():
    book = json.loads(request.form.get("book"))
    form = AddBookForm()
    return render_template("book_query_info.html", form=form, book=book)

@books.route("/add_book_to_collection", methods=["POST"])
@login_required
def add_book_to_collection():

    form = AddBookForm()
    if form.validate_on_submit():
        
        book = json.loads(request.form.get("book"))

        book_in_db = Book.objects(book_key = book["book_key"], user=current_user._get_current_object()).first()
        if book_in_db is not None:
            flash("This book is already in your collection!", "warning")
            return redirect(url_for('books.index'))

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
        flash("Book added successfully!", "success")
        return redirect(url_for('books.index'))

    return redirect(request.referrer)

@books.route("/collection", methods=["GET"])
@login_required
def collection():

    sort_by = request.args.get("sort_by", "title_asc")

    def to_dict(book):
        book_cover = book.book_cover
        author_img = book.author_img
        
        if book_cover:
            bytes_book_cover = BytesIO(book.book_cover.read())
            book_cover = f"data:image/jpeg;base64, {base64.b64encode(bytes_book_cover.getvalue()).decode()}"
        
        if author_img:
            bytes_author_img = BytesIO(book.author_img.read())
            author_img = f"data:image/jpeg;base64, {base64.b64encode(bytes_author_img.getvalue()).decode()}"

        return {
            "title": book.title,
            "book_key": book.book_key,
            "book_cover": book_cover,
            "author": book.author,
            "author_img": author_img,
            "publish_year": book.publish_year,
            "notes": book.notes,
            "rating": book.rating,
            "date": book.date
        }
    
    books_qs = Book.objects(user=current_user)

    if sort_by == "title_asc":
        books_qs = books_qs.order_by("title")
    elif sort_by == "title_desc":
        books_qs = books_qs.order_by("-title")
    elif sort_by == "rating_asc":
        books_qs = books_qs.order_by("rating")
    elif sort_by == "rating_desc":
        books_qs = books_qs.order_by("-rating")
    elif sort_by == "date_asc":
        books_qs = books_qs.order_by("date")
    elif sort_by == "date_desc":
        books_qs = books_qs.order_by("-date")

    book_collection = [to_dict(book) for book in books_qs]
    return render_template("book_collection.html", book_collection=book_collection)

@books.route("/modify_book_in_collection", methods=["POST"])
@login_required
def modify_book_in_collection():

    form = ModifyBookForm()
    if form.validate_on_submit():
        
        book = json.loads(request.form.get("book"))

        book_in_db = Book.objects(book_key = book["book_key"]).first()

        book_in_db.notes = form.notes.data
        book_in_db.rating = int(form.rating.data)
        book_in_db.date = current_time()
        
        book_in_db.save()
        flash("Book updated successfully!", "success")
        return redirect(url_for('books.index'))

    return redirect(request.referrer)

@books.route("/book_info", methods=["POST"])
@login_required
def book_info():
    book = json.loads(request.form.get("book"))
    form = ModifyBookForm()
    form.notes.data = book["notes"]
    form.rating.data = int(book["rating"])
    return render_template("book_info.html", form=form, book=book)