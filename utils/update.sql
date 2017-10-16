INSERT INTO dnd_pub (pubkey, fullname, abbr, edition, notes) VALUES
('phb5e', "Player's Handbook", 'PHB', '5th', Null),
('dmg5e', "Dungeon Master's Guide", 'DMG', '5th', Null),
('mm5e', 'Monster Manual', 'MM', '5th', Null),
('cos5e', 'Curse of Strahd', 'COS', '5th', Null),
('hdq5e', 'Hoard of the Dragon Queen', 'HDQ', '5th', Null),
('oota5e', 'Out of the Abyss', 'OOTA', '5th', Null),
('pota5e', 'Princes of the Apocalypse', 'POTA', '5th', Null),
('rot5e', 'Rise of Tiamat', 'ROT', '5th', Null),
('aa5e', 'Adversaries & Allies', 'AA', '5th', Null),
('tob5e', 'Tome of Beasts', 'TOB', '5th', Null),
('skt5e', "Storm King's Thunder", 'SKT', '5th', Null),
('vgm5e', "Volo's Guide to Monsters", 'VGM', '5th', Null),
('fef5e', 'Fifth Edition Foes', 'FEF', '5th', Null);

--Example updates for setting path links for backup digital pubs 
--UPDATE dnd_pub SET link = "/some/path/D&D 5E - Players Handbook.pdf", page_adjust = 1 WHERE pubkey = 'phb5e';
--UPDATE dnd_pub SET link = "/some/path/D&D 5E - Dungeon Masters Guide.pdf", page_adjust = 0 WHERE pubkey = 'dmg5e';
--UPDATE dnd_pub SET link = "/some/path/D&D 5E - Monster Manual.pdf", page_adjust = 1 WHERE pubkey = 'mm5e';
--UPDATE dnd_pub SET link = "/some/path/D&D 5E - Hoard of the Dragon Queen with Supplement.pdf", page_adjust = 1 WHERE pubkey = 'hdq5e';
--UPDATE dnd_pub SET link = "/some/path/D&D 5E - The Rise of Tiamat.pdf", page_adjust = 1 WHERE pubkey = 'rot5e';


