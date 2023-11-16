# use data from github.com/Badestrand/russian-dictionary
from slovli_helper import DB_NAME
import os
import sqlite3


_DELIMITER = "\t"
_SOURCE_DIR = "/Users/ravenorourke/russian-dictionary"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
try:
    cursor.execute("CREATE TABLE dictionary(word text, length int, translation text)")
except sqlite3.OperationalError as e:
    print(e)

for f in os.listdir(_SOURCE_DIR):
    if f.endswith(".csv"):
        with open(os.path.join(_SOURCE_DIR, f), "r") as c:
            _FIELDS = {}
            for i, field in enumerate(c.readline().split(_DELIMITER)):
                _FIELDS[field.strip()] = i

            r = c.readline()
            while r:
                r = r.split(_DELIMITER)
                q = f'''INSERT INTO dictionary VALUES (\"{r[_FIELDS["bare"]].replace('"', '')}\", {len(r[_FIELDS["bare"]])}, \"{'(' + f[:-5] + ') ' + r[_FIELDS["translations_en"]].replace('"', '')}\")'''
                cursor.execute(q)
                r = c.readline()
        connection.commit()
connection.close()
