import sqlite3

def create_database():

    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    cur.execute("PRAGMA FOREIGN_KEYS = ON")

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

def get_anime_genres(Anime_id):
    #Initiate connection and cursor
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    #Create a Selector which gives genres based on mal_id
    res = cur.execute("""
        SELECT genre.name
        FROM AnimeGenre
        JOIN genre ON genre.genre_id = AnimeGenre.genre_id
        WHERE AnimeGenre.mal_id = ?
        """, (Anime_id,))

    

    #Fetch the genres and return them
    genres = res.fetchall()
    connection.close()
    return(genres)


def add_anime(anime):
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""INSERT INTO anime(mal_id,main_title,english_title,score,episodes,airing_status,approved,type,score_votes,favorites,duration,year,synopsis)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(mal_id) DO UPDATE SET
        main_title=excluded.main_title,
        english_title=excluded.english_title,
        score=excluded.score,
        episodes=excluded.episodes,
        airing_status=excluded.airing_status,
        approved=excluded.approved,
        type=excluded.type,
        score_votes=excluded.score_votes,
        favorites=excluded.favorites,
        duration=excluded.duration,
        year=excluded.year,
        synopsis=excluded.synopsis
    """,(anime["mal_id"],anime["main_title"],anime["english_title"],anime["score"],anime["episodes"],anime["airing_status"],anime["approved"],anime["type"],anime["score_votes"],anime["favorites"],anime["duration"],anime["year"],anime["synopsis"]) )

    #For Loop to add genre to its own table(creating Genre_id in the process) and then also fetching that Genre_ID and then adding that and MAL_ID to the connection TABLE
    for genre in anime["genres"]:
        cur.execute("""INSERT OR IGNORE INTO genre(name)
        VALUES(?)""",(genre,))
        res = cur.execute("""SELECT genre_id
        FROM genre
        WHERE name = ?
        """,(genre,))

        genre_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeGenre(mal_id,genre_id)
        VALUES(?,?)
          """,(anime["mal_id"],genre_id))


    #For Loop to add studio to its own table(creating studio_id in the process) and then also fetching that studio_id and then adding that and MAL_ID to the connection TABLE
    for studio in anime["studio_name"]:
        cur.execute("""INSERT OR IGNORE INTO studio(name)
        VALUES(?)""",(studio,))
        res = cur.execute("""SELECT studio_id
        FROM studio
        WHERE name = ?
        """,(studio,))

        studio_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeStudio(mal_id,studio_id)
        VALUES(?,?)
          """,(anime["mal_id"],studio_id))
    
    #For Loop to add themes to its own table(creating theme_id in the process) and then also fetching that theme_id and then adding that and MAL_ID to the connection TABLE
    for theme in anime["themes"]:
        cur.execute("""INSERT OR IGNORE INTO themes(name)
        VALUES(?)""",(theme,))
        res = cur.execute("""SELECT theme_id
        FROM themes
        WHERE name = ?
        """,(theme,))

        theme_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeThemes(mal_id,theme_id)
        VALUES(?,?)
          """,(anime["mal_id"],theme_id))    

    #For Loop to add themes to its own table(creating theme_id in the process) and then also fetching that theme_id and then adding that and MAL_ID to the connection TABLE
    for demographic in anime["demographics"]:
        cur.execute("""INSERT OR IGNORE INTO demographic(name)
        VALUES(?)""",(demographic,))
        res = cur.execute("""SELECT demographic_id
        FROM demographic
        WHERE name = ?
        """,(demographic,))

        demographic_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeDemographic(mal_id,demographic_id)
        VALUES(?,?)
          """,(anime["mal_id"],demographic_id))        
    connection.commit()
    connection.close()


if __name__ == "__main__":

