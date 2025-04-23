from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username = user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique = True, required = True, min_length = 1, max_length = 40)
    email = db.EmailField(unique = True, required = True)
    password = db.StringField(required = True)
    profile_pic = db.ImageField()

    def get_id(self):
        return self.username

class Book(db.Document):
    user = db.ReferenceField(User)
    notes = db.StringField()
    rating = db.IntField()
    date = db.StringField(required = True)
    book_key = db.StringField(required = True)
    title = db.StringField(required = True)
    book_cover = db.ImageField()
    author = db.StringField(required = True)
    author_img = db.ImageField()
    publish_year = db.StringField(required = True)