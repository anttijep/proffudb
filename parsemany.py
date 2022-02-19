#!/usr/bin/python3
import cgi
print("Content-Type: text/html;charset=UTF-8\n\n")
import cgitb
cgitb.enable()
import mariadb
import html

config = configparser.ConfigParser()
if not os.path.exists('db.ini'):
    with open("db.ini", "w") as f:
        config["SERVER"] = { "user":"", "password":"","host":"","database":"","port":""}
        config.write(f)
    print("something went wrong...")
    exit(1)

querycharid = """
SELECT c.charid
FROM Characters c
WHERE c.CharName=?
"""
insertskill = """
INSERT INTO Skills (SkillName, Profession)
values (?, ?)
"""
insertcharskill = """
INSERT KnownSkills (charid, Skillid)
values (?, (
SELECT s.id FROM Skills s
WHERE SkillName=? AND Profession=?)
)
"""

form = cgi.FieldStorage()


if not "text" in form:
    print("invalid input")
    exit()

s = html.escape(form["text"].value.title())
lines = str.splitlines(s)
size = len(lines)

if size < 3:
    print("Invalid input")
    exit()

charname = lines[0].strip()
errors = []
profname = ""
skills = []
charskills = []

config.read('db.ini')
conn = mariadb.connect(
user=config['SERVER']['user'],
password=config['SERVER']['password'],
host=config['SERVER']['host'],
database=config['SERVER']['database'],
port=int(config['SERVER']['port']),
)
cur = conn.cursor()
i = 1
escapeseq = "-"
cid = -1
try:
    cur.execute(querycharid, [charname])
    cid = cur.fetchone()
    if cid is None:
        print("character not found")
        exit(0)
    cid = cid[0]

except (mariadb.Error, mariadb.Warning) as ex:
    print("character not found")
    exit(0)

while i < size:
    if lines[i].startswith(escapeseq):
        i += 1
        continue
    profname = lines[i].strip()
    i += 1
    while i < size:
        crline = lines[i].strip()
        if crline.startswith(escapeseq):
            break
        try:
            cur.execute(insertskill, [crline, profname])
            conn.commit()
        except (mariadb.Error, mariadb.Warning) as ex:
            errors.append(crline + ", " + profname + " :: " + str(ex))
        try:
            cur.execute(insertcharskill, [cid, crline, profname])
            conn.commit()
        except (mariadb.Error, mariadb.Warning) as ex:
            errors.append(str(cid) + ", " + crline + ", " + profname + " :: " + str(ex))
        i += 1
    i += 1

conn.close()

if not errors:
    print("success")
for e in errors:
    print(str(e) + "<br>")


