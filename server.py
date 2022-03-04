from flask import Flask, render_template
import os
from conference_sand_table_class import ConferenceSandTable

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/my-link/')
def my_link():
    os.system("python3 main.py")

    return 'Running!'




if __name__ == '__main__':
    app.run(debug=True)
