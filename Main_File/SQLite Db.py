import sqlite3
import json

connection = sqlite3.connect("anime.db")
cur = connection.cursor()
cur.execute("PRAGMA FOREIGN KEYS = ON")



### Creation of Main Table Containing most information which doesnt contain multiple catagories as for example Genres
cur.execute("""CREATE TABLE IF NOT EXISTS anime (
    mal_id INTEGER PRIMARY KEY,
    main_title TEXT NOT NULL,
    english_title TEXT,
    score REAL,
    episodes INTEGER,
    airing_status TEXT,
    approved INTEGER NOT NULL CHECK (approved IN (0, 1)),
    type TEXT,
    score_votes INTEGER,
    favorites INTEGER,
    duration TEXT,
    year INTEGER,
    synopsis TEXT
)""")

### Creation of the Genre Table 
cur.execute("""CREATE TABLE IF NOT EXISTS genre(
    genre_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")

### Creation of the connection table between the Genre Table and the Anime Table
cur.execute("""CREATE TABLE IF NOT EXISTS AnimeGenre(
    mal_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (mal_id)
    REFERENCES anime(mal_id),
    FOREIGN KEY(genre_id)
    REFERENCES genre(genre_id),
    PRIMARY KEY (mal_id,genre_id)
)""")

### Creation of the Studio Table 
cur.execute("""CREATE TABLE IF NOT EXISTS studio(
    studio_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")

### Creation of the connection table between the Studio Table and the Anime Table
cur.execute("""CREATE TABLE IF NOT EXISTS AnimeStudio(
    mal_id INTEGER,
    studio_id INTEGER,
    FOREIGN KEY (mal_id)
    REFERENCES anime(mal_id),
    FOREIGN KEY(studio_id)
    REFERENCES studio(studio_id),
    PRIMARY KEY (mal_id,studio_id)
)""")

### Creation of the Themes Table 
cur.execute("""CREATE TABLE IF NOT EXISTS themes(
    theme_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")

### Creation of the connection table between the Themes Table and the Anime Table
cur.execute("""CREATE TABLE IF NOT EXISTS AnimeThemes(
    mal_id INTEGER,
    theme_id INTEGER,
    FOREIGN KEY (mal_id)
    REFERENCES anime(mal_id),
    FOREIGN KEY(theme_id)
    REFERENCES themes(theme_id),
    PRIMARY KEY (mal_id,theme_id)
)""")

### Creation of the Demographics Table 
cur.execute("""CREATE TABLE IF NOT EXISTS demographic(
    demographic_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)""")

### Creation of the connection table between the Demographics Table and the Anime Table
cur.execute("""CREATE TABLE IF NOT EXISTS AnimeDemographic(
    mal_id INTEGER,
    demographic_id INTEGER,
    FOREIGN KEY (mal_id)
    REFERENCES anime(mal_id),
    FOREIGN KEY(demographic_id)
    REFERENCES demographic(demographic_id),
    PRIMARY KEY (mal_id,demographic_id)
)""")

cur.execute("""

""")











### Sort of function to insert test into anime
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