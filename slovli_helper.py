from flask import Flask, request, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import sqlite3

DB_NAME = "slovlihelper.db"
app = Flask(__name__)
CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/search", methods=["GET"])
def search():
    t = {}
    if v := _valid_request(request):
        q = _build_query(v["num_characters"], v["letters"], v["exclude"])
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        r = cursor.execute(q).fetchall()
        connection.close()
        for w in r:
            t[w[0]] = w[2]
        return render_template('index.html',
                               result=json.dumps(t),
                               num_characters=v["num_characters"],
                               letters=v["letters"],
                               exclude=v["exclude"]
                               )
    return render_template('index.html')


def _valid_request(request):
    try:
        assert 0 < int(request.args["num_characters"]) < 50, "invalid value for num_characters"
        assert type(request.args["letters"]) == str and 0 <= len(
            request.args["letters"]) <= 33, "invalid value for letters"
        assert type(request.args["exclude"]) == str and 0 <= len(
            request.args["exclude"]) <= 33, "invalid value for exclude"
    except Exception as e:
        print(e)
        return False
    return {
        "num_characters": request.args["num_characters"],
        "letters": _safe_letters(request.args["letters"]),
        "exclude": _safe_letters(request.args["exclude"]),
    }


def _safe_letters(string):
    _ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    r = ""
    for l in string:
        l = l.lower()
        if l in _ALPHABET_LOWER:
            r += l
    return r


def _build_query(num_chars, letters, excluded):
    q = f"SELECT * FROM dictionary WHERE length IS {num_chars}"
    for l in letters:
        q += f" AND word LIKE '%{l}%'"
    for e in excluded:
        q += f" AND NOT word LIKE '%{e}%'"
    q += " LIMIT 50"
    return q
