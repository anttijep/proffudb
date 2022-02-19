#!/usr/bin/python3
import cgi
print("Content-Type: text/plain;charset=UTF-8\n\n")
import mariadb
import html
import configparser

config = configparser.ConfigParser()
if not os.path.exists('db.ini'):
    with open("db.ini", "w") as f:
        config["SERVER"] = { "user":"", "password":"","host":"","database":"","port":""}
        config.write(f)
    print("something went wrong...")
    exit(1)

form = cgi.FieldStorage()


if not "charname" in form:
    print("invalid input")
    exit()

s = html.escape(form["charname"].value.replace(" ", "").capitalize())


config.read('db.ini')
conn = mariadb.connect(
user=config['SERVER']['user'],
password=config['SERVER']['password'],
host=config['SERVER']['host'],
database=config['SERVER']['database'],
port=int(config['SERVER']['port']),
)
cur = conn.cursor()

query = """
INSERT INTO Characters (CharName)
Values (?)
"""

try:
    cur.execute(query, [s])
    conn.commit()
    print("success")
except:
    print("something went wrong...")
conn.close()


