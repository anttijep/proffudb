#!/usr/bin/python3
import cgi
print("Content-Type: text/plain;charset=UTF-8\n")
import mariadb
import html
import configparser
import os


config = configparser.ConfigParser()
if not os.path.exists('db.ini'):
    with open("db.ini", "w") as f:
        config["SERVER"] = { "user":"", "password":"","host":"","database":"","port":""}
        config.write(f)
    print("something went wrong...")
    exit(1)


form = cgi.FieldStorage()


if not "skill" in form or not "name" or not "prof" in form:
    print("invalid input")
    exit(1)

name = html.escape(form["name"].value.title())
skill = html.escape(form["skill"].value.title())
prof = html.escape(form["prof"].value.title())


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
INSERT INTO KnownSkills (charid, skillid)
VALUES (
(SELECT charid
FROM Characters
WHERE CharName=?)
,(
SELECT id
FROM Skills s
WHERE SkillName=? AND Profession=?)
)
"""

try:
    cur.execute(query, [name, skill, prof])
    conn.commit()
    print("ADDED: ", name,  " ", skill, " ", prof)
except Exception as ex:
    print("something went wrong...")
conn.close()


