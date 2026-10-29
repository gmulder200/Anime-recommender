import sqlite3

connection = sqlite3.connect("anime.db")

cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS anime (mal_id INTEGER PRIMARY KEY,title TEXT NOT NULL,english_title TEXT,score REAL,episodes INTEGER,status TEXT,approved INTEGER NOT NULL CHECK (approved IN (0, 1)))")
