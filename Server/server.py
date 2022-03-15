import time

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, RadioField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, InputRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# Initialize the Database
db = SQLAlchemy(app)



# Figure out how to create Flask Forms, style them, and insert user input into
# SQLAlchemy DBs.

def sha256(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


# Create Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    email_and_password_hash = db.Column(db.String(64), nullable=False, unique=True)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_added = db.Column(db.String(len("dd/mm/yyyy hh:mm:ss")), nullable=False)

    def __init__(self, first_name, last_name, email, password, timestamp: datetime):
        self.email = email
        self.email_and_password_hash = sha256(email + ": " + password)
        self.first_name = first_name
        self.last_name = last_name
        self.date_added = timestamp.strftime("%m/%d/%Y %H:%M:%S")

    def __repr__(self):
        return "<Name %r>" % (self.first_name + " " + self.last_name)


class Equations(db.Model):
    row = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    equation = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, equation):
        self.id = user_id
        self.equation = equation







EQUATIONS = ["sin(4 * theta)", ]

# Create a Form Class
class EquationForm(FlaskForm):
    equation = StringField("Enter Equation", validators=[DataRequired()])
    submit = SubmitField("Add")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    password1 = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password1', message='Passwords must match')])
    agree = BooleanField("I agree to the ", validators=[InputRequired()])
    create = SubmitField("Create")


@app.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and sha256(form.email.data + ": " + form.password.data) == user.email_and_password_hash:
            session["user_id"] = user.id
            return redirect(url_for("home", user=user.first_name + user.last_name))
        else:
            flash("Incorrect Credentials")
            form.email.data = ""
            form.password.data = ""
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password1.data,
            timestamp=datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        flash("You've successfully created an account!")

    return render_template("signup.html", form=form)


@app.route("/<user>")
def home(user):
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        return render_template('home.html', user=user.first_name + " " + user.last_name)
    else:
        return redirect(url_for("login"))


@app.route("/<user>/equations", methods=["GET", "POST"])
def equations(user):
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


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
