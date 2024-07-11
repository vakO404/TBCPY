from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    description = db.Column(db.String())
    image_url=db.Column(db.String())
    rating = db.Column(db.Float, nullable=True, default=0.0)
    rating_count = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, price, description, image_url, rating ):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url
        self.rating = rating
class User( db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Delivery(db.Model, UserMixin):

    __tablename__ = "delivery"

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    email = db.Column(db.String)
    phone_number = db.Column(db.Integer())
    country = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String())
    post_code = db.Column(db.Integer)
    birthday = db.Column(db.Date())



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)