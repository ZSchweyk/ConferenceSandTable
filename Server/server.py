from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"

EQUATIONS = ["sin(4 * theta)", ]


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
        user = email[:email.index("@")]
        return redirect(url_for("home", user=user))


@app.route("/home/<string:email>")
def home(user):
    return render_template('home.html', user=user)


@app.route("/equations", methods=["GET", "POST"])
def equations():
    name = None
    form = EquationForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("equations.html", equations=EQUATIONS, name=name, form=form)


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
