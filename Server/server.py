import time
import sqlalchemy.exc
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from flask_forms import *
from useful_functions import *

app = Flask(__name__)
app.secret_key = "my super secret key that no one is supposed to know"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=10)

# Initialize the Database
db = SQLAlchemy(app)
from models import *  # models imports db above, explaining why I have this import here. It avoids circular import
# errors.


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
            password=form.password1.data
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("Account already exists")
            flash("Incorrect Credentials")
            return render_template("signup.html", form=form)

        form.first_name.data = ""
        form.last_name.data = ""
        form.email.data = ""

        # Log the user in
        session.permanent = True
        session["user_id"] = new_user.id
        session["flast"] = new_user.first_name[0].upper() + new_user.last_name[0].upper() + new_user.last_name[1:].lower()
        return redirect(url_for("home", user_flast=session["flast"]))

    return render_template("signup.html", form=form)


@app.route("/<user_flast>/home", methods=["POST", "GET"])
def home(user_flast):
    if "user_id" in session:
        form = EquationForm()
        user = Users.query.filter_by(id=session["user_id"]).first()
        rows = Equations.query.filter_by(id=session["user_id"]).all()
        equations = [row.equation for row in rows]
        print("equations:", rows)
        if form.validate_on_submit():
            print("Validated")
            # add equation to database.db
            new_equation = Equations(
                user_id=session["user_id"],
                equation=remove_spaces(form.equation.data)
            )
            if new_equation.equation not in equations:
                db.session.add(new_equation)
                db.session.commit()
                form.equation.data = ""
                return redirect(url_for("home", user_flast=session["flast"], form=None))
            else:
                flash("Equation already exists.")
        return render_template(
            'home.html',
            user=user,
            form=form,
            equations=equations
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
        return render_template("profile.html", user=user)


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
