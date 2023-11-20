from flask import Flask, request, render_template
from flask_cors import CORS
import json
import sqlite3

DB_NAME = "slovlihelper.db"
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/search", methods=["GET"])
def search():
    q = _build_query(request.args["num_characters"], request.args["letters"].lower(), request.args["exclude"].lower())
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    r = cursor.execute(q).fetchall()
    connection.close()
    t = {}
    for w in r:
        t[w[0]] = w[2]
    return render_template('index.html', result=json.dumps(t), num_characters=request.args["num_characters"], letters=request.args["letters"], exclude=request.args["exclude"])


def _build_query(num_chars, letters, excluded):
    q = f"SELECT * FROM dictionary WHERE length IS {num_chars}"
    for l in letters:
        q += f" AND word LIKE '%{l}%'"
    for e in excluded:
        q += f" AND NOT word LIKE '%{e}%'"
    return q
