from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User, Book

users = Blueprint("users", __name__)

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ User Management views ************ """

@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("books.index"))
    elif request.method == "POST":
        if form.validate_on_submit():

            hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username = form.username.data, email = form.email.data, password = hashed)
            user.save()
            return redirect(url_for("users.login"))
    else:
        return render_template("register.html", form = form)


@users.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("books.index"))
    elif request.method == "POST":
        if form.validate_on_submit():

            user = User.objects(username = form.username.data).first()

            if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
                login_user(user)
                return redirect(url_for("users.account"))
            else:
                flash("Login failed. Check your username and/or password")
                return redirect(url_for("users.login"))
    else:
        return render_template("login.html", form = form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("books.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()

    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # if User.objects(username=update_username_form.submit_username.data) is None:
            current_user.modify(username=update_username_form.username.data)
            current_user.save()
            return redirect(url_for("users.login"))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            img = update_profile_pic_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f"images/{filename[-3:]}"

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
                
            current_user.save()
            return redirect(url_for("users.login"))
    return render_template("account.html", image = get_b64_img(current_user.username), update_username_form = update_username_form, update_profile_pic_form = update_profile_pic_form)
