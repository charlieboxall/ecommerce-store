from . import database
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

class User(database.Model, UserMixin):
    max_char = 200
    # Unique id for each user
    id = database.Column(database.Integer, primary_key=True)

    fname = database.Column(database.String(max_char))

    username = database.Column(database.String(20), unique=True)

    # Each user must have a unqiue email, none can be the same
    email = database.Column(database.String(max_char), unique=True)

    password = database.Column(database.String(max_char))

class Item(database.Model):
    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(50))

    item_type = database.Column(database.String(50))

    price = database.Column(database.Float)

    env_impact = database.Column(database.Float)

    desc = database.Column(database.String(2000))

    filename = database.Column(database.String(50))

    stock = database.Column(database.Integer)

    exclusive = database.Column(database.Integer) # True = 1, False = 0

class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)

    user_id = database.Column(database.Integer)

    order_json = database.Column(JSON)

    datetime = database.Column(database.String(100))

    total = database.Column(database.Float)


