#!/usr/bin/python3
import cgi
import mariadb
import json
import configparser
import os

def response(js):
    out = json.dumps(js)
    print("Content-type: application/json;charset=UTF-8\n")
    print(out)

config = configparser.ConfigParser()
if not os.path.exists('db.ini'):
    with open("db.ini", "w") as f:
        config["SERVER"] = { "user":"", "password":"","host":"","database":"","port":""}
        config.write(f)
    print("something went wrong...")
    exit(1)

config.read('db.ini')

conn = mariadb.connect(
user=config['SERVER']['user'],
password=config['SERVER']['password'],
host=config['SERVER']['host'],
database=config['SERVER']['database'],
port=int(config['SERVER']['port']),
)
def getresult(query, bindings = []):

    cur = conn.cursor()
    if len(bindings) == 0:
        cur.execute(query)
    else:
        cur.execute(query, bindings)
    results = cur.fetchall()
    return results

form = cgi.FieldStorage()
if "name" not in form:
    response({})
    exit(0)

name = form["name"].value

charinfo = """
SELECT CharName, Info
FROM Characters
WHERE CharName=?
"""

qry = """
SELECT s.SkillName, s.Profession
FROM KnownSkills k, Skills s
JOIN Characters c ON charid = c.charid
WHERE k.skillid=s.id AND c.CharName=? AND c.charid = k.charid
ORDER BY s.SkillName ASC
"""


try:
    out = {}
    result = getresult(charinfo, [name])
    if len(result) == 0:
        response({})
        exit(0)
    out["name"] = result[0][0]
    out["info"] = result[0][1]
    result = getresult(qry, [name])
    for res in result:
        if res[1] in out:
            out[res[1]].append(res[0])
        else:
            out[res[1]] = [res[0]]
    response(out)
except Exception as ex:
    pass

conn.close()


