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
    return render_template('index.html', result=json.dumps(t))


def _build_query(num_chars, letters, excluded):
    q = f"SELECT * FROM dictionary WHERE length IS {num_chars}"
    for l in letters:
        q += f" AND word LIKE '%{l}%'"
    for e in excluded:
        q += f" AND NOT word LIKE '%{e}%'"
    return q


def main():
    n = int(input("How many characters? ") or 0)
    l = input("Containing which letters? ").strip().lower()
    e = input("Excluding which letters? ").strip().lower()
    q = _build_query(n, l, e)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    r = cursor.execute(q).fetchall()
    connection.close()

    print(f"{len(r)} results:")
    for w in r:
        print(f"{w[0]}: {w[2]}")


if __name__ == "__main__":
    # main()
    pass
