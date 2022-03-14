from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, RadioField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, InputRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"

# Initialize the Database
db = SQLAlchemy(app)
# db.create_all()


# Figure out how to create Flask Forms, style them, and insert user input into
# SQLAlchemy DBs.

def sha256(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    email_and_password_hash = db.Column(db.String(64), nullable=False, unique=True)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.email_and_password_hash = sha256(self.email + ": " + self.password)
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "<Name %r>" % (self.first_name + " " + self.last_name)


# @app.route("/user/add", methods=["GET", "POST"])


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
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password1', message='Passwords must match')])
    agree = BooleanField("I agree to the ", validators=[DataRequired()])
    create = SubmitField("Create")


@app.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("home", user="ASDF"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        form = SignupForm()
        return render_template("signup.html", form=form)
    else:
        first = request.form["FirstName"]
        last = request.form["LastName"]
        email = request.form["Email"]
        password1 = request.form["Password1"]
        password2 = request.form["Password2"]
        if password1 != password2:
            flash("Passwords don't match")
            return redirect(url_for("signup"))
        hash = sha256(email + password1)
        print("HASH:", hash)
        # Create the user in the database
        user = email[:email.index("@")]
        return redirect(url_for("home", user=user))


@app.route("/<user>")
def home(user):
    return render_template('home.html', user=user)


@app.route("/<user>/equations", methods=["GET", "POST"])
def equations(user):
    form = EquationForm()
    if form.validate_on_submit():
        name = form.equation.data
        form.equation.data = ""
        flash("Equation successfully added!")
    print(user)
    return render_template("equations.html", equations=EQUATIONS, form=form)


@app.route("/terms_and_conditions")
def terms_page():
    return render_template("terms.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# @app.route("/equation", methods=["GET", "POST"])
# def equation():
#     name = None
#     form = EquationForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ""
#     return render_template("equations_form", name=name, form=form)


if __name__ == '__main__':
    app.run(debug=True)
