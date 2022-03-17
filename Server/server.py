import time

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, RadioField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, InputRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

from flask_forms import *

app = Flask(__name__)
app.secret_key = "my super secret key that no one is supposed to know"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=10)

# Initialize the Database
db = SQLAlchemy(app)


# Figure out how to create Flask Forms, style them, and insert user input into
# SQLAlchemy DBs.

def sha256(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    salt = db.Column(db.String(64), unique=True, nullable=False)
    salted_password_hash = db.Column(db.String(64), nullable=False, unique=True)
    date_added = db.Column(db.String(len("dd/mm/yyyy hh:mm:ss")), nullable=False)

    def __init__(self, first_name, last_name, email, password, timestamp: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.salt = sha256(self.email)
        self.salted_password_hash = sha256(self.salt + password)
        self.date_added = timestamp.strftime("%m/%d/%Y %H:%M:%S")

    def __repr__(self):
        return "<Name %r>" % (self.first_name + " " + self.last_name)


class Equations(db.Model):
    row = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    equation = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.String(len("dd/mm/yyyy hh:mm:ss")), nullable=False)

    def __init__(self, user_id, equation, timestamp: datetime):
        self.id = user_id
        self.equation = equation
        self.date_added = timestamp.strftime("%m/%d/%Y %H:%M:%S")


@app.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()

        if user is not None and sha256(user.salt + form.password.data) == user.salted_password_hash:
            session.permanent = True
            session["user_id"] = user.id
            session["flast"] = user.first_name[0].upper() + user.last_name[0].upper() + user.last_name[1:].lower()
            return redirect(url_for("home", user_flast=session["flast"]))
        else:
            flash("Incorrect Credentials")
            form.email.data = ""
            form.password.data = ""
            return render_template("login.html", form=form)
    else:
        if "user" in session:
            return redirect(url_for("home", user_flast=session["flast"]))
        return render_template("login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password1.data,
            timestamp=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        form.first_name.data = ""
        form.last_name.data = ""
        form.email.data = ""
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/<user_flast>/home", methods=["POST", "GET"])
def home(user_flast):
    if "user_id" in session:
        form = EquationForm()
        user = Users.query.filter_by(id=session["user_id"]).first()
        rows = Equations.query.filter_by(id=session["user_id"]).all()
        print("equations:", rows)
        if form.validate_on_submit():
            print("Validated")
            # add equation to database.db
            new_equation = Equations(
                user_id=session["user_id"],
                equation=form.equation.data,
                timestamp=datetime.now()
            )
            db.session.add(new_equation)
            db.session.commit()
            form.equation.data = ""
            return redirect(url_for("home", user_flast=session["flast"], form=None))
        return render_template(
            'home.html',
            user=user.first_name + " " + user.last_name,
            form=form,
            equations=[row.equation for row in rows]
        )
    else:
        return redirect(url_for("login"))


@app.route("/<user_flast>/logout")
def logout(user_flast):
    session.pop("user_id", None)
    session.pop("flast", None)
    return redirect(url_for("login"))


@app.route("/<user_flast>/profile")
def profile(user_flast):
    form = ProfileForm()
    if form.validate_on_submit():
        # Update the user's fields
        pass

    if "user_id" in session:
        user_id = session["user_id"]
        user = Users.query.filter_by(id=user_id).first()
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        return render_template("profile.html", first_name=first_name, last_name=last_name, email=email)


@app.route("/<user_flast>/equations", methods=["GET", "POST"])
def equations(user_flast):
    form = EquationForm()
    if form.validate_on_submit():
        name = form.equation.data
        form.equation.data = ""
        flash("Equation successfully added!")
    return render_template("equations.html", equations=EQUATIONS, form=form)


@app.route("/terms_and_conditions")
def terms_page():
    return render_template("terms.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# def loop(start_string):
#     previous = start_string
#     while True:
#         new = sha256(previous)
#         print(new)
#         previous = new


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
