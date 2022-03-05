from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/run', methods=["POST", "GET"])
def send_to_run_page():
    if request.method == 'POST':
        fields = request.form
        equations = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g"
        ]
        if fields["Password"] == "asdf" and fields["First"] != "" and fields["Last"] != "":
            return render_template("run.html", fields=fields, equations=equations)
        else:
            return login()


@app.route("/draw_equation/")
def draw_equation():
    # os.system("python3 main.py")
    return "Running"


if __name__ == '__main__':
    app.run(debug=True)
