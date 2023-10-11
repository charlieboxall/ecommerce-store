from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

database = SQLAlchemy()
database_name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_name}"
    database.init_app(app)

    from .perspectives import perspectives
    from .auth import auth

    app.register_blueprint(perspectives, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Create database
    from .models import User, Item, Order
    with app.app_context():
        database.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    # Loading users with primary key (id)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
