import os
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))

db_data = path + "/data.db"
sh_data = path + "/data.sql"

def add_url(source, url):
    con = sqlite3.connect(db_data)
    c = con.cursor()
    c.execute(
        "insert or ignore into urls (source, url) values (?, ?)", (source, url))
    c.close()
    con.commit()
    con.close()

if __name__ == "__main__":
    con = sqlite3.connect(db_data)
    with open(sh_data, 'r') as schema:
        c = con.cursor()
        qry = schema.read()
        c.executescript(qry)
        con.commit()
        c.close()
    con.close()
