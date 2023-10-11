from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import database
from flask_login import login_user, login_required, logout_user, current_user

# hash passwords, so they don't get stored as is, but as hash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("perspectives.home"))
    # If logging in
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Valid email? - is email in the database
        c_user = User.query.filter_by(username=username).first() # current_user
        if c_user:
            if check_password_hash(c_user.password, password):
                # User exists and has logged in succesfully
                login_user(c_user)
                return redirect(url_for("perspectives.admin"))
            
            else:
                # Incorrect password
                flash("Log in unsuccesful - username or password incorrect.", category="invalid")
        else:
            # Account does not exist with that email
            flash("Log in unsuccesful - username or password incorrect.", category="invalid")
        
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    # Redirect to log in page after logged out
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("perspectives.home"))
    
    def has_upper(string):
        for char in string:
            if char.isupper():
                return True
        return False

    def has_lower(string):
        for char in string:
            if char.islower():
                return True
        return False
    
    def has_numeric(string):
        for char in string:
            if char.isnumeric():
                return True
        return False

    def valid_username(string):
        for char in string:
            if not(char.isalpha() or char.isnumeric()):
                return False
        return True
            
    if request.method == "POST":
        fname = request.form.get("fname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confpassword = request.form.get("confpassword")

        c_user = User.query.filter_by(email=email).first()
        c_user2 = User.query.filter_by(username=username).first()
        if c_user:
            flash("Account with this email already exists.", category="invalid")
        elif c_user2:
            flash("Account with this username already exists.", category="invalid")
        elif len(username) > 20:
            flash("Username must not be greater than 20 characters.", category="invalid")
        elif not(valid_username(username)):
            flash("Username must not include any special characters or spaces.", category="invalid")
        elif len(email) < 4:
            flash("Email not valid.", category="invalid")
        elif password != confpassword:
            flash("Passwords do not match.", category="invalid")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", category="invalid")
        elif not(has_upper(password)):
            flash("Password must contain atleast 1 uppercase letter.", category="invalid")
        elif not(has_lower(password)):
            flash("Password must contain atleast 1 lowercase letter.", category="invalid")
        elif not(has_numeric(password)):
            flash("Password must contain atleast 1 number.", category="invalid")
        else:
            new_user = User(fname=fname, username=username, email=email, password=generate_password_hash(password, method="sha384"))
            database.session.add(new_user)
            database.session.commit()

            login_user(new_user)
            #flash("Account created.", category="valid")
            return redirect(url_for("perspectives.home"))

    return render_template("signup.html", user=current_user)
