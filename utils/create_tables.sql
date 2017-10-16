-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS dnd_index;
CREATE TABLE dnd_index (pubkey TEXT, version TEXT, entry TEXT, idx TEXT, idx_text TEXT, page INT, notes TEXT, PRIMARY KEY (pubkey, version, idx, page));

DROP TABLE IF EXISTS dnd_pub;
CREATE TABLE dnd_pub (pubkey TEXT PRIMARY KEY, fullname TEXT, abbr TEXT, edition TEXT, notes TEXT, link TEXT, page_adjust INTEGER DEFAULT (0));

DROP TABLE IF EXISTS dnd_monsters;
CREATE TABLE dnd_monsters (name TEXT, pubkey TEXT, category TEXT, npc_name TEXT, size TEXT, type TEXT, tags TEXT, alignment TEXT, envrionment TEXT, challenge REAL, xp INTEGER, page INTEGER, srd BOOLEAN, description TEXT, PRIMARY KEY(name, pubkey));

DROP TABLE IF EXISTS dnd_spells;
CREATE TABLE dnd_spells (name TEXT PRIMARY KEY, level TEXT, school TEXT, classes TEXT, subclasses TEXT, ritual BOOLEAN, concentration BOOLEAN);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
