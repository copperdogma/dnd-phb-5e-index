#!/usr/bin/env python3
import sqlite3 as sqlite
import os
import json
import re
from txt_to_json import list_to_json

def insert_rows_json(c, pubkey, version, data, listpre = None):
    sql = "INSERT OR IGNORE INTO dnd_index (pubkey, version, entry, idx, idx_text, page, notes) VALUES (?,?,?,?,?,?,?);"
    listno = 1
    for d in data:
        entry = d['name']
        if 'note' in d.keys():
            note = ';'.join(d['note'])
        else:
            note = None
        if listpre == None:
            l = str(listno)
            idx_text = d['name']
        else:
            l = '.'.join((listpre[0], str(listno)))
            idx_text = '|'.join((listpre[1], d['name']))
        if 'pages' in d.keys():
            pages = []
            for p in d['pages']:
                rng = []
                if isinstance(p, str):
                    pgs = []
                    for i in p.split('-'):
                        pgs.append(re.findall(r'\d+', i)[0])
                    if len(pgs)<2:
                        rng.append(int(pgs[0]))
                    else:
                        rng = list(range(int(pgs[0]), int(pgs[1])+1))
                elif isinstance(p, int):
                    rng.append(p)
                for i in rng:
                    pages.append(i)
            pages = list(set(pages)) #remove duplicates
            print(pubkey, version, d['name'], l, pages, note, sep='|')
            for page in pages:
                c.execute(sql,(pubkey, version, entry, l, idx_text, page, note))
        else:
            page = None
            print(pubkey, version, d['name'], l, page, note, sep='|')
            c.execute(sql,(pubkey, version, entry, l, idx_text, page, note))


        if 'children' in d.keys():
            insert_rows_json(c, pubkey, version, d['children'], (l,idx_text))
        listno += 1

try:
    scrptdir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    scrptdir = os.getcwd()

scrptpath = os.path.join(scrptdir, "dmdb.sqlite")
conn = sqlite.connect(scrptpath)
c = conn.cursor()

### lets create tables and load in some data
sql = "DROP TABLE IF EXISTS dnd_index;"
c.execute(sql)
sql = """CREATE TABLE dnd_index (pubkey TEXT, version TEXT, entry TEXT, idx TEXT, 
         idx_text TEXT, page INT, notes TEXT, PRIMARY KEY (pubkey, version, idx, page));"""
c.execute(sql)

sql = "DROP TABLE IF EXISTS dnd_pub;"
c.execute(sql)
sql = "CREATE TABLE dnd_pub (pubkey TEXT PRIMARY KEY, fullname TEXT, abbr TEXT, edition TEXT, notes TEXT, link TEXT, page_adjust INTEGER DEFAULT (0));"
c.execute(sql)
# sql = """INSERT INTO dnd_pub (pubkey, fullname, abbr, edition, notes) VALUES (?,?,?,?,?);"""
# recs = [('phb5e', "Player's Handbook", 'PHB', '5th', None),
#         ('dmg5e', "Dungeon Master's Guide", 'DMG', '5th', None),
#         ('mm5e', 'Monster Manual', 'MM', '5th', None),
#         ('cos5e', 'Curse of Strahd', 'COS', '5th', None),
#         ('hdq5e', 'Hoard of the Dragon Queen', 'HDQ', '5th', None),
#         ('oota5e', 'Out of the Abyss', 'OOTA', '5th', None),
#         ('pota5e', 'Princes of the Apocalypse', 'POTA', '5th', None),
#         ('rot5e', 'Rise of Tiamat', 'ROT', '5th', None),
#         ('aa5e', 'Adversaries & Allies', 'AA', '5th', None),
#         ('tob5e', 'Tome of Beasts', 'TOB', '5th', None),
#         ('skt5e', "Storm King's Thunder", 'SKT', '5th', None),
#         ('vgm5e', "Volo's Guide to Monsters", 'VGM', '5th', None),
#         ('fef5e', 'Fifth Edition Foes', 'FEF', '5th', None),
#         ]
# c.executemany(sql, recs)

with open (os.path.join(scrptdir, '..', "PHB Index Improved.json")) as f:
    data = json.load(f)
insert_rows_json(c, 'phb5e', 'improved', data)

with open (os.path.join(scrptdir, '..', "DMG Index Improved.json")) as f:
    data = json.load(f)
insert_rows_json(c, 'dmg5e', 'improved', data)

with open (os.path.join(scrptdir, '..', "PHB Index Original.txt")) as f:
    data = f.read().strip().split('\n')
    mainlst = list_to_json(data, 0)
insert_rows_json(c, 'phb5e', 'original', mainlst)

with open (os.path.join(scrptdir, '..', "DMG Index Original.txt")) as f:
    data = f.read().strip().split('\n')
    mainlst = list_to_json(data, 0)
insert_rows_json(c, 'dmg5e', 'original', mainlst)

with open (os.path.join(scrptdir, '..', "PHB Spell Index.txt")) as f:
    data = f.read().strip().split('\n')
    mainlst = list_to_json(data, 0)
insert_rows_json(c, 'phb5e', 'spells', mainlst)

with open (os.path.join(scrptdir, '..', "MM Index.txt")) as f:
    data = f.read().strip().split('\n')
    mainlst = list_to_json(data, 0)
insert_rows_json(c, 'mm5e', 'original', mainlst)

with open(os.path.join(scrptdir, "update.sql")) as f:
    script = f.read()
    c.executescript(script)
conn.commit()
conn.close()

