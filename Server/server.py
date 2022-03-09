from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"

# Initialize the Database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credentials_hash = db.Column(db.String(64), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return "<Name %r>" % self.name


# @app.route("/user/add", methods=["GET", "POST"])
# def

EQUATIONS = ["sin(4 * theta)", ]


def sha256(string: str):
    return hashlib.sha256(string.encode()).hexdigest()


# Create a Form Class
class EquationForm(FlaskForm):
    equation = StringField("Enter Equation", validators=[DataRequired()])
    submit = SubmitField("Add")


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["Email"]
        password = request.form["Password"]
        hash = sha256(email + password)
        print("HASH:", hash)
        print("LENGTH:", len(hash))
        user = email[:email.index("@")]
        return redirect(url_for("home", user=user))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        first = request.form["FirstName"]
        last = request.form["LastName"]
        email = request.form["Email"]
        password1 = request.form["Password1"]
        password2 = request.form["Password2"]
        agree_status = request.form["AgreeStatus"]
        if password1 != password2:
            flash("Passwords don't match")
        if not agree_status:
            flash("Please agree to the terms and conditions to continue.")
        hash = sha256(email + password)
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
