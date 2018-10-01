import os
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))

db_seeds = path + "/seeds.db"
sh_seeds = path + "/seeds.sql"

def add_url(tp, source, url):
    con = sqlite3.connect(db_seeds)
    c = con.cursor()
    c.execute(
        "insert or ignore into urls (type, source, url) values (?, ?, ?)", (tp, source, url))
    c.close()
    con.commit()
    con.close()

if __name__ == "__main__":
    con = sqlite3.connect(db_seeds)
    with open(sh_seeds, 'r') as schema:
        c = con.cursor()
        qry = schema.read()
        c.executescript(qry)
        con.commit()
        c.close()
    con.close()
