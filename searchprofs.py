#!/usr/bin/python3
import cgi
import mariadb
import json
import configparser

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
if "skill" not in form:
    response({})
    exit(0)


search = '%' + form["skill"].value.title().replace("*","%") + '%'


qry = """
SELECT s.SkillName, c.CharName, c.Info FROM KnownSkills k, Skills s
JOIN Characters c ON charid = c.charid
WHERE k.skillid=s.id AND SkillName LIKE ? AND c.charid = k.charid
LIMIT 50
"""
qrywithprof = """
SELECT s.SkillName, c.CharName, c.Info FROM KnownSkills k, Skills s
JOIN Characters c ON charid = c.charid
WHERE k.skillid=s.id AND SkillName LIKE ? AND c.charid = k.charid AND s.Profession=?
LIMIT 50
"""

prof = ""
if "prof" in form:
    prof = form["prof"].value.title().strip()
else:
    prof = "Any"

try:
    if prof == "" or prof == "Any":
        result = getresult(qry, [search])
    else:
        result = getresult(qrywithprof, [search, prof])
    out = {}
    for res in result:
        if res[0] in out:
            out[res[0]].append([res[1], res[2]])
        else:
            out[res[0]] = [[res[1], res[2]]]
    response(out)
except Exception as ex:
    pass

conn.close()


