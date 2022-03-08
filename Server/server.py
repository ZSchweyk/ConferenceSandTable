from flask import Flask, render_template, request
import os

app = Flask(__name__)

EQUATIONS = ["sin(4 * theta)", ]


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/equations', methods=["POST", "GET"])
def equations():
    if request.method == 'POST':
        fields = request.form

        if fields["Email"] == "asdf@gmail.com" and fields["Password"] == "asdf":
            return render_template("equations.html", equations=EQUATIONS)
        else:
            return login()


@app.route("/add_equation", methods=["POST", "GET"])
def add_equation():
    if request.method == "POST":
        print(request.form["equation"])
        EQUATIONS.append(request.form["equation"])
        return render_template("equations.html", equations=EQUATIONS)


@app.route("/remove_equation/<equation>", methods=["POST", "GET"])
def remove_equation(equation):
    if request.method == "POST":
        print("Deleted")
        pass


@app.route("/draw_equation/")
def draw_equation():
    # os.system("python3 main.py")
    return "Running"


if __name__ == '__main__':
    app.run(debug=True)
