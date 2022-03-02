#!/usr/bin/python3
import cgi
import mariadb
import html
import configparser
import os
import json


config = configparser.ConfigParser()
if not os.path.exists('db.ini'):
    with open("db.ini", "w") as f:
        config["SERVER"] = { "user":"", "password":"","host":"","database":"","port":""}
        config.write(f)
    print("something went wrong...")
    exit(1)

query = """
SELECT SkillName, Profession
FROM Skills
Order BY SkillName ASC;
"""

config.read('db.ini')
conn = mariadb.connect(
user=config['SERVER']['user'],
password=config['SERVER']['password'],
host=config['SERVER']['host'],
database=config['SERVER']['database'],
port=int(config['SERVER']['port']),
)
cur = conn.cursor()


try:
    cur.execute(query)
    resp = cur.fetchall()
    rdict = {}
    for r in resp:
        if r[1] in rdict:
            rdict[r[1]].append(r[0])
        else:
            rdict[r[1]] = [r[0]]
    with open("allskills.json", "w") as f:
        f.write(json.dumps(rdict))

except Exception as ex:
    print(str(ex))

conn.close()


