import sqlite3

connection = sqlite3.connect("anime.db")

cur = connection.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS anime (
    mal_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    english_title TEXT,
    score REAL,
    episodes INTEGER,
    status TEXT,
    approved INTEGER NOT NULL CHECK (approved IN (0, 1))
)""")




sql = """INSERT INTO anime(mal_id,title,score,approved)
 VALUES (?,?,?,?)
 ON CONFLICT(mal_id) DO UPDATE SET
    title=excluded.title,
    score=excluded.score,
    approved=excluded.approved
 """


cur.execute(sql, (52991, "Example Anime", 9, 1))

res = cur.execute("SELECT * FROM anime")
print(res.fetchall())

connection.commit()
connection.close()