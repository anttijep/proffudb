#!/usr/bin/python3
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
SELECT s.SkillName, s.Profession, s.spellid
FROM Skills s
WHERE SkillName=? AND Profession=?
"""

update = """
UPDATE Skills
SET spellid = ?, SkillName=?
WHERE SkillName=? AND Profession=?
"""
add = """
INSERT INTO Skills (SkillName, Profession, spellid)
VALUES (?, ?, ?)
"""

professions = ["Alchemy", "Blacksmithing", "Cooking", "Enchanting", "Engineering", "Jewelcrafting", "Leatherworking", "Tailoring"]

for p in professions:
    with open("spellids/"+p+".txt", "r") as f:
        ids = json.load(f)
        for i in ids:
            try:
                cur.execute(query, [ids[i], p])
                ret = cur.fetchone()
                if not ret:
                    print("ADD: ", ids[i], " ", p, " ", i)
                    cur.execute(add, [ids[i], p, i])
                    conn.commit()
                    continue
                if ret[2] is not None:
                    print("IGNORE: ", ids[i]," ", i, " ", p)
                    continue
                print("UPDATE: ", ids[i]," ", i, " ", p)
                cur.execute(update, [i, ids[i], ids[i], p])
                conn.commit()
            except Exception as ex:
                print(str(ex))
                exit(1)
conn.close()



